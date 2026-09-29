#!/usr/bin/env python3
"""ovitmugen — tmux manager of the session layer (layout C: frame + agents).

Source : ~/ia-sync/zsh/session/ovitmugen.py   (surgical table; `bash deploy.sh` spreads)
Live   : ~/.config/zsh/session/ovitmugen.py
Design : ~/unikuklatrix/nablarva/.dev/session/ovitmugen-00-console/raw/
         draft.trajectory.ovitmugen-architecture.2026-09-23.md
Wiring : session/base.zsh PARTITION 5 → ovitmugen.zsh (engine) · aliases in keyboard.zsh

Two tmux servers, never mixed:
  AGENTS  tmux -L default     base <slug> (one window = one tab = one agent)
                              views <slug>--left (frame's left pane), <slug>--<win> (columns)
  FRAME   tmux -L ovitmugen   one session per bed: left pane = client of <slug>--left,
                              right pane = fixed app (runbook). Own config, prefix C-a.

LAWS — read before editing:
  L-a  views only. Never send-keys / paste-buffer into a pane (nablarva flag L4).
  L-b  a viewer never owns lifetime. Closing the frame or a view never kills an agent.
  L-c  never kill a pane whose command is not a bare shell or whose shell has children.
  L-d  every tmux call names its server (-L). runbook runs INSIDE the frame: $TMUX lies.
  L-e  after creation, address windows/panes by id (@N / %N). No '=' on pane targets
       (`=s:0.1` → "can't find pane" on tmux 3.7c).
  L-f  `--dry-run` prints the literal commands: that output IS the manual recipe.
Stdlib only. Exit codes: 0 ok · 1 refused/error · 2 usage.
"""
from __future__ import annotations

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
TIMEOUT = 3                                   # seconds per tmux call — never stall a UI
SHELLS = {"zsh", "bash", "sh", "dash", "fish", "ksh", "tcsh"}
HELPER_CHILDREN = ("gitstatusd",)             # prompt helpers (p10k) — not an agent
DEFAULT_TABS = ["cSharp", "bus", "implement", "audit"]
DEFAULT_SPLIT = "40%"                         # width of the FIXED (right) pane → 60/40
DEFAULT_FIXED = "runbook"
LEFT = "--left"
FMT_WIN = "#{window_id}\t#{window_index}\t#{window_name}\t#{window_active}"
FMT_PANE = "#{window_id}\t#{pane_id}\t#{pane_current_command}\t#{pane_pid}\t#{pane_dead}"
FMT_SESS = "#{session_name}\t#{session_group}\t#{session_attached}\t#{session_windows}"


class OvError(Exception):
    """Refusal or failure with a message meant for the operator."""


# --------------------------------------------------------------------------- tmux

class Tmux:
    """One tmux server, always addressed by socket name (law L-d)."""

    def __init__(self, sock: str, conf: str | None = None):
        self.sock, self.conf = sock, conf

    def argv(self, *args) -> list[str]:
        a = ["tmux", "-L", self.sock]
        if self.conf:
            a += ["-f", self.conf]
        return a + [str(x) for x in args]

    def run(self, *args, check: bool = False, keep_tmux_env: bool = False):
        env = dict(os.environ)
        if not keep_tmux_env:
            env.pop("TMUX", None)             # -L decides the server, not the caller's $TMUX
        try:
            p = subprocess.run(self.argv(*args), capture_output=True, text=True,
                               timeout=TIMEOUT, env=env)
        except subprocess.TimeoutExpired:
            raise OvError(f"tmux -L {self.sock} {args[0]}: timed out after {TIMEOUT}s")
        except FileNotFoundError:
            raise OvError("tmux not found on PATH")
        if check and p.returncode != 0:
            msg = p.stderr.strip() or f"exit {p.returncode}"
            raise OvError(f"tmux -L {self.sock} {' '.join(map(str, args))}: {msg}")
        return p

    def lines(self, *args) -> list[str]:
        p = self.run(*args)
        return p.stdout.splitlines() if p.returncode == 0 else []

    def has(self, session: str) -> bool:
        return self.run("has-session", "-t", f"={session}").returncode == 0


def servers() -> tuple[Tmux, Tmux]:
    """(agents, frame) — env overrides exist for selftest and odd setups."""
    agents = Tmux(os.environ.get("OV_AGENTS_SOCKET", "default"),
                  os.environ.get("OV_AGENTS_CONF") or None)
    frame = Tmux(os.environ.get("OV_FRAME_SOCKET", "ovitmugen"),
                 os.environ.get("OV_FRAME_CONF", str(HERE / "ovitmugen.tmux.conf")))
    return agents, frame


# --------------------------------------------------------------------------- state

def sessions(t: Tmux) -> list[dict]:
    out = []
    for line in t.lines("list-sessions", "-F", FMT_SESS):
        name, group, attached, nwin = line.split("\t")
        out.append({"name": name, "group": group, "attached": int(attached or 0),
                    "windows": int(nwin or 0)})
    return out


def windows(t: Tmux, session: str) -> list[dict]:
    out = []
    for line in t.lines("list-windows", "-t", f"={session}", "-F", FMT_WIN):
        wid, idx, name, active = line.split("\t")
        out.append({"id": wid, "index": int(idx), "name": name, "active": active == "1"})
    return out


def children_map() -> dict[int, list[int]]:
    """ppid → [pid] from /proc (no pgrep dependency); prompt helpers left out."""
    kids: dict[int, list[int]] = {}
    for d in os.listdir("/proc"):
        if not d.isdigit():
            continue
        try:
            with open(f"/proc/{d}/stat") as f:
                s = f.read()
            comm = s[s.index("(") + 1:s.rindex(")")]
            ppid = int(s[s.rindex(")") + 2:].split()[1])
        except (OSError, ValueError, IndexError):
            continue
        if comm.startswith(HELPER_CHILDREN):
            continue
        kids.setdefault(ppid, []).append(int(d))
    return kids


def pane_busy(cmd: str, pid: int, kids: dict[int, list[int]]) -> bool:
    """Law L-c: busy = not a bare shell, or a shell with children."""
    return cmd.lstrip("-") not in SHELLS or bool(kids.get(pid))


