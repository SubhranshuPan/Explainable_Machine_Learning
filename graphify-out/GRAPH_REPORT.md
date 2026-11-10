# Graph Report - Explainable_Machine_Learning  (2026-11-10)

## Corpus Check
- Corpus is ~5,186 words - fits in a single context window. You may not need a graph.

## Summary
- 339 nodes · 511 edges · 23 communities (22 shown, 1 thin omitted)
- Extraction: 85% EXTRACTED · 14% INFERRED · 0% AMBIGUOUS · INFERRED: 74 edges (avg confidence: 0.83)
- Token cost: 1,240,381 input · 0 output

## Community Hubs (Navigation)
- Submission Pipeline & Setup
- Shared PermFIT Code
- Report Findings
- LIME & SHAP Lecture
- Case Study Brief
- Explainability Lecture
- Interpretable Model Types
- Marking & Template
- Perturbation Method Comparison
- RF Patient PermFIT
- Beat Class Examples
- RF Beat PermFIT
- SVM Patient PermFIT
- SVM Patient Confusion
- RF Patient Confusion
- PermFIT Comparison Grid
- RF Beat Confusion
- SVM Beat Confusion
- SVM vs RF Profiles
- SVM Beat PermFIT
- Task 3 Confusion Matrix
- Class Imbalance
- Graphify Tooling

## God Nodes (most connected - your core abstractions)
1. `Final_Submission README` - 21 edges
2. `Report: Explaining ECG Arrhythmia Classifiers with PermFIT` - 14 edges
3. `LIME (Local Interpretable Model-agnostic Explanations)` - 14 edges
4. `SHAP (Shapley Additive Explanations)` - 14 edges
5. `PermFIT (permutation feature importance with K-fold cross-fitting)` - 11 edges
6. `run_permfit()` - 10 edges
7. `Lecture 2: LIME and SHAP (ML Interpretability)` - 10 edges
8. `Appendix A - Code and reproducibility (walkthrough.ipynb, run_all.sh)` - 9 edges
9. `Explainable Models` - 9 edges
10. `Example ECG Beat per Class (Task 1 figure)` - 9 edges

## Surprising Connections (you probably didn't know these)
- `Finding: both classifiers rely mainly on QRS complex (slices 5-7)` --conceptually_related_to--> `SVM PermFIT ranking: slice 6 most important (both protocols)`  [INFERRED]
  README.md → Final_Submission/results/log_task4_permfit_svm.txt
- `Finding: both classifiers rely mainly on QRS complex (slices 5-7)` --references--> `SVM vs RF comparison table`  [INFERRED]
  README.md → Final_Submission/results/log_task5_compare_classifiers.txt
- `Finding: both classifiers rely mainly on QRS complex (slices 5-7)` --references--> `Per-slice importance table (RF vs SVM)`  [INFERRED]
  README.md → Final_Submission/results/log_task5_compare_classifiers.txt
- `Repository README` --references--> `Final_Submission README`  [EXTRACTED]
  README.md → Final_Submission/README.md
- `SVM classifier` --conceptually_related_to--> `scikit-learn`  [INFERRED]
  Final_Submission/README.md → Final_Submission/requirements.txt

## Import Cycles
- None detected.

