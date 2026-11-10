import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
    ConfusionMatrixDisplay
)

# Load patient datasets
train_data = pd.read_csv('train_patients.csv', header=None)
test_data = pd.read_csv('test_patients.csv', header=None)

# Extract ECG features
X_train = train_data.iloc[:, :-2].values
X_test = test_data.iloc[:, :-2].values

# Extract class labels
y_train = train_data.iloc[:, -2].values
y_test = test_data.iloc[:, -2].values

# Extract patient IDs (only for checking)
patient_train = train_data.iloc[:, -1].values
patient_test = test_data.iloc[:, -1].values

# Create SVM model
model = make_pipeline(
    StandardScaler(),
    SVC(max_iter=10000, random_state=42)
)

# Train SVM model
model.fit(X_train, y_train)
y_pred = model.predict(X_test)

# Define evaluation function
def evaluate_model(y_test, y_pred):
    accuracy = accuracy_score(y_test, y_pred)

    precision = precision_score(
        y_test, y_pred,
        average='macro',
        zero_division=0
    )

    recall = recall_score(
        y_test, y_pred,
        average='macro',
        zero_division=0
    )

    f1 = f1_score(
        y_test, y_pred,
        average='macro',
        zero_division=0
    )

    print("Accuracy:", accuracy)
    print("Precision:", precision)
    print("Recall:", recall)
    print("F1-score:", f1)

    cm = confusion_matrix(
        y_test, y_pred,
        labels=[1, 2, 3, 4, 5, 6, 7, 8]
    )

    disp = ConfusionMatrixDisplay(
        confusion_matrix=cm,
        display_labels=['N', 'L', 'R', 'V', 'A', 'F', 'f', '/']
    )

    disp.plot(cmap='Blues')
    plt.title('Patient-holdout Confusion Matrix')
    plt.show()

    return accuracy, precision, recall, f1, cm


results = evaluate_model(y_test, y_pred)