def tabs(t: Tmux, slug: str) -> list[dict]:
    """Windows of the base with agent detection. ● busy / ○ idle."""
    kids = children_map()
    per: dict[str, dict] = {}
    for line in t.lines("list-panes", "-s", "-t", f"={slug}", "-F", FMT_PANE):
        wid, pid_, cmd, ppid, dead = line.split("\t")
        busy = dead != "1" and pane_busy(cmd, int(ppid or 0), kids)
        w = per.setdefault(wid, {"busy": False, "cmd": cmd})
        if busy and not w["busy"]:
            w["cmd"] = cmd
        w["busy"] = w["busy"] or busy
    out = []
    for w in windows(t, slug):
        info = per.get(w["id"], {"busy": False, "cmd": "?"})
        # busy = kill-safety (fg program OR shell children, law L-c) · fg = display count:
        # a program other than a shell in the foreground (startup shells never count).
        out.append({**w, "busy": info["busy"], "cmd": info["cmd"],
                    "fg": info["cmd"].lstrip("-") not in SHELLS and info["cmd"] != "?"})
    return out


def view_current(t: Tmux, view: str) -> str | None:
    for w in windows(t, view):
        if w["active"]:
            return w["id"]
    return None


# --------------------------------------------------------------------------- presets

def load_presets() -> dict:
    path = Path(os.environ.get("OV_PRESETS", HERE / "ovitmugen.presets.json"))
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return {}
    except (OSError, ValueError) as e:
        raise OvError(f"presets {path}: {e}")
    return {k: v for k, v in data.items() if not k.startswith("_")}


def project_of(root: str | None) -> str | None:
    """<project>/.dev/session → <project> (where agents in the tabs should start)."""
    if not root:
        return None
    r = Path(root).expanduser().resolve()
    return str(r.parent.parent) if r.name == "session" and r.parent.name == ".dev" else None


def fixed_argv(name: str, root: str | None = None) -> list[str]:
    """Named fixed-pane commands only — presets never carry raw shell strings.
    NB: runbook resolves its root as --root > $RB_ROOT > cwd walk-up. $RB_ROOT (the
    operator's default bench) would win over the cwd, so the bed's root is passed
    explicitly — else a nablarva bed's frame opens runbook on ~/ia-sync (walk bug
    2026-09-29)."""
    rb = [sys.executable or "python3", str(HERE / "runbook.py")]
    table = {
        "runbook": rb + (["--root", str(Path(root).expanduser())] if root else []),
        "shell": [os.environ.get("SHELL", "/bin/sh")],
    }
    if name not in table:
        raise OvError(f"unknown fixed command '{name}' (known: {', '.join(table)})")
    return table[name]


# --------------------------------------------------------------------------- plan / apply
# An op: {"srv": "agents"|"frame", "args": [...], "desc": str, "capture": name|None}.
# "<<name>>" in args is replaced by an id captured from an earlier op (-P -F prints it).

def op(srv, args, desc, capture=None, fmt="#{window_id}"):
    if capture:                               # flags go before any trailing shell-command
        args = [args[0], "-P", "-F", fmt] + list(args[1:])
    return {"srv": srv, "args": list(args), "desc": desc, "capture": capture}


def plan_up(slug: str, want_tabs: list[str], split: str, fixed: str, cwd: str,
            size: tuple[int, int], root: str | None = None) -> list[dict]:
    if not slug or "--" in slug or any(c in slug for c in ":.= \t"):
        raise OvError(f"bad slug '{slug}' (no '--', ':', '.', '=', spaces)")
    A, F = servers()
    ops: list[dict] = []
    view = slug + LEFT
    base_exists = A.has(slug)
    existing = windows(A, slug) if base_exists else []
    names = [w["name"] for w in existing]
    want = list(dict.fromkeys(want_tabs or ([] if base_exists else DEFAULT_TABS)))
    missing = [n for n in want if n not in names]
    first_ref = existing[0]["id"] if existing else None

    n = 0
    if not base_exists:
        first = missing.pop(0)
        ops.append(op("agents", ["new-session", "-d", "-s", slug, "-n", first, "-c", cwd],
                      f"base session '{slug}' with tab '{first}'", capture="w0"))
        ops.append(op("agents", ["set-option", "-w", "-t", "<<w0>>", "window-size", "latest"],
                      "tab follows the latest client, not the largest (risk R1)"))
        first_ref, n = "<<w0>>", 1
    for name in missing:
        cap = f"w{n}"
        ops.append(op("agents", ["new-window", "-d", "-t", f"={slug}:", "-n", name, "-c", cwd],
                      f"tab '{name}'", capture=cap))
        ops.append(op("agents", ["set-option", "-w", "-t", f"<<{cap}>>", "window-size", "latest"],
                      f"tab '{name}' follows the latest client"))
        n += 1

    if not A.has(view):
        ops.append(op("agents", ["new-session", "-d", "-t", f"={slug}", "-s", view],
                      f"left view '{view}' (own current window, shares the tabs)"))
        ops.append(op("agents", ["select-window", "-t", f"={view}:{first_ref}"],
                      "left view starts on the first tab"))

    # NB: the pane command runs through the user's shell (zsh): a bare `=word` is zsh
    #     equals-expansion (`=foo` → path of command foo) and kills the attach. shlex.join
    #     does not quote '=', so the exact-match target is single-quoted by hand.
    left_cmd = ("env -u TMUX " + shlex.join(A.argv("attach", "-t")) + f" '={view}'")
    if not F.has(slug):
        cols, rows = size
        ops.append(op("frame", ["new-session", "-d", "-s", slug, "-x", cols, "-y", rows,
                                "-c", cwd, left_cmd],
                      f"frame '{slug}': left pane shows '{view}'", capture="fl",
                      fmt="#{pane_id}"))
        ops.append(op("frame", ["set-environment", "-g", "OV_PY", str(HERE / "ovitmugen.py")],
                      "frame knows where ovitmugen lives (C-a t popup)"))
        ops.append(op("frame", ["set-environment", "-g", "OV_AGENTS_SOCKET", A.sock],
                      "frame popup talks to the same agents server"))
        ops.append(op("frame", ["split-window", "-h", "-l", split, "-t", "<<fl>>", "-c", cwd,
                                shlex.join(fixed_argv(fixed, root))],
                      f"fixed right pane: {fixed} ({split})", capture="fr", fmt="#{pane_id}"))
        ops.append(op("frame", ["select-pane", "-t", "<<fl>>"], "focus the left (agents) pane"))
    else:
        # remain-on-exit keeps exited panes visible as "Pane is dead". Revive each with its
        # ORIGINAL start command (respawn-pane without a command): left = inner detach,
        # right = the fixed app quit (q / C-c in runbook exits 0).
        want_rb = shlex.join(fixed_argv("runbook", root)) if root else None
        for line in F.lines("list-panes", "-t", f"={slug}", "-F",
                            "#{pane_id}\t#{pane_dead}\t#{pane_left}\t#{pane_start_command}"):
            pid_, dead, left, start = (line.split("\t") + [""])[:4]
            if want_rb and left != "0" and "runbook.py" in start and start != want_rb:
                ops.append(op("frame", ["respawn-pane", "-k", "-t", pid_, "-c", cwd, want_rb],
                              f"fixed runbook showed another root — reopen on {root}"))
                continue
            if dead == "1":
                which = "left pane (inner detach) — reconnect" if left == "0" else \
                        "fixed pane (app quit) — restart"
                ops.append(op("frame", ["respawn-pane", "-t", pid_], f"{which} it"))
    return ops


