# G09 run-02 C1 caretaker HOLD

Native caretaker handle: `/root/g09_run02_caretaker` (assigned default, gpt-6-luna/high, fork_turns:none). Role contract: `codex/agents/implementer.toml`, SHA256 `bb431c1c0bc5fda7e385c62a2e371df39c75155a9e21f476b6ed5c3fdd2792c7`.

Loaded run-02 pins: contract `84be154eb074088af75f003cd760b0ccb904061afb46851135e8ad4203f1d214`; source manifest `d72e6b552f7e05e2e5c5657631526b989dea28d2cc3a372919845a1c86ad51db`; controller `98a42758f046528d2e8f23441bd7e5fbfccd889d3cbeb6d85a46e3e87184c64b`; TUNNEL `a4a9a7bbdc45cb10c21b7f174915b15f9b87aa84a46c66255bfb982446a8b4ab`; consult `284adb1318b369d61e3a7b26c7f1e677c78e3b73d618ee64dabf8e6be2a25b88`; caretaker brief `2a3da02b743d353602d2c217ba63e23b74f213e15788adc32ed045f70a9174ed`.

Offline readiness and R1/A1 compilation passed; plan and compiled packets were created under `caretaker/`. Immediately before the first live effect, current preservation passed: 97 protected files, 9 foreign files, journal and pulse reconciliations valid, run-01 release false, run-02 release true.

First authorized live command was `python3 -B .../caretaker/run_operations.py profile researcher` with escalation. It exited 2 with `release lacks fresh operator message provenance`. Exact profile receipt `caretaker/operations/run02.researcher.profile.operation.json` is absent, consistent with validation failing before profile RPC/reservation. No profile RPC, open, or target ask is evidenced; no target attempt submitted. Stop: no retry, repair, or subsequent operation.

Mismatch: RELEASE records `message_reference`; adapter `require_release` requires `operator_message_reference`. This capsule records the observed disagreement; no files outside caretaker evidence/RETURN were changed.

Uncertainty: native profile capability remains unknown. Next task: Cartan adjudicates the release/adapter field mismatch; any changed frozen source requires the authorized repair and independent verification path before a fresh POINT.
