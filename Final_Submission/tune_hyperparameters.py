"""Choose the Random Forest settings for Task 5 (recorded in ecg_utils.make_model).

Grid search with 3-fold stratified cross-validation on an 8,000-beat random subset
of the beat hold-out training data. The test sets are never used for tuning.
Scoring = macro F1, so every arrhythmia class counts equally.

The SVM grid over C is included for reference only: Tasks 2 and 3 keep their own
SVM settings (default C=1), and Task 4 explains exactly those models.
"""
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, StratifiedKFold, train_test_split
from sklearn.svm import SVC

from ecg_utils import RESULTS_DIR, SEED, load_split

X, y, _, _ = load_split("beats")
X_tune, _, y_tune, _ = train_test_split(X, y, train_size=8000, stratify=y, random_state=SEED)
cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=SEED)

searches = {
    "SVM": GridSearchCV(SVC(kernel="rbf", gamma="scale"), {"C": [1, 10, 100]},
                        cv=cv, scoring="f1_macro", n_jobs=-1),
    "Random Forest": GridSearchCV(RandomForestClassifier(n_estimators=200, random_state=SEED),
                                  {"max_features": ["sqrt", 0.1], "min_samples_leaf": [1, 3]},
                                  cv=cv, scoring="f1_macro", n_jobs=-1),
}
rows = []
for name, search in searches.items():
    search.fit(X_tune, y_tune)
    print(f"{name}: best {search.best_params_}  CV macro-F1 = {search.best_score_:.3f}")
    for params, mean, std in zip(search.cv_results_["params"], search.cv_results_["mean_test_score"],
                                 search.cv_results_["std_test_score"]):
        rows.append({"model": name, "params": str(params), "cv_macro_f1": round(mean, 3), "std": round(std, 3)})

pd.DataFrame(rows).to_csv(RESULTS_DIR / "tuning_results.csv", index=False)
