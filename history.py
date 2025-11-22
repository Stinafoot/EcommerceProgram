import sqlite3
from datetime import datetime

class OrderHistory:
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    def viewHistory(self, userID):
        try:
            conn = sqlite3.connect(self.databaseName)
        except:
            print("Failed to connect to database.")
            return

        cursor = conn.cursor()
        query = "SELECT OrderNumber, ItemNumber, Cost, Date FROM Orders WHERE UserID=?"
        cursor.execute(query, (userID,))
        orders = cursor.fetchall()

        if not orders:
            print("\nNo order history found.")
        else:
            print("\nOrder History:")
            for order in orders:
                print(f"Order Number: {order[0]}, Items: {order[1]}, Total Cost: {order[2]}, Date: {order[3]}")

        cursor.close()
        conn.close()

    def viewOrder(self, userID, orderID):
        try:
            conn = sqlite3.connect(self.databaseName)
        except:
            print("Failed to connect to database.")
            return

        cursor = conn.cursor()
        query = """SELECT o.OrderNumber, i.ISBN, inv.Title, i.Quantity
                   FROM OrderItems i
                   JOIN Orders o ON i.OrderNumber = o.OrderNumber
                   JOIN Inventory inv ON i.ISBN = inv.ISBN
                   WHERE o.UserID=? AND o.OrderNumber=?"""
        cursor.execute(query, (userID, orderID))
        items = cursor.fetchall()

        if not items:
            print("\nNo such order found.")
        else:
            print(f"\nOrder Number: {orderID}")
            for item in items:
                print(f"ISBN: {item[1]}, Title: {item[2]}, Quantity: {item[3]}")

        cursor.close()
        conn.close()

    def createOrder(self, userID, totalItems, totalCost):
        try:
            conn = sqlite3.connect(self.databaseName)
        except:
            print("Failed to connect to database.")
            return None

        cursor = conn.cursor()
        orderNumber = str(datetime.now().timestamp()).replace('.', '')[-6:]  # unique order number
        date = datetime.now().strftime("%m/%d/%Y %H:%M")
        query = "INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (orderNumber, userID, totalItems, f"${totalCost:.2f}", date))
        conn.commit()

        cursor.close()
        conn.close()
        return orderNumber

    def addOrderItems(self, orderID, items):
        """
        items should be a list of tuples: [(ISBN1, qty1), (ISBN2, qty2), ...]
        """
        try:
            conn = sqlite3.connect(self.databaseName)
        except:
            print("Failed to connect to database.")
            return

        cursor = conn.cursor()

        for ISBN, quantity in items:
            query = "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)"
            cursor.execute(query, (orderID, ISBN, quantity))

        conn.commit()
        cursor.close()
        conn.close()
        print("Order items added successfully.")
