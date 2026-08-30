#!/usr/bin/env python3
import json, subprocess, sys, tempfile
from pathlib import Path

def run(cmd, cwd, expect=0):
    p = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if p.returncode != expect:
        raise RuntimeError(f"{cmd} rc={p.returncode}, expected={expect}\nstdout={p.stdout}\nstderr={p.stderr}")
    return {'command': ' '.join(cmd), 'rc': p.returncode, 'stdout': p.stdout.strip(), 'stderr': p.stderr.strip()}

with tempfile.TemporaryDirectory(prefix='developer-workflow-') as td:
    repo = Path(td)
    (repo / 'calculator.py').write_text('def safe_divide(a, b):\n    return a / b\n')
    (repo / 'test_calculator.py').write_text(
        'import unittest\nfrom calculator import safe_divide\n\n'
        'class Tests(unittest.TestCase):\n'
        '    def test_normal_division(self): self.assertEqual(safe_divide(8, 2), 4)\n'
        '    def test_zero_returns_none(self): self.assertIsNone(safe_divide(8, 0))\n\n'
        "if __name__ == '__main__': unittest.main()\n")
    run(['git','init','-q'], repo)
    run(['git','config','user.email','developer-test@localhost'], repo)
    run(['git','config','user.name','Developer Test'], repo)
    run(['git','add','.'], repo)
    run(['git','commit','-qm','fixture: deliberate divide-by-zero bug'], repo)

    red = run([sys.executable,'-m','unittest','-q','test_calculator.Tests.test_zero_returns_none'], repo, expect=1)
    (repo / 'calculator.py').write_text('def safe_divide(a, b):\n    if b == 0:\n        return None\n    return a / b\n')
    focused = run([sys.executable,'-m','unittest','-q','test_calculator.Tests.test_zero_returns_none'], repo)
    broad = run([sys.executable,'-m','unittest','discover','-q'], repo)
    compile_check = run([sys.executable,'-m','compileall','-q','.'], repo)
    diff_check = run(['git','diff','--check'], repo)
    diff = run(['git','diff','--','calculator.py'], repo)
    if 'if b == 0:' not in diff['stdout'] or 'test_calculator.py' in diff['stdout']:
        raise RuntimeError('diff review failed: implementation missing or regression test was weakened')
    # The reverse patch is supplied explicitly so rollback is checked without mutating the repository.
    patch = subprocess.run(['git','diff'], cwd=repo, text=True, capture_output=True, check=True).stdout
    rp = subprocess.run(['git','apply','--check','-R','-'], cwd=repo, input=patch, text=True, capture_output=True)
    if rp.returncode != 0:
        raise RuntimeError(f'rollback check failed: {rp.stderr}')

    print(json.dumps({
        'ok': True,
        'red_test_rc': red['rc'],
        'focused_test': focused,
        'broader_suite': broad,
        'compile_check': compile_check,
        'diff_check': diff_check,
        'changed_files': ['calculator.py'],
        'rollback_check_rc': rp.returncode,
        'risk': 'isolated temporary repository; no production files changed'
    }, indent=2))