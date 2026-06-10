import sqlite3
import json
import os
from datetime import datetime

DB_PATH = "auditx.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            industry TEXT,
            created_at TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS audits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            client_name TEXT,
            overall_score INTEGER,
            risk_level TEXT,
            frameworks TEXT,
            report_path TEXT,
            pdf_path TEXT,
            word_path TEXT,
            created_at TEXT,
            FOREIGN KEY (client_id) REFERENCES clients(id)
        )
    ''')
    conn.commit()
    conn.close()

def save_audit(client_name, overall_score, risk_level, frameworks, report_path, pdf_path, word_path):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    c.execute('''
        INSERT INTO audits (client_name, overall_score, risk_level, frameworks, report_path, pdf_path, word_path, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (client_name, overall_score, risk_level, json.dumps(frameworks), report_path, pdf_path, word_path, now))
    conn.commit()
    conn.close()

def get_all_audits():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM audits ORDER BY created_at DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def get_client_audits(client_name):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT * FROM audits WHERE client_name = ? ORDER BY created_at DESC', (client_name,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_audit_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT COUNT(*) FROM audits')
    total = c.fetchone()[0]
    c.execute('SELECT COUNT(DISTINCT client_name) FROM audits')
    clients = c.fetchone()[0]
    c.execute('SELECT AVG(overall_score) FROM audits')
    avg_score = c.fetchone()[0]
    conn.close()
    return {
        "total_audits": total,
        "total_clients": clients,
        "avg_score": round(avg_score, 1) if avg_score else 0
    }

init_db()
