# Peer-B initial ask: preserved unknown boundary

The caretaker invoked `run_shim.py peer-b ask tunnel.peer-b.state.json prompt.peer-b.txt` after
the authorized peer-B open. The controller reported a running cell and then a completed cell,
but no `peer-b.ask.receipt.json`, stdout, or stderr artifact exists. The saved state remains the
open preflight state: `threadId: null`, `lastTurnId: null`, model `gpt-6.1-sol`, sandbox
`read-only`. This does not prove no remote request began. Per POINT/FUNCTION, do not retry or
read without a saved target identity.
