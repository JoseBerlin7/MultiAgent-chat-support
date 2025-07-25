'''Purpose: custom logging logic for console + file logs'''
import sqlite3
from datetime import datetime

class message_logger:
    def get_connection(self):
        return sqlite3.connect("convo_log.db")
    async def log_message(self, customer_id, sender, message, agent=""):
        with self.get_connection() as conn:
            c = conn.cursor()
            timestamp = datetime.now().isoformat()
            c.execute(
                'INSERT INTO conversations (customer_id, timestamp, sender, message, agent) VALUES (?, ?, ?, ?, ?)',
                (customer_id, timestamp, sender, message, agent)
            )
            conn.commit()

    def get_last_chat(self, customer_id, num_chat):
        with self.get_connection() as conn:
            c = conn.cursor()
            c.execute(f"SELECT sender, message FROM conversations WHERE customer_id={customer_id} ORDER BY timestamp DESC LIMIT {num_chat}")

            messages = c.fetchall()
            return messages[::-1]
            