'''Containing reusable database functions.'''

import sqlite3
# from datetime import datetime


class create_tables():
    def get_connection(self, db_name):
        return sqlite3.connect(db_name)

    def create_customer_db(self):
        with self.get_connection("users.db") as conn:
            c = conn.cursor()
            c.execute(
                '''CREATE TABLE IF NOT EXISTS customers (
                    customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT UNIQUE NOT NULL,
                    account_stat TEXT NOT NULL,
                    current_plan TEXT,
                    balance REAL DEFAULT 0.0)
                    '''
            )
            # Dummy data for customers
            customers = [
                ("Alice wonderland", "alice.wonderland@bla.com", "+12345678901", "active","prepaid", 50.75),
                ("Jefferson smith", "Jefferson.smith@bla.com", "+12345678902", "active","prepaid", 12.00),
                ("Carol mark", "carol.mark@bla.com", "+12345678903", "suspended","No plan", 0.00),
                ("David", "david.lee@bla.com", "+12345678904", "active", "postpaid", 30.50),
                ("Eve Brown", "eve.brown@bla.com", "+12345678905", "active", "postpaid", 15.20),
            ]
            
            # Inserting all dummy data
            c.executemany('''
                INSERT INTO customers (name, email, phone, account_stat, current_plan, balance)
                    Values (?,?,?,?,?,?)''',customers)
            
            conn.commit()

    def create_conversation_log_db(self):
        with self.get_connection("convo_log.db") as conn:
            c = conn.cursor()

            c.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                    message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    timestamp TEXT NOT NULL,
                    sender TEXT NOT NULL CHECK(sender IN ('user','assistant')),
                    message TEXT NOT NULL,
                    agent TEXT,
                    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
                    )
                    ''')
            conn.commit()

    def create_tickets_db(self):
        with self.get_connection("customer_tickets.db") as conn:
            c = conn.cursor()

            c.execute('''
                    CREATE TABLE IF NOT EXISTS tickets (
                    ticket_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    customer_id INTEGER NOT NULL,
                    created_at INTEGER NOT NULL,
                    ticket_message TEXT NOT NULL,
                    status TEXT NOT NULL CHECK(status IN ('OPEN', 'CLOSE', 'ON HOLD')),
                    FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
                    )
                    ''')
            conn.commit()
    
    def __init__(self):
        self.create_conversation_log_db()
        self.create_tickets_db()
        self.create_customer_db()