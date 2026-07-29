import random
from database import insert_metrics

# Generate 500 realistic historical records
for _ in range(500):

    cpu = round(random.uniform(20, 95), 2)
    memory = round(random.uniform(30, 90), 2)
    network = round(random.uniform(10, 500), 2)
    disk = round(random.uniform(20, 80), 2)

    network_score = min(network / 5, 100)

    health_score = max(
        0,
        min(
            100,
            int(
                100 - (
                    cpu * 0.4 +
                    memory * 0.4 +
                    network_score * 0.2
                )
            )
        )
    )

    insert_metrics(
        cpu,
        memory,
        network,
        disk,
        health_score
    )

print("✅ 500 sample records inserted successfully!")