"""Shared code for Tasks 4 and 5 of the ECG arrhythmia explainability case study.

Holds the data loading, the model definitions (copied from Tasks 2 and 3),
the evaluation metrics, the PermFIT algorithm and its plots.

CSV layout (made by 00_preprocess.ipynb and 01_split_resample.ipynb):
    columns 0..274 -> one standardised heartbeat (275 samples, R-peak in the middle)
    column  275    -> class ID 1..8 (see CLASS_NAMES)
    column  276    -> MIT-BIH record (patient) number
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_recall_fscore_support, ConfusionMatrixDisplay)
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

# ----------------------------------------------------------------------------- paths
ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"
RESULTS_DIR = ROOT / "results"
for _d in (FIG_DIR, RESULTS_DIR):
    _d.mkdir(exist_ok=True)

# ----------------------------------------------------------------------------- constants
SEED = 42
BEAT_LENGTH = 275
CLASS_IDS = [1, 2, 3, 4, 5, 6, 7, 8]
CLASS_NAMES = ["N", "L", "R", "V", "A", "F", "f", "/"]

N_SLICES, SLICE_LENGTH = 11, 25          # 11 x 25 = 275 samples
# ECG regions covered by the slices (lecture "Application of PFI in ECG Classification")
SLICE_REGIONS = [("PR interval", 1, 4), ("QRS complex", 5, 7), ("ST segment / T-wave", 8, 11)]


# ----------------------------------------------------------------------------- data
def load_split(name):
    """Load the train/test CSVs of one validation protocol.

    name: 'beats' (beat hold-out) or 'patients' (patient hold-out).
    Returns X_train, y_train, X_test, y_test with y = class IDs 1..8.
    """
    out = []
    for part in ("train", "test"):
        arr = np.loadtxt(DATA_DIR / f"{part}_{name}.csv", delimiter=",")
        out += [arr[:, :BEAT_LENGTH], arr[:, BEAT_LENGTH].astype(int)]
    return tuple(out)


def one_hot(y, classes=CLASS_IDS):
    """One-hot encode class IDs -> array of shape (n, len(classes))."""
    return (np.asarray(y)[:, None] == np.asarray(classes)[None, :]).astype(float)


# ----------------------------------------------------------------------------- models
def make_model(name, split, probability=False):
    """The models explained in Tasks 4 and 5.

    SVM: exactly the models built in Tasks 2 and 3, so PermFIT explains those models.
         split='beats'    -> task2_svm.py:  SVC(kernel="rbf")
         split='patients' -> task3.py:      make_pipeline(StandardScaler(), SVC(max_iter=10000, random_state=42))
    Random Forest (Task 5): 300 trees, 10% of the 275 time points tried at each split,
         chosen by 3-fold CV grid search (tune_hyperparameters.py). Same for both splits.

    probability=True is only needed for PermFIT, which compares predicted class
    probabilities with the true one-hot labels. An SVM has no probabilities of its own,
    so its scores are calibrated with Platt scaling (CalibratedClassifierCV, sklearn's
    replacement for the deprecated SVC(probability=True)). The decision boundary is the
    same SVM; only probabilities are added on top.
    """
    if name == "SVM":
        if split == "beats":
            svm = SVC(kernel="rbf")
        elif split == "patients":
            svm = make_pipeline(StandardScaler(), SVC(max_iter=10000, random_state=SEED))
        else:
            raise ValueError(f"unknown split {split!r}")
        return CalibratedClassifierCV(svm, method="sigmoid", ensemble=False) if probability else svm
    if name == "Random Forest":
        return RandomForestClassifier(n_estimators=300, max_features=0.1, min_samples_leaf=1,
                                      n_jobs=-1, random_state=SEED)
    raise ValueError(f"unknown model {name!r}")


# ----------------------------------------------------------------------------- evaluation
def evaluate(y_true, y_pred, title="", save_as=None):
    """Accuracy, per-class + macro precision/recall/F1 and a confusion matrix.

    Macro averages only use classes that occur in y_true. In the patient hold-out
    test set L, R and A never occur, so their recall is undefined; counting them as 0
    would unfairly pull the macro score down.
    """
    present = [c for c in CLASS_IDS if c in set(np.asarray(y_true))]
    acc = accuracy_score(y_true, y_pred)
    p, r, f, support = precision_recall_fscore_support(y_true, y_pred, labels=CLASS_IDS, zero_division=0)

    print(f"=== {title} ===\nAccuracy: {acc:.4f}\n")
    print(f"{'class':>5} {'precision':>9} {'recall':>7} {'f1':>6} {'support':>8}")
    for name, cid, pi, ri, fi, si in zip(CLASS_NAMES, CLASS_IDS, p, r, f, support):
        note = "" if cid in present else "   (not in test set)"
        print(f"{name:>5} {pi:9.3f} {ri:7.3f} {fi:6.3f} {si:8d}{note}")
    idx = [CLASS_IDS.index(c) for c in present]
    macro = dict(precision=p[idx].mean(), recall=r[idx].mean(), f1=f[idx].mean())
    print(f"\nMacro (classes present): precision={macro['precision']:.3f} "
          f"recall={macro['recall']:.3f} f1={macro['f1']:.3f}\n")

    cm = confusion_matrix(y_true, y_pred, labels=CLASS_IDS)
    with np.errstate(invalid="ignore", divide="ignore"):
        cm_norm = np.nan_to_num(cm / cm.sum(axis=1, keepdims=True))
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ConfusionMatrixDisplay(cm_norm, display_labels=CLASS_NAMES).plot(
        ax=ax, cmap="Blues", values_format=".2f", colorbar=False)
    ax.set_title(f"{title}\n(rows = true class, normalised)")
    fig.tight_layout()
    if save_as:
        fig.savefig(FIG_DIR / save_as, dpi=200)
    plt.close(fig)

    return dict(model=title, accuracy=acc, macro_precision=macro["precision"],
                macro_recall=macro["recall"], macro_f1=macro["f1"])


# ----------------------------------------------------------------------------- PermFIT
def perturb_slice(X, j, mode, rng, slice_length=SLICE_LENGTH):
    """Return a copy of X with slice j (0-based) destroyed in one of four ways.

    shuffle : shuffle the 25 points inside the slice, separately for every beat
              (the method asked for in the case study)
    permute : give every beat the slice of another, randomly chosen beat
              (classic permutation feature importance)
    zero    : set the slice to 0
    mean    : replace the slice by its own average value (a flat line)
    """
    s, e = j * slice_length, (j + 1) * slice_length
    Xp = X.copy()
    if mode == "shuffle":
        Xp[:, s:e] = rng.permuted(X[:, s:e], axis=1)
    elif mode == "permute":
        Xp[:, s:e] = X[rng.permutation(len(X)), s:e]
    elif mode == "zero":
        Xp[:, s:e] = 0.0
    elif mode == "mean":
        Xp[:, s:e] = X[:, s:e].mean(axis=1, keepdims=True)
    else:
        raise ValueError(f"unknown mode {mode!r}")
    return Xp


def compute_permfit_ecg(model, X, y, n_splits=5, n_slices=N_SLICES, slice_length=SLICE_LENGTH,
                        modes=("shuffle",), random_state=SEED, verbose=True):
    """PermFIT: permutation feature importance with stratified K-fold cross-fitting.

    For every fold k: fit a fresh copy of `model` on the other K-1 folds, then for
    every beat i in fold k and every slice j compute

        M_ij = sum_c (Y_ic - p_c(X_i^(j)))^2  -  sum_c (Y_ic - p_c(X_i))^2

    i.e. the squared error between the one-hot label Y_i and the predicted class
    probabilities p(.) after slice j was destroyed, minus the same error on the
    intact beat. M_ij > 0 means the model got worse, so slice j mattered for beat i.
    Every beat is scored by a model that never saw it during training.

    Parameters
    ----------
    model : unfitted sklearn classifier with predict_proba
            (for the SVM use make_model("SVM", split, probability=True)).
    X, y  : beats (N, 275) and class IDs (N,).
    modes : perturbation types to evaluate, see perturb_slice(). All modes reuse the
            same fitted fold models, so extra modes only cost predictions.

    Returns
    -------
    dict mode -> {
        "mean":     (n_slices,)  mean importance  M_j  (average over all N beats)
        "per_fold": (n_splits, n_slices) mean importance inside each fold
        "acc_drop": (n_slices,)  drop in accuracy (percentage points) per slice
        "M":        (N, n_slices) the full beat-level importance matrix
    }
    plus key "baseline": per-fold accuracy and squared error of the intact beats.
    """
    N, D = X.shape
    assert D == n_slices * slice_length, f"expected {n_slices * slice_length} features, got {D}"
    skf = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=random_state)
    rng = np.random.default_rng(random_state)

    res = {m: {"M": np.zeros((N, n_slices)), "per_fold": np.zeros((n_splits, n_slices)),
               "correct": np.zeros((N, n_slices), dtype=bool)} for m in modes}
    base_correct = np.zeros(N, dtype=bool)
    baseline = {"accuracy": [], "sq_error": []}

    for k, (tr, va) in enumerate(skf.split(X, y)):
        fold_model = clone(model).fit(X[tr], y[tr])
        classes = fold_model.classes_                 # column order of predict_proba
        Y_va = one_hot(y[va], classes)

        p_clean = fold_model.predict_proba(X[va])
        loss_clean = ((Y_va - p_clean) ** 2).sum(axis=1)
        base_correct[va] = classes[p_clean.argmax(1)] == y[va]
        baseline["accuracy"].append(base_correct[va].mean())
        baseline["sq_error"].append(loss_clean.mean())
        if verbose:
            print(f"  fold {k + 1}/{n_splits}: train {len(tr)}, test {len(va)}, "
                  f"accuracy {baseline['accuracy'][-1]:.3f}", flush=True)

        for m in modes:
            for j in range(n_slices):
                p_perm = fold_model.predict_proba(perturb_slice(X[va], j, m, rng, slice_length))
                loss_perm = ((Y_va - p_perm) ** 2).sum(axis=1)
                res[m]["M"][va, j] = loss_perm - loss_clean
                res[m]["per_fold"][k, j] = (loss_perm - loss_clean).mean()
                res[m]["correct"][va, j] = classes[p_perm.argmax(1)] == y[va]

    out = {"baseline": {key: np.array(v) for key, v in baseline.items()}}
    for m in modes:
        out[m] = {"mean": res[m]["M"].mean(axis=0), "per_fold": res[m]["per_fold"], "M": res[m]["M"],
                  "acc_drop": 100 * (base_correct.mean() - res[m]["correct"].mean(axis=0))}
    return out


def plot_permfit_importance(mean_importance, per_fold=None, title="", ax=None, save_path=None):
    """Bar chart of the 11 slice importances, shaded by ECG region.

    Error bars (if per_fold is given) show the spread across the 5 CV folds.
    """
    own_fig = ax is None
    if own_fig:
        fig, ax = plt.subplots(figsize=(9, 4.5))
    slices = np.arange(1, len(mean_importance) + 1)
    colors = {"PR interval": "royalblue", "QRS complex": "crimson", "ST segment / T-wave": "darkgreen"}
    for label, a, b in SLICE_REGIONS:
        ax.axvspan(a - 0.5, b + 0.5, color=colors[label], alpha=0.12,
                   label=f"{label} (slices {a}-{b})")
    yerr = per_fold.std(axis=0) if per_fold is not None else None
    ax.bar(slices, mean_importance, yerr=yerr, capsize=3, color="navy", width=0.6, zorder=3)
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks(slices)
    ax.set_xlabel("ECG slice (25 samples each; R-peak in slice 6)")
    ax.set_ylabel(r"mean importance $\bar{M}_j$")
    ax.set_title(title)
    ax.grid(axis="y", ls=":", alpha=0.6, zorder=0)
    if own_fig:
        ax.legend(loc="upper left", fontsize=8)
        fig.tight_layout()
        if save_path:
            fig.savefig(save_path, dpi=200)
        plt.close(fig)
    return ax
