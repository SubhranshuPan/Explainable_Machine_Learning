# Explainable Machine Learning: ECG Arrhythmia Case Study

Group coursework: classify single heartbeats from the MIT-BIH Arrhythmia Database into 8 classes with an
SVM and a Random Forest, and explain the models with PermFIT permutation feature importance.

**Everything that is submitted is in [`Final_Submission/`](Final_Submission/)**: code, notebooks, results,
figures and the report. Its [README](Final_Submission/README.md) explains how to run it.

## Repository structure

```
.
├── Final_Submission/          the submission (zipped and uploaded as-is)
│   ├── walkthrough.ipynb      all tasks in one notebook, with explanations and saved outputs
│   ├── 00_preprocess.ipynb    raw MIT-BIH records -> one standardised beat per row
│   ├── 01_split_resample.ipynb  beat / patient hold-out splits and class re-sampling
│   ├── task1.py … task5_compare_classifiers.py, tune_hyperparameters.py, ecg_utils.py
│   ├── figures/ results/      every figure and number used in the report
│   ├── Report.docx  Report.pdf
│   └── README.md  requirements.txt  run_all.sh
├── course_material/           case study brief, lecture slides, report template, marking sheet, Delta form
├── make_submission_zip.sh     builds Final_Submission.zip without the local data folders
├── graphify-out/              code knowledge graph (graphify tool)
└── CLAUDE.md  .claude/  .vscode/   editor and assistant settings
```

Not in git (rebuilt or downloaded locally): `mitbih/` (raw data, about 100 MB), `data/` (generated
CSVs, about 1.2 GB) and `.venv/`. `Final_Submission/data` and `Final_Submission/mitbih` are local links to
these two folders.

## Quick start

```bash
cd Final_Submission
python3 -m venv .venv && source .venv/bin/activate
python -m pip install -r requirements.txt
jupyter notebook walkthrough.ipynb      # Run All: downloads the data on the first run
```

## Making the submission zip

```bash
./make_submission_zip.sh     # -> Final_Submission.zip (about 5 MB, data folders left out)
```

## Results in one line

Both classifiers base their decisions mainly on the QRS complex (slices 5–7, R-peak in slice 6). The SVM
generalises better to unseen patients (accuracy 0.866 vs 0.836); see the report for the full discussion.
