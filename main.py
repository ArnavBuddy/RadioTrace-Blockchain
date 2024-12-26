from tkinter import Tk
from blockchain import Blockchain
from blockchain_db import BlockchainDatabase
from radio_trace_gui import RadioTraceGUI

def main():
    # Initialize SQLite database
    db = BlockchainDatabase()

    # Initialize Blockchain
    blockchain = Blockchain(db)

    # Initialize and run the GUI
    root = Tk()
    app = RadioTraceGUI(root)
    app.db = db        # Pass database reference to GUI
    app.blockchain = blockchain  # Pass blockchain reference to GUI
    root.mainloop()

if __name__ == "__main__":
    main()
