#!/usr/bin/env bash
# Reproduce every result of the case study, in order.
# Needs: Python environment from requirements.txt, raw MIT-BIH files in ./mitbih/
set -euo pipefail
cd "$(dirname "$0")"
mkdir -p data figures results
export MPLBACKEND=Agg
PY=${PYTHON:-python3}

if [ "$(ls mitbih/*.dat 2>/dev/null | wc -l)" -lt 48 ]; then
    echo "== Downloading the MIT-BIH database from PhysioNet into mitbih/ (about 100 MB) =="
    $PY -c "import wfdb; wfdb.dl_database('mitdb', 'mitbih')"
fi

echo "== Data preparation (notebooks provided by the course, with fixes) =="
$PY -m jupyter nbconvert --to notebook --execute --inplace 00_preprocess.ipynb
$PY -m jupyter nbconvert --to notebook --execute --inplace 01_split_resample.ipynb

echo "== Tasks =="
$PY task1.py                     | tee results/log_task1.txt
$PY task2_svm.py                 | tee results/log_task2_svm.txt
$PY task3.py                     | tee results/log_task3.txt
$PY tune_hyperparameters.py      | tee results/log_tune_hyperparameters.txt
$PY task4_permfit.py SVM         | tee results/log_task4_permfit_svm.txt        # slowest step
$PY task5_compare_classifiers.py | tee results/log_task5_compare_classifiers.txt
echo "Done. Figures in figures/, numbers in results/."
