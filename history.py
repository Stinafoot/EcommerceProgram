import sqlite3
import random
from datetime import datetime

class OrderHistory:

    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

   #view orders of users 
    def viewHistory(self, userID):
        conn = sqlite3.connect(self.databaseName)
        cur = conn.cursor()

        cur.execute("""
            SELECT OrderNumber, ItemNumber, Cost, Date
            FROM Orders
            WHERE UserID = ?
            ORDER BY Date DESC
        """, (userID,))

        orders = cur.fetchall()
        conn.close()

        if not orders:
            print("\nNo previous orders found.")
            return

        print("\n--- ORDER HISTORY ---")
        for order in orders:
            print(f"\nOrder Number: {order[0]}")
            print(f"Items: {order[1]}")
            print(f"Cost: ${order[2]:.2f}")
            print(f"Date: {order[3]}")
            print("-" * 40)

    #view specific orders
    def viewOrder(self, userID, orderID):
        conn = sqlite3.connect(self.databaseName)
        cur = conn.cursor()

        # verify the order belongs to the user
        cur.execute("""
            SELECT OrderNumber, ItemNumber, Cost, Date
            FROM Orders
            WHERE UserID = ? AND OrderNumber = ?
        """, (userID, orderID))

        order = cur.fetchone()

        if order is None:
            print("\nError: Order does not exist or does not belong to this user.")
            conn.close()
            return

        # fetch items included in this order
        cur.execute("""
            SELECT ISBN, Quantity
            FROM OrderItems
            WHERE OrderNumber = ?
        """, (orderID,))

        items = cur.fetchall()
        conn.close()

        print("\n--- ORDER DETAILS ---")
        print(f"Order #: {order[0]}")
        print(f"Items Total: {order[1]}")
        print(f"Order Cost: ${order[2]:.2f}")
        print(f"Date: {order[3]}\n")

        print("Books Purchased:")
        for isbn, qty in items:
            print(f"ISBN: {isbn} | Quantity: {qty}")

        print("-" * 40)

   #creates the order header
    def createOrder(self, userID, quantity, cost, date):
        conn = sqlite3.connect(self.databaseName)
        cur = conn.cursor()

        # Generate unique order number
        while True:
            orderID = str(random.randint(100000, 999999))
            cur.execute("SELECT OrderNumber FROM Orders WHERE OrderNumber = ?", (orderID,))
            if cur.fetchone() is None:
                break

        # Insert new order
        cur.execute("""
            INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date)
            VALUES (?, ?, ?, ?, ?)
        """, (orderID, userID, quantity, cost, date))

        conn.commit()
        conn.close()

        return orderID

   #add order items
    def addOrderItems(self, userID, orderID):
        conn = sqlite3.connect(self.databaseName)
        cur = conn.cursor()

        # Pull items from Cart table
        cur.execute("""
            SELECT ISBN, Quantity
            FROM Cart
            WHERE UserID = ?
        """, (userID,))

        items = cur.fetchall()

        # Insert items into OrderItems
        for isbn, qty in items:
            cur.execute("""
                INSERT INTO OrderItems (OrderNumber, ISBN, Quantity)
                VALUES (?, ?, ?)
            """, (orderID, isbn, qty))

        conn.commit()
        conn.close()
