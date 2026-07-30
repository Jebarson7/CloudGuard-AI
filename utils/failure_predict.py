import joblib

model = joblib.load("failure_model.pkl")

def predict_failure(cpu, memory, network, disk, health_score):

    probability = model.predict_proba([[
        cpu,
        memory,
        network,
        disk,
        health_score
    ]])[0][1]

    return probability * 100