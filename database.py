# Making the program to be able to store data permanently
import os, sqlite3

# Function for connecting to the database
"""
If printing_shop.db does not exist then it will be created automatically
If it exists → it will be opened
"""
def connect():
    database_path = "data/printing_shop.db"               # creating the path where the database is located

    if not os.path.exists("data"):                        # checking if this folder => (data) is not there
        os.makedirs("data")                               # if it's not there create it automatically

    conn = sqlite3.connect(database_path)                 # then set the connection with the database
    return conn


# Function for creating all the tables needed in the database
def create_tables():
    # setting connection to the database
    conn = connect()
    cursor = conn.cursor()

    # creating customers table, confirm if it is existing before creating a new one
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (               
            customer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
        )
    """)

    # creating printing table, confirm if it is existing before creating a new one
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS print_jobs (
            job_id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            pages INTEGER NOT NULL,
            cost REAL NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
            FOREIGN KEY(customer_id)
            REFERENCES customers(customer_id)
        )
    """)

    # creating stock table, confirm if it is existing before creating a new one
    cursor.execute("""      
        CREATE TABLE IF NOT EXISTS stock (
            stock_id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL COLLATE NOCASE,
            quantity INTEGER NOT NULL DEFAULT 0,
            is_printing_material TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'ACTIVE',
            
            CONSTRAINT rule_no_duplicate_names UNIQUE (item_name)
        );
    """)

    # creating settings price table, confirm if it is existing before creating a new one
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS settings_price (               
            setting_id INTEGER PRIMARY KEY AUTOINCREMENT,
            settings_name TEXT NOT NULL COLLATE NOCASE UNIQUE,
            price_tag INTEGER NOT NULL
        )
    """)

    # creating log history table, confirm if it is existing before creating a new one
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stock_history (               
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,        
            stock_id INTEGER NOT NULL,   
            action TEXT NOT NULL,     
            quantity INTEGER NOT NULL,
            remarks TEXT,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            
            FOREIGN KEY(stock_id)
            REFERENCES stock(stock_id)
        )
    """)

    conn.commit()
    conn.close()