def render(ops: list[dict]) -> list[str]:
    A, F = servers()
    srv = {"agents": A, "frame": F}
    out = []
    for o in ops:
        out.append(f"# {o['desc']}" + (f"  → prints <<{o['capture']}>>" if o["capture"] else ""))
        out.append(shlex.join(srv[o["srv"]].argv(*o["args"])))
    return out


def apply(ops: list[dict]) -> dict:
    A, F = servers()
    srv = {"agents": A, "frame": F}
    got: dict[str, str] = {}
    for o in ops:
        args = []
        for a in o["args"]:
            a = str(a)
            for k, v in got.items():
                a = a.replace(f"<<{k}>>", v)
            args.append(a)
        p = srv[o["srv"]].run(*args, check=True)
        if o["capture"]:
            got[o["capture"]] = p.stdout.strip().splitlines()[-1]
    return got


# --------------------------------------------------------------------------- commands

def inside(t: Tmux) -> bool:
    """Is the caller a client of server t? ($TMUX = socket_path,pid,session)."""
    sock = os.environ.get("TMUX", "").split(",")[0]
    return bool(sock) and Path(sock).name == t.sock


def bed_names(A: Tmux | None = None) -> list[str]:
    """Beds = base sessions. A session in another session's group is a VIEW (columns,
    <slug>--left, or any hand-made `new-session -t`), never listed as its own bed. An
    orphan group (base killed, views left) shows once, under its first member."""
    A = A or servers()[0]
    all_s = sessions(A)
    names = {s["name"] for s in all_s}
    out, seen_orphan = [], set()
    for s in all_s:
        g = s["group"]
        if not g or g == s["name"]:
            out.append(s["name"])
        elif g not in names and g not in seen_orphan:
            seen_orphan.add(g)
            out.append(s["name"])
    return out


def session_root_from_cwd(cwd: str | None = None) -> str | None:
    """Inside <project>/.dev/session/<bed>/… → '<project>/.dev/session'."""
    p = Path(cwd or os.getcwd()).resolve()
    for d in [p, *p.parents]:
        if d.parent.name == "session" and d.parent.parent.name == ".dev":
            return str(d.parent)
    return None


def session_bed_from_cwd(cwd: str | None = None) -> str | None:
    """Inside <project>/.dev/session/<bed>/… → '<bed>' (the RUNBOOK bed's folder name)."""
    p = Path(cwd or os.getcwd()).resolve()
    for d in [p, *p.parents]:
        if d.parent.name == "session" and d.parent.parent.name == ".dev":
            return d.name
    return None


def resolve_slug(given: str | None, need_existing: bool = False) -> str:
    """Slug rules (P2.1): given → frame's bed (inside a frame) → RUNBOOK bed folder of the
    cwd → the only frame that is up. Otherwise refuse and name the beds."""
    if given and not given.startswith("#{"):
        return given
    for cand in (frame_slug(), session_bed_from_cwd()):
        if cand:
            return cand
    A, F = servers()
    frames = [s["name"] for s in sessions(F)]
    if len(frames) == 1:
        return frames[0]
    beds = bed_names(A)
    why = f"{len(frames)} frames up" if frames else "no frame up"
    raise OvError(f"which bed? ({why}; not inside a frame or a .dev/session/<bed>/ dir) — "
                  f"beds: {', '.join(beds) or 'none'}  (ov-ls for details)")


def tabs_spec(spec: list[str], split: str | None = None, fixed: str | None = None):
    """['@preset'] or tab names → (tabs, split, fixed); explicit split/fixed win."""
    want = list(spec)
    if want and want[0].startswith("@"):
        presets = load_presets()
        key = want[0][1:]
        if key not in presets:
            raise OvError(f"no preset '{key}' (have: {', '.join(presets) or 'none'})")
        p = presets[key]
        return (list(p.get("tabs", [])), split or p.get("split", DEFAULT_SPLIT),
                fixed or p.get("fixed", DEFAULT_FIXED))
    return want, split or DEFAULT_SPLIT, fixed or DEFAULT_FIXED


def build_bed(slug: str, spec: list[str] | None = None, root: str | None = None) -> int:
    """Build every missing part (base, tabs, view, frame) without attaching. Returns steps.
    root = the bed's <project>/.dev/session: runbook opens there, tabs start in <project>."""
    want, split, fixed = tabs_spec(spec or [])
    size = shutil.get_terminal_size((200, 50))
    cwd = project_of(root) or os.getcwd()
    ops = plan_up(slug, want, split, fixed, cwd, (size.columns, size.lines), root)
    apply(ops)
    return len(ops)