## Hyperedges (group relationships)
- **PermFIT slice-importance evidence that QRS (slice 6) dominates** — final_submission_results_log_task4_permfit_svm_slice_ranking, final_submission_results_log_task5_compare_classifiers_rf_permfit_ranking, final_submission_results_log_task5_compare_classifiers_slice_importance_table, readme_qrs_complex_finding [INFERRED 0.85]
- **2 models x 2 hold-out protocols evaluation** — final_submission_readme_svm_classifier, final_submission_readme_random_forest_classifier, final_submission_readme_beat_hold_out, final_submission_readme_patient_hold_out, final_submission_results_log_task5_compare_classifiers_comparison_table [EXTRACTED 1.00]
- **PermFIT explanation pipeline (cross-fitting, slices, perturbation, calibrated probabilities)** — final_submission_report_permfit, final_submission_report_ecg_slices, final_submission_report_shuffle_within_slice, final_submission_report_platt_scaling, final_submission_report_accuracy_drop_metric, final_submission_report_perturbation_sensitivity [EXTRACTED 1.00]
- **Generalisation gap: leakage vs unseen-patient evaluation** — final_submission_report_beat_hold_out, final_submission_report_patient_hold_out, final_submission_report_data_leakage, final_submission_report_patient_split_bug, final_submission_report_fusion_class_collapse, final_submission_report_classification_results [EXTRACTED 1.00]
- **Explainability findings: QRS reliance and artefact debugging** — final_submission_report_qrs_hypothesis, final_submission_report_permfit_slice_importance, final_submission_report_qrs_complex, final_submission_report_edge_padding_artefact [EXTRACTED 1.00]
- **ECG Data Preparation Pipeline (load, pre-process, resample, split)** — course_material_case_study_ecg_explainability_mit_bih_arrhythmia_database, course_material_case_study_ecg_explainability_wfdb_package, course_material_case_study_ecg_explainability_r_peak_centering_standardization, course_material_case_study_ecg_explainability_bootstrap_resampling, course_material_case_study_ecg_explainability_beat_holdout_protocol, course_material_case_study_ecg_explainability_patient_holdout_protocol [EXTRACTED 1.00]
- **PermFIT Explanation Procedure for ECG Classifiers** — course_material_case_study_ecg_explainability_permfit_algorithm, course_material_case_study_ecg_explainability_stratified_kfold_cv, course_material_case_study_ecg_explainability_time_slices, course_material_case_study_ecg_explainability_perturbation_strategies, course_material_case_study_ecg_explainability_feature_importance_matrix [EXTRACTED 1.00]
- **Model-agnostic explanation methods (PFI, LIME, SHAP)** — course_material_lecture_1_explainability_ml_permutation_feature_importance, course_material_lecture_1_explainability_ml_lime, course_material_lecture_1_explainability_ml_shap, course_material_lecture_1_explainability_ml_model_agnostic [EXTRACTED 1.00]
- **ECG preprocessing flow (denoise, R-peak segment, resample)** — course_material_lecture_1_explainability_ml_mit_bih_dataset, course_material_lecture_1_explainability_ml_ecg_noise, course_material_lecture_1_explainability_ml_ecg_preprocessing, course_material_lecture_1_explainability_ml_class_imbalance, course_material_lecture_1_explainability_ml_bootstrap_resampling [EXTRACTED 1.00]
- **PFI applied to ECG via 11-segment slicing and perturbation** — course_material_lecture_1_explainability_ml_permutation_feature_importance, course_material_lecture_1_explainability_ml_ecg_11_segments, course_material_lecture_1_explainability_ml_perturbation_strategies, course_material_lecture_1_explainability_ml_ecg_classification [EXTRACTED 1.00]
- **SHAP uniqueness properties (local accuracy, missingness, consistency)** — course_material_lecture_2_ml_interpretability_local_accuracy, course_material_lecture_2_ml_interpretability_missingness, course_material_lecture_2_ml_interpretability_consistency, course_material_lecture_2_ml_interpretability_additive_feature_attribution [EXTRACTED 1.00]
- **LIME segment explanations of ECG classifiers (CNN, LSTM, MLP)** — course_material_lecture_2_ml_interpretability_lime_cnn_ecg, course_material_lecture_2_ml_interpretability_lime_lstm_ecg, course_material_lecture_2_ml_interpretability_lime_mlp_ecg, course_material_lecture_2_ml_interpretability_ecg_beat_11_segments, course_material_lecture_2_ml_interpretability_recurrent_tabular_explainer [EXTRACTED 1.00]
- **LIME explainer family by data type** — course_material_lecture_2_ml_interpretability_lime_tabular_explainer, course_material_lecture_2_ml_interpretability_lime_text_explainer, course_material_lecture_2_ml_interpretability_lime_image_explainer, course_material_lecture_2_ml_interpretability_recurrent_tabular_explainer [EXTRACTED 1.00]
- **Case study assessment rubric (100 pts)** — course_material_marking_sheet_introduction_criterion, course_material_marking_sheet_methods_criterion, course_material_marking_sheet_results_criterion, course_material_marking_sheet_discussion_criterion, course_material_marking_sheet_code_implementation_criterion [EXTRACTED 1.00]
- **Required report structure (Intro/Methods/Results/Discussion)** — course_material_report_template_introduction_section, course_material_report_template_methods_section, course_material_report_template_results_section, course_material_report_template_discussion_section [EXTRACTED 1.00]
- **Random Forest patient hold-out evaluation: N 0.91, V 0.99, / 1.00 recall; F split N 0.43 / V 0.53 and f 0.00 recall; L, R, A rows empty (no test patients for those classes)** — final_submission_figures_cm_random_forest_patients_random_forest_classifier, final_submission_figures_cm_random_forest_patients_patient_holdout_evaluation, final_submission_figures_cm_random_forest_patients_ecg_beat_classes, final_submission_figures_cm_random_forest_patients_fusion_beat_misclassification [INFERRED 0.85]
- **SVM inter-patient generalisation evaluation** — final_submission_figures_cm_svm_patients_svm_classifier, final_submission_figures_cm_svm_patients_patient_hold_out_split, final_submission_figures_cm_svm_patients_strong_n_v_paced_recall, final_submission_figures_cm_svm_patients_fusion_beat_confusion, final_submission_figures_cm_svm_patients_classes_absent_in_test_patients [INFERRED 0.85]
- **PermFIT 2x2 comparison: model x hold-out scheme over ECG slice regions** — final_submission_figures_permfit_comparison_grid_permfit_slice_importance, final_submission_figures_permfit_comparison_grid_beat_vs_patient_holdout, final_submission_figures_permfit_comparison_grid_svm_vs_rf_importance_profile, final_submission_figures_permfit_comparison_grid_ecg_slice_regions [EXTRACTED 1.00]
- **PermFIT slice perturbation strategies** — final_submission_figures_permfit_perturbation_methods_shuffle_perturbation, final_submission_figures_permfit_perturbation_methods_permute_perturbation, final_submission_figures_permfit_perturbation_methods_zero_perturbation, final_submission_figures_permfit_perturbation_methods_mean_perturbation [EXTRACTED 1.00]
- **PermFIT SVM vs RF slice-importance comparison across hold-out splits** — final_submission_figures_permfit_profiles_svm_vs_rf_permfit, final_submission_figures_permfit_profiles_svm_vs_rf_qrs_complex_importance, final_submission_figures_permfit_profiles_svm_vs_rf_rf_diffuse_importance, final_submission_figures_permfit_profiles_svm_vs_rf_beat_vs_patient_holdout [INFERRED 0.85]
- **Cardiac phase regions partitioning the 11 ECG slices** — final_submission_figures_permfit_random_forest_beats_pr_interval, final_submission_figures_permfit_random_forest_beats_qrs_complex, final_submission_figures_permfit_random_forest_beats_st_segment_t_wave, final_submission_figures_permfit_random_forest_beats_ecg_slices [EXTRACTED 1.00]
- **ECG waveform regions scored by PermFIT slice importance** — final_submission_figures_permfit_random_forest_patients_pr_interval, final_submission_figures_permfit_random_forest_patients_qrs_complex, final_submission_figures_permfit_random_forest_patients_st_segment_t_wave, final_submission_figures_permfit_random_forest_patients_mean_slice_importance [EXTRACTED 1.00]
- **PermFIT SVM beat hold-out slice importance analysis** — final_submission_figures_permfit_svm_beats_permfit_shuffle_within_slice, final_submission_figures_permfit_svm_beats_ecg_slice_regions, final_submission_figures_permfit_svm_beats_beat_holdout_split, final_submission_figures_permfit_svm_beats_qrs_dominance_finding [INFERRED 0.85]
- **ECG wave regions scored by PermFIT for SVM (patient hold-out)** — final_submission_figures_permfit_svm_patients_pr_interval, final_submission_figures_permfit_svm_patients_qrs_complex_dominance, final_submission_figures_permfit_svm_patients_st_segment_t_wave [EXTRACTED 1.00]
- **Eight MIT-BIH heartbeat classes shown as one example beat each** — final_submission_figures_task1_ecg_beats_class_n, final_submission_figures_task1_ecg_beats_class_l, final_submission_figures_task1_ecg_beats_class_r, final_submission_figures_task1_ecg_beats_class_v, final_submission_figures_task1_ecg_beats_class_a, final_submission_figures_task1_ecg_beats_class_f, final_submission_figures_task1_ecg_beats_class_f_lower, final_submission_figures_task1_ecg_beats_class_paced [EXTRACTED 1.00]

