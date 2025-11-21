import sqlite3
import random
from datetime import datetime

class OrderHistory:
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    # View all orders for a user
    def viewHistory(self, userID):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")
            return False

        cursor = connection.cursor()

        query = "SELECT OrderNumber, ItemNumber, Cost, Date FROM Orders WHERE UserID=?"
        cursor.execute(query, (userID,))
        orders = cursor.fetchall()

        if not orders:
            print("\nNo order history found.")
        else:
            print("\nOrder History:")
            for order in orders:
                print(f"Order Number: {order[0]}, Total Items: {order[1]}, Total Cost: {order[2]}, Date: {order[3]}")

        cursor.close()
        connection.close()
        return True

    # View specific order details
    def viewOrder(self, userID, orderID):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")
            return False

        cursor = connection.cursor()

        # Check if order belongs to the user
        query = "SELECT OrderNumber, ItemNumber, Cost, Date FROM Orders WHERE OrderNumber=? AND UserID=?"
        cursor.execute(query, (orderID, userID))
        order = cursor.fetchone()

        if not order:
            print("\nOrder not found.")
            cursor.close()
            connection.close()
            return False

        print(f"\nOrder Number: {order[0]}, Total Items: {order[1]}, Total Cost: {order[2]}, Date: {order[3]}")

        # Fetch order items
        query_items = """
            SELECT Inventory.Title, OrderItems.ISBN, OrderItems.Quantity, Inventory.Price
            FROM OrderItems
            JOIN Inventory ON OrderItems.ISBN = Inventory.ISBN
            WHERE OrderItems.OrderNumber=?
        """
        cursor.execute(query_items, (orderID,))
        items = cursor.fetchall()

        if not items:
            print("No items found in this order.")
        else:
            print("\nItems in Order:")
            for item in items:
                print(f"Title: {item[0]}, ISBN: {item[1]}, Quantity: {item[2]}, Price per unit: {item[3]}")

        cursor.close()
        connection.close()
        return True

    # Create a new order and return the generated order number
    def createOrder(self, userID, totalItems, totalCost, date=None):
        if date is None:
            date = datetime.now().strftime("%m/%d/%Y %H:%M")

        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")
            return None

        cursor = connection.cursor()

        # Generate unique order number
        while True:
            orderID = str(random.randint(100000, 999999))
            cursor.execute("SELECT * FROM Orders WHERE OrderNumber=?", (orderID,))
            if not cursor.fetchall():
                break

        query = "INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date) VALUES (?, ?, ?, ?, ?)"
        cursor.execute(query, (orderID, userID, totalItems, f"${totalCost:.2f}", date))
        connection.commit()

        cursor.close()
        connection.close()

        return orderID

    # Add items from the cart to the order
    
    def addOrderItems(self, orderID, cartItems):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")
            return False

        cursor = connection.cursor()

        query = "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)"
        for item in cartItems:
            ISBN, quantity = item
            cursor.execute(query, (orderID, ISBN, quantity))

        connection.commit()
        cursor.close()
        connection.close()
        return True
