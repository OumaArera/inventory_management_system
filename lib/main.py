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
        pass

class Products:
    def __init__(self, name, price, quantity):
        pass

class Customers:
    def __init__(self, first_name, last_name):
        pass

class OrderManagement:
    def __init__(self, product_ordered, price, quantity, 
                 order_amount, order_number, order_date, 
                 customer_name, order_status):
        pass