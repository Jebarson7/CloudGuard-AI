import joblib

model = joblib.load("models/anomaly_model.pkl")

def detect_anomaly(cpu, memory, network, disk, health_score):

    result = model.predict([[
        cpu,
        memory,
        network,
        disk,
        health_score
    ]])

    return result[0]