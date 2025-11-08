class OrderHistory:

#Retrieve and display a user's past orders.
def view_order_history(self, user_name):
    connection = self.connect()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT order_id, total, items, date
        FROM orders
        WHERE user_name = ?
        ORDER BY date DESC
    """, (user_name,))

    orders = cursor.fetchall()
    connection.close()

    if not orders:
        print(f"\nNo previous orders found for {user_name}.")
    else:
        print(f"\n--- Order History for {user_name} ---")
        for order in orders:
            print(f"Order ID: {order[0]}")
            print(f"Date: {order[3]}")
            print(f"Total: ${order[1]:.2f}")
            print(f"Items: {order[2]}")
            print("-" * 40)
