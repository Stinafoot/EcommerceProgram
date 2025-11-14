import sqlite3
import sys
import random
from history import *
from cart import *

class Inventory:
    ##constructor
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName
    

    ##functionl requirement functions
    def viewInventory(self):
        try: 
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")

            sys.exit()
        
        cursor = connection.cursor()

        query = "SELECT ISBN, Title, Author, Genre, Pages, ReleaseDate, Price, Stock FROM Inventory"
        cursor.execute(query)
        result = cursor.fetchall()

        if len(result) == 0:
            print("\nInventory is empty.")
            cursor.close()
            connection.close()
            return False

        print("\nInventory:")
        for column in result:
            print(f"ISBN: {column[0]}, Title: {column[1]}, Author: {column[2]}, Genre: {column[3]}, 
            Pages: {column[4]}, ReleaseDate: {column[5]}, Price: {column[6]}, Stock: {column[7]}")
        
        cursor.close()
        connection.close()
        return True

    def searchInventory(self):
        Title = input("Enter title of the book you would like to find: ")

        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection")
            sys.exit()

        cursor = connection.cursor()

        query = "SELECT ISBN, Title, Author, Genre, Pages, ReleaseDate, Price, Stock FROM Inventory WHERE Title LIKE ?"
        data = ('%' + Title + '%')

        cursor.execute(query, data)
        result = cursor.fetchall()

        if len(result) == 0:
            print("\nNo books with this title.")
            cursor.close()
            connection.close()
            return False

        print("\nSearch Results")
        for column in result:
            print(f"ISBN: {column[0]}, Title: {column[1]}, Author: {column[2]}, Genre: {column[3]}, 
            Pages: {column[4]}, ReleaseDate: {column[5]}, Price: {column[6]}, Stock: {column[7]}")

        cursor.close()
        connection.close()

        return True

    def decreaseStock(self, ISBN, quantity=1):
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")
            sys.exit()

        cursor = connection.cursor()

        query = "SELECT Stock FROM Inventory WHERE ISBN=?"
        cursor.execute(query, (ISBN))
        result = cursor.fetchone()

        if result is None:
            print(f"\nNo book with ISBN: {ISBN} found.")
            cursor.close()
            connection.close()
            return False

        stock = result[0]


        if stock < quantity:
            print(f"Not enough copies in stock. Current copy count: {stock}")
            cursor.close()
            connection.close()
            return False

           
        new_stock = stock - quantity
        update_query = "UPDATE Inventory SET Stock=? WHERE ISBN=?"
        cursor.execute(update_query, (new_stock, ISBN))
        connection.commit()

        cursor.close()
        connection.close()

        print(f"Stock updated successfully. New stock for ISBN {ISBN}: {new_stock}")
        return True

    ##getters
    def getDatabaseName(self):
        return self.databaseName
    
    def setDatabaseName(self):
        self.databaseName = databaseName

    