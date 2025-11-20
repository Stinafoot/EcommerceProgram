import sqlite3
import sys
import random
from inventory import *
from history import *



class Cart:
    
    ## constructor
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

    ## functional requirement functions

    def viewCart(self, userID):

        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        ## sets up query and uses user input
        query = """SELECT ISBN.ISBN, ISBN.title, Cart.Quantity, ISBN.Price 
                   FROM Cart 
                   JOIN ISBN ON Cart.ISBN = ISBN.ISBN 
                   WHERE Cart.UserID=?"""
        data = (userID,)

        cursor.execute(query, data)
        result = cursor.fetchall()

        ## nothing was grabbed

        if(len(result) == 0):
            print("\nYour cart is empty.")

        else:
            print("\nYour Cart:")
            for row in result:
                print(f"ISBN: {row[0]}, Title: {row[1]}, Quantity: {row[2]}, Price: {row[3]}")

        ## closes connection
        cursor.close()
        connection.close()


    def addToCart(self, userID, ISBN, quantity=1):

        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        ## sets up query and uses user input 
        query = "INSERT INTO Cart (UserID, ISBN, Quantity) VALUES (?, ?, ?)"
        data = (userID, ISBN, quantity)

        cursor.execute(query, data)
        connection.commit()

        print("\n Book added to cart.")

        ## closes connection
        cursor.close()
        connection.close()    


    def removeFromCart(self, userID, ISBN):

        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()

        ## sets up query and uses user input 
        query = "DELETE FROM Cart WHERE UserID=? AND ISBN=?"
        data = (userID, ISBN)

        cursor.execute(query, data)
        connection.commit()

        print("\n Book was removed from cart.")

        ## closes connection
        cursor.close()
        connection.close()
    
    def checkOut(self, userID):
        ## setup database and query the database
        try:
            connection = sqlite3.connect(self.databaseName)

        except:
            print("Failed database connection.")

            ## exits the program if unsuccessful
            sys.exit()

        ## cursor to send queries through
        cursor = connection.cursor()


        ## sets up query to get all cart items
        query = """SELECT ISBN.ISBN, Cart.Quantity, ISBN.Price
                    FROM Cart
                    JOIN ISBN ON Cart.ISBN = ISBN.ISBN
                    WHERE Cart.UserID=?"""
        data = (userID,)
        cursor.execute(query, data)
        cartItems = cursor.fetchall()

        ## Add if cart is emtpy code

        if(len(cartItems) == 0):
            print("\nYour cart is empty.")
            cursor.close()
            connection.close()
            return
            
        ## create order

        inventory = Inventory()
        orders = OrderHistory()

        orderID = orders.createOrder(userID)

        ## process each cart item
        for item in cartItems:

            ISBN, quantity, price = item

            ## add to order details
            orders.addOrderItems(orderID, ISBN, quantity, price)

            ## update inventory
            inventory.decreaseStock(ISBN, quantity)

        ## Clear the cart
        query = "DELETE FROM Cart WHERE UserID=?"
        data = (userID,)

        cursor.execute(query, data)
        connection.commit()

        print("\nCheckout successful. Your cart is now empty.")

        ## closes connection
        cursor.close()

        connection.close()
