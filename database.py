import sqlite3

conn = sqlite3.connect("predictions.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    size INTEGER,
    complexity INTEGER,
    experience INTEGER,
    prediction TEXT,
    risk_score INTEGER
)
""")

conn.commit()
conn.close()

print("Database Created Successfully!")