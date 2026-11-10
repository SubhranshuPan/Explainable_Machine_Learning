# Graph Report - Explainable_Machine_Learning  (2026-11-10)

## Corpus Check
- 20 files · ~6,324 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 14 file(s) not represented in the graph (top: .ipynb 5, .csv 4, .npz 4)

## Summary
- 294 nodes · 440 edges · 19 communities (18 shown, 1 thin omitted)
- Extraction: 74% EXTRACTED · 25% INFERRED · 1% AMBIGUOUS · INFERRED: 112 edges (avg confidence: 0.83)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `63127f62`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- XAI Theory and PFI
- Validation Protocols and Leakage
- ECG Preprocessing Lecture
- PermFIT algorithm (Algorithm 1, K-fold cross-fitted permutation importance)
- Class Balance and Test Sets
- numpy
- Preprocessed Beat Classes
- Report Template and Marking
- task5_compare_classifiers.py
- RF Patient Hold-out Results
- SVM Beat Hold-out Results
- SVM Patient Hold-out Results
- Raw ECG Signal Record 234
- RF Beat Hold-out Results
- Beat Window and Morphology
- Dataset Class Imbalance
- SHAP Attribution Properties
- Graphify Tooling
- ECG Arrhythmia Classification and Explainability (MIT-BIH)

## God Nodes (most connected - your core abstractions)
1. `Local Interpretable Model-agnostic Explanations (LIME)` - 18 edges
2. `Explainability in Machine Learning Lecture Slides` - 13 edges
3. `Preprocessed ECG Beat Examples (8 classes)` - 11 edges
4. `Shapley Additive Explanations (SHAP)` - 9 edges
5. `ML Interpretability Part 2 Lecture Slides (LIME and SHAP)` - 8 edges
6. `Permutation Feature Importance (PFI)` - 8 edges
7. `Phase A: Data ingestion & preprocessing (48 records, 149,768 beats, R-peak at index 137, length 275)` - 8 edges
8. `ECG Explainability Project Master Log & Progress Tracker` - 8 edges
9. `run_all.sh script` - 7 edges
10. `ECG Data Pre-processing Pipeline` - 7 edges

## Surprising Connections (you probably didn't know these)
- `Evaluation function: accuracy, precision, recall, F1, confusion matrix` --implements--> `evaluate()`  [INFERRED]
  explainability_machineLearning.pdf → src/ecg_utils.py
- `Notebook pipeline: data_preprocess -> data_split_resample -> classification` --references--> `evaluate()`  [INFERRED]
  README.md → src/ecg_utils.py
- `Load hold-out CSVs into NumPy arrays (e.g. 31920x275 train, 37863x275 test)` --implements--> `load_split()`  [INFERRED]
  explainability_machineLearning.pdf → src/ecg_utils.py
- `One-hot encoding of heartbeat class labels` --implements--> `one_hot()`  [INFERRED]
  explainability_machineLearning.pdf → src/ecg_utils.py
