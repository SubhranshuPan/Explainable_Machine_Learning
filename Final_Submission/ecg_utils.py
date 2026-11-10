"""Shared code for Tasks 4 and 5: data loading, models, evaluation and PermFIT."""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, precision_recall_fscore_support, ConfusionMatrixDisplay
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

DATA_DIR = Path("data")
FIG_DIR = Path("figures")
RESULTS_DIR = Path("results")
FIG_DIR.mkdir(exist_ok=True)
RESULTS_DIR.mkdir(exist_ok=True)

SEED = 42
CLASS_IDS = [1, 2, 3, 4, 5, 6, 7, 8]
CLASS_NAMES = ["N", "L", "R", "V", "A", "F", "f", "/"]
SPLITS = {"beats": "beat hold-out", "patients": "patient hold-out"}

# each beat (275 samples) is cut into 11 slices of 25 samples
N_SLICES = 11
SLICE_LENGTH = 25
SLICE_REGIONS = [("PR interval", 1, 4), ("QRS complex", 5, 7), ("ST segment / T-wave", 8, 11)]


def load_split(name):
    # name = "beats" or "patients"; column 275 is the label, column 276 the record number
    train = np.loadtxt(DATA_DIR / f"train_{name}.csv", delimiter=",")
    test = np.loadtxt(DATA_DIR / f"test_{name}.csv", delimiter=",")
    return train[:, :275], train[:, 275].astype(int), test[:, :275], test[:, 275].astype(int)


def make_model(name, split, probability=False):
    if name == "Random Forest":
        # settings from tune_hyperparameters.py
        return RandomForestClassifier(n_estimators=300, max_features=0.1, min_samples_leaf=1,
                                      n_jobs=-1, random_state=SEED)

    # same SVMs as task2_svm.py (beats) and task3.py (patients)
    if split == "beats":
        model = SVC(kernel="rbf")
    else:
        model = make_pipeline(StandardScaler(), SVC(max_iter=10000, random_state=SEED))

    # PermFIT needs class probabilities, so add Platt scaling on top of the SVM
    if probability:
        model = CalibratedClassifierCV(model, method="sigmoid", ensemble=False)
    return model


def evaluate(y_true, y_pred, title, save_as):
    acc = accuracy_score(y_true, y_pred)
    p, r, f, support = precision_recall_fscore_support(y_true, y_pred, labels=CLASS_IDS, zero_division=0)

    # macro scores only use the classes that appear in the test set
    present = [c for c in CLASS_IDS if c in y_true]
    idx = [CLASS_IDS.index(c) for c in present]
    scores = {"model": title, "accuracy": acc, "macro_precision": p[idx].mean(),
              "macro_recall": r[idx].mean(), "macro_f1": f[idx].mean()}

    print(f"=== {title} ===")
    print(f"Accuracy: {acc:.4f}\n")
    print("class precision  recall     f1  support")
    for i, name in enumerate(CLASS_NAMES):
        note = "" if CLASS_IDS[i] in present else "   (not in test set)"
        print(f"{name:>5} {p[i]:9.3f} {r[i]:7.3f} {f[i]:6.3f} {support[i]:8d}{note}")
    print(f"\nMacro (classes present): precision={scores['macro_precision']:.3f} "
          f"recall={scores['macro_recall']:.3f} f1={scores['macro_f1']:.3f}\n")

    # confusion matrix with each row divided by the number of beats of that class
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_IDS)
    cm = cm / np.maximum(cm.sum(axis=1, keepdims=True), 1)
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ConfusionMatrixDisplay(cm, display_labels=CLASS_NAMES).plot(ax=ax, cmap="Blues", values_format=".2f", colorbar=False)
    ax.set_title(f"{title}\n(rows = true class, normalised)")
    fig.tight_layout()
    fig.savefig(FIG_DIR / save_as, dpi=200)
    return scores


