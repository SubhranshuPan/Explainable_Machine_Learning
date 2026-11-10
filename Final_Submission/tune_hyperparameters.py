"""Grid search for the Random Forest settings used in Task 5.

3-fold cross-validation on 8,000 training beats (beat hold-out), scored with macro F1.
The SVM grid is only for reference: Tasks 2 and 3 keep their own SVM settings (C = 1).
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
    "SVM": GridSearchCV(SVC(kernel="rbf"), {"C": [1, 10, 100]}, cv=cv, scoring="f1_macro", n_jobs=-1),
    "Random Forest": GridSearchCV(RandomForestClassifier(n_estimators=200, random_state=SEED),
                                  {"max_features": ["sqrt", 0.1], "min_samples_leaf": [1, 3]},
                                  cv=cv, scoring="f1_macro", n_jobs=-1),
}

rows = []
for name, search in searches.items():
    search.fit(X_tune, y_tune)
    print(f"{name}: best {search.best_params_}  CV macro-F1 = {search.best_score_:.3f}")
    results = search.cv_results_
    for params, mean, std in zip(results["params"], results["mean_test_score"], results["std_test_score"]):
        rows.append({"model": name, "params": str(params), "cv_macro_f1": round(mean, 3), "std": round(std, 3)})

pd.DataFrame(rows).to_csv(RESULTS_DIR / "tuning_results.csv", index=False)
