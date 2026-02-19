# om1-doctor

Diagnostics + report tool for OM1 node runners.

## Install (uv)
uv venv
.\.venv\Scripts\activate
uv pip install -e .

## Usage
om1-doctor doctor --service om1
om1-doctor report --service om1 --md-out report.md
om1-doctor service-template --workdir C:\OM1 --user om1
