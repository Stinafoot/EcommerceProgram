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
        """Create orders table if it does not exist."""
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL,
                items TEXT NOT NULL,
                total REAL NOT NULL,
                date TEXT NOT NULL
            )
        """)

        connection.commit()
        connection.close()

    # save order
    def save_order(self, user_name, cart_items, total_cost):
        """
        Save an order to the database.
        cart_items: dict such as {"item_name": quantity}
        total_cost: float
        """

        connection = self.connect()
        cursor = connection.cursor()

        items_string = ", ".join([f"{item} (x{qty})" for item, qty in cart_items.items()])
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        cursor.execute("""
            INSERT INTO orders (user_name, items, total, date)
            VALUES (?, ?, ?, ?)
        """, (user_name, items_string, total_cost, timestamp))

        connection.commit()
        connection.close()

        print("\nOrder successfully saved to history!")

    #view order history
    def view_order_history(self, user_name):
        connection = self.connect()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT order_id, total, items, date
            FROM orders
            WHERE user_name = ?
            ORDER BY date DESC
        """, (user_name,))

        orders = cursor.fetchall()
        connection.close()

        if not orders:
            print(f"\nNo previous orders found for {user_name}.")
        else:
            print(f"\n--- Order History for {user_name} ---")
            for order in orders:
                print(f"\nOrder ID: {order[0]}")
                print(f"Date: {order[3]}")
                print(f"Total: ${order[1]:.2f}")
                print(f"Items: {order[2]}")
                print("-" * 40)