def close_idle_tab(slug: str, ref: str) -> dict:
    """Close ONE idle tab (○). Refuses a busy tab (law L-c) and the last tab (it would end
    the bed and every view — that is ov-down's job). Busy is re-read at close time."""
    A, _ = servers()
    w = resolve_tab(A, slug, ref)
    now = {t["id"]: t for t in tabs(A, slug)}
    if len(now) <= 1:
        raise OvError(f"'{w['name']}' is the last tab — closing it ends the bed; "
                      f"use: ov-down {slug} --idle")
    t = now.get(w["id"])
    if t and t["busy"]:
        raise OvError(f"'{w['name']}' runs {t['cmd']} — end the agent in its tab first "
                      "(/exit), then close the empty tab")
    A.run("kill-window", "-t", w["id"], check=True)
    return w


OPEN = "open:"   # console result prefix: the host must hand its terminal to the frame


def attach_argv(slug: str) -> list[str]:
    return servers()[1].argv("attach", "-t", f"={slug}")


def open_frame(slug: str, root: str | None = None) -> str:
    """Console `o`: build any missing part (frame included), then show this bed's frame.
    Inside the frame server → switch the client, return a message. Plain terminal →
    return OPEN+slug: the host leaves curses and execs attach_argv(slug). Inside any
    other tmux → refuse (a frame inside tmux nests)."""
    n = build_bed(slug, [], root)
    _, F = servers()
    if inside(F):
        F.run("switch-client", "-t", f"={slug}", check=True, keep_tmux_env=True)
        return f"frame '{slug}' shown" + (f" ({n} steps built)" if n else "")
    if os.environ.get("TMUX"):
        raise OvError(f"inside tmux — leave it (C-b d), then: ov-up {slug}")
    return OPEN + slug


def exec_attach(slug: str) -> None:
    """Replace this process with the frame client on the controlling terminal.
    NB: tmux refuses a terminal named "/dev/tty" ("open terminal failed: can't use
    /dev/tty"), so never reopen that alias: keep a real tty fd, or reopen the REAL
    device path (os.ttyname of a std fd that is a tty)."""
    if not os.isatty(0):
        real = next((os.ttyname(fd) for fd in (1, 2) if os.isatty(fd)), None)
        if real:
            try:
                fd = os.open(real, os.O_RDWR)
                for std in (0, 1, 2):
                    os.dup2(fd, std)
            except OSError:
                pass
    env = dict(os.environ)
    env.pop("TMUX", None)
    os.execvpe("tmux", attach_argv(slug), env)


def cmd_up(a) -> int:
    A, F = servers()
    a.slug = resolve_slug(a.slug)
    want, split, fixed = tabs_spec(a.tabs, a.split_given, a.fixed_given)
    dups = _dups(A, a.slug)
    if dups:
        print(f"ovitmugen: warning — '{a.slug}' has duplicate tab names {sorted(dups)}; "
              "address them by id (@N)", file=sys.stderr)
    size = shutil.get_terminal_size((200, 50))
    root = a.root or (session_root_from_cwd() if session_bed_from_cwd() == a.slug else None)
    ops = plan_up(a.slug, want, split, fixed, project_of(root) or os.getcwd(),
                  (size.columns, size.lines), root)
    attach = ["attach", "-t", f"={a.slug}"]
    if a.dry_run:
        print("\n".join(render(ops) or ["# nothing to build — bed is complete"]))
        if not a.no_attach:
            print("# attach the frame (plain terminal)")
            print(shlex.join(F.argv(*attach)))
        return 0
    apply(ops)
    print(f"ovitmugen: bed '{a.slug}' ready ({len(ops)} steps)", file=sys.stderr)
    if a.no_attach:
        return 0
    if inside(F):
        F.run("switch-client", "-t", f"={a.slug}", check=True, keep_tmux_env=True)
        return 0
    if os.environ.get("TMUX") and not a.force:
        raise OvError("you are inside tmux — open a plain terminal and run it there, "
                      f"or attach later: {shlex.join(F.argv(*attach))}  (--force nests)")
    env = dict(os.environ)
    env.pop("TMUX", None)
    os.execvpe("tmux", F.argv(*attach), env)
    return 0


def _dups(A: Tmux, slug: str) -> set[str]:
    names = [w["name"] for w in windows(A, slug)]
    return {n for n in names if names.count(n) > 1}


def resolve_tab(A: Tmux, slug: str, ref: str) -> dict:
    ws = windows(A, slug)
    if ref.startswith("@"):
        hit = [w for w in ws if w["id"] == ref]
    elif ref.isdigit():
        hit = [w for w in ws if w["index"] == int(ref)]
    else:
        hit = [w for w in ws if w["name"] == ref]
    if not hit:
        have = ", ".join(f"{w['index']}:{w['name']}({w['id']})" for w in ws) or "none"
        raise OvError(f"no tab '{ref}' in '{slug}' (have: {have})")
    if len(hit) > 1:
        ids = ", ".join(w["id"] for w in hit)
        raise OvError(f"tab name '{ref}' is ambiguous in '{slug}' ({ids}) — use the id")
    return hit[0]


def switch_tab(slug: str, ref: str) -> dict:
    A, _ = servers()
    view = slug + LEFT
    if not A.has(view):
        raise OvError(f"no left view '{view}' — run: ov-up {slug}")
    w = resolve_tab(A, slug, ref)
    A.run("select-window", "-t", f"={view}:{w['id']}", check=True)
    return w


def cmd_tab(a) -> int:
    slug, ref = (a.args[0], a.args[1]) if len(a.args) == 2 else (resolve_slug(None), a.args[0])
    w = switch_tab(slug, ref)
    print(f"ovitmugen: left pane → {w['index']}:{w['name']} ({w['id']})", file=sys.stderr)
    return 0


