import sqlite3


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
    customer_name TEXT,
    order_status TEXT,
    FOREIGN KEY (product_id) REFERENCES products(id),
    FOREIGN KEY (product_price) REFERENCES products(price) 
)
""")


class Categories: 
    def __init__(self, category_name):
        self.category_name = category_name


    # Creates a new order in the products_categories table
    def create_category(self):
        try:
            cursor.execute("""INSERT INTO products_categories(category_name) VALUES(?)""", (self.category_name,))
            self.id = cursor.lastrowid
            print("Category added successfully!")

        except sqlite3.Error as error:
            print(f"Error adding the category: {error}")
                

    # Removes a category from the table
    def delete_category(self, id):
        try:
            cursor.execute("""DELETE FROM products_categories WHERE id = ?""", (id,))
            print("Product removed successfully!")

        except sqlite3.Error as error:
            print(f"Unable to delete category, error:  {error}")


    # Displays all the categories
    def all_categories(self):
        try:
            cursor.execute("""SELECT * FROM products_categories""")
            categories = cursor.fetchall()
            categories_list = []

            # Iterates through the fetched categories and appends them to the list
            for category in categories:
                categories_list.append(f"{category[0]}   {category[1]}")

            return "\n".join(categories_list)

        except sqlite3.Error as error:
            print(f"Error fetching data: {error}")


    # Modifies the categories
    def update_category(self):
        self.all_categories()  # Call all_categories() to display the categories

        while True:
            category_id = input("Enter category ID to update: ")
            if category_id.strip().isdigit():  # Check if the input is a digit
                category_id = int(category_id)
                break
            else:
                choice = input("Invalid ID! Do you want to try again? (yes/no): ").lower()
                if choice.startswith("n"):
                    print("Update cancelled!")
                    return
        
        new_name = input("Enter new name: ")
        if not new_name.strip():
            print("Invalid input! New name cannot be empty.")
            return

        try:
            cursor.execute("""UPDATE products_categories
                            SET category_name = ?
                            WHERE id = ? 
                            """, (new_name, category_id))
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
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity

    def add_product(self):
        pass

    def update_product(self):
        pass

    def delete_product(self):
        pass

    def display_all_products(self):
        pass

    @classmethod
    def input_form(cls):
        pass

class Customers:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def add_customer(self):
        pass

    def update_customer(self):
        pass

    def delete_customer(self):
        pass

    def show_all_customers(self):
        pass

    @classmethod
    def input_form(cls):
        pass

class OrderManagement:
    def __init__(self, product_ordered, price, quantity, 
                 order_amount, order_number, order_date, 
                 customer_name, order_status):
        self.product_ordered = product_ordered
        self.price = price
        self.quantity = quantity
        self.order_amount = order_amount
        self.order_number = order_number
        self.order_date = order_date
        self.customer_name = customer_name
        self.order_status = order_status


    def add_order(self):
        pass

    def change_order_status(self):
        pass

    def delete_order(self):
        pass

    def orders_report(self):
        pass

    @classmethod
    def input_form(cls):
        pass



