"""
train_model.py
---------------
Trains a classifier on training_data.csv to predict whether a student
is "At Risk" or "Safe", based on attendance % and marks %.
Saves the trained model to at_risk_model.joblib for the app to use later.
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import joblib

# --- Step A: Load the data ---
data = pd.read_csv("training_data.csv")
X = data[["attendance_pct", "marks_pct"]]   # features (inputs)
y = data["risk_label"]                       # label (what we're predicting)

# --- Step B: Split into training and testing sets ---
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# --- Step C: Train the model ---
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# --- Step D: Evaluate on data it has NEVER seen ---
predictions = model.predict(X_test)
accuracy = accuracy_score(y_test, predictions)

print(f"Accuracy on test set: {accuracy:.2%}")
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, predictions, labels=["Safe", "At Risk"]))
print("\nClassification Report:")
print(classification_report(y_test, predictions))

# --- Step E: Save the trained model to disk ---
joblib.dump(model, "at_risk_model.joblib")
print("\nModel saved to at_risk_model.joblib")