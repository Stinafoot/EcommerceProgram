import sqlite3
from datetime import datetime
import random

class OrderHistory:
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    # Create a new order in Orders table
    def createOrder(self, userID, totalQuantity, totalCost):
        orderID = str(random.randint(100000, 999999))  # unique order number
        date = datetime.now().strftime("%m/%d/%Y %H:%M")

        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()

            query = """
            INSERT INTO Orders (OrderNumber, UserID, ItemNumber, Cost, Date)
            VALUES (?, ?, ?, ?, ?)
            """
            cursor.execute(query, (orderID, userID, totalQuantity, f"${totalCost:.2f}", date))

            connection.commit()
            cursor.close()
            connection.close()

            return orderID

        except Exception as e:
            print("Error creating order:", e)
            return None

    # Add items to OrderItems table
  
    def addOrderItems(self, userID, orderID, cartItems):
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()

            for item in cartItems:
                ISBN, quantity = item
                cursor.execute(
                    "INSERT INTO OrderItems (OrderNumber, ISBN, Quantity) VALUES (?, ?, ?)",
                    (orderID, ISBN, quantity)
                )

            connection.commit()
            cursor.close()
            connection.close()

        except Exception as e:
            print("Error adding order items:", e)

    # View all orders for a user
    def viewHistory(self, userID):
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()

            query = "SELECT OrderNumber, ItemNumber, Cost, Date FROM Orders WHERE UserID=?"
            cursor.execute(query, (userID,))
            results = cursor.fetchall()

            if not results:
                print("No order history found.")
            else:
                print("\nOrder History:")
                for row in results:
                    print(f"Order Number: {row[0]}, Items: {row[1]}, Cost: {row[2]}, Date: {row[3]}")

            cursor.close()
            connection.close()

        except Exception as e:
            print("Error viewing history:", e)

    ## View details of a single order
    def viewOrder(self, userID, orderID):
        try:
            connection = sqlite3.connect(self.databaseName)
            cursor = connection.cursor()

            # Verify order belongs to user
            cursor.execute("SELECT * FROM Orders WHERE OrderNumber=? AND UserID=?", (orderID, userID))
            order = cursor.fetchone()
            if not order:
                print(f"No order {orderID} found for this user.")
                cursor.close()
                connection.close()
                return

            print(f"\nOrder Number: {order[0]}, Total Items: {order[2]}, Total Cost: {order[3]}, Date: {order[4]}")
            print("Items in this order:")

            cursor.execute("SELECT ISBN, Quantity FROM OrderItems WHERE OrderNumber=?", (orderID,))
            items = cursor.fetchall()
            for item in items:
                print(f"ISBN: {item[0]}, Quantity: {item[1]}")

            cursor.close()
            connection.close()

        except Exception as e:
            print("Error viewing order:", e)
