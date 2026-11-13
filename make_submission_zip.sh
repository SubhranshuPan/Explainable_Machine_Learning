#!/usr/bin/env bash
# Zip Final_Submission for upload as GroupH_ECG.zip, leaving out local-only things:
# the 1.2 GB data/ folder, the raw mitbih/ files (both are links on this machine),
# the old Word copy of the report, a local .venv, notebook checkpoints,
# Python caches and macOS .DS_Store files.
set -euo pipefail
cd "$(dirname "$0")"
ZIP=GroupH_ECG.zip
rm -f "$ZIP"
zip -r -q "$ZIP" Final_Submission \
    -x "Final_Submission/data" "Final_Submission/data/*" \
       "Final_Submission/mitbih" "Final_Submission/mitbih/*" \
       "Final_Submission/Report.docx" "Final_Submission/.venv/*" \
       "*/.ipynb_checkpoints/*" "*/__pycache__/*" "*.DS_Store"
echo "Created $ZIP ($(du -h "$ZIP" | cut -f1))"
