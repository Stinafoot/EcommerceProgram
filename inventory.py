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
        try: ##try, except block for connecting to database
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")

            sys.exit() ##exit if there is a failure
        
        cursor = connection.cursor()

        query = "SELECT ISBN, Title, Author, Genre, Pages, ReleaseDate, Price, Stock FROM Inventory" ##calls the information desired for function
        cursor.execute(query)
        result = cursor.fetchall() ##fetches everything

        if len(result) == 0:  ##if nothing returns 0 and closes connection
            print("\nInventory is empty.")
            cursor.close() 
            connection.close() ##closes connection to inventory
            return False

        print("\nInventory:") ##if database returns with information, prints out inventory contents
        for column in result:
            print(f"ISBN: {column[0]}, Title: {column[1]}, Author: {column[2]}, Genre: {column[3]}, Pages: {column[4]}, Release Date: {column[5]}, Price: {column[6]}, Stock: {column[7]}") ##prints inventory in an organized manner 
        
        cursor.close()
        connection.close() ##closes the connection to the database after successful retrieval 
        return True

    def searchInventory(self):
        Title = input("Enter title of the book you would like to find: ")

        try: ##try except for connecting to database
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection")
            sys.exit() ##exits if it fails to connect

        cursor = connection.cursor()

        query = "SELECT ISBN, Title, Author, Genre, Pages, ReleaseDate, Price, Stock FROM Inventory WHERE Title LIKE ?" ##searches the database for the information on books where the title matches what the user searched
        data = ('%' + Title + '%',) ##allows user to search for a full title, or a partial title

        cursor.execute(query, data)
        result = cursor.fetchall() ##fetches all information associated with searched titles, or partial title 

        if len(result) == 0: ## if title does not match, even partially, it will return nothing
            print("\nNo books with this title.")
            cursor.close()
            connection.close() ##closes connection to database
            return False

        print("\nSearch Results")
        for column in result: ##outputs the searched for title, in an organized manner
            print(f"ISBN: {column[0]}, Title: {column[1]}, Author: {column[2]}, Genre: {column[3]}, Pages: {column[4]}, Release Date: {column[5]}, Price: {column[6]}, Stock: {column[7]}")

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

        query = "SELECT Stock FROM Inventory WHERE ISBN=?" ##finds the stock of selected book based off of ISBN
        cursor.execute(query, (ISBN,))
        result = cursor.fetchone() ##fetches just the stock information and book

        if result is None: ##if nothing returns, returns that there is nothing in the inventory
            print(f"\nNo book with ISBN: {ISBN} found.")
            cursor.close()
            connection.close()
            return False

        stock = result[0] 


        if stock < quantity: ##checks that there is enough copies in stock
            print(f"Not enough copies in stock. Current copy count: {stock}")
            cursor.close()
            connection.close()
            return False

           
        new_stock = stock - quantity ##updates the new stock number after user buys copies
        update_query = "UPDATE Inventory SET Stock=? WHERE ISBN=?" ##updates the database with new stock number
        cursor.execute(update_query, (new_stock, ISBN))
        connection.commit()

        cursor.close()
        connection.close()

        print(f"Stock updated successfully. New stock for ISBN {ISBN}: {new_stock}")
        return True

    ##getter
    def getDatabaseName(self):
        return self.databaseName
    ##setter
    def setDatabaseName(self):
        self.databaseName = databaseName

    