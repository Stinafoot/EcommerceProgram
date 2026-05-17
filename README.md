# Ecommerce Program
Book store Ecommerce

# Online Bookstore Management System (SQLite + Python)

## Overview
This project is a command-line based online bookstore system built using Python and SQLite. It simulates a real-world e-commerce workflow including user accounts, inventory management, shopping cart functionality, and order history tracking.

---

## Features

- User account creation and login system
- View and search book inventory
- Add/remove items from shopping cart
- Checkout system with automatic stock updates
- Order history tracking and order detail viewing
- Persistent data storage using SQLite

---

## System Architecture

The project is structured into modular components:

- **User Module** → Handles authentication and account management  
- **Inventory Module** → Manages book catalog and stock updates  
- **Cart Module** → Handles shopping cart operations and checkout  
- **Order History Module** → Stores and retrieves past orders  
- **SQLite Database** → Stores all persistent application data  

---

## Database Design

The system uses SQLite with the following tables:

- User
- Inventory
- Cart
- Orders
- OrderItems

Relationships are handled using foreign keys to maintain data integrity.

---

## How to Run

1. Install Python 3.x
2. Run database setup script:
   bash
   python database_setup.py

Start the application:

python main.py

---

## Security Note
Passwords are stored in plaintext for educational purposes only.
Random ID generation is used for simplicity, not production security.

---

## Key Learning Outcomes
Working with SQLite databases in Python
Designing relational database schemas
Implementing CRUD operations
Building modular backend systems
Managing user sessions in CLI applications

---

## Future Improvements
Password hashing (bcrypt)
GUI interface (Tkinter or React frontend)
REST API version using FastAPI
Improved order ID system (UUIDs)

---

##  Authors

Built as a university project demonstrating full-stack backend logic using Python and SQLite.
@Stinafoot
@LilacLuLu31 
@graciemsu
