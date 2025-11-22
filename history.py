import sqlite3
from datetime import datetime
import random

class OrderHistory:
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    # View all orders for a user
    def viewHistory(self, userID):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()

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
        connection.close()

    # View a specific order
    def viewOrder(self, userID, orderID):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()

        # Check if order belongs to the user
        query = "SELECT OrderNumber, ItemNumber, Cost, Date FROM Orders WHERE OrderNumber=? AND UserID=?"
        cursor.execute(query, (orderID, userID))
        order = cursor.fetchone()

        if not order:
            print("\nOrder not found.")
            cursor.close()
            connection.close()
            return

        print(f"\nOrder Number: {order[0]}, Total Items: {order[1]}, Total Cost: {order[2]}, Date: {order[3]}")
        print("Order Items:")

        query = """SELECT Inventory.ISBN, Inventory.Title, OrderItems.Quantity
                   FROM OrderItems
                   JOIN Inventory ON OrderItems.ISBN = Inventory.ISBN
                   WHERE OrderNumber=?"""
        cursor.execute(query, (orderID,))
        items = cursor.fetchall()

        for item in items:
            print(f"ISBN: {item[0]}, Title: {item[1]}, Quantity: {item[2]}")

        cursor.close()
        connection.close()

    # Create a new order and return its OrderNumber
    # Cart will call this before calling addOrderItems
    def createOrder(self, userID, totalItems, totalCost, date=None):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()

        # Generate unique OrderNumber
        while True:
            orderID = str(random.randint(100000, 999999))
            cursor.execute("SELECT * FROM Orders WHERE OrderNumber=?", (orderID,))
            if not cursor.fetchone():
                break

        if date is None:
            date = datetime.now().strftime("%m/%d/%Y %H:%M")

        query = "INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (orderID, userID, totalItems, f"${totalCost:.2f}", date))
        connection.commit()
        cursor.close()
        connection.close()
        return orderID

    # Add order items – Cart passes userID and orderID
    # This function now grabs items directly from the Cart table
    def addOrderItems(self, userID, orderID):
        connection = sqlite3.connect(self.databaseName)
        cursor = connection.cursor()

        # Get all items from user's cart
        query = "SELECT ISBN, Quantity FROM Cart WHERE UserID=?"
        cursor.execute(query, (userID,))
        cartItems = cursor.fetchall()

        # Insert each item into OrderItems
        for item in cartItems:
            ISBN, quantity = item
            cursor.execute(
                "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)",
                (orderID, ISBN, quantity)
            )

        connection.commit()
        cursor.close()
        connection.close()
