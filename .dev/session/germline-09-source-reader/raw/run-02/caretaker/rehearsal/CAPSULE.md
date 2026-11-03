State: PREPARED-HOLD. Evidence: readiness emitted the documented unresolved/invalid HOLD diagnostic; exact inspect lookup returned `unknown / missing-or-malformed-receipt` (exit 0). The readiness exit 2 is documented/expected, not independently captured because its first wrapper used zsh’s read-only `status`; the command was not repeated. Pin acceptance is therefore unconfirmed.

Eight isolated fixtures are classified in [DECISIONS.json](DECISIONS.json); every `new_target_attempts` is 0. Simulated IDs were not operated. No release, profile, vault, target, or product action occurred.

Loaded paths and hashes, plus visible caretaker task handle, are in [LOAD.json](LOAD.json). Command stdout/stderr and exit records are in [COMMANDS.json](COMMANDS.json) and sibling logs.

Blocker: HOLD remains unresolved and current pin acceptance is not proved. Next action: Cartan resolves the HOLD/pin status and issues any fresh authorized POINT before further preparation or dispatch.
