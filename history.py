import sqlite3
import random
from datetime import datetime

class OrderHistory:

    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName
        self.create_tables()

    # connect to database
    def connect(self):
        return sqlite3.connect(self.databaseName)

    # create Orders + OrderItems tables
    def create_tables(self):
        conn = self.connect()
        cur = conn.cursor()

        # Orders table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                OrderNumber TEXT PRIMARY KEY,
                UserID TEXT NOT NULL,
                ItemNumber INTEGER NOT NULL,
                Cost REAL NOT NULL,
                Date TEXT NOT NULL
            );
        """)

        # OrderItems table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS OrderItems (
                OrderNumber TEXT NOT NULL,
                ISBN TEXT NOT NULL,
                Quantity INTEGER NOT NULL
            );
        """)

        conn.commit()
        conn.close()

    
    # View order history 
    def viewHistory(self, userID):
        conn = self.connect()
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

    
    #  VIEW SINGLE ORDER
    
    def viewOrder(self, userID, orderID):
        conn = self.connect()
        cur = conn.cursor()

        # confirm order belongs to user
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

        # fetch order items
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

        # show items
        print("Books Purchased:")
        for item in items:
            print(f"ISBN: {item[0]} | Quantity: {item[1]}")

        print("-" * 40)

   
    #  CREATE ORDER (used by Cart checkout)
   
    def createOrder(self, userID, quantity, cost, date):
        conn = self.connect()
        cur = conn.cursor()

        # generate unique random orderID
        while True:
            orderID = str(random.randint(100000, 999999))
            cur.execute("SELECT OrderNumber FROM Orders WHERE OrderNumber = ?", (orderID,))
            if cur.fetchone() is None:
                break

        # insert into Orders
        cur.execute("""
            INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date)
            VALUES (?, ?, ?, ?, ?)
        """, (orderID, userID, quantity, cost, date))

        conn.commit()
        conn.close()

        return orderID  # VERY IMPORTANT for checkout

    
    #  ADD ORDER ITEMS (copies items from cart → OrderItems)
    
    def addOrderItems(self, userID, orderID):
        conn = self.connect()
        cur = conn.cursor()

        # get items from Cart table
        cur.execute("""
            SELECT ISBN, Quantity 
            FROM Cart
            WHERE UserID = ?
        """, (userID,))

        cartItems = cur.fetchall()

        # copy into OrderItems table
        for item in cartItems:
            cur.execute("""
                INSERT INTO OrderItems (OrderNumber, ISBN, Quantity)
                VALUES (?, ?, ?)
            """, (orderID, item[0], item[1]))

        conn.commit()
        conn.close()