def bed_report(slug: str) -> dict:
    A, F = servers()
    all_s = sessions(A)
    views = [s["name"] for s in all_s if s["group"] == slug and s["name"] != slug]
    frame = next((s for s in sessions(F) if s["name"] == slug), None)
    cur = view_current(A, slug + LEFT) if (slug + LEFT) in views else None
    return {
        "bed": slug,
        "tabs": [{**t, "left": t["id"] == cur} for t in tabs(A, slug)],
        "views": views,
        "frame": None if frame is None else {"attached": frame["attached"]},
    }


def cmd_ls(a) -> int:
    A, _ = servers()
    beds = [a.slug] if a.slug else bed_names(A)
    if a.slug and not A.has(a.slug):
        raise OvError(f"no bed '{a.slug}' on tmux -L {A.sock}")
    reports = [bed_report(b) for b in beds]
    if a.json:
        print(json.dumps(reports, indent=2))
        return 0
    if not reports:
        print(f"ovitmugen: no sessions on tmux -L {A.sock}")
    for r in reports:
        fr = "frame: down" if r["frame"] is None else \
             f"frame: up ({r['frame']['attached']} attached)"
        vs = " ".join(v[len(r["bed"]):] if v.startswith(r["bed"] + "--") else v
                      for v in r["views"]) or "-"
        print(f"{r['bed']}   {fr}   views: {vs}")
        for t in r["tabs"]:
            mark = "●" if t["busy"] else "○"
            left = "   ← left pane" if t["left"] else ""
            print(f"  {mark} {t['index']:>2} {t['name']:<16} {t['id']:<5} {t['cmd']}{left}")
    return 0


def plan_down(slug: str, level: str) -> list[dict]:
    """Peel layers. frame ⊂ views ⊂ idle. Never touches a busy tab (law L-c)."""
    A, F = servers()
    ops = []
    if F.has(slug):
        ops.append(op("frame", ["kill-session", "-t", f"={slug}"],
                      f"close frame '{slug}' (agents untouched)"))
    if level in ("views", "idle"):
        views = [s["name"] for s in sessions(A)
                 if s["name"].startswith(slug + "--") and s["group"] == slug]
        if views and not A.has(slug):
            raise OvError(f"base '{slug}' is gone — killing its last view would kill the "
                          f"windows. Refusing; inspect with: tmux -L {A.sock} ls")
        for v in views:
            ops.append(op("agents", ["kill-session", "-t", f"={v}"],
                          f"close view '{v}' (tabs live on in '{slug}')"))
    if level == "idle":
        for t in tabs(A, slug):
            if not t["busy"]:
                ops.append(op("agents", ["kill-window", "-t", t["id"]],
                              f"close idle tab {t['name']} ({t['id']}, {t['cmd']})"))
    return ops


def cmd_down(a) -> int:
    level = "idle" if a.idle else "views" if a.views else "frame"
    a.slug = resolve_slug(a.slug)
    ops = plan_down(a.slug, level)
    if a.dry_run:
        print("\n".join(render(ops) or ["# nothing to close"]))
        return 0
    apply(ops)
    kept = [t for t in tabs(servers()[0], a.slug) if t["busy"]] if level == "idle" else []
    print(f"ovitmugen: down --{level} '{a.slug}': {len(ops)} closed"
          + (f"; kept {len(kept)} tab(s) with a running agent" if kept else ""),
          file=sys.stderr)
    return 0


# --------------------------------------------------------------------------- console

def frame_slug() -> str | None:
    """The bed this process's frame shows, when running inside the frame server."""
    _, F = servers()
    if not inside(F):
        return None
    p = F.run("display-message", "-p", "#{session_name}", keep_tmux_env=True)
    return p.stdout.strip() or None


def cmd_console(a) -> int:
    slug = resolve_slug(a.slug)
    import curses
    import locale
    locale.setlocale(locale.LC_ALL, "")
    os.environ.setdefault("ESCDELAY", "25")
    got = curses.wrapper(console_view, slug)
    if got and got.startswith(OPEN):
        exec_attach(got[len(OPEN):])
    if got:
        print(f"ovitmugen: {got}", file=sys.stderr)
    return 0


def console_view(scr, slug: str, root: str | None = None) -> str | None:
    """The one console view (§5.7). Hosts: `ov-console` (own curses screen), the frame's
    C-a t popup, and runbook's T modal (runbook's screen — its 1 s tick is switched off
    here; the caller restores it). Returns a one-line result for the host, or None.
    Keys: Enter switch left pane · a add tab · x x close an IDLE tab · o open the bed's
    frame · b build a missing bed · r refresh · q back. Closing never touches a ● tab (law L-c)."""
    import curses
    try:
        curses.curs_set(0)
    except curses.error:
        pass
    scr.timeout(-1)                           # block on keys; a host tick would raise
    A, F = servers()
    sel, msg, armed = 0, "", None
    while True:
        exists = A.has(slug)
        rows = []
        if exists:
            try:
                rows = bed_report(slug)["tabs"]
            except OvError as e:
                msg = str(e)
        if rows:
            sel = max(0, min(sel, len(rows) - 1))
        scr.erase()
        h, w = scr.getmaxyx()
        _put(scr, 0, 0, f" ovitmugen · {slug}", w, curses.A_BOLD)
        if exists:
            hint = " Enter switch · a add · x x close idle · o open frame · r · q"
        else:
            hint = " b build this bed · q back"
            _put(scr, 3, 0, f" no tmux bed '{slug}' yet", w, curses.A_NORMAL)
        _put(scr, 1, 0, hint, w, curses.A_DIM)
        for i, t in enumerate(rows[: max(0, h - 4)]):
            mark = "●" if t["busy"] else "○"
            left = "  ← left pane" if t["left"] else ""
            line = f" {'>' if i == sel else ' '} {mark} {t['index']:>2} {t['name']:<16} {t['cmd']}{left}"
            _put(scr, 3 + i, 0, line, w, curses.A_REVERSE if i == sel else curses.A_NORMAL)
        if msg:
            _put(scr, h - 1, 0, " " + msg, w, curses.A_BOLD)
        scr.refresh()
        try:
            k = scr.get_wch()
        except curses.error:
            continue
        msg = ""
        if k != "x":
            armed = None                      # any other key disarms the close confirm
        if k in ("q", "\x1b"):
            return None
        if k in ("j", curses.KEY_DOWN):
            sel += 1
        elif k in ("k", curses.KEY_UP):
            sel -= 1
        elif k == "r":
            pass
        elif k in ("\n", "\r", curses.KEY_ENTER) and rows:
            try:
                return "left pane → " + switch_tab(slug, rows[sel]["id"])["name"]
            except OvError as e:
                msg = str(e)
        elif k == "a" and exists:
            name = _prompt(scr, "new tab name: ")
            if name:
                try:
                    build_bed(slug, [name], root)
                    msg = f"added tab '{name}'"
                except OvError as e:
                    msg = str(e)
        elif k == "x" and rows:
            t = rows[sel]
            if t["busy"]:
                msg = f"'{t['name']}' runs {t['cmd']} — end the agent there first (/exit)"
            elif armed != t["id"]:
                armed, msg = t["id"], f"close idle tab '{t['name']}'? press x again"
            else:
                armed = None
                try:
                    close_idle_tab(slug, t["id"])
                    msg = f"closed tab '{t['name']}'"
                except OvError as e:
                    msg = str(e)
        elif k == "o" and exists:
            try:
                return open_frame(slug, root)
            except OvError as e:
                msg = str(e)
        elif k == "b" and not exists:
            name = _prompt(scr, f"bed name [{slug}]: ") or slug
            spec = _prompt(scr, "tabs: @preset or names [cSharp bus implement audit]: ")
            try:
                n = build_bed(name, spec.split() if spec else [], root)
            except OvError as e:
                msg = str(e)
                continue
            if inside(F):                     # we are in a frame → show the new one
                F.run("switch-client", "-t", f"={name}", keep_tmux_env=True)
                return f"built '{name}' ({n} steps) — frame switched"
            slug = name                       # stay on the new bed (any name): o opens it
            msg = f"built '{name}' ({n} steps) — o opens its frame"


