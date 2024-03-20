import sqlite3
from random import choices, sample
from datetime import datetime
import string


# Establish connection to SQLite database
conn = sqlite3.connect("inventory_management.db")
cursor = conn.cursor()


# Create products categories table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products_categories(
    id INTEGER PRIMARY KEY,
    category_name TEXT
)
""")


# Create a products table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products(
    id INTEGER PRIMARY KEY,
    category_id INTEGER,
    product_name TEXT,
    price REAL,
    quantity INTEGER,
    FOREIGN KEY (category_id) REFERENCES products_categories(id)
)
""")


# Create customers table
cursor.execute("""
CREATE TABLE IF NOT EXISTS customers(
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT
)
""")


# Create orders table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
    id INTEGER PRIMARY KEY,
    product_id INTEGER,
    product_ordered TEXT,
    product_price REAL,
    quantity INTEGER,
    order_amount REAL,
    order_number TEXT,
    order_date TEXT,
    customer_id INTEGER,
    order_status TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (product_price) REFERENCES products(price), 
    FOREIGN KEY (customer_id) REFERENCES customers(id)          
)
""")


class Categories: 
    def __init__(self, category_name=None):
        self.category_name = category_name


    # Creates a new order in the products_categories table
    def create_category(self):
        try:
            cursor.execute("""INSERT INTO products_categories(category_name) VALUES(?)""", (self.category_name,))
            conn.commit()
            self.id = cursor.lastrowid
            print("Category added successfully!")

        except sqlite3.Error as error:
            print(f"Error adding the category: {error}")
                

    def delete_category(self):
        categories = self.all_categories()
        print(categories)

        while True:
            category_id = input("Enter category ID: ")

            if category_id.isdigit():
                category_id = int(category_id)

                if any(category_id == int(cat.split()[0]) for cat in categories.split("\n")):
                    break
                else:
                    print("Invalid ID. Please select ID from the")

            else:
                print("Invalid ID. ID must be a number.")
            
        try:
            cursor.execute("""DELETE FROM products_categories WHERE id = ?""", (category_id,))
            conn.commit()
            print("Category removed successfully!")

        except sqlite3.Error as error:
            print(f"Unable to delete category, error:  {error}")


    # Displays all the categories
    def all_categories(self):
        try:

            # Fetches all categories from the db
            cursor.execute("""SELECT * FROM products_categories""")
            categories = cursor.fetchall()
            categories_list = []

            # Iterates through the fetched categories and appends them to the list
            for category in categories:
                categories_list.append(f"{category[0]} {category[1]}")
            
            return "\n".join(categories_list)

        except sqlite3.Error as error:
            print(f"Error fetching data: {error}")


    # Modifies the categories
    def update_category(self):
        categories = self.all_categories() 
        print(categories)

        # Check that user has entered a valid id
        while True:
            category_id = input("Enter category ID to update: ")
            if category_id.isdigit():  # Check if the input is a digit
                category_id = int(category_id)
                if any(category_id == int(cat.split()[0]) for cat in categories):
                    break
                else:
                    print("Invalid ID. Please select ID from above.")
            else:
                print("Invalid ID. ID must be a number.")
        
        # Checks that user has entered a valid name
        new_name = input("Enter new name: ")
        if not new_name.strip():
            print("Invalid input! New name cannot be empty.")
            return

        # Tries to update the name and handle exception if any
        try:
            cursor.execute("""UPDATE products_categories
                            SET category_name = ?
                            WHERE id = ? 
                            """, (new_name, category_id))
            conn.commit()
            print("Category updated successfully!")

        except sqlite3.Error as error:
            print(f"Update not successful: {error}")


    # Enables user to interact with db
    @classmethod
    def add_category_input_form(cls):
        while True:
            name = input("Enter category: ")
            if name.strip(): # Checks if user has entered a name
                return cls(name)
            else:
                print("Name cannot be empty! Try again.")
    

class Products:
    def __init__(self, product_name = None, price = None, quantity = None):
        self.product_name = product_name
        self.price = price
        self.quantity = quantity

    def add_product(self):
        try:

            # Fetch and print categories list
            categories = Categories()
            categories_list = categories.all_categories()
            print("Available Categories:")
            print(categories_list)


            while True:

                product_category_id = input("Enter category's id: ")

                if product_category_id.isdigit():
                    product_category_id = int(product_category_id)
                    break
                else:
                    print("Invalid input, category id must be a number.")

            cursor.execute("""INSERT INTO products(category_id, product_name, price, quantity)
                              VALUES (?, ?, ?, ?)""", (product_category_id, self.product_name, self.price, self.quantity))
            conn.commit()
            print(f"Product '{self.product_name}' added successfully!")

        except sqlite3.Error as error:
            print(f"Error adding {self.product_name}, error: {error}")


    def update_product(self):
        products_ls = self.display_all_products()
        print(products_ls)

        # Confirm that product id is valid
        while True:
            product_id = input("Enter product's id: ")

            if product_id.isdigit():
                product_id = int(product_id)
                break

            else:
                print("Invalid id, id must be a number.")


        # Check if new price is a number
        while True:
            new_price = input("Enter new price: ")
            # Check if new_price is numeric
            if new_price.replace('.', '', 1).isdigit():
                break

        try:
            
            cursor.execute("""UPDATE products
                            SET price = ?
                            WHERE id = ?""", (new_price, product_id))
            conn.commit()
            print("Price updated successfully!")

        except sqlite3.Error as err:
            print(f"There was an error {err}")


    def delete_product(self):
        
        # Print products list
        product_list = self.display_all_products()
        print(product_list)


        # Check if id is valid
        while True:
            product_id = input("Enter product's id: ")

            if product_id.isdigit():
                product_id = int(product_id)
                break

            else:
                print("Invaid id. Id must be a number.")

        try:
            cursor.execute("""DELETE FROM products WHERE id = ?""", (product_id,))
            conn.commit()
            print("Item deleted successfully!")

        except sqlite3.Error as err:
            print(f"There was an error deleting the item: {err}")


    # Render all the products in the database
    def display_all_products(self):
        
        try:
            cursor.execute("""SELECT * FROM products""")
            products = cursor.fetchall()
            products_list = []

            for product in products:
                products_list.append(f"{product[0]} {product[1]} {product[2]} {product[3]} {product[4]}")

            return "\n".join(products_list)

        except sqlite3.Error as error:
            print(f"Fetching products unsuccessful, error: {error}")


    @classmethod
    def input_form(cls):

        # Checks that name is not an empty string
        while True:
            product_name = input("Enter product's name: ")

            if product_name.strip():
                break

        # Checks that price is a number.
        while True:
            price = input("Enter price: ")

            if price.replace('.', '', 1).isdigit():
                break


        # Checks that quantity is a digit
        while True:
            quantity = input("Enter quantity: ")

            if quantity.isdigit():
                quantity = int(quantity)
                break

        return cls(product_name, price, quantity)
    


class Customers:

    def __init__(self, first_name = None, last_name = None):
        self.first_name = first_name
        self.last_name = last_name


    # Adds customer to the db
    def add_customer(self):
        try:
            cursor.execute("""INSERT INTO customers(first_name, last_name) VALUES(?, ?)""", (self.first_name, self.last_name))
            conn.commit()
            self.id= cursor.lastrowid
            print(f"{self.first_name} {self.last_name} added successfully.")

        except sqlite3.Error as error:
            print(f"Error adding user: {error}")


    # Delete all customers from the table
    def delete_customer(self):
        customer_list = self.show_all_customers()
        print(customer_list)

        while True:
         choice = input("Enter customer's id: ")

         if choice.isdigit():
             break
         
        try:
            cursor.execute("""DELETE FROM customers WHERE id = ?""", (choice))
            conn.commit()
            print("Deleted successfully.")

        except sqlite3.Error as error:
            print(f"Delete unsuccessful, error: {error}")


    # Displays all customers in a list
    def show_all_customers(self):
        try:
            cursor.execute("""SELECT * FROM customers""")
            customers = cursor.fetchall()
            customers_list = []

            for customer in customers:
                customers_list.append(f"{customer[0]} {customer[1]} {customer[2]}")

            return "\n".join(customers_list)

        except sqlite3.Error as error:
            print(f"Error in fetching customers: {error}")

    @classmethod
    def input_form(cls):
        
        while True:
            customer_first_name = input("Enter customer's first name: ")

            if customer_first_name.strip():
                break
            
        while True:
            customer_last_name = input("Enter customer's last name: ")

            if customer_last_name.strip():
                break
        
        return cls(customer_first_name, customer_last_name)


class OrderManagement:
    def __init__(self):
        pass
        

    # Adds order to the db.
    def add_order(self):

        # Display product details
        products = Products()
        products_list = products.display_all_products()
        print(products_list)

        # Checks if user has entered a valid id
        while True:
            product_id = input("Enter product's id: ")
            if product_id.isdigit():
                product_id = int(product_id)
                break

            else:
                print("Invalid ID. ID must be a number.")


        # Display customer details
        customer = Customers()
        customer_details = customer.show_all_customers()
        print(customer_details)

        while True:
            customer_id = input("Enter customer's id: ")
            # Check if entered id is a number
            if customer_id.isdigit():
                customer_id = int(customer_id)
                break
            else:
                print("Invalid ID. ID must be a number.")


        order_status = "Pending"
        order_number = self.generate_order_number()
        current_time = datetime.now()

        # id INTEGER PRIMARY KEY,
        # category_id INTEGER,
        # product_name TEXT,
        # price REAL,
        # quantity INTEGER,

        try:
            # Fetch product details from database based on product_id
            cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            product_data = cursor.fetchone()

            if product_data is None:
                print("Product not found.")
                return
            
            product_ordered = product_data[2]
            product_price = product_data[3]
            available_quantity = product_data[4]

            if available_quantity == 0:
                print("Product is out of stock.")
                return
            
            # Customer enters quantity
            while True:
                quantity = input("Enter quantity to order: ")
                if quantity.isdigit() and int(quantity) <= available_quantity:
                    break

                elif not quantity.isdigit():
                    print("Quantity must be an integer.")
                    
                else:
                    print("The quantity orderd is more than the availale quantities.")


            new_quantity = available_quantity - int(quantity)
            order_amount = product_price * int(quantity)

            # Start a transaction
            conn.execute("BEGIN")
            
            # Insert order into the database
            cursor.execute("""INSERT INTO orders(product_id, product_ordered, product_price, 
                           quantity, order_amount, order_number, order_date, customer_id, order_status) 
                           VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                           (product_id, product_ordered, product_price, quantity, order_amount, order_number,
                            current_time, customer_id, order_status))

            # Update product quantity
            cursor.execute("""UPDATE products
                               SET quantity = ?
                               WHERE id = ?""", (new_quantity, product_id))
            
            # Commit the transaction
            conn.commit()
            print("Order successfully placed.")

        except sqlite3.Error as err:
            print(f"There was an error adding the order. Error: {err}")


    # Generate order number
    def generate_order_number(self):
        # Generate 5 random uppercase letters
        letters = "".join(choices(string.ascii_uppercase, k=5))
        # Generate random 4 numbers
        digits = "".join(choices(string.digits, k=4))
        # Generate random order number
        order_number = "".join(sample(letters + digits, k= 9))

        return order_number
    


    def change_order_status(self):
        report_list = self.orders_report()
        print(report_list)

        while True:
            order_id = input("Enter order id: ")

            if order_id.isdigit():
                order_id = int(order_id)
                break

            else:
                print("Invalid ID. ID must be a number.")

        while True:
            print("1 - Pending")
            print("2 - Completed")
            order_status = input("Enter order status(1 or 2): ")

            if order_status == "1" or order_status == "2":
                break
            else:
                print("Invalid choice. Enter 1 or 2.  ")

        try:
            cursor.execute("""UPDATE orders
                           SET order_status = ?
                           WHERE id = ?
                           """, ("pending" if order_status == "1" else "completed", order_id))
            conn.commit()
            print("Update successfull.")

        except sqlite3.Error as err:
            print(f"There was an error changing order status. Error: {err}")

        
    def delete_order(self):
        report_list = self.orders_report()
        print(report_list)

        while True:
            order_id = input("Enter order id: ")

            if order_id.isdigit():
                order_id = int(order_id)
                break

            else:
                print("Invalid ID. ID must be a number.")

        try:
            cursor.execute("""DELETE FROM orders WHERE id = ?""", (order_id,))
            conn.commit()
            print("Item deleted successfully.")

        except sqlite3.Error as err:
            print(f"There was an error deleting the item. Error: {err}")

    # Fetches data of all the orders
    def orders_report(self):
        try:
            cursor.execute("""SELECT * FROM orders""")
            conn.commit()
            report = cursor.fetchall()
            report_list = []

            for item in report:
                report_list.append(f"{item[0]} {item[1]} {item[2]} {item[3]} {item[4]} {item[5]} {item[6]} {item[7]} {item[8]}")

            return "\n".join(report_list)

        except sqlite3.Error as err:
            print(f"There was an error fetching orders. \nError: {err}")


    # Fetches data of all the orders
    def comprehensive_report(self):
        try:
            cursor.execute("""SELECT o.id, c.first_name, c.last_name, pcat.category_name, o.product_ordered, 
                                    o.product_price, o.quantity, o.order_amount, o.order_number, o.order_date, 
                                    o.order_status
                             FROM orders o
                             JOIN customers c ON o.customer_id = c.id
                             JOIN products p ON o.product_id = p.id
                             JOIN products_categories pcat ON p.category_id = pcat.id""")
            report = cursor.fetchall()
            report_list = []

            for item in report:
                report_list.append(f"{item[0]}   {item[1]}  {item[2]}  {item[3]}  {item[4]}       {item[5]}   {item[6]}         {item[7]} {item[8]}   {item[9]}   {item[10]}")
            print(['ID  Name        Category   Item         Price      Qty      Total    Order No.           Time                 Status'])
            print(report_list)

        except sqlite3.Error as err:
            print(f"There was an error fetching orders. \nError: {err}")



