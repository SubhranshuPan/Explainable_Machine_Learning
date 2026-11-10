"""Task 4: PermFIT on the SVMs of Task 2 (beat hold-out) and Task 3 (patient hold-out).

Run:  python task4_permfit.py                  (SVM, about 35 min)
      python task4_permfit.py "Random Forest"
"""
import sys
import time

import numpy as np
import matplotlib.pyplot as plt

from ecg_utils import FIG_DIR, RESULTS_DIR, SPLITS, compute_permfit_ecg, load_split, make_model, plot_permfit_importance

# shuffle is the main method, the other three are a sensitivity check
MODES = ("shuffle", "permute", "zero", "mean")


def tag(model_name, split):
    return model_name.replace(" ", "_").lower() + "_" + split


def run_permfit(model_name, split):
    X, y, _, _ = load_split(split)
    print(f"\n[{model_name} | {SPLITS[split]}] PermFIT on {len(X)} training beats", flush=True)
    start = time.time()
    res = compute_permfit_ecg(make_model(model_name, split, probability=True), X, y, modes=MODES)
    print(f"  done in {(time.time() - start) / 60:.1f} min")

    arrays = {"baseline_accuracy": res["baseline"]["accuracy"], "baseline_sq_error": res["baseline"]["sq_error"]}
    for m in MODES:
        for key in ("mean", "per_fold", "acc_drop"):
            arrays[f"{m}_{key}"] = res[m][key]
    np.savez(RESULTS_DIR / f"permfit_{tag(model_name, split)}.npz", **arrays)

    fig, ax = plt.subplots(figsize=(9, 4.5))
    plot_permfit_importance(res["shuffle"]["mean"], res["shuffle"]["per_fold"],
                            f"PermFIT (shuffle within slice) - {model_name}, {SPLITS[split]}", ax)
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG_DIR / f"permfit_{tag(model_name, split)}.png", dpi=200)
    plt.close(fig)

    ranking = np.argsort(-res["shuffle"]["mean"]) + 1
    print(f"  slices ranked by importance (shuffle): {ranking.tolist()}")


if __name__ == "__main__":
    model_name = sys.argv[1] if len(sys.argv) > 1 else "SVM"
    for split in SPLITS:
        run_permfit(model_name, split)
