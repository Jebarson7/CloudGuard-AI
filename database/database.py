import sqlite3

def create_database():
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS metrics (
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


# 👇 Add this line here
create_database()


def insert_metrics(cpu, memory, network, disk, health_score):
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO metrics (cpu, memory, network, disk, health_score)
    VALUES (?, ?, ?, ?, ?)
    """, (cpu, memory, network, disk, health_score))

    conn.commit()
    conn.close()