def main():
    while True:
        print("\n=== Inventory Management System ===")
        print("1. Add Category")
        print("2. Update Category")
        print("3. Delete Category")
        print("4. Add Product")
        print("5. Update Product")
        print("6. Delete Product")
        print("7. Add Customer")
        print("8. Delete Customer")
        print("9. Place Order")
        print("10. Change Order Status")
        print("11. Delete Order")
        print("12. Order Report")
        print("13. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            category = Categories.add_category_input_form()
            category.create_category()

        elif choice == "2":
            category = Categories()
            category.update_category()

        elif choice == "3":
            category = Categories()
            category.delete_category()

        elif choice == "4":
            product = Products.input_form()
            product.add_product()

        elif choice == "5":
            product = Products()
            product.update_product()

        elif choice == "6":
            product = Products()
            product.delete_product()

        elif choice == "7":
            customer = Customers.input_form()
            customer.add_customer()

        elif choice == "8":
            customer = Customers()
            customer.delete_customer()

        elif choice == "9":
            order_management = OrderManagement()
            order_management.add_order()

        elif choice == "10":
            order_management = OrderManagement()
            order_management.change_order_status()

        elif choice == "11":
            order_management = OrderManagement()
            order_management.delete_order()

        elif choice == "12":
            order_management = OrderManagement()
            order_management.comprehensive_report()

        elif choice == "13":
            print("Exiting the program...")
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 12.")

if __name__ == "__main__":
    main()
    conn.close()




