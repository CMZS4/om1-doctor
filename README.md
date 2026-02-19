# OM1 Doctor

Professional diagnostics and troubleshooting CLI tool for OM1 node operators.

---

## 🚀 Purpose

Node runners often experience:

- Service not starting
- Points not increasing
- Permission errors
- Disk full issues
- Out-of-memory (OOM) crashes
- Misconfigured environment variables
- Port conflicts

OM1 Doctor provides a **single-command health check** and generates a **shareable Markdown report** for debugging and support.

---

## 🧠 What It Does

- System health checks (Disk, RAM)
- Python & uv detection
- Service status check (systemd on Linux)
- Local port scan
- Log signature detection (common failure patterns)
- Markdown report generator (ready for GitHub / Discord)

---

## 📦 Installation (Windows)

```powershell
python -m venv .venv
.\.venv\Scripts\activate
python -m pip install -e .
```

---
---

## Installation (Linux / VPS)

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

Run diagnostics:

```bash
om1-doctor doctor
```

Generate report:

```bash
om1-doctor report --md-out report.md
```

## ▶ Usage

### Run diagnostics

```powershell
om1-doctor doctor
```

### Generate Markdown report

```powershell
om1-doctor report --md-out report.md
```

### Print Linux systemd service template

```powershell
om1-doctor service-template
```

---

## 📝 Example Output

```
OM1 Doctor Summary

Disk free     OK
RAM available OK
Python        OK
uv            OK
systemd       INFO
Local ports   OK
```

---

## 📊 Example Markdown Report

The generated report includes:

- Timestamp
- Host information
- Service name
- Health checks
- Detected log issues
- Suggested fixes

This can be directly pasted into a GitHub issue or shared in Discord for support.

---

## 🛠 Roadmap

- Deep Linux service inspection
- Auto-fix suggestions
- JSON export
- CI test coverage
- OM1 integration proposal

---

## 🤝 Contribution Intent

This tool is designed to reduce support overhead and improve troubleshooting efficiency for OM1 node operators.

Future goal: propose integration into the official OM1 tooling ecosystem.

---

## 📄 License

MIT
## Changelog

- v0.2: Cross-platform diagnostics
- Configurable --ports option
- Improved signature matching
- Added pytest coverage
