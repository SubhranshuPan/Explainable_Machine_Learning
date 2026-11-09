import numpy as np
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score,
    f1_score, confusion_matrix
)

# read beat holdout data
train = np.loadtxt("./train_beats.csv", delimiter=",")
test = np.loadtxt("./test_beats.csv", delimiter=",")

X_train, y_train = train[:, :275], train[:, 275].astype(int)
X_test, y_test = test[:, :275], test[:, 275].astype(int)

def evaluate_model(model, X_test, y_test):
    y_pred = model.predict(X_test)
    labels = [1, 2, 3, 4, 5, 6, 7, 8]

    results = {
        "accuracy": accuracy_score(y_test, y_pred),
        "precision_macro": precision_score(
            y_test, y_pred, labels=labels, average="macro", zero_division=0
        ),
        "recall_macro": recall_score(
            y_test, y_pred, labels=labels, average="macro", zero_division=0
        ),
        "f1_macro": f1_score(
            y_test, y_pred, labels=labels, average="macro", zero_division=0
        ),
        "confusion_matrix": confusion_matrix(
            y_test, y_pred, labels=labels
        )
    }

    print("Accuracy:", results["accuracy"])
    print("Precision (macro):", results["precision_macro"])
    print("Recall (macro):", results["recall_macro"])
    print("F1 score (macro):", results["f1_macro"])
    print("Confusion matrix:")
    print(results["confusion_matrix"])

    return results

# training
svm = SVC(kernel="rbf")
svm.fit(X_train, y_train)
results = evaluate_model(svm, X_test, y_test)