def _put(scr, y, x, text, w, attr):
    try:
        scr.addnstr(y, x, text, max(0, w - 1), attr)
    except Exception:
        pass


def _prompt(scr, label: str) -> str:
    import curses
    h, w = scr.getmaxyx()
    _put(scr, h - 1, 0, " " + label + " " * (w - len(label) - 2), w, curses.A_BOLD)
    curses.echo()
    curses.curs_set(1)
    try:
        raw = scr.getstr(h - 1, len(label) + 1, 40)
    finally:
        curses.noecho()
        curses.curs_set(0)
    return raw.decode("utf-8", "replace").strip()


# --------------------------------------------------------------------------- selftest

def selftest() -> int:
    """Isolated servers (own sockets, blank agents config, the REAL frame config).
    Never touches `-L default` or `-L ovitmugen`. Prints PASS/FAIL; non-zero on failure."""
    tag = f"ovt{os.getpid()}"
    keep = {k: os.environ.get(k) for k in
            ("OV_AGENTS_SOCKET", "OV_AGENTS_CONF", "OV_FRAME_SOCKET", "OV_PRESETS", "TMUX")}
    tmp = tempfile.mkdtemp(prefix="ovitmugen-selftest-")
    presets = Path(tmp) / "presets.json"
    presets.write_text(json.dumps({"_about": "test", "duo": {"tabs": ["alpha", "beta"],
                                                             "fixed": "shell", "split": "30%"}}))
    os.environ.update({"OV_AGENTS_SOCKET": f"{tag}-agents", "OV_AGENTS_CONF": "/dev/null",
                       "OV_FRAME_SOCKET": f"{tag}-frame", "OV_PRESETS": str(presets)})
    os.environ.pop("TMUX", None)
    A, F = servers()
    fails = 0

    def check(name, cond, detail=""):
        nonlocal fails
        print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"  [{detail}]"))
        fails += 0 if cond else 1

    def wait(pred, secs=3.0):
        end = time.time() + secs
        while time.time() < end:
            if pred():
                return True
            time.sleep(0.1)
        return pred()

    try:
        slug = "bed"
        ops = plan_up(slug, [], DEFAULT_SPLIT, "shell", tmp, (160, 40))
        txt = "\n".join(render(ops))
        check("plan on empty server builds base, 4 tabs, view, frame",
              txt.count("new-window") == 3 and f"-s {slug}--left" in txt and "split-window" in txt,
              txt)
        check("every rendered command names its server (-L)",
              all(l.startswith("tmux -L ") for l in render(ops) if not l.startswith("#")))
        check("no send-keys / paste-buffer anywhere in the plan (law L-a)",
              "send-keys" not in txt and "paste-buffer" not in txt)

        apply(ops)
        ws = windows(A, slug)
        check("base has the default tabs in order",
              [w["name"] for w in ws] == DEFAULT_TABS, [w["name"] for w in ws])
        check("each tab has window-size latest (risk R1)",
              all(A.run("show-options", "-wv", "-t", w["id"], "window-size").stdout.strip()
                  == "latest" for w in ws))
        check("left view exists in the base's group",
              any(s["name"] == slug + LEFT and s["group"] == slug for s in sessions(A)))
        check("frame config loaded (prefix C-a)",
              F.run("show-options", "-gv", "prefix").stdout.strip() == "C-a")
        panes = F.lines("list-panes", "-t", f"={slug}", "-F", "#{pane_current_command}")
        check("frame has 2 panes", len(panes) == 2, panes)
        check("left pane is a live client of the agents view",
              wait(lambda: any(s["name"] == slug + LEFT and s["attached"] >= 1
                               for s in sessions(A))))

        check("re-plan on a complete bed is empty (idempotent)",
              plan_up(slug, [], DEFAULT_SPLIT, "shell", tmp, (160, 40)) == [])

        switch_tab(slug, "bus")
        cur = {w["id"]: w["name"] for w in windows(A, slug)}.get(view_current(A, slug + LEFT))
        base_cur = next(w["name"] for w in windows(A, slug) if w["active"])
        check("tab switch moves the left view to 'bus'", cur == "bus", cur)
        check("base's own current window did not move (views are independent)",
              base_cur == "cSharp", base_cur)

        A.run("new-window", "-d", "-t", f"={slug}:", "-n", "busy", "sleep 600", check=True)
        # shells have transient children while the prompt initialises — wait for settle.
        # (A transient "busy" is the SAFE error: it only ever refuses a close.)
        settled = wait(lambda: not any(t["busy"] for t in tabs(A, slug) if t["name"] != "busy"), 8)
        busy = {t["name"]: t["busy"] for t in tabs(A, slug)}
        check("agent detection: 'sleep' tab busy, shell tabs idle",
              settled and busy.get("busy") is True and busy.get("cSharp") is False,
              [(t["name"], t["cmd"], t["busy"]) for t in tabs(A, slug)])

        A.run("new-window", "-d", "-t", f"={slug}:", "-n", "bus", check=True)
        try:
            switch_tab(slug, "bus")
            check("duplicate tab name is refused", False, "no error raised")
        except OvError as e:
            check("duplicate tab name is refused", "ambiguous" in str(e), str(e))

        # inner detach → left pane dead → up respawns it (remain-on-exit in frame conf)
        A.run("detach-client", "-s", f"={slug}{LEFT}")
        dead = wait(lambda: "1" in F.lines("list-panes", "-t", f"={slug}", "-F", "#{pane_dead}"))
        re_ops = plan_up(slug, [], DEFAULT_SPLIT, "shell", tmp, (160, 40))
        check("after inner detach, up plans exactly a respawn of the left pane",
              dead and [o["args"][0] for o in re_ops] == ["respawn-pane"],
              [o["args"][0] for o in re_ops])
        apply(re_ops)
        check("left pane reconnected",
              wait(lambda: any(s["name"] == slug + LEFT and s["attached"] >= 1
                               for s in sessions(A))))

        # fixed app quits (runbook q / C-c → exit 0) → dead right pane → up restarts it
        right = [l.split("\t")[0] for l in F.lines("list-panes", "-t", f"={slug}", "-F",
                                                     "#{pane_id}\t#{pane_left}")
                 if l.split("\t")[1] != "0"]
        F.run("respawn-pane", "-k", "-t", right[0], "exit 0")
        def right_dead():
            return F.run("display-message", "-p", "-t", right[0],
                         "#{pane_dead}").stdout.strip() == "1"
        rdead = wait(right_dead)
        r_ops = plan_up(slug, [], DEFAULT_SPLIT, "shell", tmp, (160, 40))
        check("after the fixed app quits, up plans a respawn of the right pane only",
              rdead and len(r_ops) == 1 and r_ops[0]["args"][:3] == ["respawn-pane", "-t", right[0]],
              [o["args"] for o in r_ops])
        apply(r_ops)
        check("fixed pane restarted (alive again)",
              wait(lambda: all(l.endswith(" 0") for l in F.lines(
                  "list-panes", "-t", f"={slug}", "-F", "#{pane_left} #{pane_dead}"))))

        # P2.1 — close from the console: busy refused, idle closed (by id: 'bus' is duplicated)
        ids = {t["name"]: t["id"] for t in tabs(A, slug)}
        try:
            close_idle_tab(slug, ids["busy"])
            check("closing a busy tab is refused", False, "no error raised")
        except OvError as e:
            check("closing a busy tab is refused", "end the agent" in str(e), str(e))
        close_idle_tab(slug, ids["implement"])
        check("closing an idle tab works",
              "implement" not in [t["name"] for t in tabs(A, slug)])

        # P2.1 — grouped views are not beds
        A.run("new-session", "-d", "-t", f"={slug}", "-s", "hand-view", check=True)
        names = bed_names(A)
        check("ov-ls: a hand-made grouped view is not listed as a bed",
              slug in names and "hand-view" not in names and slug + LEFT not in names, names)
        check("bed report lists the hand-made view under its bed",
              "hand-view" in bed_report(slug)["views"])
        A.run("kill-session", "-t", "=hand-view")

        # P2.1 — slug rules: given → cwd .dev/session/<bed>/ → the only frame up
        check("slug: an explicit name wins", resolve_slug("given") == "given")
        deep = Path(tmp) / "proj" / ".dev" / "session" / "my-bed" / "raw"
        deep.mkdir(parents=True)
        here = os.getcwd()
        try:
            os.chdir(deep)
            check("slug: inside .dev/session/<bed>/ → the RUNBOOK bed's folder name",
                  resolve_slug(None) == "my-bed")
            os.chdir(tmp)
            check("slug: exactly one frame up → that frame", resolve_slug(None) == slug)
        finally:
            os.chdir(here)
        # P2.2 — console `o`: rebuild a missing frame, then ask the host to attach
        F.run("kill-session", "-t", f"={slug}", check=True)
        got = open_frame(slug)
        check("o: a missing frame is rebuilt and the host is asked to attach",
              got == OPEN + slug and F.has(slug), got)
        check("o: attach argv targets this bed's frame on the frame server",
              attach_argv(slug)[-2:] == ["-t", f"={slug}"] and F.sock in attach_argv(slug))
        os.environ["TMUX"] = "/tmp/some-other-tmux-sock,1,0"
        try:
            open_frame(slug)
            check("o: inside another tmux it refuses (would nest)", False, "no error raised")
        except OvError as e:
            check("o: inside another tmux it refuses (would nest)", "inside tmux" in str(e), str(e))
        finally:
            os.environ.pop("TMUX", None)

        # walk bug 2026-09-29 — the frame's runbook must open on the bed's own root
        proot = Path(tmp) / "proj" / ".dev" / "session"
        rp = plan_up("rooted", [], DEFAULT_SPLIT, "runbook", project_of(str(proot)) or tmp,
                     (160, 40), str(proot))
        txt = "\n".join(render(rp))
        check("root: runbook gets --root <bed session root>, tabs start in the project",
              f"--root {proot}" in txt and f"-c {proot.parent.parent}" in txt, txt[-400:])
        A.run("new-session", "-d", "-s", "rerooted", check=True)
        A.run("new-session", "-d", "-t", "=rerooted", "-s", "rerooted--left", check=True)
        F.run("new-session", "-d", "-s", "rerooted", "sleep 600", check=True)
        F.run("split-window", "-h", "-t", "rerooted", "sleep 600 # runbook.py", check=True)
        fix = plan_up("rerooted", [], DEFAULT_SPLIT, "runbook", tmp, (160, 40), str(proot))
        check("root: an existing frame's runbook on another root is reopened on the right one",
              [o["args"][:2] for o in fix] == [["respawn-pane", "-k"]]
              and f"--root {proot}" in fix[0]["args"][-1], [o["args"] for o in fix])
        for srv in (F, A):
            srv.run("kill-session", "-t", "=rerooted")
        A.run("kill-session", "-t", "=rerooted--left")

        check("frame binds C-a q to persistent pane numbers",
              any(" q " in l and "display-panes -d 0" in l
                  for l in F.lines("list-keys", "-T", "prefix")))

        apply(plan_down(slug, "idle"))
        left = [t["name"] for t in tabs(A, slug)]
        check("down --idle keeps only the busy tab", left == ["busy"], left)
        check("down --idle closed frame and views",
              not F.has(slug) and not A.has(slug + LEFT))

        slug2 = "duo"
        here = os.getcwd()
        os.chdir(tmp)
        try:
            build_bed(slug2, ["@duo"])                 # the console's b path, via a preset
        finally:
            os.chdir(here)
        check("second bed built from preset @duo (two beds, one agents server)",
              [w["name"] for w in windows(A, slug2)] == ["alpha", "beta"] and A.has(slug))
        fw = [int(x) for x in F.lines("list-panes", "-t", f"={slug2}", "-F", "#{pane_width}")]
        check("preset split 30% sizes the fixed pane", len(fw) == 2 and fw[1] < fw[0], fw)
        close_idle_tab(slug2, "alpha")
        try:
            close_idle_tab(slug2, "beta")
            check("the last tab is refused (would end the bed)", False, "no error raised")
        except OvError as e:
            check("the last tab is refused (would end the bed)", "last tab" in str(e), str(e))
        try:
            os.chdir(tmp)
            A.run("new-session", "-d", "-s", "third", check=True)
            F.run("new-session", "-d", "-s", "third", "sleep 60", check=True)
            try:
                resolve_slug(None)
                check("slug: two frames and no hint → refused with the bed list", False)
            except OvError as e:
                check("slug: two frames and no hint → refused with the bed list",
                      "which bed?" in str(e) and "duo" in str(e), str(e))
        finally:
            os.chdir(here)
        try:
            plan_up("a--b", [], DEFAULT_SPLIT, "shell", tmp, (80, 24))
            check("slug with '--' refused", False)
        except OvError:
            check("slug with '--' refused", True)
    except Exception as e:                                  # report, never leave servers behind
        check("selftest ran without exception", False, f"{type(e).__name__}: {e}")
    finally:
        sock_dir = Path(os.environ.get("TMUX_TMPDIR", "/tmp")) / f"tmux-{os.getuid()}"
        for t in (A, F):
            t.run("kill-server")
            try:
                (sock_dir / t.sock).unlink()          # kill-server leaves the socket file
            except OSError:
                pass
        shutil.rmtree(tmp, ignore_errors=True)
        for k, v in keep.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    print(f"ovitmugen selftest: {'OK' if not fails else f'{fails} FAILED'}")
    return 1 if fails else 0