- `LIME surrogate optimisation & SHAP game-theoretic axioms` --semantically_similar_to--> `Permutation feature importance`  [INFERRED] [semantically similar]
  README.md → explainability_machineLearning.pdf

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **ECG Preprocessing Pipeline (filter, R-peak, segment, resample)** — explainabilitymachinelearning__2__ecg_data_preprocessing, explainabilitymachinelearning__2__ecg_noise_filtering, explainabilitymachinelearning__2__r_peak_annotation, explainabilitymachinelearning__2__ecg_beat_segmentation, explainabilitymachinelearning__2__beat_standardization, explainabilitymachinelearning__2__class_imbalance_bootstrap_resampling [EXTRACTED 1.00]
- **ECG preprocessing flow (WFDB read, dual-channel extraction, R-peak centering, standardization, resampling)** — explainability_machinelearning_wfdb_package, explainability_machinelearning_dual_channel_beat_extraction, explainability_machinelearning_r_peak_centering, explainability_machinelearning_beat_standardization, explainability_machinelearning_bootstrap_resampling [EXTRACTED 1.00]
- **PermFIT explanation pipeline (stratified K-fold CV, slice shuffling, importance matrix)** — explainability_machinelearning_permfit_algorithm, explainability_machinelearning_stratified_kfold_cv, explainability_machinelearning_slice_perturbation, explainability_machinelearning_feature_importance_matrix, explainability_machinelearning_permutation_feature_importance [EXTRACTED 1.00]
- **MIT-BIH 8-class beat taxonomy (N, L, R, V, A, F, f, /)** — figures_ecg_data_preprocessed_class_n, figures_ecg_data_preprocessed_class_l, figures_ecg_data_preprocessed_class_r, figures_ecg_data_preprocessed_class_v, figures_ecg_data_preprocessed_class_a, figures_ecg_data_preprocessed_class_f_fusion_ventricular, figures_ecg_data_preprocessed_class_f_fusion_paced, figures_ecg_data_preprocessed_class_paced [EXTRACTED 1.00]
- **Model-Agnostic Explanation Methods (PFI, LIME, SHAP)** — explainabilitymachinelearning__2__model_agnostic_approaches, explainabilitymachinelearning__2__permutation_feature_importance, ml_interpretability_part2__1__lime, ml_interpretability_part2__1__shap [EXTRACTED 1.00]
- **Random Forest evaluation on MIT-BIH beats under beat hold-out** — figures_cm_random_forest_beat, random_forest_classifier, beat_hold_out_protocol, ecg_beat_classes_mit_bih [EXTRACTED 1.00]
- **SHAP Uniqueness Properties of Additive Feature Attribution** — ml_interpretability_part2__1__shap, ml_interpretability_part2__1__additive_feature_attribution_methods, ml_interpretability_part2__1__local_accuracy_property, ml_interpretability_part2__1__missingness_property, ml_interpretability_part2__1__consistency_property [EXTRACTED 1.00]
- **SVM evaluation under beat hold-out on MIT-BIH 8-class beats** — figures_cm_svm_beat, figures_cm_svm_beat_svm_classifier, figures_cm_svm_beat_beat_hold_out_protocol, figures_cm_svm_beat_mit_bih_beat_classes, figures_cm_svm_beat_row_normalised_confusion_matrix [EXTRACTED 1.00]
- **Rare-class failure under inter-patient evaluation** — figures_cm_random_forest_patient_patient_hold_out, figures_cm_random_forest_patient_fusion_beat_failure, figures_cm_random_forest_patient_paced_fusion_failure, figures_cm_random_forest_patient_missing_test_classes [INFERRED 0.75]
- **Beat preprocessing: segmentation + standardisation (+ edge artifact)** — figures_ecg_data_preprocessed_beat_segmentation_window, figures_ecg_data_preprocessed_amplitude_standardisation, figures_ecg_data_preprocessed_first_sample_artifact [INFERRED 0.75]
- **Beat segmentation and normalisation producing class-separable morphologies** — figures_example_beats_per_class_r_peak_centred_beat_window, figures_example_beats_per_class_amplitude_standardisation, figures_example_beats_per_class_beat_morphology_differences, figures_example_beats_per_class_mit_bih_beat_classes [INFERRED 0.75]
- **Two-lead raw ECG recording of record 234** — figures_ecg_data_unpreprocessed_mit_bih_record_234, figures_ecg_data_unpreprocessed_mlii_lead, figures_ecg_data_unpreprocessed_v5_lead, figures_ecg_data_unpreprocessed_r_peak_qrs_complex [INFERRED 0.85]
- **Patient hold-out test set class coverage and imbalance** — figures_counts_test_patients_patient_hold_out_test_set, figures_counts_test_patients_class_distribution, figures_counts_test_patients_absent_classes_l_r_a, figures_counts_test_patients_class_imbalance [INFERRED 0.85]
- **SVM Patient Hold-out Evaluation Results** — figures_cm_svm_patient_svm_classifier, figures_cm_svm_patient_patient_hold_out, figures_cm_svm_patient_fusion_beat_confusion, figures_cm_svm_patient_strong_n_v_paced, figures_cm_svm_patient_absent_test_classes [INFERRED 0.85]
- **Report structure aligned with marking rubric (Intro/Methods/Results/Discussion)** — report_template_introduction_section, report_template_methods_section, report_template_results_section, report_template_discussion_section, marking_sheet_introduction_criterion, marking_sheet_methods_criterion, marking_sheet_results_criterion, marking_sheet_discussion_criterion [INFERRED 0.95]

## Communities (19 total, 1 thin omitted)

### Community 0 - "XAI Theory and PFI"
Cohesion: 0.08
Nodes (29): Arrieta et al. 2020 - Explainable Artificial Intelligence (XAI): Concepts, taxonomies, opportunities and challenges (Information Fusion), Convolutional Neural Networks, Decision Trees, Explainability in Machine Learning Lecture Slides, Dr. Fani Deligianni (University of Glasgow), Global Explanations, Linear Regression, Logistic Regression (+21 more)

