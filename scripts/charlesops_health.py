#!/usr/bin/env python3
import argparse, json, shutil, subprocess, time
from pathlib import Path

LOG = Path('/home/tom/hermes-workspace/logs/charlesops_health.jsonl')

def run(cmd, timeout=12):
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {'rc': p.returncode, 'out': p.stdout.strip()[:4000], 'err': p.stderr.strip()[:1000]}
    except Exception as e:
        return {'rc': 127, 'out': '', 'err': str(e)}

def classify(f):
    return {
        'failed_service': f['service_rc'] != 0,
        'low_disk': f['disk_used_pct'] >= 90,
        'model_fallback_needed': f['model_probe_rc'] != 0 and bool(f['known_fallback']),
        'tailscale_problem': f['tailscale_rc'] != 0,
        'post_reboot_recovery_needed': f['boot_age_seconds'] < 900 and f['service_rc'] != 0,
    }

def self_test():
    base = dict(service_rc=0, disk_used_pct=40, model_probe_rc=0, known_fallback='llama3.2', tailscale_rc=0, boot_age_seconds=5000)
    cases = [
        ('failed_service', {'service_rc': 3}),
        ('low_disk', {'disk_used_pct': 95}),
        ('model_fallback_needed', {'model_probe_rc': 1}),
        ('tailscale_problem', {'tailscale_rc': 1}),
        ('post_reboot_recovery_needed', {'service_rc': 3, 'boot_age_seconds': 100}),
    ]
    results=[]
    for expected, delta in cases:
        f=base.copy(); f.update(delta); got=classify(f)
        results.append({'scenario': expected, 'pass': got[expected], 'classification': got})
    return {'pass': all(x['pass'] for x in results), 'scenarios': results}

def health():
    du=shutil.disk_usage('/')
    disk=round(100*du.used/du.total, 1)
    services={name: run(['systemctl','--user','is-active',name]) for name in ('hermes-gateway.service','openclaw.service')}
    gpu=run(['nvidia-smi','--query-gpu=name,memory.used,memory.total,temperature.gpu','--format=csv,noheader'])
    ollama=run(['ollama','list'])
    tailscale=run(['tailscale','status','--json'])
    uptime=run(['cat','/proc/uptime'])
    boot_age=float(uptime['out'].split()[0]) if uptime['rc']==0 and uptime['out'] else -1
    backup_candidates=['/home/tom/backups','/home/tom/hermes-backups','/mnt/backups']
    backups=[p for p in backup_candidates if Path(p).exists()]
    facts={'service_rc': 0 if any(v['rc']==0 for v in services.values()) else 3,
           'disk_used_pct': disk, 'model_probe_rc': ollama['rc'], 'known_fallback': 'llama3.2:3b',
           'tailscale_rc': tailscale['rc'], 'boot_age_seconds': boot_age}
    result={'timestamp': int(time.time()), 'host_checks': {'services':services,'disk_used_pct':disk,'gpu':gpu,'ollama':ollama,'tailscale_rc':tailscale['rc'],'backup_paths':backups,'boot_age_seconds':boot_age}, 'classification':classify(facts)}
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open('a') as fh: fh.write(json.dumps(result,sort_keys=True)+'\n')
    return result

if __name__ == '__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--self-test',action='store_true'); a=ap.parse_args()
    result=self_test() if a.self_test else health()
    print(json.dumps(result,indent=2,sort_keys=True)); raise SystemExit(0 if result.get('pass',True) else 1)