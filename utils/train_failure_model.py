import sqlite3
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestClassifier

# Read data
conn = sqlite3.connect("metrics.db")
df = pd.read_sql_query("SELECT * FROM metrics", conn)
conn.close()

# Create failure labels
df["failure"] = (
    (df["cpu"] > 85) |
    (df["memory"] > 90) |
    (df["health_score"] < 30)
).astype(int)

X = df[["cpu", "memory", "network", "disk", "health_score"]]
y = df["failure"]

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "failure_model.pkl")

print("Failure Prediction Model Created!")