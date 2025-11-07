class Inventory:

    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName
        sample = ""

    def Inventory():
    
    def Inventory(self, databaseName):
        
    def viewInventory(self):

    def searchInventory(self):

    def decreaseStock(self, ISBN, quantity=1)
        try:
            connection = sqlite3.connect(self.databaseName)
        except:
            print("Failed database connection.")
            sys.exit()

        query = "SELECT stock FROM inventory WHERE ISBN = ?", (ISBN)
        result = query 
        if stock < quantity:
            print("Not enough copies in stock")
            return
        new_stock = stock - quantity
