import sqlite3
import json

class BlockchainDatabase:
    def __init__(self, db_name="blockchain.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Create blocks table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS blocks (
                "index" INTEGER PRIMARY KEY,
                timestamp TEXT,
                transactions TEXT,
                previous_hash TEXT,
                hash TEXT,
                nonce INTEGER
            )
        """)
        # Create pending transactions table with "transaction" fixed
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS pending_transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                "transaction" TEXT
            )
        """)
        self.conn.commit()

    def add_block(self, block):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO blocks ("index", timestamp, transactions, previous_hash, hash, nonce)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            block.index,
            block.timestamp,
            json.dumps(block.transactions),
            block.previous_hash,
            block.hash,
            block.nonce
        ))
        self.conn.commit()

    def get_all_blocks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM blocks")
        rows = cursor.fetchall()
        return rows

    def add_pending_transaction(self, transaction):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO pending_transactions ("transaction") VALUES (?)
        """, (json.dumps(transaction),))
        self.conn.commit()

    def get_pending_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM pending_transactions")
        rows = cursor.fetchall()
        return [json.loads(row[1]) for row in rows]

    def clear_pending_transactions(self):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM pending_transactions")
        self.conn.commit()
