"""Harmless buffered process to test native session/PID observations across the sandbox."""
import json
import os
from pathlib import Path
import time

out = Path(__file__).with_name('session-visibility-runner.json')
if out.exists():
    raise RuntimeError('Refusing to overwrite earlier probe')
record = {'pid': os.getpid(), 'start': Path('/proc/self/stat').read_text().rsplit(')', 1)[1].split()[19],
          'pid_namespace_inode': os.stat('/proc/self/ns/pid').st_ino,
          'started_unix': time.time(), 'stage': 'pending'}
with out.open('x') as handle:
    json.dump(record, handle, indent=2)
time.sleep(20)
record.update(stage='completed', ended_unix=time.time())
out.write_text(json.dumps(record, indent=2) + '\n')
print('buffered probe completed', flush=True)
