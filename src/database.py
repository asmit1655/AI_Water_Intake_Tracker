import sqlite3
from datetime import datetime

DB_name="water_tracker.db"

def create_table():
    conn=sqlite3.connect(DB_name)
    cursor=conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS water_tracker (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, intake_ml INTEGER, user_id TEXT)")
    conn.commit()
    conn.close()
    
def log_intake(user_id,intake_ml):
    conn=sqlite3.connect(DB_name)
    cursor=conn.cursor()
    date_today=datetime.today().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO water_tracker (user_id, intake_ml, date) VALUES (?, ?, ?)", (user_id,intake_ml,date_today))
    conn.commit()
    conn.close()
    
def get_intake_history(user_id):
    conn=sqlite3.connect(DB_name)
    cursor=conn.cursor()
    print(f"Querying for user_id: {user_id}")
    
    cursor.execute("PRAGMA table_info(water_tracker)")
    columns = cursor.fetchall()
    for col in columns:
        print(col)

    
    cursor.execute("SELECT * FROM water_tracker")
    all_data = cursor.fetchall()
    print("All data:", all_data)
    user_id = user_id.lower().strip()
    cursor.execute("SELECT intake_ml, date FROM water_tracker WHERE user_id = ?", (user_id,))
    history = cursor.fetchall()
    print("Filtered history:", history)
    conn.close()
    return history

create_table()