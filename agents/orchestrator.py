from agents.monitoring_agent import collect_metrics
from agents.anomaly_agent import detect_anomaly
from agents.diagnosis_agent import diagnose
from agents.planning_agent import generate_plan
from agents.reasoning_agent import analyze
from agents.memory_agent import save_incident, find_similar
from agents.parser_agent import extract_root_cause
from agents.approval_agent import request_approval
from agents.action_agent import execute_action
from agents.report_agent import generate_report
from agents.predictive_agent import predict_failure

def run_workflow():

    metrics = collect_metrics()

    cpu = metrics["cpu"]
    memory = metrics["memory"]
    network = metrics["network"]
    risk = metrics["risk"]

    anomaly = detect_anomaly(metrics)

    prediction = predict_failure(metrics)

    reasoning = analyze(metrics)

    scenario = reasoning["scenario"]

    history = find_similar(scenario)

    diagnosis = diagnose(metrics)

    plan = generate_plan(
        metrics,
        scenario
    )

    root_cause = extract_root_cause(scenario)

    approval = request_approval(risk)

    action = execute_action(
        scenario,
        approval
    )

    workflow = {
        "metrics": metrics,
        "reasoning": reasoning,
        "root_cause": root_cause,
        "plan": plan,
        "action": action
    }

    report = generate_report(workflow)

    save_incident(
        cpu,
        memory,
        network,
        risk,
        scenario,
        root_cause,
        plan,
        action["action"],
        action["status"]
    )

    return {
        "metrics": metrics,
        "anomaly": anomaly,
        "prediction": prediction,
        "reasoning": reasoning,
        "history": history,
        "root_cause": root_cause,
        "diagnosis": diagnosis,
        "plan": plan,
        "approval": approval,
        "action": action,
        "report": report
    }

if __name__ == "__main__":

    workflow = run_workflow()

    print(workflow)