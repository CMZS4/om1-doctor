from __future__ import annotations
import re

SIGNATURES = [
    ("PERM_DENIED", "Permission denied", r"Permission denied", "Check file permissions / run as correct user."),
    ("OOM_KILLED", "Out of memory kill", r"oom-killer|Killed process|Out of memory", "Increase RAM / lower load / add swap."),
    ("DISK_FULL", "No space left", r"No space left on device", "Free disk space on server."),
    ("CONN_REFUSED", "Connection refused", r"Connection refused", "Check endpoints, firewall, service running."),
    ("MISSING_ENV", "Missing env var", r"KeyError:|Missing .*ENV|environment variable", "Set required env vars, check .env/docs."),
]

def match_signatures(text: str):
    hits = []
    for sid, title, pat, hint in SIGNATURES:
        if re.search(pat, text, re.IGNORECASE):
            hits.append({"id": sid, "title": title, "hint": hint})
    return hits
