"""Task 4 - Explain the SVM models of Tasks 2 and 3 with PermFIT.

The models are exactly those of task2_svm.py (beat hold-out) and task3.py
(patient hold-out); see ecg_utils.make_model.

PermFIT = permutation feature importance with stratified 5-fold cross-fitting
(Mi et al. 2021, Algorithm 1 in the case study handout):
  1. split the training beats into 5 folds, stratified on the beat class;
  2. for each fold, train a new SVM on the other 4 folds;
  3. for each of the 11 slices (25 samples each), destroy that slice in the
     held-out beats and measure how much worse the prediction gets;
  4. average over all beats -> one importance score per slice.

Main perturbation (as asked in the handout): shuffle the points inside the slice.
Zero, mean and between-beat permutation are also computed as a sensitivity check;
they reuse the same fitted models, so they only cost extra predictions.

Usage:  python task4_permfit.py            (SVM, both protocols, ~20-40 min)
        python task4_permfit.py "Random Forest"
Output: results/permfit_<model>_<split>.npz and figures/permfit_<model>_<split>.png
"""
import sys
import time

import numpy as np

from ecg_utils import (FIG_DIR, RESULTS_DIR, compute_permfit_ecg, load_split, make_model,
                       plot_permfit_importance)

MODES = ("shuffle", "permute", "zero", "mean")
SPLITS = {"beats": "beat hold-out", "patients": "patient hold-out"}


def tag(model_name, split):
    return f"{model_name.replace(' ', '_').lower()}_{split}"


def run_permfit(model_name, split):
    """Run PermFIT on the training data of one protocol, save numbers and a figure."""
    X, y, _, _ = load_split(split)
    print(f"\n[{model_name} | {SPLITS[split]}] PermFIT on {X.shape[0]} training beats", flush=True)
    start = time.time()
    res = compute_permfit_ecg(make_model(model_name, split, probability=True), X, y, modes=MODES)
    print(f"  done in {(time.time() - start) / 60:.1f} min")

    arrays = {"baseline_accuracy": res["baseline"]["accuracy"],
              "baseline_sq_error": res["baseline"]["sq_error"]}
    for m in MODES:
        for key in ("mean", "per_fold", "acc_drop"):
            arrays[f"{m}_{key}"] = res[m][key]
    np.savez(RESULTS_DIR / f"permfit_{tag(model_name, split)}.npz", **arrays)

    plot_permfit_importance(res["shuffle"]["mean"], res["shuffle"]["per_fold"],
                            title=f"PermFIT (shuffle within slice) - {model_name}, {SPLITS[split]}",
                            save_path=FIG_DIR / f"permfit_{tag(model_name, split)}.png")
    order = np.argsort(-res["shuffle"]["mean"]) + 1
    print(f"  slices ranked by importance (shuffle): {order.tolist()}")
    return res


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "SVM"
    for split in SPLITS:
        run_permfit(model_name, split)
