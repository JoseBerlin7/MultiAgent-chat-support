'''Containing reusable database functions.'''

import sqlite3

def init_db():
    conn = sqlite3.connect("chat_log.db")
    c = conn.cursor()
    c.execute(
        '''CREATE TABLE IF NOT EXISTS message_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            message TEXT
            intent TEXT,
            agent TEXT,
            timestamp DATETIME DEFAULT CURRNET_TIMESTAMP)'''
    )
    conn.commit()
    conn.close()