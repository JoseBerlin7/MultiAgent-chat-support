'''Purpose: Defining DB tables'''
import sqlite3
from datetime import datetime

class DB_schemas():
    def __init__(self, db_path = "users.db"):
        self.db_path = db_path

    def get_connection(self, database_path = "users.db"):
        return sqlite3.connect(database_path)

    def get_customer_data(self, customer_id=""):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(f"SELECT * FROM customers WHERE customer_id = '{customer_id}'")
            row = c.fetchone()
            return dict(row) if row else None
        
    def get_customer_id(self, phone=""):
        with self.get_connection() as conn:
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute(f"SELECT customer_id FROM customers WHERE phone = '{phone}'")
            row = c.fetchone()
            return dict(row) if row else None
    
    def update_customer(self, phone, **fields):
        if not fields:
            raise ValueError("No fields specified for update.")
        set_clause = ", ".join([f"{field}=?" for field in fields])
        values = list(fields.values())
        values.append(phone)
        with self.get_conn() as conn:
            cur = conn.cursor()
            cur.execute(f"UPDATE customers SET {set_clause} WHERE phone = '{phone}'")
            conn.commit()
            return cur.rowcount > 0
        
    def log_conversation(self, customer_id, sender, message, agent_name):
        with self.get_connection("conversations.db") as conn:
            c = conn.cursor()
            timestamp = datetime.utcnow().isoformat()
            c.execute('''
                INSERT INTO conversations (customer_id, timestamp, sender, message, agent)
                    VALUES (?,?,?,?,?)
                    ''', (customer_id, timestamp, sender, message, agent_name))
            conn.commit()
            return c.lastrowid
    
    def add_ticket(self, customer_id, message="",status="OPEN"):
        now = datetime.utcnow().isoformat()
        with self.get_connection('customer_tickets.db') as conn:
            c =  conn.cursor()
            c.execute('''INSERT INTO tickets (customer_id,created_at,ticket_message,status) 
                      VALUES (?,?,?,?)''', (customer_id,now,message,status))
            conn.commit()
            return c.lastrowid
        
    def delete_all(self,database_name, table_name, customer_id=""):
        with self.get_connection(database_name) as conn:
            c = conn.cursor()
            if customer_id =="":
                c.execute(f"DELETE FROM {table_name}")
            else:
                c.execute(f"DELETE FROM {table_name} WHERE customer_id = {customer_id}")
            conn.commit

# c = DB_schemas()
# print(c.get_customer_data(phone="+12345678905"))

   
        
