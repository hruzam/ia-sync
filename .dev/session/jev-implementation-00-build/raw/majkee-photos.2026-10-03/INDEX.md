---
what: majkee's photos and phone screenshots behind the Jev smoothing, 2026-10-03 and 2026-10-04
copied_by: flight, 2026-10-05, at majkee's request, so that Cartan can look at them
source: >-
  majkee's mobile app uploads into Flight's Claude Code session (host-local, office):
  ~/.claude/uploads/5325e884-a1cd-434a-bfb8-13885be3bf1b/<id>-image.jpg.
  The copies are byte-identical; nothing was rotated, resized or edited.
transcribed_in: ../flight-jev-map.md §1 (the ids p0–p5 and T[1]–[3] match these file names)
---

# majkee's photos: Jev implementation notes, tunnel protocols, study screens

| file | what it shows | map §1 id | upload id |
|---|---|---|---|
| `p0.jev-implementation.creative-buffer-loop.jpg` | Page 0: goal, roles map, "main philosophy" (deterministic process first). **Shot sideways.** | p0 | 37d580c1 |
| `p1.jev-implementation.protocol-1-shuttle.jpg` | Page 1 (dated 2026-10-03): where Jev sits in the loop; `/shuttle/`; Q1.1–Q1.3 | Q1.1–Q1.3 | dbf32a6f |
| `p2.jev-implementation.protocol-2-placement.jpg` | Page 2: Q2.1 (A) operational device · (B) relay/router · (C) PTY attractor; living session with watchdogs | Q2.1 | 2540c001 |
| `p3.jev-implementation.harness-shape-challenger.jpg` | Page 3: Q3.1 harness richness vs vendor TUIs · Q3.2 Jev as a different shape · X.1 challenger organ | Q3.1, Q3.2, X.1 | d64393cd |
| `p4.jev-implementation.math-conflict-judgement.jpg` | Page 4: Q3.3 maths, proof by conflict; [JUD] diagram; `-p` locked "not use" | Q3.3 | 6e640200 |
| `p5.jev-implementation.cascade-schema-map.jpg` | Page 5: no composite now; Q3.4 cascade; "schema, map and use cases most wanted" | p5, Q3.4 | a745d682 |
| `t1.tunnel.protocol-1-two-hemispheres.jpg` | Tunnel Protocol [1]: Codex head (cSharp) ⇄ Claude bus; spawns; PADs for the human | T[1] | 23e20bde |
| `t2.tunnel.protocol-2-claude-head-codex-workers.jpg` | Tunnel Protocol [2]: Claude head spawning Codex bus + implementer; Q1 "same main?" | T[2] | ff52c001 |
| `t3.tunnel.protocol-3-tester-hands-on.jpg` | Tunnel Protocol [3]: tester with hands on the computer; PAD-writer sub | T[3] | 2922e928 |
| `s1.study.advisor-agent-stack.jpg` | Screenshot: a post about Claude Code's advisor, with a third-party "JEV fork layer" mock | study | 8a5e7b9f |
| `s2.study.jev-as-a-judge.post-1.jpg` | Screenshot: post about the CMU paper "JEV-as-a-Judge" (arXiv 2609.26550, v1 abstract) | study | 9f342da1 |
| `s3.study.jev-as-a-judge.post-2.jpg` | Same post, scrolled: abstract and figure 1 | study | 605975d3 |
| `s4.study.jev-engineering-coding-agents.jpg` | Screenshot: post about "Jev Engineering for Coding Agents" (independent note; five typed decisions; cost table) | study | 54d13d2d |

The paper and the advisor feature were checked against their sources; see the map's §3.

## Handling notes

- **Size: 22 MB.** Keep these out of git unless majkee decides otherwise. Account for them
  in the cSharp promotion manifest (local provenance), and do not prune them before the
  manifest does.
- **Git-excluded on this clone only** (majkee, 2026-10-05). Rule:
  `.dev/session/**/*.jpg` in `~/ia-sync/.git/info/exclude`. It is never pushed and never
  syncs to home.
  - The `.jpg` files therefore **do not show in `git status`**. List this folder directly
    when building the manifest.
  - This `INDEX.md` stays visible to git.
  - The same rule also covers the untracked protocol photos in
    `.dev/session/tunnel-upgrade-01-parametrization/raw/`.
- **Faint text bleeds through** on some notebook sheets from the reverse side of the paper
  (printed Czech documents). Look before sharing beyond this host.
- **The screenshots show public social-media posts** by third parties. They are kept as
  study provenance only.

## Verify

Run in this folder:

```text
2a2e87b297ed2e76d143ad061bb7314fcb3f169e85f770c7b0241797a0fd9261  p0.jev-implementation.creative-buffer-loop.jpg
c53713b82374f98835eb7002a05b5cf5d02f6c19df78e5079524f243130ffc4c  p1.jev-implementation.protocol-1-shuttle.jpg
04deb200bf0e1b32e2ef2293089ec7d420f633500319f5e1d73d0bcac41fca4d  p2.jev-implementation.protocol-2-placement.jpg
730591271ddd6b20e5402894231294c0b7bd3d3c6889f7db1ddf24379f6454c7  p3.jev-implementation.harness-shape-challenger.jpg
83032258b73119da8a2b3a9d46bc16230a17228ee7862e75608a5e1620def8b5  p4.jev-implementation.math-conflict-judgement.jpg
38f7e06907a06eacf58f6e564e637fdd03b779b5062306e71633a9448611a9c6  p5.jev-implementation.cascade-schema-map.jpg
34d63d9a8a711ee38afcf7b609eb52ee08cc5e49d1feb13333b29e11f30de774  s1.study.advisor-agent-stack.jpg
04843650c7b8b0ee2b1460e1959fe2132ac1128da5916d472133f6d622bcd0da  s2.study.jev-as-a-judge.post-1.jpg
bc3a66f25332469879482be3423350325b0d213c6c1aaeb26d9797d382a3c13a  s3.study.jev-as-a-judge.post-2.jpg
308f3e46dc521a1237cdd2c6e26b71949c32c3f622886cd8621e6ea019edc061  s4.study.jev-engineering-coding-agents.jpg
f8d9ef33a224444dc1bf4b5898dc8dc39af5387d7f04f48529a0fca42f1527b3  t1.tunnel.protocol-1-two-hemispheres.jpg
446b767298de5f1a5479817969e01e3b4eef923a8041eacde2342447c601bbee  t2.tunnel.protocol-2-claude-head-codex-workers.jpg
b24d5504cb8d25aab55e0a6dce5ddfffd00784140f69a0a891513cd87293a52a  t3.tunnel.protocol-3-tester-hands-on.jpg
```

Save the block above as `SHA256SUMS` and run `sha256sum -c SHA256SUMS`, or compare by eye
against `sha256sum *.jpg`.
