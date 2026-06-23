def predict_risk(cpu, memory, network):

    score = 0

    if cpu > 80:
        score += 40
    elif cpu > 50:
        score += 20

    if memory > 80:
        score += 40
    elif memory > 50:
        score += 20

    if network > 500:
        score += 20

    if score >= 70:
        return "HIGH RISK"
    elif score >= 40:
        return "MEDIUM RISK"
    else:
        return "LOW RISK"