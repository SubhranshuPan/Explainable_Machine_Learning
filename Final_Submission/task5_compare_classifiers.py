"""Task 5 - Apply the same explainability technique to a different classifier and compare.

Second classifier: Random Forest (300 decision trees, majority vote).
Why it is a good contrast to the SVM: the SVM compares whole beats with stored
"support" beats (a smooth similarity in all 275 dimensions), while each tree asks
yes/no questions about individual time points. PermFIT shows whether the two
models rely on the same parts of the heartbeat.

Steps:
  1. train + evaluate the Random Forest on both protocols; the SVM predictions saved
     by task2_svm.py / task3.py are scored with the same function, so all four
     models get identical metrics and confusion-matrix plots;
  2. run PermFIT on the Random Forest (same function and settings as Task 4);
  3. compare SVM vs Random Forest: classification table, importance figures, tables.

Needs the outputs of task2_svm.py, task3.py and task4_permfit.py (run run_all.sh).
"""
import json

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from ecg_utils import (FIG_DIR, RESULTS_DIR, SLICE_REGIONS, evaluate, load_split, make_model,
                       plot_permfit_importance)
from task4_permfit import MODES, SPLITS, run_permfit, tag

MODELS = ["SVM", "Random Forest"]

# 1. Classification results of all four models
SVM_PREDICTIONS = {"beats": "task2_svm_beats_pred.npy", "patients": "task3_svm_patients_pred.npy"}
for split, split_name in SPLITS.items():
    X_train, y_train, X_test, y_test = load_split(split)
    # SVM: predictions made by the Task 2 / Task 3 scripts
    res = evaluate(y_test, np.load(RESULTS_DIR / SVM_PREDICTIONS[split]), title=f"SVM - {split_name}",
                   save_as=f"cm_svm_{split}.png")
    (RESULTS_DIR / f"metrics_svm_{split}.json").write_text(json.dumps(res, indent=2))
    # Random Forest: trained here
    rf = make_model("Random Forest", split).fit(X_train, y_train)
    res = evaluate(y_test, rf.predict(X_test), title=f"Random Forest - {split_name}",
                   save_as=f"cm_random_forest_{split}.png")
    (RESULTS_DIR / f"metrics_random_forest_{split}.json").write_text(json.dumps(res, indent=2))

# 2. PermFIT on the Random Forest 
for split in SPLITS:
    run_permfit("Random Forest", split)

# 3. Comparison 
rows = []
for model in MODELS:
    for split, split_name in SPLITS.items():
        m = json.loads((RESULTS_DIR / f"metrics_{tag(model, split)}.json").read_text())
        rows.append({"model": model, "protocol": split_name, "accuracy": m["accuracy"],
                     "macro_precision": m["macro_precision"], "macro_recall": m["macro_recall"],
                     "macro_f1": m["macro_f1"]})
table = pd.DataFrame(rows).round(3)
table.to_csv(RESULTS_DIR / "classification_summary.csv", index=False)
print("\nClassification results\n", table.to_string(index=False))

pf = {(model, split): np.load(RESULTS_DIR / f"permfit_{tag(model, split)}.npz")
      for model in MODELS for split in SPLITS}

# 3a. 2x2 grid of importance bars (main method: shuffle within slice)
fig, axes = plt.subplots(2, 2, figsize=(15, 8), sharex=True)
for r, model in enumerate(MODELS):
    for c, (split, split_name) in enumerate(SPLITS.items()):
        d = pf[model, split]
        plot_permfit_importance(d["shuffle_mean"], d["shuffle_per_fold"], ax=axes[r, c],
                                title=f"{model} - {split_name}")
axes[0, 0].legend(loc="upper left", fontsize=8)
fig.suptitle("PermFIT slice importance (shuffle within slice, error bars = spread over 5 folds)")
fig.tight_layout()
fig.savefig(FIG_DIR / "permfit_comparison_grid.png", dpi=200)
plt.close(fig)

# 3b. Normalised profiles: share of total importance per slice, both models on one plot
fig, axes = plt.subplots(1, 2, figsize=(15, 4.5), sharey=True)
width = 0.38
for ax, (split, split_name) in zip(axes, SPLITS.items()):
    for k, model in enumerate(MODELS):
        imp = np.clip(pf[model, split]["shuffle_mean"], 0, None)
        ax.bar(np.arange(1, 12) + (k - 0.5) * width, 100 * imp / imp.sum(), width, label=model)
    for label, a, b in SLICE_REGIONS:
        if label == "QRS complex":
            ax.axvspan(a - 0.5, b + 0.5, color="crimson", alpha=0.1, label="QRS complex (slices 5-7)")
    ax.set_xticks(np.arange(1, 12))
    ax.set_xlabel("ECG slice")
    ax.set_title(split_name)
axes[0].set_ylabel("% of total importance")
axes[0].legend(fontsize=8)
fig.suptitle("Where does each model look? (importance normalised to 100% per model)")
fig.tight_layout()
fig.savefig(FIG_DIR / "permfit_profiles_svm_vs_rf.png", dpi=200)
plt.close(fig)

# 3c. Sensitivity to the perturbation method (beat hold-out)
fig, axes = plt.subplots(1, 2, figsize=(15, 4.5), sharey=False)
for ax, model in zip(axes, MODELS):
    for k, mode in enumerate(MODES):
        ax.plot(np.arange(1, 12), pf[model, "beats"][f"{mode}_mean"], marker="o", label=mode)
    ax.axvspan(4.5, 7.5, color="crimson", alpha=0.1)
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks(np.arange(1, 12))
    ax.set_xlabel("ECG slice")
    ax.set_title(f"{model} - beat hold-out")
axes[0].set_ylabel(r"mean importance $\bar{M}_j$")
axes[0].legend(title="perturbation")
fig.suptitle("Same model, different ways of destroying a slice")
fig.tight_layout()
fig.savefig(FIG_DIR / "permfit_perturbation_methods.png", dpi=200)
plt.close(fig)

# 3d. Tables for the report
long = []
for (model, split), d in pf.items():
    for mode in MODES:
        for j in range(11):
            long.append({"model": model, "protocol": SPLITS[split], "perturbation": mode, "slice": j + 1,
                         "importance": d[f"{mode}_mean"][j], "fold_std": d[f"{mode}_per_fold"][:, j].std(),
                         "accuracy_drop_pct": d[f"{mode}_acc_drop"][j]})
long = pd.DataFrame(long)
long.to_csv(RESULTS_DIR / "permfit_all_results.csv", index=False)

main = (long[long.perturbation == "shuffle"]
        .pivot_table(index="slice", columns=["model", "protocol"], values="importance").round(4))
main.to_csv(RESULTS_DIR / "permfit_shuffle_table.csv")
print("\nPermFIT importance (shuffle within slice)\n", main.to_string())

for (model, split), d in pf.items():
    print(f"{model:13s} {SPLITS[split]:17s} PermFIT CV baseline accuracy "
          f"{d['baseline_accuracy'].mean():.3f}  top-3 slices {(np.argsort(-d['shuffle_mean'])[:3] + 1).tolist()}")