## Communities (23 total, 1 thin omitted)

### Community 0 - "Submission Pipeline & Setup"
Cohesion: 0.08
Nodes (30): Final_Submission README, 8 heartbeat classes (N, L, R, V, A, F, f, /), 11 heartbeat slices (PR interval 1-4, QRS 5-7, ST/T-wave 8-11), MIT-BIH Arrhythmia Database, Random Forest classifier, RUN_PERMFIT flag, Standardised 275-sample R-peak-centred beat, SVM classifier (+22 more)

### Community 1 - "Shared PermFIT Code"
Cohesion: 0.11
Nodes (13): compute_permfit_ecg(), evaluate(), load_split(), make_model(), one_hot(), perturb_slice(), plot_permfit_importance(), Appendix A - Code and reproducibility (walkthrough.ipynb, run_all.sh) (+5 more)

### Community 2 - "Report Findings"
Cohesion: 0.08
Nodes (38): Report: Explaining ECG Arrhythmia Classifiers with PermFIT, Accuracy drop per slice (percentage points), Arrieta et al. 2020 - Explainable AI (XAI): concepts, taxonomies (Information Fusion), Beat hold-out protocol (random 75/25), Beat preprocessing (275-sample R-peak window, z-score), Bootstrap class balancing (resample to mean abnormal class size), Classification results (Table 3), Row-normalised confusion matrices (Figure 3) (+30 more)

