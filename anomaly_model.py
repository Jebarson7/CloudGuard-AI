import sqlite3
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

# Read historical data
conn = sqlite3.connect("real_metrics.db")
df = pd.read_sql_query("SELECT * FROM metrics", conn)
conn.close()

# Features used for anomaly detection
X = df[["cpu", "memory", "network", "disk", "health_score"]]

# Train Isolation Forest
model = IsolationForest(
    contamination=0.05,   # About 5% of data is considered unusual
    random_state=42
)

model.fit(X)

joblib.dump(model, "anomaly_model.pkl")

print("Anomaly Detection Model Created!")