### Community 1 - "Validation Protocols and Leakage"
Cohesion: 0.07
Nodes (41): Beat hold-out validation protocol (75/25 split), Class imbalance in MIT-BIH (dominant N beats), Apply same explainability technique to different classifiers and discuss, Clustering task: visualize class separation, classify on cluster features, Load hold-out CSVs into NumPy arrays (e.g. 31920x275 train, 37863x275 test), Dual-channel beat extraction and stacking, Pre-processing of ECG data for arrhythmia detection (coursework handout), Eight arrhythmia beat classes (N, L, R, V, A, F, f, /) and class IDs 1-8 (+33 more)

### Community 2 - "ECG Preprocessing Lecture"
Cohesion: 0.11
Nodes (21): Eight Arrhythmia Beat Classes (N, L, R, V, A, F, f, /), Coursework Assessment Tasks, Beat Standardization, Clustering for Data Structure Visualization, Segmentation into Individual ECG Beats, ECG Data Pre-processing Pipeline, ECG Noise Filtering, ECG Noise Interference (Baseline Wander, Electrode Contact, Motion Artifacts, Power Line) (+13 more)

### Community 3 - "PermFIT algorithm (Algorithm 1, K-fold cross-fitted permutation importance)"
Cohesion: 0.21
Nodes (10): Arrhythmia, ECG morphology: P-wave, QRS complex, T-wave, ECG noise sources (baseline wander, electrode contact, motion artifacts, power line), Electrocardiogram (ECG), Feature importance matrix M_ij (squared-error difference permuted vs original), Mi, Zou, Zou & Hu (2021) Permutation-based identification of important biomarkers (Nature Communications), PermFIT algorithm (Algorithm 1, K-fold cross-fitted permutation importance), Stratified 5-fold cross-validation on heartbeat class (+2 more)

### Community 4 - "Class Balance and Test Sets"
Cohesion: 0.12
Nodes (18): Balanced Training Set (3874 beats per class), Class Balancing via Resampling, Test Beats Class-Count Bar Chart, Class Imbalance (N-dominant, F rarest), MIT-BIH 8 Beat Classes (N, L, R, V, A, F, f, /), Test Set Beat Class Distribution, Test Patients Beat Class Count Bar Chart, Test Patients Class Distribution (N 9363, V 1087, F 387, f 1138, / 2507; total 14482) (+10 more)

### Community 5 - "numpy"
Cohesion: 0.07
Nodes (10): compute_permfit_ecg(), evaluate(), load_split(), make_model(), one_hot(), perturb_slice(), plot_permfit_importance(), evaluate() (+2 more)

### Community 6 - "Preprocessed Beat Classes"
Cohesion: 0.26
Nodes (12): Preprocessed ECG Beat Examples (8 classes), Per-beat amplitude standardisation (z-score), Fixed-length R-peak-centred beat window (~275 samples), Class A (Atrial premature beat), Class f (Fusion of paced and normal beat), Class F (Fusion of ventricular and normal beat), Class L (Left bundle branch block beat), Class N (Normal beat) (+4 more)

### Community 7 - "Report Template and Marking"
Cohesion: 0.27
Nodes (10): Marking: Discussion (20 points), Marking: Introduction (10 points), Case study marking sheet (100 points), Marking: Methods (15 points), Marking: Results incl. experiment rationale (40 points), Report Discussion: conclusions and why, Report Introduction: case study and predictive/exploratory question, Report Methods: main idea and parameters to tune (+2 more)

### Community 8 - "task5_compare_classifiers.py"
Cohesion: 0.13
Nodes (4): MPLBACKEND, run_all.sh script, run_permfit(), tag()

### Community 9 - "RF Patient Hold-out Results"
Cohesion: 0.43
Nodes (7): Random Forest Confusion Matrix (Patient Hold-out), Fusion Beat (F) Misclassification, Classes Absent from Held-out Records (L, R, A), MIT-BIH 8 Beat Classes (N, L, R, V, A, F, f, /), Paced-Fusion Beat (f) Misclassification, Patient Hold-out Protocol, Random Forest Classifier

### Community 10 - "SVM Beat Hold-out Results"
Cohesion: 0.43
Nodes (7): SVM Confusion Matrix – Beat Hold-out, Atrial premature (A) beats misclassified as Normal (N) – 6%, Beat Hold-out Protocol (random 75/25 split), Fusion (F) beats misclassified as Ventricular (V) 4% / Normal (N) 3%, MIT-BIH 8 Beat Classes (N, L, R, V, A, F, f, /), Row-normalised Confusion Matrix (per-class recall), SVM Classifier

### Community 11 - "SVM Patient Hold-out Results"
Cohesion: 0.38
Nodes (7): SVM Patient Hold-out Confusion Matrix, L/R/A Absent from Patient Test Set, Fusion Beats (F, f) Poorly Generalised, MIT-BIH 8 Beat Classes (N, L, R, V, A, F, f, /), Patient Hold-out Protocol, Strong N, V, Paced (/) Recognition, SVM Classifier