### Community 3 - "LIME & SHAP Lecture"
Cohesion: 0.11
Nodes (15): Lecture 2: LIME and SHAP (ML Interpretability), ECG beat split into 11 segments (PR interval, QRS complex, ST segment), Dr. Fani Deligianni (University of Glasgow), LIME weights for CNN ECG classification (class 1 & 3), LIME Image Explainer, LIME weights for LSTM ECG classification (class 1), LIME weights for MLP ECG classification (class 1), LIME Tabular Explainer (+7 more)

### Community 4 - "Case Study Brief"
Cohesion: 0.08
Nodes (29): Case Study: ECG Explainability (Pre-processing & Arrhythmia Detection), Arrhythmia, Assessed Exercise Requirements, Beat Hold-out Validation Protocol (75/25 split), Bootstrap Resampling (sklearn resample, up/down-sampling), Class Imbalance (dominance of N beats), Clustering Task (6-member groups), Electrocardiogram (ECG) (+21 more)

### Community 5 - "Explainability Lecture"
Cohesion: 0.09
Nodes (26): Lecture 1: Explainability in ML (Deligianni slides), Assessment Tasks (holdout + patient-holdout classification, PFI, clustering), Eight Beat Classes (N, L, R, V, A, F, f, /), Class Imbalance (Normal class over-represented), Clustering for Data Visualisation (6-member groups), Electrocardiogram (P-wave, QRS complex, T-wave), ECG Beat Classification, ECG Noise Interference (baseline wander, electrode contact, motion, power line) (+18 more)

### Community 6 - "Interpretable Model Types"
Cohesion: 0.19
Nodes (10): Decision Trees, Interpretable vs Explainable Spectrum (Grey Area), K-Nearest Neighbours, Linear Regression, Logistic Regression, Neural Networks / CNNs / Deep Learning, Random Forests, Molnar - Interpretable Machine Learning (book) (+2 more)

