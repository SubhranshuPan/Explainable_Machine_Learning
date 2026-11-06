# ECG Explainability Project Master Log & Progress Tracker 

## 1. Project Overview &amp; Group Metadata 
- Group Size: [4 / 5 / 6 members] 
- Selected Classifiers: [e.g., 1. SVM (RBF Kernel), 2. 1D-CNN / Random Forest]
- Individual Role / Tasks: [e.g., Preprocessing & PFI Implementation] 

--- 

✓ - Symbol to copy and paste in checkboxes.

---


## 2. Theoretical &amp; Mathematical Checkpoints (Self-Study) 
- [ ] ECG Morphology: P-wave (atrial depol), QRS (ventricular depol), T-wave (ventricular repol) 
- [ ] Signal standardisation formula: z = (x - mu) / sigma 
- [ ] MIT-BIH 8 classes mapped to IDs 1-8 
- [ ] Beat hold-out (data leakage risk) vs. Patient hold-out (leave patients 104, 113, 119, 208, 210) 
- [ ] PermFIT algorithm math: slice perturbation across 11 intervals (25 samples each) 
- [ ] LIME surrogate optimization & SHAP game-theoretic axioms (Local accuracy, Missingness, Consistency) 

--- 

## 3. Implementation & Experimental Milestones 

### Phase A: Data Ingestion &amp; Preprocessing 
- [x] Download MIT-BIH records into `mitbih/` directory (48 records, SHA256-verified)
- [x] Extract dual-channel beats, center R-peaks at index 137 (length 275) → 149,768 labelled beats
- [x] Generate class histogram showing initial imbalance 
- [x] Resample training set with replacement → 3,874 samples/class (beat split), 4,423 samples/class (patient split)
- [x] Create `train_beats.csv`, `test_beats.csv`, `train_patients.csv`, `test_patients.csv` 
- [x] Fixed patient-split bug: original code duplicated rows ~5× and leaked the test patients into training (handout's 25,789/class)

### Phase B: Model Training & Evaluation 
- [ ] Model 1 (SVM): Beat Hold-Out (Acc, Prec, Rec, F1, Confusion Matrix) 
- [ ] Model 1 (SVM): Patient Hold-Out (Acc, Prec, Rec, F1, Confusion Matrix) 
- [ ] Model 2 (e.g., CNN / RF): Beat Hold-Out 
- [ ] Model 2 (e.g., CNN / RF): Patient Hold-Out 
- [ ] Quantify performance drop between beat hold-out and patient hold-out (identifying data leakage) 

### Phase C: Explainability (PFI / PermFIT) 
- [ ] Implement stratified 5-fold CV for PermFIT 
- [ ] Apply random slice perturbation across 11 segments of 25 samples 
- [ ] Compute mean importance vector `M_j` for Model 1 (Beat vs. Patient hold-out) 
- [ ] Compute mean importance vector `M_j` for Model 2 (Beat vs. Patient hold-out) 
- [ ] Verify if segments 5-7 (QRS complex) receive highest attribution 

### Phase D: Clustering (If 6 members) 
- [ ] Run clustering (e.g., K-Means / PCA projection) on beat representations 
- [ ] Evaluate cluster separation across the 8 arrhythmia categories 
- [ ] Train classifier using cluster features 

--- 

## 4. Group Progress & Work Distribution Log 
| Member | Assigned Sub-Task | Status | Key Results / Observations | 
| :--- | :--- | :--- | :--- | 
| Som | Math formulation &amp; PFI function | In Progress | Derived PermFIT formula and 11-segment slicing | 
| [Peer 1] | WFDB parsing &amp; R-peak centering | Pending | | 
| [Peer 2] | Beat &amp; Patient split CSV pipelines | Pending | | 
| [Peer 3] | SVM implementation &amp; tuning | Pending | | 
| [Peer 4] | Second classifier (CNN / RF) | Pending | | 
| [Peer 5] | Clustering &amp; Report drafting | Pending | |

---

## 5. How to reproduce

```bash
# 1. Environment (Python 3.14 tested)
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt

# 2. Data: download https://physionet.org/content/mitdb/1.0.0/ and put the
#    48 records' .dat / .hea / .atr files in ./mitbih/

# 3. Run the notebooks in order (outputs go to data/ and figures/)
cd notebooks
../.venv/bin/jupyter nbconvert --to notebook --execute --inplace data_preprocess.ipynb
../.venv/bin/jupyter nbconvert --to notebook --execute --inplace data_split_resample.ipynb
../.venv/bin/jupyter nbconvert --to notebook --execute --inplace classification.ipynb
```

| Folder / file | Contents |
| :--- | :--- |
| `notebooks/data_preprocess.ipynb` | Raw MIT-BIH → one standardised 275-sample beat per row (`data/all_data.csv`) |
| `notebooks/data_split_resample.ipynb` | Beat hold-out (75/25) and patient hold-out splits, class re-sampling |
| `notebooks/classification.ipynb` | SVM and Random Forest on both splits: accuracy, precision, recall, F1, confusion matrices |
| `src/ecg_utils.py` | Shared loading + evaluation functions |
| `figures/` | All figures used in the report |
