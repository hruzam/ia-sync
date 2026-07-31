---
name: pull
description: >
  Invoke as /pull <scope>. Local image extraction runner — sibling to /refresh.
  Reads scope config from raw.research/<scope>/draft/README.md (pull: section),
  processes screenshot batches from photos_path, writes code-extraction report to report/.
  Scope is mandatory — if omitted, lists scopes with a pull: section configured.
  Use for periodically processing screenshot batches from video channels or social posts.
tools:
  - Read
  - Write
---

I am the `/pull` skill — local image extraction runner for research scopes.
The variable part lives in the scope's `draft/README.md` under the `pull:` key.
I read it, process the batch, and prompt once before writing.

## Steps

1. **Check scope argument.** If missing:
   - Glob `~/reposoma/raw.research/*/draft/README.md` to find all scope configs
   - List only scopes whose README contains a `pull:` section
   - Ask which scope to run
   - Stop here

2. **Read scope config** from `~/reposoma/raw.research/<scope>/draft/README.md`.
   Extract the `pull:` block: `photos_path`, `output_path`, `purpose`.
   If no `pull:` section found: report the error, list pull-enabled scopes, stop.

3. **List images** in `photos_path`. Accepted: `.png`, `.jpg`, `.jpeg`, `.webp`, `.heic`.
   Skip any `processed/` subfolder — those are already done.
   If folder empty or missing: report and stop.
   If `.heic` files present: note in footer — HEIC may render as blank on some systems;
   convert to PNG first if extraction produces no output.

4. **Read each image** via Read tool. For each:
   - Extract all visible code (preserve indentation and language)
   - Extract any surrounding text context: title bar, captions, channel label, description text
   - Note the filename as the source reference

5. **Synthesize in-session.** Group images by inferred topic if multiple cover the same
   technique or video. For each group or single image:
   - Technique / topic (inferred from code + context)
   - Full extracted code (indentation preserved)
   - Language detected (php, blade, js, etc.)
   - Explanation: 2–4 sentences — what the technique does, when to use it, anything notable
   - Source hint: video title or channel label if visible in screenshot

6. **Prepare write artifact** (`output_path` with `<YYYY-MM-DD>` substituted to today):
   ```
   # <scope> pull — <date>
   _Extracted: <date> | Images: <count> | Source: <purpose one-liner>_

   ## <technique or topic>

   ```<lang>
   <extracted code>
   ```

   **What it does:** <explanation>
   **Context:** <source hint if visible>

   ---
   [repeat per topic / group]

   ## Pull metadata
   - Images read: <filenames list>
   - Topics found: <N>
   - HEIC warnings: <filenames if any — else omit line>
   ```

7. **Single confirm prompt:**
   ```
   ## Pull summary
   - Images read: N
   - Topics found: N
   - Output: <output_path>

   Write report? (yes / no)
   Move processed images to <photos_path>/processed/? (yes / no)
   ```
   Both questions independent.
   **On write yes:** write the output file.
   **On move yes:** move all processed images to `<photos_path>/processed/`
   (create the subfolder if it does not exist).
