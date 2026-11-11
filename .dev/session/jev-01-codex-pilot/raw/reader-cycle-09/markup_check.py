import json, markdown
from pathlib import Path
root=Path('/home/hruzam/ia-sync/.dev/session/jev-01-codex-pilot/raw/reader-cycle-09')
view=next(root.glob('jev-view-*/view.md'))
source=view.read_text()
checks=[]
for extensions in ([], ['fenced_code']):
    html=markdown.markdown(source,extensions=extensions)
    checks.append({'extensions':extensions,'raw_fixture_script_element':'<script>DEMO_ONLY</script>' in html,
                   'escaped_fixture_script':'&lt;script&gt;DEMO_ONLY&lt;/script&gt;' in html})
pty=(root/'pty.raw').read_bytes()
result={'view':str(view),'parser':'Python-Markdown '+markdown.__version__,'checks':checks,
        'pty_80x24_full_scenario_01_visible':b'01-memory-notes' in pty,
        'pty_80x24_full_scenario_02_visible':b'02-mixed-judgments' in pty,
        'pty_80x24_synthetic_prefix_visible':b'SYNTHETIC' in pty}
(root/'markup-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
