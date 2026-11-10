# ECG Arrhythmia Classification and Explainability (MIT-BIH)

We classify single heartbeats into 8 arrhythmia classes (N, L, R, V, A, F, f, /) with an
SVM, testing on random beats (beat hold-out) and on unseen patients (patient hold-out).
PermFIT permutation feature importance then explains which parts of the heartbeat the
models rely on. The same analysis is repeated with a Random Forest for comparison.

The report is `Report.docx` (also exported as `Report.pdf`).

## How to run

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
# put the 48 MIT-BIH records (.dat/.hea/.atr) from https://physionet.org/content/mitdb/1.0.0/ in ./mitbih/
PYTHON=.venv/bin/python bash run_all.sh
```

Run all commands from this folder. `run_all.sh` runs the steps below in order. Every
random step uses seed 42, so a rerun gives the same numbers. The slowest step is
Task 4: the SVM is refitted in 5 folds, about 20–40 minutes on a laptop.

## Files

| File | Task | What it does |
|---|---|---|
| `00_preprocess.ipynb` | data | Raw MIT-BIH → one standardised 275-sample beat per row, R-peak centred (`data/all_data.csv`) |
| `01_split_resample.ipynb` | data | Beat hold-out (75/25) and patient hold-out splits, class re-sampling of the training sets |
| `task1.py` | 1 | Example beat per class and class distribution |
| `task2_svm.py` | 2 | SVM, beat hold-out: accuracy, precision, recall, F1, confusion matrix |
| `task3.py` | 3 | SVM, patient hold-out (records 104, 113, 119, 208, 210 held out) |
| `task4_permfit.py` | 4 | PermFIT on the Task 2 and Task 3 SVMs (11 slices × 25 samples, stratified 5-fold) |
| `tune_hyperparameters.py` | 5 | Grid search for the Random Forest settings |
| `task5_compare_classifiers.py` | 5 | Random Forest on both protocols, the same PermFIT, SVM vs RF comparison |
| `ecg_utils.py` | 4, 5 | Shared data loading, model definitions, metrics, PermFIT and plots |
| `figures/` | report | Every figure used in the report |
| `results/` | report | Metrics (`.json`), PermFIT numbers (`.npz`, `.csv`) and run logs |

Tasks 1–3 are the team members' scripts with small fixes, each marked `# FIX:` in the code:
- data paths point to `data/`;
- figures and predictions are saved;
- Task 1 plots a beat from the middle of each class;
- Task 3's macro scores average only the classes present in the test set.

## Key settings

| | Value | Source |
|---|---|---|
| SVM, beat hold-out | `SVC(kernel="rbf")` (C = 1) | `task2_svm.py` |
| SVM, patient hold-out | `StandardScaler` + `SVC(max_iter=10000)` | `task3.py` |
| Random Forest | 300 trees, `max_features=0.1` | `tune_hyperparameters.py` |
| PermFIT folds | 5, stratified on the beat class | case study handout |
| Slices | 11 × 25 samples: 1–4 PR interval, 5–7 QRS complex, 8–11 ST segment / T-wave | lecture slides |
| Perturbation | main: shuffle the points within a slice. Sensitivity check: zero, mean, swap between beats | handout |
| SVM probabilities | Platt scaling (`CalibratedClassifierCV`) | needed for PermFIT's squared error |

## Notes on the data pipeline

* **Patient-split bug fixed.** The original split code repeated the training rows about 5 times, which leaked the
  5 test patients into training. That is why the handout shows 25,789 beats per class; the correct number is 4,423.
* **Fixed record order.** Records are read in sorted order, so the splits are identical on every computer.
* **Two rows per beat.** Each beat appears twice, once for each ECG channel, as the handout describes.
* **Spike at sample 0.** The beat window holds 274 samples and is padded with one zero. After standardisation
  that zero becomes a spike. It was kept to match the course code and falls in slice 1.

## Contributions

| Member | Work |
|---|---|
| [name] | Task 1: data inspection (`task1.py`) |
| [name] | Task 2: beat hold-out SVM (`task2_svm.py`) |
| [name] | Task 3: patient hold-out SVM (`task3.py`) |
| [name] | Task 4: PermFIT; Task 5: Random Forest comparison; integration |
