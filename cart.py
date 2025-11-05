import sqlite3
import sys
import random


class Cart:
    
    ## constructor
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName

        self.cartID = ""

    ## functional requirement functions
    def addToCart(self, userID):
        productID = input("Product ID to add to cart: ")
        quantity = input("Quantity: ")

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
        query = "INSERT INTO Cart (UserID, ProductID, Quantity)"
        data = (userID, productID, quantity)

        cursor.execute(query, data)
        connection.commit()

        print("\nProduct added to cart successfully.")

        ## closes connection
        cursor.close()
        connection.close()    

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
        query = """SELECT Product.ProductID, Product.Name, Cart.Quantity, Product.Price 
                   FROM Cart 
                   JOIN Product ON Cart.ProductID = Product.ProductID 
                   WHERE Cart.UserID=?"""
        data = (userID,)

        cursor.execute(query, data)
        result = cursor.fetchall()

        if(len(result) == 0):
            print("\nYour cart is empty.")

        else:
            print("\nYour Cart:")
            for row in result:
                print(f"Product ID: {row[0]}, Name: {row[1]}, Quantity: {row[2]}, Price: {row[3]}")

        ## closes connection
        cursor.close()
        connection.close()
