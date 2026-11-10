# ECG Arrhythmia Classification and Explainability (MIT-BIH)

We classify single heartbeats into 8 arrhythmia classes (N, L, R, V, A, F, f, /) with an
SVM, testing on random beats (beat hold-out) and on unseen patients (patient hold-out).
PermFIT permutation feature importance then explains which parts of the heartbeat the
models rely on. The same analysis is repeated with a Random Forest for comparison.

The report is `Report.docx` (also exported as `Report.pdf`).

**Quick tour:** open `walkthrough.ipynb`. It contains all the code of Tasks 1–5 in order, with short
explanations. Its outputs (all plots and tables) are saved, so it can be read without running anything.

## How to run the notebook

**You need:** Python 3.10 or newer ([python.org](https://www.python.org/downloads/)), about 2 GB of free disk
space, 8 GB of RAM, and an internet connection for the first run. The raw data is not in the zip; the
notebook downloads it.

### 1. Unzip and open a terminal in the folder

Unzip `Final_Submission.zip`, open a terminal (macOS/Linux: *Terminal*; Windows: *PowerShell*) and go into
the folder:

```bash
cd path/to/Final_Submission
```

### 2. Create a Python environment and install the packages (once, about 3 minutes)

macOS / Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows (PowerShell):

```powershell
py -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
```

### 3. Open the notebook with that environment

Either **Jupyter in the browser**: with the environment still active (step 2), run

```bash
jupyter notebook walkthrough.ipynb
```

and choose *Run ▸ Run All Cells*.

Or **VS Code** (with the *Python* and *Jupyter* extensions): *File ▸ Open Folder* ▸ `Final_Submission`, open
`walkthrough.ipynb`, click *Select Kernel* (top right) ▸ *Python Environments* ▸ `.venv`, then *Run All*.

### 4. What happens on the first run

The first code cell prepares everything, which takes about 5 minutes:
1. it downloads the 48 MIT-BIH records from PhysioNet into `mitbih/` (about 100 MB);
2. it builds `data/` (about 1.2 GB) by running `00_preprocess.ipynb` and `01_split_resample.ipynb`.

It prints `Setup OK`. The rest of the notebook takes about 3 minutes. Later runs skip both steps.

PermFIT is slow (about 1.5 hours), so by default the notebook loads its saved results from `results/`. To
recompute them, set `RUN_PERMFIT = True` in the second code cell.

### Troubleshooting

| Problem | Fix |
|---|---|
| `Missing packages ...` or `ModuleNotFoundError` | The notebook is using a different Python. Select the `.venv` kernel (step 3), or activate the environment before starting `jupyter notebook`. |
| `python3` / `py` not found | Install Python from python.org. On Windows, tick *Add python.exe to PATH* during installation. |
| PowerShell blocks `activate` | Run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` once, or skip activating and use `.venv\Scripts\python -m pip install -r requirements.txt`. |
| `Open this notebook from inside the Final_Submission folder` | Start Jupyter or VS Code in this folder, not in a parent folder. |
| The download fails (no internet or firewall) | Download the ZIP from <https://physionet.org/content/mitdb/1.0.0/>, unzip it, and put the 48 `.dat`, `.hea` and `.atr` files directly in a folder `mitbih/` inside this folder. Then run again. |

With the package versions we used (Python 3.14, scikit-learn 1.9, NumPy 2.5), the numbers match the report
exactly. Other versions can change the last digits.

## Rerun everything from the scripts (optional)

`run_all.sh` runs the same steps as the notebook with the `.py` files, and also recomputes PermFIT for the
SVM (about 40 minutes in total). macOS / Linux, from this folder with the environment active:

```bash
bash run_all.sh
```

It downloads the data if `mitbih/` is empty. Every random step uses seed 42, so a rerun gives the same
numbers.

## Files

| File | Task | What it does |
|---|---|---|
| `00_preprocess.ipynb` | data | Raw MIT-BIH → one standardised 275-sample beat per row, R-peak centred (`data/all_data.csv`) |
| `01_split_resample.ipynb` | data | Beat hold-out (75/25) and patient hold-out splits, class re-sampling of the training sets |
| `walkthrough.ipynb` | 1–5 | Runs every task in order with explanations; outputs saved (PermFIT loaded from `results/` unless `RUN_PERMFIT = True`) |
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
