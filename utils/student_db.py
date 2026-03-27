import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'student_records.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS search_records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT,
            search_time TEXT,
            question TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_record(student_id: str, search_time: str, question: str):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO search_records (student_id, search_time, question)
        VALUES (?, ?, ?)
    ''', (student_id, search_time, question))
    conn.commit()
    conn.close()

def get_most_searched_questions(limit=10):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        SELECT question, COUNT(*) as count 
        FROM search_records 
        GROUP BY question 
        ORDER BY count DESC 
        LIMIT ?
    ''', (limit,))
    results = cursor.fetchall()
    conn.close()
    return results

# Initialize the db when imported
init_db()
