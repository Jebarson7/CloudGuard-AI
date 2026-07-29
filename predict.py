import joblib

model = joblib.load("model.pkl")

def predict_future_cpu(
        cpu,
        memory,
        network,
        disk,
        health_score):

    value = model.predict([[
        cpu,
        memory,
        network,
        disk,
        health_score
    ]])

    return round(float(value[0]), 2)