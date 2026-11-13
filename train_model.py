import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, accuracy_score

# 1. Load cleaned features
df = pd.read_csv("data/cleaned_features.csv")

X = pd.get_dummies(df.drop(columns=["customerID", "churn_label"]), drop_first=True)
y = df["churn_label"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 2. Train Logistic Regression & Random Forest models
lr = LogisticRegression(max_iter=1000).fit(X_train, y_train)
rf = RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42).fit(X_train, y_train)

# 3. Evaluate & Print Metrics
rf_probs = rf.predict_proba(X_test)[:, 1]
rf_preds = rf.predict(X_test)
print(f"Random Forest Accuracy: {accuracy_score(y_test, rf_preds):.2f}")
print(f"Random Forest ROC-AUC:  {roc_auc_score(y_test, rf_probs):.2f}")

# 4. Score all customers & export for Tableau Dashboard
df["churn_probability"] = rf.predict_proba(X)[:, 1]
df["risk_segment"] = pd.cut(
    df["churn_probability"],
    bins=[0, 0.3, 0.7, 1.0],
    labels=["Low Risk", "Medium Risk", "High Risk"]
)
df.to_csv("data/tableau_churn_output.csv", index=False)
print("Exported data/tableau_churn_output.csv for Tableau!")