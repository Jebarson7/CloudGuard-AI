from database import insert_metrics

def save_metrics(metrics, health_score):
    insert_metrics(
        cpu=metrics["cpu"],
        memory=metrics["memory"],
        network=metrics["network"],
        disk=metrics.get("disk", 0),
        health_score=health_score
    )