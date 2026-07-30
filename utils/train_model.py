import sqlite3
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

# Connect to database
conn = sqlite3.connect("metrics.db")

# Read metrics
df = pd.read_sql_query(
    "SELECT * FROM metrics ORDER BY timestamp",
    conn
)

conn.close()

print(f"Total records: {len(df)}")

# Need enough data
if len(df) < 20:
    print("Collect at least 20 records.")
    exit()

# -----------------------------
# Create future target
# -----------------------------

df["future_cpu"] = df["cpu"].shift(-1)

# Remove last row (no future value)
df = df.dropna()

# -----------------------------
# Features
# -----------------------------

X = df[
    [
        "cpu",
        "memory",
        "network",
        "disk",
        "health_score"
    ]
]

# -----------------------------
# Target
# -----------------------------

y = df["future_cpu"]

# -----------------------------
# Train model
# -----------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42
)

model.fit(X, y)

joblib.dump(model, "model.pkl")

print("Future CPU Prediction Model Created!")