### Community 7 - "Marking & Template"
Cohesion: 0.25
Nodes (11): Marking Sheet (Case Study Report), Code Implementation Criterion (15 pts): clarity, documentation, reproducibility, Discussion Criterion (20 pts): conclusions from results and why, Introduction Criterion (10 pts): case study intro + predictive/exploratory question, Methods Criterion (15 pts): main idea, important parameters to tune, Results Criterion (40 pts): experiment setup, rationale, metrics in figures/tables, Report Template, Report Discussion Section (+3 more)

### Community 8 - "Perturbation Method Comparison"
Cohesion: 0.29
Nodes (11): PermFIT Perturbation Methods Figure, Mean Importance M_j (PermFIT), Mean Perturbation, Permute Perturbation, Perturbation Method Comparison (shuffle/permute/zero/mean), Random Forest Beat Hold-out Slice Importance, Shuffle Perturbation, ECG Slice 6 Importance Peak (shaded slices 5-7) (+3 more)

### Community 9 - "RF Patient PermFIT"
Cohesion: 0.31
Nodes (10): PermFIT Random Forest Patient Hold-out Figure, ECG Beat Slices (11 x 25 samples), Mean Slice Importance M̄_j, Patient Hold-out Split, PermFIT (shuffle within slice), PR Interval (slices 1-4), QRS Complex (slices 5-7), R-peak Slice 6 Dominates Importance (~0.36) (+2 more)

### Community 10 - "Beat Class Examples"
Cohesion: 0.27
Nodes (10): Example ECG Beat per Class (Task 1 figure), 275-sample beat segment centred on R-peak (~sample 138), Class A (Atrial premature beat, label 5), Class F (Fusion of ventricular and normal, label 6), Class f (Fusion of paced and normal, label 7), Class L (Left bundle branch block, label 2), Class N (Normal beat, label 1), Class / (Paced beat, label 8) (+2 more)

### Community 11 - "RF Beat PermFIT"
Cohesion: 0.31
Nodes (9): PermFIT Random Forest Beat Hold-out Importance Chart, Beat hold-out split, ECG slices (11 x 25 samples), PermFIT (shuffle within slice), PR interval (slices 1-4), QRS complex (slices 5-7), Finding: R-peak slice 6 dominates importance, Random Forest classifier (+1 more)

### Community 12 - "SVM Patient PermFIT"
Cohesion: 0.32
Nodes (7): PermFIT SVM Patient Hold-out Figure, ECG beat split into 11 slices of 25 samples (R-peak in slice 6), Mean importance M̄_j with error bars, PR interval (slices 1-4), near-zero importance, QRS complex (slices 5-7) dominates importance; slice 6 ~0.37, ST segment / T-wave (slices 8-11), near-zero importance, SVM, patient hold-out evaluation

### Community 13 - "SVM Patient Confusion"
Cohesion: 0.38
Nodes (7): L, R, A Absent from Held-out Patients (all-zero rows), SVM Patient Hold-out Confusion Matrix (row-normalised), ECG Beat Classes (N, L, R, V, A, F, f, /), Fusion Beat Confusion (F recall 0.45, f recall 0.12), Patient Hold-out Evaluation (inter-patient split), High Recall on N (0.93), V (0.98) and Paced / (0.98), SVM Classifier

### Community 14 - "RF Patient Confusion"
Cohesion: 0.47
Nodes (6): Random Forest Confusion Matrix (Patient Hold-out), ECG Beat Classes (N, L, R, V, A, F, f, /), Fusion Beat (F, f) Misclassification, Patient Hold-out Evaluation (inter-patient split), Random Forest ECG Beat Classifier, Row-normalised Confusion Matrix (per-class recall)

### Community 15 - "PermFIT Comparison Grid"
Cohesion: 0.53
Nodes (6): PermFIT Slice Importance Comparison Grid (SVM vs RF, beat vs patient hold-out), Beat hold-out vs Patient hold-out evaluation schemes, ECG Slice Regions: PR interval (1-4), QRS complex (5-7), ST segment/T-wave (8-11), PermFIT Slice Importance (shuffle within slice, mean over 5 folds), Finding: R-peak slice 6 (QRS complex) dominates importance for both models, SVM vs Random Forest importance profile comparison

