#!/usr/bin/env bash
# Zip Final_Submission for upload, leaving out local-only things:
# the 1.2 GB data/ folder, the raw mitbih/ files (both are links on this machine),
# a local .venv, notebook checkpoints, Python caches and macOS .DS_Store files.
set -euo pipefail
cd "$(dirname "$0")"
rm -f Final_Submission.zip
zip -r -q Final_Submission.zip Final_Submission \
    -x "Final_Submission/data" "Final_Submission/data/*" \
       "Final_Submission/mitbih" "Final_Submission/mitbih/*" \
       "Final_Submission/.venv/*" "*/.ipynb_checkpoints/*" "*/__pycache__/*" "*.DS_Store"
echo "Created Final_Submission.zip ($(du -h Final_Submission.zip | cut -f1))"
