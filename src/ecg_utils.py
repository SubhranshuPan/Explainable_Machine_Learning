"""Shared helpers for the ECG arrhythmia case study.

Every CSV row produced by the notebooks has 277 columns:
    columns 0..274  -> one standardised heartbeat (275 samples, R-peak in the middle)
    column  275     -> class ID (1..8, see CLASS_NAMES)
    column  276     -> MIT-BIH record (patient) number
"""
from pathlib import Path

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import (accuracy_score, confusion_matrix,
                             precision_recall_fscore_support, ConfusionMatrixDisplay)

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
FIG_DIR = ROOT / "figures"

BEAT_LENGTH = 275
# Class IDs 1..8 as defined in the case study
CLASS_IDS = [1, 2, 3, 4, 5, 6, 7, 8]
CLASS_NAMES = ["N", "L", "R", "V", "A", "F", "f", "/"]


def load_split(name):
    """Load one of the CSVs made by data_split_resample.ipynb.

    name: 'beats' or 'patients'.
    Returns X_train, y_train, X_test, y_test (y = class IDs 1..8).
    """
    out = []
    for part in ("train", "test"):
        arr = np.loadtxt(DATA_DIR / f"{part}_{name}.csv", delimiter=",")
        out += [arr[:, :BEAT_LENGTH], arr[:, BEAT_LENGTH].astype(int)]
    return tuple(out)


def one_hot(y):
    """One-hot encode class IDs 1..8 -> array of shape (n, 8)."""
    return (np.asarray(y)[:, None] == np.array(CLASS_IDS)[None, :]).astype(float)


def evaluate(y_true, y_pred, title="", save_as=None):
    """Print accuracy, per-class and macro precision/recall/F1, and plot a confusion matrix.

    Classes that never appear in y_true (e.g. L, R, A for the held-out patients)
    are left out of the macro average, because their recall is undefined.
    Returns a dict with the headline numbers so results can be put in a table.
    """
    present = [c for c in CLASS_IDS if c in set(np.asarray(y_true))]
    acc = accuracy_score(y_true, y_pred)
    p, r, f, support = precision_recall_fscore_support(
        y_true, y_pred, labels=CLASS_IDS, zero_division=0)

    print(f"=== {title} ===")
    print(f"Accuracy: {acc:.4f}\n")
    print(f"{'class':>5} {'precision':>9} {'recall':>7} {'f1':>6} {'support':>8}")
    for name, cid, pi, ri, fi, si in zip(CLASS_NAMES, CLASS_IDS, p, r, f, support):
        flag = "" if cid in present else "   (not in test set)"
        print(f"{name:>5} {pi:9.3f} {ri:7.3f} {fi:6.3f} {si:8d}{flag}")

    idx = [CLASS_IDS.index(c) for c in present]
    macro = dict(precision=p[idx].mean(), recall=r[idx].mean(), f1=f[idx].mean())
    _, _, weighted_f1, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=present, average="weighted", zero_division=0)
    print(f"\nMacro (over classes present): precision={macro['precision']:.3f} "
          f"recall={macro['recall']:.3f} f1={macro['f1']:.3f} | weighted f1={weighted_f1:.3f}")

    # Row-normalised confusion matrix: each row shows where the beats of one true class went
    cm = confusion_matrix(y_true, y_pred, labels=CLASS_IDS)
    with np.errstate(invalid="ignore", divide="ignore"):
        cm_norm = np.nan_to_num(cm / cm.sum(axis=1, keepdims=True))
    fig, ax = plt.subplots(figsize=(6.5, 5.5))
    ConfusionMatrixDisplay(cm_norm, display_labels=CLASS_NAMES).plot(
        ax=ax, cmap="Blues", values_format=".2f", colorbar=False)
    ax.set_title(f"{title}\n(rows = true class, normalised)")
    fig.tight_layout()
    if save_as:
        FIG_DIR.mkdir(exist_ok=True)
        fig.savefig(FIG_DIR / save_as, dpi=200)
    plt.show()

    return dict(model=title, accuracy=acc, macro_precision=macro["precision"],
                macro_recall=macro["recall"], macro_f1=macro["f1"], weighted_f1=weighted_f1,
                confusion_matrix=cm)