def one_hot(y, classes):
    return (y[:, None] == classes[None, :]).astype(float)


def perturb_slice(X, j, mode, rng):
    # returns a copy of X where slice j (0-based) is destroyed
    s, e = j * SLICE_LENGTH, (j + 1) * SLICE_LENGTH
    Xp = X.copy()
    if mode == "shuffle":      # shuffle the points inside the slice (main method)
        Xp[:, s:e] = rng.permuted(X[:, s:e], axis=1)
    elif mode == "permute":    # take the slice from another random beat
        Xp[:, s:e] = X[rng.permutation(len(X)), s:e]
    elif mode == "zero":
        Xp[:, s:e] = 0.0
    elif mode == "mean":
        Xp[:, s:e] = X[:, s:e].mean(axis=1, keepdims=True)
    return Xp


def compute_permfit_ecg(model, X, y, modes=("shuffle",), n_splits=5):
    """PermFIT: importance of each slice, with stratified K-fold cross-fitting."""
    folds = StratifiedKFold(n_splits=n_splits, shuffle=True, random_state=SEED)
    rng = np.random.default_rng(SEED)

    M = {m: np.zeros((len(X), N_SLICES)) for m in modes}          # importance of slice j for beat i
    per_fold = {m: np.zeros((n_splits, N_SLICES)) for m in modes}
    correct = {m: np.zeros((len(X), N_SLICES), dtype=bool) for m in modes}
    base_correct = np.zeros(len(X), dtype=bool)
    base_acc, base_err = [], []

    for k, (train, test) in enumerate(folds.split(X, y)):
        fold_model = clone(model).fit(X[train], y[train])
        classes = fold_model.classes_
        Y = one_hot(y[test], classes)

        # squared error on the intact beats
        p = fold_model.predict_proba(X[test])
        err = ((Y - p) ** 2).sum(axis=1)
        base_correct[test] = classes[p.argmax(1)] == y[test]
        base_acc.append(base_correct[test].mean())
        base_err.append(err.mean())
        print(f"  fold {k + 1}/{n_splits}: train {len(train)}, test {len(test)}, accuracy {base_acc[-1]:.3f}", flush=True)

        # destroy each slice: importance = error after - error before
        for m in modes:
            for j in range(N_SLICES):
                p_perm = fold_model.predict_proba(perturb_slice(X[test], j, m, rng))
                M[m][test, j] = ((Y - p_perm) ** 2).sum(axis=1) - err
                per_fold[m][k, j] = M[m][test, j].mean()
                correct[m][test, j] = classes[p_perm.argmax(1)] == y[test]

    results = {"baseline": {"accuracy": np.array(base_acc), "sq_error": np.array(base_err)}}
    for m in modes:
        results[m] = {"mean": M[m].mean(axis=0), "per_fold": per_fold[m], "M": M[m],
                      "acc_drop": 100 * (base_correct.mean() - correct[m].mean(axis=0))}
    return results


def plot_permfit_importance(importance, per_fold, title, ax):
    colors = {"PR interval": "royalblue", "QRS complex": "crimson", "ST segment / T-wave": "darkgreen"}
    for label, a, b in SLICE_REGIONS:
        ax.axvspan(a - 0.5, b + 0.5, color=colors[label], alpha=0.12, label=f"{label} (slices {a}-{b})")
    slices = np.arange(1, N_SLICES + 1)
    # error bars = spread of the importance over the folds
    ax.bar(slices, importance, yerr=per_fold.std(axis=0), capsize=3, color="navy", width=0.6, zorder=3)
    ax.axhline(0, color="grey", lw=0.8)
    ax.set_xticks(slices)
    ax.set_xlabel("ECG slice (25 samples each; R-peak in slice 6)")
    ax.set_ylabel(r"mean importance $\bar{M}_j$")
    ax.set_title(title)
    ax.grid(axis="y", ls=":", alpha=0.6, zorder=0)
