import tkinter as tk
from tkinter import ttk, messagebox
from blockchain import Blockchain  # Import Blockchain class
from blockchain_db import BlockchainDatabase  # Import BlockchainDatabase class

class RadioTraceGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("RadioTrace Blockchain System")

        # Initialize Database and Blockchain
        self.db = BlockchainDatabase()
        self.blockchain = Blockchain(self.db)

        # Home Frame
        self.home_frame = tk.Frame(root)
        self.home_frame.pack(fill="both", expand=True)

        tk.Label(self.home_frame, text="RadioTrace System", font=("Arial", 20)).pack(pady=10)
        ttk.Button(self.home_frame, text="Add New Source", command=self.open_add_source).pack(pady=5)
        ttk.Button(self.home_frame, text="Mine Transactions", command=self.mine_transactions).pack(pady=5)
        ttk.Button(self.home_frame, text="View Blockchain", command=self.open_view_blockchain).pack(pady=5)

    def open_add_source(self):
        self.home_frame.pack_forget()
        add_source_frame = tk.Frame(self.root)
        add_source_frame.pack(fill="both", expand=True)

        tk.Label(add_source_frame, text="Add New Source", font=("Arial", 18)).pack(pady=10)

        tk.Label(add_source_frame, text="Source ID").pack()
        source_id_entry = ttk.Entry(add_source_frame)
        source_id_entry.pack()

        tk.Label(add_source_frame, text="Activity").pack()
        activity_entry = ttk.Entry(add_source_frame)
        activity_entry.pack()

        tk.Label(add_source_frame, text="Location").pack()
        location_entry = ttk.Entry(add_source_frame)
        location_entry.pack()

        def submit():
            source_id = source_id_entry.get()
            activity = activity_entry.get()
            location = location_entry.get()
            transaction = {"source_id": source_id, "activity": activity, "location": location}
            self.blockchain.add_transaction(transaction)
            tk.Label(add_source_frame, text="Transaction Added!", fg="green").pack()

        ttk.Button(add_source_frame, text="Submit", command=submit).pack(pady=5)
        ttk.Button(add_source_frame, text="Back", command=lambda: self.back_to_home(add_source_frame)).pack(pady=5)

    def mine_transactions(self):
        message = self.blockchain.mine_pending_transactions()
        messagebox.showinfo("Mining Result", message)

    def open_view_blockchain(self):
        self.home_frame.pack_forget()
        view_frame = tk.Frame(self.root)
        view_frame.pack(fill="both", expand=True)

        tk.Label(view_frame, text="Blockchain Viewer", font=("Arial", 18)).pack(pady=10)

        for block in self.blockchain.chain:
            block_info = f"Block {block.index}:\nHash: {block.hash}\nTransactions: {block.transactions}\n"
            tk.Label(view_frame, text=block_info, justify="left", wraplength=600).pack()

        ttk.Button(view_frame, text="Back", command=lambda: self.back_to_home(view_frame)).pack(pady=5)

    def back_to_home(self, frame):
        frame.pack_forget()
        self.home_frame.pack(fill="both", expand=True)
