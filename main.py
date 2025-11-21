from user import *
from cart import *
from inventory import *
from history import *


## COMPLETE initial pre-login menu
def initialMenu():
    ## objects for the classes
    user = User()
    cart = Cart()
    inventory = Inventory()
    history = OrderHistory()

    ## initial menu
    while(1):
        print("Pre-Login Menu:")
        print("0. Login")
        print("1. Create Account")
        print("2. Exit Program")
        initial = input("Enter your menu choice: ")
        print()

        if(initial == "0"):
            user.login()

        elif(initial == "1"):
            user.createAccount()

        ## exit program
        elif(initial == "2"):
            print("Good-bye!")
            break

        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()

        ## checks status after one menu loop...
        ## goes into main menu if applicable
        if(user.getLoggedIn()):
            mainMenu(user, cart, inventory, history)


## incomplete main menu...
def mainMenu(user, cart, inventory, history):
    while(user.getLoggedIn()):
        print("Main Menu:")
        print("0. Logout")
        print("1. View Account Information")
        print("2. Inventory Information")
        print("3. Cart Information")
        print("4. Order Information")
        option = input("Enter your menu choice: ")
        print()

        ## logging out
        if(option == "0"):
            user.logout()
            print("Successful logout.")
        elif(option == "1"):
            user.viewAccountInformation()
        elif(option == "2"):
            inventoryInformation(user, inventory)
        elif(option == "3"):
            cartInformation(user, cart)
        elif(option =="4"):
            orderHistoryInformation(user, history)
        ## incorrect menu option
        else:
            print("That's not a menu option. Please try again.")

        print()

def inventoryInformation(user, inventory):
    while(True): 
        print("Inventory Information:")
        print("0. Go Back")
        print("1. View Inventory")
        print("2. Search Inventory")
        choice = input("Enter your choice: ")
        print()

        if(choice == "0"):
            return 
        elif(choice == "1"):
            inventory.viewInventory()
        elif(choice == "2"):
            inventory.searchInventory()
        else:
            print("That is not a menu option. Please try again.")
        
        print()

def cartInformation(user, cart):
    while(True): 
        print("Cart Information:")
        print("0. Go Back")
        print("1. View Cart")
        print("2. Add items to cart")
        print("3. Remove an item from cart")
        print("4. Check Out")
        choice = input("Enter your choice: ")
        print()

        if(choice == "0"):
            return
        elif(choice == "1"):
            cart.viewCart(user.getUserID())
        elif(choice == "2"):
            ISBN = input("ISBN to add to cart: ")
            quantity = input("Quantity: ")
            cart.addToCart(user.getUserID(), ISBN, quantity)
        elif(choice == "3"):
            ISBN = input("ISBN to remove from cart: ")
            cart.removeFromCart(user.getUserID(), ISBN)
        elif(choice == "4"):
            cart.checkOut(user.getUserID())
        else:
            print("That is not a menu option. Please try again.")
        
        print()

def orderHistoryInformation(user, history):
    while(True): 
        print("Order History Information:")
        print("0. Go Back")
        print("1. View Order History")
        print("2. View Order")
        choice = input("Enter your choice: ")
        print()

        if(choice == "0"):
            return
        elif(choice == "1"):
            history.viewHistory(user.getUserID())
        elif(choice == "2"):
            orderID = input("Enter the Order Number you want to view: ")
            history.viewOrder(user.getUserID(), orderID)
        else:
            print("That is not a menu option. Please try again.")
        
        print()

def main():
    print("Welcome to the online bookstore!\n")

    initialMenu()

main()
