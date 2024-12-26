import time
import json
from blockchain_db import BlockchainDatabase

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        import hashlib
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty):
        while not self.hash.startswith('0' * difficulty):
            self.nonce += 1
            self.hash = self.compute_hash()

class Blockchain:
    def __init__(self, db: BlockchainDatabase):
        self.db = db
        self.chain = []
        self.difficulty = 2
        self.pending_transactions = self.db.get_pending_transactions()
        self.load_blocks_from_db()

    def create_genesis_block(self):
        genesis_block = Block(0, time.time(), "Genesis Block", "0")
        self.db.add_block(genesis_block)
        self.chain.append(genesis_block)

    def load_blocks_from_db(self):
        rows = self.db.get_all_blocks()
        if not rows:
            self.create_genesis_block()
        else:
            for row in rows:
                block = Block(
                    index=row[0],
                    timestamp=row[1],
                    transactions=json.loads(row[2]),
                    previous_hash=row[3]
                )
                block.hash = row[4]
                block.nonce = row[5]
                self.chain.append(block)

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        self.db.add_pending_transaction(transaction)

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return "No transactions to mine!"

        new_block = Block(
            index=len(self.chain),
            timestamp=time.time(),
            transactions=self.pending_transactions,
            previous_hash=self.chain[-1].hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.db.add_block(new_block)
        self.pending_transactions = []
        self.db.clear_pending_transactions()
        return f"Block {new_block.index} mined successfully!"
