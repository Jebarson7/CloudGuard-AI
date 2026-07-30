from real_database import insert_real_metrics

def save_real_metrics(metrics, health_score):

    insert_real_metrics(
        metrics["cpu"],
        metrics["memory"],
        metrics["network"],
        metrics.get("disk", 0),
        health_score
    )