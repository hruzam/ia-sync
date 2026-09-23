# voice-record — copy-paste command sheet (Baseus MZ10, home)

Records a claude.ai voice meeting over the MZ10 Bluetooth headset. Copy a block, run it.
No report-back — just commands.

- Records land in `~/ia-sync/.dev/session/voice-meetings-01-threshold/records/` (git-ignored — audio never
  gets committed). Naming: `YYYY-MM-DD.<label>.wav`.
- Only text transcripts/protocols leave this folder; audio moves over tailnet if ever needed.
- **Quality ceiling:** mic + playback at once = Bluetooth HFP = **16 kHz mono** (telephone-grade),
  both directions. No app raises it. If that's not enough → wired/USB mic.
- Each command derives the mic/output source itself, so a re-pair or MAC change won't stale it.

---

## Is the mic live? (run first if a record errors)

```bash
pactl list short sources | grep bluez_input || echo "no mic — reconnect the MZ10, or press play on anything for 2s to force HFP"
```

## 15-second mic-only test (talk while it runs)

```bash
ffmpeg -y -f pulse -i "$(pactl list short sources | awk '/bluez_input/{print $2; exit}')" -t 15 ~/ia-sync/.dev/session/voice-meetings-01-threshold/records/$(date +%F).mic-test.wav
```

## Play back today's mic test

```bash
pw-play ~/ia-sync/.dev/session/voice-meetings-01-threshold/records/$(date +%F).mic-test.wav
```

## Both sides (your voice + Claude's), 30-second test — run during a live voice session

```bash
ffmpeg -y -f pulse -i "$(pactl list short sources | awk '/bluez_input/{print $2; exit}')" -f pulse -i "$(pactl list short sources | awk '/bluez_output.*monitor/{print $2; exit}')" -filter_complex amix=inputs=2:duration=longest -t 30 ~/ia-sync/.dev/session/voice-meetings-01-threshold/records/$(date +%F).both-test.wav
```

## Play back today's both-sides test

```bash
pw-play ~/ia-sync/.dev/session/voice-meetings-01-threshold/records/$(date +%F).both-test.wav
```

## Full meeting — both sides, FLAC, runs until you press `q` (or Ctrl-C)

```bash
ffmpeg -y -f pulse -i "$(pactl list short sources | awk '/bluez_input/{print $2; exit}')" -f pulse -i "$(pactl list short sources | awk '/bluez_output.*monitor/{print $2; exit}')" -filter_complex amix=inputs=2:duration=longest -c:a flac ~/ia-sync/.dev/session/voice-meetings-01-threshold/records/$(date +%F-%H%M).meeting.flac
```

## Same, but hard-stop at 1 hour (add `-t 3600`)

```bash
ffmpeg -y -f pulse -i "$(pactl list short sources | awk '/bluez_input/{print $2; exit}')" -f pulse -i "$(pactl list short sources | awk '/bluez_output.*monitor/{print $2; exit}')" -filter_complex amix=inputs=2:duration=longest -t 3600 -c:a flac ~/ia-sync/.dev/session/voice-meetings-01-threshold/records/$(date +%F-%H%M).meeting.flac
```

## List what you've recorded

```bash
ls -lh ~/ia-sync/.dev/session/voice-meetings-01-threshold/records/
```

---

Notes: if the both-sides mix is unbalanced (one voice louder), `amix` takes per-input weights —
say the word and I'll add a weighted variant. Higher-than-16 kHz mic needs LE Audio (LC3) on both
ends or a wired/USB mic — not possible on the MZ10 in duplex.
