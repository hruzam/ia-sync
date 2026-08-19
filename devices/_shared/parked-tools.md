# Parked device tools

Tools built for phone/tablet ↔ PC workflows that are dormant but kept for reuse.
Rule: a parked tool's listener is OFF; only the script stays.

## screenshot harvest bridge (Laravel screenshots, phone → PC)

- **Status:** parked 2026-08-19 (job finished; port was still open — closed by @Delta)
- **Host:** home (`hruzam`, 100.110.27.60)
- **Script:** `~/reposoma/raw.research/laravel-daily-harvest/harvest-upload.py` (preserved, executable)
- **Was:** `python3 harvest-upload.py`, manual start, listened on `0.0.0.0:8033`
- **Relaunch:** `cd ~/reposoma/raw.research/laravel-daily-harvest && python3 harvest-upload.py`
- **On relaunch, harden first:** bind to the tailscale IP (100.110.27.60), not `0.0.0.0` —
  the old bind exposed it to the whole LAN. Stop it again when the batch is done.
