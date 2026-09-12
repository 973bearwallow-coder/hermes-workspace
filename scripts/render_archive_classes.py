#!/usr/bin/env python3
"""Wait for delegated class scripts, then render all archive classes."""
from pathlib import Path
import subprocess, time, sys

classes = Path('/home/tom/hermes-workspace/coaching-calls/2026-09-02-to-2026-09-09/classes')
audio = Path('/home/tom/hermes-workspace/coaching-calls/audio')
renderer = '/home/tom/hermes-workspace/scripts/render_voicebox_class.py'
python = '/home/tom/voicebox-env/bin/python'
names = [
    '2026-09-02-coffee-hour-mini-class',
    '2026-09-04-coffee-hour-mini-class',
    '2026-09-07-coffee-hour-mini-class',
    '2026-09-09-coffee-hour-mini-class',
    '2026-09-02-guild-spark-mini-class',
    '2026-09-04-guild-spark-mini-class',
    '2026-09-07-guild-spark-mini-class',
    '2026-09-09-guild-spark-mini-class',
]
deadline = time.time() + 900
missing = names.copy()
while time.time() < deadline:
    missing = [n for n in names if not (classes / f'{n}.txt').exists()]
    if not missing:
        break
    print('Waiting for:', ', '.join(missing), flush=True)
    time.sleep(10)
else:
    raise TimeoutError('Class scripts did not arrive before deadline: ' + ', '.join(missing))

for name in names:
    src = classes / f'{name}.txt'
    dst = audio / f'{name}.mp3'
    subprocess.run([python, renderer, str(src), str(dst)], check=True)
print(f'Rendered {len(names)} archive classes.', flush=True)
