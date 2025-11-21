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

    # view full order history
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

    # view details for one order
    def viewOrder(self, userID, orderID):
        conn = self.connect()
        cur = conn.cursor()

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

        # fetch items
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
        for item in items:
            print(f"ISBN: {item[0]} | Quantity: {item[1]}")

        print("-" * 40)

    # create order header
    def createOrder(self, userID, quantity, cost, date):
        conn = self.connect()
        cur = conn.cursor()

        # generate safe order #
        while True:
            orderID = str(random.randint(100000, 999999))
            cur.execute("SELECT OrderNumber FROM Orders WHERE OrderNumber = ?", (orderID,))
            if cur.fetchone() is None:
                break

        # insert order
        cur.execute("""
            INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date)
            VALUES (?, ?, ?, ?, ?)
        """, (orderID, userID, quantity, cost, date))

        conn.commit()
        conn.close()

        return orderID

    # copy items from cart to OrderItems
    def addOrderItems(self, userID, orderID):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("""
            SELECT ISBN, Quantity
            FROM Cart
            WHERE UserID = ?
        """, (userID,))
        cartItems = cur.fetchall()

        for item in cartItems:
            cur.execute("""
                INSERT INTO OrderItems (OrderNumber, ISBN, Quantity)
                VALUES (?, ?, ?)
            """, (orderID, item[0], item[1]))

        conn.commit()
        conn.close()

    # CLEAR HISTORY (optional)
    def clearHistory(self, userID):
        conn = self.connect()
        cur = conn.cursor()

        cur.execute("DELETE FROM OrderItems WHERE OrderNumber IN (SELECT OrderNumber FROM Orders WHERE UserID=?)", (userID,))
        cur.execute("DELETE FROM Orders WHERE UserID=?", (userID,))

        conn.commit()
        conn.close()
        print("\nOrder history cleared.")

    # ALL-IN-ONE CHECKOUT FUNCTION
    def checkout(self, userID, inventory):
        conn = self.connect()
        cur = conn.cursor()

        # get cart items
        cur.execute("""
            SELECT ISBN, Quantity 
            FROM Cart
            WHERE UserID = ?
        """, (userID,))
        cartItems = cur.fetchall()

        if not cartItems:
            print("\nYour cart is empty.")
            conn.close()
            return

        # calculate total + validate stock
        totalCost = 0
        totalItems = 0

        for isbn, qty in cartItems:
            # price lookup
            cur.execute("SELECT Price, Stock FROM Inventory WHERE ISBN = ?", (isbn,))
            result = cur.fetchone()

            if result is None:
                print(f"\nError: ISBN {isbn} no longer exists.")
                conn.close()
                return

            price, stock = result
            if qty > stock:
                print(f"\nNot enough stock for ISBN {isbn}. Available: {stock}")
                conn.close()
                return

            totalCost += price * qty
            totalItems += qty

        # CREATE ORDER
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        orderID = self.createOrder(userID, totalItems, totalCost, date)

        # add to OrderItems
        self.addOrderItems(userID, orderID)

        # decrease inventory
        for isbn, qty in cartItems:
            cur.execute("UPDATE Inventory SET Stock = Stock - ? WHERE ISBN = ?", (qty, isbn))

        # clear cart
        cur.execute("DELETE FROM Cart WHERE UserID = ?", (userID,))

        conn.commit()
        conn.close()

        print("\n=== Checkout Successful! ===")
        print(f"Order ID: {orderID}")
        print(f"Total Items: {totalItems}")
        print(f"Total Cost: ${totalCost:.2f}")
        print(f"Date: {date}")
        print("============================")
