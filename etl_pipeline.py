import pandas as pd
import sqlite3

# 1. Load raw customer logs & clean missing values
df = pd.read_csv("data/customer_logs.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

# 2. Load into SQLite database and query features via SQL
conn = sqlite3.connect("retainpulse.db")
df.to_sql("customers", conn, if_exists="replace", index=False)

query = """
SELECT 
    customerID,
    tenure AS months_active,
    MonthlyCharges AS monthly_spend,
    TotalCharges AS lifetime_value,
    Contract,
    PaymentMethod,
    InternetService,
    CASE WHEN Churn = 'Yes' THEN 1 ELSE 0 END AS churn_label
FROM customers
WHERE tenure > 0
"""
clean_df = pd.read_sql_query(query, conn)
clean_df.to_csv("data/cleaned_features.csv", index=False)
print("Saved cleaned_features.csv! Total rows:", len(clean_df))