### Community 16 - "RF Beat Confusion"
Cohesion: 0.50
Nodes (5): Random Forest Beat Hold-out Confusion Matrix, A and F Beats Confused with N and V, Beat-level Hold-out Evaluation, ECG Beat Classes (N, L, R, V, A, F, f, /), Random Forest Classifier

### Community 17 - "SVM Beat Confusion"
Cohesion: 0.50
Nodes (5): SVM Beat Hold-out Confusion Matrix (cm_svm_beats.png), Atrial Premature (A) misclassified as Normal (N), Beat-level Hold-out Evaluation, ECG Beat Classes (N, L, R, V, A, F, f, /), SVM Classifier

### Community 18 - "SVM vs RF Profiles"
Cohesion: 0.60
Nodes (5): PermFIT Importance Profiles: SVM vs Random Forest (beat & patient hold-out), Beat hold-out vs patient hold-out evaluation split, PermFIT (permutation feature importance), QRS complex (slices 5-7) dominates feature importance, Random Forest spreads importance more widely than SVM

### Community 19 - "SVM Beat PermFIT"
Cohesion: 0.50
Nodes (4): PermFIT SVM Beat Hold-out Importance Chart, Beat hold-out split, ECG slice regions (PR interval / QRS complex / ST-T wave), SVM relies almost entirely on QRS complex (slice 6 R-peak)

### Community 20 - "Task 3 Confusion Matrix"
Cohesion: 0.60
Nodes (5): Task 3 Patient-holdout Confusion Matrix (figure), Classes Absent from Test Patients (L, R, A), ECG Beat Classes (N, L, R, V, A, F, f, /), Fusion-of-paced (f) Beats Poorly Classified, Patient-holdout Evaluation

### Community 21 - "Class Imbalance"
Cohesion: 0.67
Nodes (3): Distribution of ECG Beat Classes (bar chart), ECG Beat Annotation Classes (N, L, R, V, A, F, f, /), ECG Beat Class Imbalance

## Ambiguous Edges - Review These
- `SVM classifier` → `Best params: SVM C=100; RF max_features=0.1, min_samples_leaf=1`  [AMBIGUOUS]
  Final_Submission/results/log_tune_hyperparameters.txt · relation: references

## Knowledge Gaps
- **75 isolated node(s):** `MPLBACKEND`, `graphify usage rules for Claude (CLAUDE.md)`, `graphify knowledge graph (graphify-out/graph.json)`, `Task 1 run log`, `Task 2 SVM run log` (+70 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 93 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `Appendix A - Code and reproducibility (walkthrough.ipynb, run_all.sh)` connect `Shared PermFIT Code` to `Report Findings`?**
  _High betweenness centrality (0.028) - this node is a cross-community bridge._
- **What connects `MPLBACKEND`, `graphify usage rules for Claude (CLAUDE.md)`, `graphify knowledge graph (graphify-out/graph.json)` to the rest of the system?**
  _75 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Submission Pipeline & Setup` be split into smaller, more focused modules?**
  _Cohesion score 0.07862679955703211 - nodes in this community are weakly interconnected._
- **Why does `Report: Explaining ECG Arrhythmia Classifiers with PermFIT` connect `Report Findings` to `Shared PermFIT Code`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Should `Shared PermFIT Code` be split into smaller, more focused modules?**
  _Cohesion score 0.11498257839721254 - nodes in this community are weakly interconnected._
- **Should `Report Findings` be split into smaller, more focused modules?**
  _Cohesion score 0.08392603129445235 - nodes in this community are weakly interconnected._

### Low-confidence Hints
_AMBIGUOUS edges — the extractor was unsure. Verify before acting on these._

- **What is the exact relationship between `SVM classifier` and `Best params: SVM C=100; RF max_features=0.1, min_samples_leaf=1`?**
  _Edge tagged AMBIGUOUS (relation: references) - confidence is low._