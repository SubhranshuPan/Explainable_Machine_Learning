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
- [ ] Download MIT-BIH records via `wfdb` into `mitbih/` directory 
- [ ] Extract dual-channel beats, center R-peaks at index 137 (length 275) 
- [ ] Generate class histogram showing initial imbalance 
- [ ] Resample training set with replacement to 3,989 samples/class 
- [ ] Create `train_beats.csv`, `test_beats.csv`, `train_patients.csv`, `test_patients.csv` 

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
