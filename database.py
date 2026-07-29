import sqlite3

# Create the database and table
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

# Function to insert metrics
def insert_metrics(cpu, memory, network, disk, health_score):
    conn = sqlite3.connect("metrics.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO metrics (cpu, memory, network, disk, health_score)
    VALUES (?, ?, ?, ?, ?)
    """, (cpu, memory, network, disk, health_score))

    conn.commit()
    conn.close()

# Main Program
if __name__ == "__main__":
    create_database()

    # Insert one sample record
    insert_metrics(
        cpu=45,
        memory=60,
        network=120,
        disk=35,
        health_score=88
    )

    print("Database created and sample data inserted successfully!")