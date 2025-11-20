import sqlite3
from datetime import datetime

class OrderHistory:

    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName
        self.create_table()

    # database setup
    def connect(self):
        return sqlite3.connect(self.databaseName)

    def create_table(self):
        """Create the orders table if it does not exist."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    #save order
    def saveOrder(self, user_id, cart_items, total_cost):
        """
        Saves a completed order:
        cart_items: {"ISBN123": qty, "ISBN999": qty}
        total_cost: float
        """
        connection = self.connect()
        cursor = connection.cursor()

        items_string = ", ".join([f"{item} (x{qty})"
                                  for item, qty in cart_items.items()])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO orders (user_id, items, total, date)
            VALUES (?, ?, ?, ?)
        """, (user_id, items_string, total_cost, timestamp))

        connection.commit()
        connection.close()

        print("\nOrder saved to history!")

    #view order history
    def viewHistory(self, user_id):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT order_id, items, total, date
            FROM orders
            WHERE user_id = ?
            ORDER BY date DESC
        """, (user_id,))

        orders = cursor.fetchall()
        connection.close()

        if not orders:
            print("\nNo order history found.")
            return

        print("\n--- Order History ---")
        for order in orders:
            print(f"\nOrder ID: {order[0]}")
            print(f"Date: {order[3]}")
            print(f"Total: ${order[2]:.2f}")
            print(f"Items: {order[1]}")
            print("-" * 40)

    # view a single order
    def viewOrder(self, user_id):
        order_id = input("Enter Order ID to view: ")

        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT order_id, items, total, date
            FROM orders
            WHERE user_id = ? AND order_id = ?
        """, (user_id, order_id))

        order = cursor.fetchone()
        connection.close()

        if order is None:
            print("\nOrder not found.")
            return

        print("\n--- Order Details ---")
        print(f"Order ID: {order[0]}")
        print(f"Date: {order[3]}")
        print(f"Total: ${order[2]:.2f}")
        print(f"Items: {order[1]}")
        print("-" * 40)