### Community 12 - "Raw ECG Signal Record 234"
Cohesion: 0.33
Nodes (7): Unpreprocessed ECG Signal Plot (Record 234), Baseline Wander and High-Frequency Noise in Raw ECG, MIT-BIH Record 234, MLII Lead (modified limb lead II), R Peak / QRS Complex, V5 Precordial Lead, MIT-BIH Arrhythmia Database

### Community 13 - "RF Beat Hold-out Results"
Cohesion: 0.40
Nodes (6): Beat Hold-out Protocol (random 75/25 split), MIT-BIH 8 Beat Classes (N, L, R, V, A, F, f, /), Random Forest Confusion Matrix (Beat Hold-out), RF beat hold-out: A and F beats most often misclassified (A->N 7%, F->V 6%, F->N 5%), Random Forest Classifier, Row-normalised Confusion Matrix (per-class recall)

### Community 14 - "Beat Window and Morphology"
Cohesion: 0.70
Nodes (5): Example Heartbeat of Each Class (figure), Per-beat Amplitude Standardisation, Class-specific Beat Morphology, MIT-BIH 8 Beat Classes (N, L, R, V, A, F, f, /), R-peak Centred Beat Window (~275 samples @ 360 Hz)

### Community 15 - "Dataset Class Imbalance"
Cohesion: 0.83
Nodes (4): Beat Class Counts - All Data (bar chart), Severe Class Imbalance (N-dominated), MIT-BIH Arrhythmia Database, MIT-BIH 8 Beat Classes (N, L, R, V, A, F, f, /)

### Community 16 - "SHAP Attribution Properties"
Cohesion: 0.50
Nodes (4): Additive Feature Attribution Methods, Consistency Property, Local Accuracy Property, Missingness Property

### Community 18 - "ECG Arrhythmia Classification and Explainability (MIT-BIH)"
Cohesion: 0.29
Nodes (6): Contributions, ECG Arrhythmia Classification and Explainability (MIT-BIH), Files, How to run, Key settings, Notes on the data pipeline

## Ambiguous Edges - Review These
- `Shapley Additive Explanations (SHAP)` → `11-Segment ECG Beat Slicing (Segment Averaging)`  [AMBIGUOUS]
  ML_interpretability-part2 (1).pdf · relation: conceptually_related_to
- `biosppy` → `ECG noise sources (baseline wander, electrode contact, motion artifacts, power line)`  [AMBIGUOUS]
  requirements.txt · relation: conceptually_related_to
- `Per-beat amplitude standardisation (z-score)` → `Spike at sample 0 (edge artifact)`  [AMBIGUOUS]
  figures/ecg_data_preprocessed.jpg · relation: conceptually_related_to

## Knowledge Gaps
- **39 isolated node(s):** `MPLBACKEND`, `LIME Tabular Explainer`, `LIME Text Explainer`, `Locally Linear Surrogate Model`, `Mi et al. 2021 - Permutation-based identification of important biomarkers for complex diseases via machine learning models (Nature Communications)` (+34 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 77 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `evaluate()` connect `numpy` to `Validation Protocols and Leakage`?**
  _High betweenness centrality (0.068) - this node is a cross-community bridge._
- **Are the 3 inferred relationships involving `Local Interpretable Model-agnostic Explanations (LIME)` (e.g. with `Post-hoc Surrogate Model Explanations` and `Ribeiro et al. 2016 - "Why Should I Trust You?": Explaining the Predictions of Any Classifier (KDD)`) actually correct?**
  _`Local Interpretable Model-agnostic Explanations (LIME)` has 3 INFERRED edges - model-reasoned connections that need verification._
- **What connects `MPLBACKEND`, `LIME Tabular Explainer`, `LIME Text Explainer` to the rest of the system?**
  _39 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `XAI Theory and PFI` be split into smaller, more focused modules?**
  _Cohesion score 0.08246225319396051 - nodes in this community are weakly interconnected._
- **Why does `Notebook pipeline: data_preprocess -> data_split_resample -> classification` connect `Validation Protocols and Leakage` to `numpy`?**
  _High betweenness centrality (0.043) - this node is a cross-community bridge._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `Shapley Additive Explanations (SHAP)` and `11-Segment ECG Beat Slicing (Segment Averaging)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._
- **What is the exact relationship between `biosppy` and `ECG noise sources (baseline wander, electrode contact, motion artifacts, power line)`?**
  _Edge tagged AMBIGUOUS (relation: conceptually_related_to) - confidence is low._