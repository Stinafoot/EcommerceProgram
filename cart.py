import sqlite3
import sys
import random


class Cart:
    
    ## constructor
    def __init__(self, databaseName="methods.db"):
        self.databaseName = databaseName
