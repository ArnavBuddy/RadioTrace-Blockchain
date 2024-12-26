import sqlite3

# Connect to the database
conn = sqlite3.connect("blockchain.db")

# Create a cursor
cursor = conn.cursor()

# Query and print all blocks
cursor.execute("SELECT * FROM blocks")
blocks = cursor.fetchall()
print("Blocks:")
for block in blocks:
    print(block)

# Query and print pending transactions
cursor.execute("SELECT * FROM pending_transactions")
transactions = cursor.fetchall()
print("\nPending Transactions:")
for transaction in transactions:
    print(transaction)

# Close the connection
conn.close()