# --------------------------------------------------------------------------- CLI

def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(prog="ovitmugen", description="tmux manager: frame + agents")
    sub = ap.add_subparsers(dest="cmd", required=True)

    u = sub.add_parser("up", help="build missing parts of a bed, then attach the frame")
    u.add_argument("slug", nargs="?", help="default: frame's bed / .dev/session/<bed> cwd / only frame")
    u.add_argument("tabs", nargs="*", help="tab names, or @preset")
    u.add_argument("--split", default=None, help=f"fixed (right) pane width, default {DEFAULT_SPLIT.replace('%', '%%')}")
    u.add_argument("--fixed", default=None, help=f"fixed pane command name, default {DEFAULT_FIXED}")
    u.add_argument("--root", default=None,
                   help="the bed's <project>/.dev/session: runbook opens there, tabs start "
                        "in <project>; re-roots an existing frame's runbook pane")
    u.add_argument("--dry-run", action="store_true", help="print the tmux commands only")
    u.add_argument("--no-attach", action="store_true")
    u.add_argument("--force", action="store_true", help="attach even from inside tmux (nests)")

    t = sub.add_parser("tab", help="switch the left pane to a tab (name, index or @id)")
    t.add_argument("args", nargs="+", metavar="[slug] tab")

    l = sub.add_parser("ls", help="beds, tabs (● agent / ○ idle), views, frame")
    l.add_argument("slug", nargs="?")
    l.add_argument("--json", action="store_true")

    d = sub.add_parser("down", help="peel layers; never closes a tab with a running agent")
    d.add_argument("slug", nargs="?")
    g = d.add_mutually_exclusive_group()
    g.add_argument("--frame", action="store_true", help="close the frame only (default)")
    g.add_argument("--views", action="store_true", help="frame + all views")
    g.add_argument("--idle", action="store_true", help="frame + views + idle tabs")
    d.add_argument("--dry-run", action="store_true")

    c = sub.add_parser("console", help="curses view of a bed's tabs")
    c.add_argument("slug", nargs="?")

    sub.add_parser("selftest", help="isolated servers, PASS/FAIL, zero side effects")

    a = ap.parse_args(argv)
    if a.cmd == "up":
        a.split_given, a.fixed_given = a.split, a.fixed
    if a.cmd == "up" and a.slug and a.slug.startswith("@"):
        a.tabs, a.slug = [a.slug, *a.tabs], None          # `ov-up @csharp` → preset, slug by rules
    if a.cmd == "tab" and len(a.args) > 2:
        ap.error("tab takes [slug] tab")
    try:
        return {"up": cmd_up, "tab": cmd_tab, "ls": cmd_ls, "down": cmd_down,
                "console": cmd_console, "selftest": lambda _a: selftest()}[a.cmd](a)
    except OvError as e:
        print(f"ovitmugen: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
