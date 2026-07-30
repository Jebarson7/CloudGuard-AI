import sqlite3

conn = sqlite3.connect("real_metrics.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS metrics(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    cpu REAL,
    memory REAL,
    network REAL,
    disk REAL,
    health_score REAL
)
""")

conn.commit()
conn.close()


def insert_real_metrics(cpu, memory, network, disk, health_score):

    conn = sqlite3.connect("real_metrics.db")

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO metrics(
        cpu,
        memory,
        network,
        disk,
        health_score
    )
    VALUES(?,?,?,?,?)
    """, (
        cpu,
        memory,
        network,
        disk,
        health_score
    ))

    conn.commit()
    conn.close()