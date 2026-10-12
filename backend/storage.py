import sqlite3
import json
from datetime import datetime

DB_PATH = "history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    # 按session_id隔离用户记录
    cur.execute('''
    CREATE TABLE IF NOT EXISTS records (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        content TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    ''')
    cur.execute('CREATE INDEX IF NOT EXISTS idx_session ON records(session_id)')
    conn.commit()
    conn.close()

def save_record(session_id: str, record: dict):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO records(session_id, content, created_at) VALUES (?, ?, ?)",
        (session_id, json.dumps(record, ensure_ascii=False), record["created_at"])
    )
    conn.commit()
    conn.close()

def get_history(session_id: str, limit: int):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute('''
        SELECT content FROM records
        WHERE session_id = ?
        ORDER BY created_at DESC
        LIMIT ?
    ''', (session_id, limit))
    rows = cur.fetchall()
    conn.close()
    # 把json字符串转回字典数组返回给接口
    return [json.loads(row[0]) for row in rows]
