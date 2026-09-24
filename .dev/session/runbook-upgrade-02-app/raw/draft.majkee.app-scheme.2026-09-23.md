---
what is it:
created: 

---

# 1. what is it

> decission where we go now and next,
> this should be architectural session also claude (oraculum | trajectory) + codex (now cartan).

## 1.1. nablarva *(itself)*

- agentive framework, multisession drive, decentralized rag connector
- multisession driwing -mesage buss and control mechanism over vendors and sessions


---

# 2.process

1. read all first -> reconsiliation
2. `~/ia-sync/zsh/session/`-> look please on all runbook-tool sessions . `-00` is finished, `coordination` should be also. but need check if anything is not flying.

## 2.1. planning phase

**questions which should be answered**
1. wrapper| ui -> still terminal or some terminal wraper + process window -> real app -> than build should move seriously to `~/unikuklatrix/nablarva/.dev/session/toobox-instarmux
2. but also prepared for your advices

# 3. APP parts

## 3.1. termbrana

 - semitransparent foil allowing one typewriting system over all (keys, shortcuts, lighter navigation for terminal inputs -> agentive UI)
 - bridge between terminal, ai session, browser (firefox), files
 - example: have file on line nr. xxx will add `NOTE<nr>` -> open appropriate buffer collector for notes -> I can attach ai session on specific notes, same should be allowed in browser by press any key I can make note with address and anchor to specific HTML part or  
 - requires `instatmux` -> dashboard part with sessions
 --> if to much - heavy on one toobox can be splitted to parts per scope of process. 

---

## 3.2. ovitmugen *(tool)*
- origin `instar` - phase session (taken from biological names), `tmux`
-> tmux manager - part of runbook tool
- reconsiliate if columns are enough layout, I assume growing needs more space, untill today it was only helper
- holding session dashboard

###### function ADD
- click on some selected session vault, run tmux manager over it (user
  should fill session name, number of 'columns' - I assume windows and name for bed - postures, we can have generic fallback - default_(n), cSharp, bus,... I can add to existing scheme also new beds for another agentive sessions
## function create
no bond to specific `.dev/session/<specific-session>`

## another managing options
 like 
 - kill whole tmux session, extend to another beds


### 3.1.1. demanded tree

```tree

└── global-tmux-session # majkee: assume per <slug> f.e.. maybe I am not understanding what session is here (coliding to twins?)
    │
    ├── window_1 # f.e. bed for agent who will drive task proces like cSharp (somebody in charge)
    │	 └── cSharp # pane, majkee: still not understanding why is pane something different from window
    │
    ├── window_2
	...	 └── bus # here is another agentive session with different task


```

--> **reconsiliate** if columns are enough layout, I assume growing needs more space, untill
  today it was only helper

### 3.2.x. @Trajectory notes — tips, observations, upgrade ideas *(append-only, dated)*

> Full architecture: `~/unikuklatrix/nablarva/.dev/session/ovitmugen-00-console/raw/draft.trajectory.ovitmugen-architecture.2026-09-23.md`
> These notes are the short, growing layer on top of it. Newest at the bottom.

**2026-09-24 · answers to the inline questions in 3.1.1**
- *"what is session here, colliding to twins?"* A session = a named group of windows. It
  remembers **one** current window, so two terminals on one session always show the same
  window (the twins). Fix: every terminal column gets its own **view** session (`<slug>--<win>`),
  sharing the same windows. Columns are then independent.
- *"why is pane different from window?"* Window = a whole screen (a tab). Pane = a piece of
  that screen when you split it. Every window has at least 1 pane; the agent runs in the pane.
  One agent per window → you can ignore panes.
- *"are columns enough layout?"* Yes, with layout C: the left pane switches between tabs, so
  it grows by adding **tabs**, not columns. Screen width stops being the limit.

**2026-09-24 · decided so far** (source: architecture doc §1, §5.7, §9)
- layout C: frame (own tmux server `ovitmugen`) + agents (normal tmux) · left = tabs, right = runbook fixed
- split 60/40, live resize `C-a <` / `C-a >` · prefix `C-a` (`C-a C-a` = shell start-of-line)
- tabs = empty shells, agents started by hand · console = one view: popup `C-a t` / runbook `T` / `ov`
- docs in nablarva · build in `~/ia-sync/zsh/session/` → `bash deploy.sh`

**2026-09-24 · tips (learned the hard way, 2026-09-23)**
- **Address by ID, not by name**, after creating anything. One session had two windows named
  `bus`, and any `:bus` target became a guess. tmux hands back IDs (`@12`, `%7`) at creation.
- **`=` on a pane target fails** (`=frame:0.1` → can't find pane). `=` is fine for session/window.
- **Name the tmux server in every call** (`-L default` / `-L ovitmugen`). runbook runs *inside*
  the frame, so a bare `tmux` from runbook would hit the frame, not the agents.
- **`window-size largest`** (`~/.tmux.conf`): a tab seen in the narrow left pane *and* on the phone
  gets sized to the phone's width, so the left pane crops. Plan: per-window `window-size latest`.
- Safe-kill rule used in the cleanup: a pane hosts an agent if its command isn't a bare shell
  **or** the shell has child processes. Never kill those.

**2026-09-24 · principles worth keeping beyond ovitmugen** (candidates, not law)
- **A viewer never owns lifetime.** Frame, termbrana foil, a future GUI: they only *show*.
  Closing a viewer must never kill an agent or the broker. Direct consequence for nablarva
  docket 4 (broker as a tmux pane): the broker gets a **tab in the agents server**, never a
  pane in the frame.
- **Dry-run = the manual recipe.** Every zsh/py brick's `--dry-run` prints the literal
  commands; that output is the HELP. Tool and docs can't drift apart.
- **ovitmugen never types into panes** (no `send-keys`, nablarva L4). It switches *views* only.
  If someone asks "can ovitmugen send the prompt to tab X?", the answer is no; that's the bus's job.

**upgrade ideas (not scheduled, pick when needed)**
- `ov ls --json` → termbrana reads it as its dashboard source (3.1 "requires … dashboard part with sessions")
- phone view `<slug>--phone`: the phone attaches to its own view and never steals the left pane's tab
- permanent console pane as a preset option (`"fixed": ["runbook","ovitmugen"]`) if the popup gets used constantly
- t41 folds into ovitmugen (`t41` = thin alias over `ov up`), one preset file for both
- cross-host frame: home shows office agents (`ssh -t office tmux -L ovitmugen attach`), nablarva Stage 2
- tab badges in the console: `●` agent running · `○` empty · later `!` = agent waiting for input (read-only signal, never input)

---

## 3.3. instarmux *(tool)*

## 3.4. reposoma *(tool, not `~/reposoma` - this is substrate)*