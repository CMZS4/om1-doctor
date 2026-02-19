from __future__ import annotations
import os, shutil, socket, subprocess
from pathlib import Path
from datetime import datetime
import psutil

from .checks.signatures import match_signatures

def _run(cmd: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out.strip()
    except Exception as e:
        return 1, str(e)

def _port_open(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.2)
        return s.connect_ex(("127.0.0.1", port)) == 0

def build_report(service_name: str, log_path: Path | None):
    checks = []
    now = datetime.utcnow().isoformat() + "Z"

    du = shutil.disk_usage(Path.cwd().anchor)
    ram = psutil.virtual_memory()

    checks.append({
        "name": "Disk free",
        "status": "OK" if du.free > 5 * 1024**3 else "WARN",
        "details": f"{du.free/1024**3:.1f} GB free on drive"
    })
    checks.append({
        "name": "RAM available",
        "status": "OK" if ram.available > 1 * 1024**3 else "WARN",
        "details": f"{ram.available/1024**3:.1f} GB available"
    })

    code, out = _run(["python", "--version"])
    checks.append({
        "name": "Python",
        "status": "OK" if code == 0 else "FAIL",
        "details": out
    })
    code, out = _run(["uv", "--version"])
    checks.append({
        "name": "uv",
        "status": "OK" if code == 0 else "WARN",
        "details": out or "uv not found"
    })

    # systemctl won't exist on Windows (that's fine)
    code, out = _run(["systemctl", "status", service_name, "--no-pager"])
    checks.append({
        "name": f"systemd:{service_name}",
        "status": "OK" if code == 0 else "INFO",
        "details": "systemctl not available on Windows (expected)"
    })

    ports = [8000, 8545]
    port_details = ", ".join([f"{p}:{'open' if _port_open(p) else 'closed'}" for p in ports])
    checks.append({
        "name": "Local ports",
        "status": "OK",
        "details": port_details
    })

    findings = []
    if log_path and log_path.exists():
        tail = log_path.read_text(errors="ignore")[-20000:]
        findings = match_signatures(tail)

    return {
        "generated_at": now,
        "host": os.environ.get("COMPUTERNAME", "unknown"),
        "service_name": service_name,
        "log_path": str(log_path) if log_path else None,
        "checks": checks,
        "findings": findings
    }

def report_to_markdown(rep: dict) -> str:
    lines = []
    lines.append(f"# OM1 Doctor Report")
    lines.append(f"- Generated: `{rep['generated_at']}`")
    lines.append(f"- Host: `{rep['host']}`")
    lines.append(f"- Service: `{rep['service_name']}`")
    if rep.get("log_path"):
        lines.append(f"- Log: `{rep['log_path']}`")
    lines.append("")
    lines.append("## Checks")
    for c in rep["checks"]:
        lines.append(f"- **{c['name']}**: `{c['status']}` — {c.get('details','')}")
    lines.append("")
    lines.append("## Findings (log signatures)")
    if rep["findings"]:
        for f in rep["findings"]:
            lines.append(f"- `{f['id']}`: {f['title']} — {f['hint']}")
    else:
        lines.append("- (none)")
    return "\n".join(lines)
