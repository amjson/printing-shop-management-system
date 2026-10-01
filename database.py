# Making the program to be able to store data permanently
import os, sqlite3
from datetime import datetime

# Function for connecting to the database
"""
If printing_shop.db does not exist then it will be created automatically
If it exists → it will be used
"""
def connect():
    database_path = "data/printing_shop_v2.db"           # creating the path where the database is located

    if not os.path.exists("data"):                        # checking if this folder => (data) is not there
        os.makedirs("data")                               # if it's not there create it automatically

    # print(database_path)
    conn = sqlite3.connect(database_path)                 # then set the connection with the database
    return conn

# ==================================================================================
# ============== CREATING FUNCTIONS NEEDED IN VERSION 2.0 APPLICATION  =============
# ==================================================================================

# =============== [ 1. FUNCTIONS FOR TABLE CREATION ] ===============
def initialize_database():
    conn = connect()
    cursor = conn.cursor()

    # changed version 2 customer table => tbl_customer
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_customers (
            customer_id TEXT PRIMARY KEY,
            fullname TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            customer_type TEXT NOT NULL,
            customer_status TEXT NOT NULL
        )
    """)

    # creating log history for customers
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_customers_history (               
            history_id INTEGER PRIMARY KEY AUTOINCREMENT,        
            customer_id TEXT NOT NULL,   
            action TEXT NOT NULL,
            date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY(customer_id)
            REFERENCES tbl_customers(customer_id)
        )
    """)

    # creating stocks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_stock (
            stock_id TEXT PRIMARY KEY,
            item_name TEXT NOT NULL COLLATE NOCASE,
            quantity INTEGER NOT NULL DEFAULT 0,
            is_printing_material TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'ACTIVE',

            CONSTRAINT rule_no_duplicate_names UNIQUE (item_name)
        );
    """)

    # creating log history table
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

    # creating settings price table
    cursor.execute("""
       CREATE TABLE IF NOT EXISTS printing_price (               
           price_id INTEGER PRIMARY KEY AUTOINCREMENT,
           price_per_page INTEGER NOT NULL,
           price_type TEXT NOT NULL UNIQUE
       )
    """)

    # creating settings price table
    cursor.execute(""" 
       CREATE TABLE IF NOT EXISTS tbl_print_jobs (
          job_id INTEGER PRIMARY KEY AUTOINCREMENT,
          customer_id TEXT NOT NULL,
          print_type TEXT NOT NULL,
          pages INTEGER NOT NULL,
          cost REAL NOT NULL,
          date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
          FOREIGN KEY(customer_id)
          REFERENCES tbl_customers(customer_id)
       )
    """)

    conn.commit()
    conn.close()


# =============== [ 2. FUNCTIONS FOR CUSTOMER MODULE ] ===============
# ---------- Saving customer in the table
def save_customer_to_database(customer_id, fullname, phone, customer_type_selected, confirm_reactivate=False, old_id=None):
    conn = connect()
    cursor = conn.cursor()

    try:
        # 1. If reactivation was approved
        if confirm_reactivate:
            cursor.execute(
                """UPDATE tbl_customers 
                SET customer_status = ?
                WHERE customer_id = ? """,
                ("ACTIVE", old_id)
            )

            action = "REACTIVATE"

            # Record the action in customer log
            log_customer_history(cursor, old_id, action)

        # 2. Add the new customer
        if not confirm_reactivate:
            cursor.execute(
                """INSERT INTO tbl_customers (customer_id, fullname, phone_number, customer_type, customer_status) VALUES (?, ?, ?, ?, ?) """,
                (customer_id, fullname, phone, customer_type_selected, "ACTIVE")
            )

            action = "ADD"

            # Record the action in customer log
            log_customer_history(cursor, customer_id, action)

        # 3. Everything succeeded
        conn.commit()

        return True

    except Exception as error:
        conn.rollback()
        print("Something went wrong:", error)
        return False
    finally:
        cursor.close()
        conn.close()

# ---------- getting last customer id
def get_last_customer_id():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT customer_id FROM tbl_customers ORDER BY customer_id DESC LIMIT 1")
    last_customer = cursor.fetchone()

    conn.close()

    return last_customer

# ---------- checking if a customer already exist
def get_customer_existence(fullname, phone, customer_type_selected):
    conn = connect()
    cursor = conn.cursor()

    # Adding 'COLLATE NOCASE' makes 'JOHN', 'john', and 'John' completely identical matches
    cursor.execute(
        """SELECT customer_id, fullname, phone_number, customer_type 
        FROM tbl_customers 
        WHERE fullname = ? COLLATE NOCASE AND phone_number = ? AND customer_type = ? AND customer_status = ?""",
        (fullname, phone, customer_type_selected, "INACTIVE")
    )

    customer_exist = cursor.fetchone()
    cursor.close()
    conn.close()

    return customer_exist  # Returns a tuple (id, name, phone, type) or None (which evaluates to False)

# ---------- updating specific customer
def update_customer_in_database(customer_id, fullname, phone, customer_type):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE tbl_customers SET 
        fullname = ?, phone_number = ?, customer_type= ? 
        WHERE customer_id = ?""",
       (fullname, phone, customer_type, customer_id)
    )

    action = "UPDATE"

    # Record the action in customer log
    log_customer_history(cursor, customer_id, action)

    conn.commit()
    cursor.close()
    conn.close()

    return True

# ---------- Displaying customer records
def get_all_customers(sort_column="customer_id", sort_order="ASC"):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        f"""
            SELECT customer_id, fullname, phone_number, customer_type
            FROM tbl_customers
            WHERE customer_status = 'ACTIVE' 
            ORDER BY {sort_column} {sort_order}
        """
    )
    customers = cursor.fetchall()

    conn.close()

    return customers

# ---------- search customer by customer id or name or phone
def search_customers(search_text):
    conn = connect()
    cursor = conn.cursor()

    # Customer ID → flexible search
    # Full Name   → flexible search
    # Phone       → exact match
    cursor.execute(
        """
        SELECT customer_id, fullname, phone_number, customer_type
        FROM tbl_customers
        WHERE (customer_id LIKE ? OR fullname LIKE ? OR phone_number = ?) AND customer_status = 'ACTIVE'
        """,
        (f"%{search_text}%", f"%{search_text}%", search_text)
    )

    customers = cursor.fetchall()
    conn.close()

    return customers

# ---------- Delete specific customer using soft delete
def delete_customer_in_database(customer_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """ UPDATE tbl_customers SET customer_status=?
         WHERE customer_id = ? """,
        ('INACTIVE', customer_id)
    )

    action = "DEACTIVATE"

    # Record the action in customer log
    log_customer_history(cursor, customer_id, action)

    conn.commit()
    cursor.close()
    conn.close()

    return True

# ---------- Display customer history
def view_customer_history(sort_column="tbl_customers_history.date_created", sort_order="ASC"):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        f"""
        SELECT
            tbl_customers_history.customer_id,
            tbl_customers.fullname,
            tbl_customers_history.action,
            strftime('%m-%d %H:%M', tbl_customers_history.date_created)
        FROM tbl_customers_history
        JOIN tbl_customers
        ON tbl_customers_history.customer_id = tbl_customers.customer_id
        ORDER BY {sort_column} {sort_order}
        """
    )

    customer_history = cursor.fetchall()

    cursor.close()
    conn.close()

    return customer_history

# ---------- Record log activities involving customers record
def log_customer_history(cursor, customer_id, action):
    cursor.execute(
        """INSERT INTO tbl_customers_history (customer_id, action) VALUES (?, ?)""",
        (customer_id, action)
    )

# ---------- getting recent activities
def recent_activity_history():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT        
            tbl_customers.fullname,
            tbl_customers_history.action,
            strftime('%m-%d %H:%M', tbl_customers_history.date_created)
        FROM tbl_customers_history
        JOIN tbl_customers
        ON tbl_customers_history.customer_id = tbl_customers.customer_id
        ORDER BY tbl_customers_history.date_created DESC 
        LIMIT 5
        """
    )

    recent = cursor.fetchall()
    cursor.close()
    conn.close()
    return recent

# ---------- getting customers metrics
def fetch_customer_metrics():
    conn = connect()
    cursor = conn.cursor()

    # 1. Total Customers
    cursor.execute("SELECT COUNT(*) FROM tbl_customers")
    total = cursor.fetchone()[0] or 0

    # 2. Active Customers
    cursor.execute("SELECT COUNT(*) FROM tbl_customers WHERE customer_status = 'ACTIVE'")
    active = cursor.fetchone()[0] or 0

    # 3. Inactive Customers
    cursor.execute("SELECT COUNT(*) FROM tbl_customers WHERE customer_status = 'INACTIVE'")
    inactive = cursor.fetchone()[0] or 0

    cursor.close()
    conn.close()
    return total, active, inactive


# =============== [ 3. FUNCTIONS FOR STOCK MODULE ] ===============
# ---------- Display available stock record
def view_stock():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT stock_id, item_name, quantity, is_printing_material, status FROM tbl_stock WHERE status = 'ACTIVE' ")
    stock = cursor.fetchall()

    cursor.close()
    conn.close()

    return stock

# ---------- Display stock history
def view_history(sort_column="date_created", sort_order="ASC"):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        f"""
            SELECT history_id, stock_id, action, quantity, remarks, strftime('%m-%d %H:%M', date_created) FROM stock_history
            ORDER BY {sort_column} {sort_order}
        """
    )
    stock = cursor.fetchall()

    cursor.close()
    conn.close()

    return stock

# ---------- getting last stock id
def get_last_stock_id():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT stock_id FROM tbl_stock ORDER BY stock_id DESC LIMIT 1")
    last_stock = cursor.fetchone()

    conn.close()

    return last_stock

# ---------- search stock by stock id or item name
def search_stock(search_text):
    conn = connect()
    cursor = conn.cursor()

    # Stock ID   → flexible search
    # Stock Name → exact match
    cursor.execute(
        """ SELECT stock_id, item_name, quantity, is_printing_material, status
        FROM tbl_stock
        WHERE (stock_id LIKE ? OR item_name LIKE ?) AND  status = 'ACTIVE' """,
        (f"%{search_text}%", f"%{search_text}%")
    )

    stock = cursor.fetchall()
    conn.close()

    return stock

# ---------- checking for active printing item
def get_active_printing_material():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT stock_id, item_name FROM tbl_stock WHERE is_printing_material=? AND status = ? ",
        ("Yes", "ACTIVE")
    )

    current_printing = cursor.fetchone()
    cursor.close()
    conn.close()

    if current_printing:
        return current_printing
    return False

# ---------- checking for item existence
def get_stock_by_name(item_name):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT stock_id, item_name FROM tbl_stock WHERE item_name = ? AND status = ? ",
        (item_name, "INACTIVE")
    )

    item_exist = cursor.fetchone()
    cursor.close()
    conn.close()

    if item_exist:
        return item_exist
    return False

# ---------- adding new stock item
def save_stock_to_database(stock_id, name, quantity, printing_material, reason, confirm_replace=False, old_stock_id=None, confirm_reactivate=False, stock_id_exist=None):
    conn = connect()
    cursor = conn.cursor()

    try:
        # 1. If reactivation was approved
        if confirm_reactivate:
            cursor.execute(
                "UPDATE tbl_stock SET quantity = ?, is_printing_material = ?, status = ? WHERE stock_id = ? ",
                (quantity, printing_material, "ACTIVE", stock_id_exist)
            )
            action = "REACTIVATE"

            # Record the action in stock log
            log_stock_history(cursor, stock_id_exist, action, quantity, reason)

        # 2. If replacement was approved
        if confirm_replace:
            cursor.execute(
                "UPDATE tbl_stock SET is_printing_material = ? WHERE stock_id = ? ",
                ("No", old_stock_id)
            )
            action = "REPLACE"

            # Record the action in stock log
            log_stock_history(cursor, old_stock_id, action, quantity, reason)

        # 3. Add the new stock
        if not confirm_reactivate:
            cursor.execute(
                "INSERT INTO tbl_stock (stock_id, item_name, quantity, is_printing_material, status) VALUES (?, ?, ?, ?, ?)",
                (stock_id, name, quantity, printing_material, "ACTIVE")
            )

            action = "ADD"

            # Record the action in stock log
            log_stock_history(cursor, stock_id, action, quantity, reason)

        # 4. Everything succeeded
        conn.commit()

        return True

    except Exception as error:
        conn.rollback()
        print("Something went wrong:", error)
        return False
    finally:
        cursor.close()
        conn.close()

# ---------- update stock item
def update_stock_record_info(stock_id, stock_name, stock_quantity, printing_material, reason, confirm_replace, old_stock_id):
    conn = connect()
    cursor = conn.cursor()

    try:
        # 1. If replacement was approved
        if confirm_replace:
            cursor.execute(
                "UPDATE tbl_stock SET is_printing_material = ? WHERE stock_id = ? ",
                ("No", old_stock_id)
            )

            action = "REPLACE"

            # Record the action in stock log
            log_stock_history(cursor, old_stock_id, action, stock_quantity, reason)

        # 2. If replacement isn't necessary
        cursor.execute(
            """ UPDATE tbl_stock
                SET item_name = ?, quantity = quantity + ?, is_printing_material = ?
                WHERE stock_id = ? """,
            (stock_name, stock_quantity, printing_material, stock_id)
        )

        action = "RESTOCK"

        # Record the action in stock log
        log_stock_history(cursor, stock_id, action, stock_quantity, reason)

        conn.commit()

        return True

    except Exception as error:
        conn.rollback()
        print("Something went wrong:", error)
        return False
    finally:
        cursor.close()
        conn.close()

# ---------- delete stock item by stock id
def delete_stock_from_database(stock_id, reason):
    conn = connect()
    cursor = conn.cursor()

    """
    We have two database operations that need to succeed together, 
    and we need a way to recover if something unexpected happens.
    """
    try:
        # Perform soft delete
        cursor.execute(
            """ UPDATE tbl_stock SET status=?, is_printing_material=? WHERE stock_id = ? """,
            ('INACTIVE', 'No', stock_id)
        )

        action = "DEACTIVATE"
        quantity = 0

        # Record the action in stock log
        log_stock_history(cursor, stock_id, action, quantity, reason)

        conn.commit()

        return True
    except Exception as error:
        # If something goes wrong while executing the try block, come here.
        conn.rollback()
        print("Something went wrong:", error)
        return False
    finally:
        cursor.close()
        conn.close()

# ---------- Record log activity involving stock
def log_stock_history(cursor, stock_id, action, quantity, remarks):
    cursor.execute(
        """INSERT INTO stock_history (stock_id, action, quantity, remarks) VALUES (?, ?, ?, ?)""",
        (stock_id, action, quantity, remarks)
    )


# =============== [ 4. FUNCTIONS FOR PRINTING MODULE ] ===============
# ---------- checking for customer id existence before doing printing operation
def check_customer_id(customer_id):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT customer_id 
        FROM tbl_customers 
        WHERE customer_id = ? AND customer_status = ?""",
        (customer_id, "ACTIVE")
    )

    id_exist = cursor.fetchone()
    cursor.close()
    conn.close()

    if id_exist:
        return True
    return False

# ---------- checking for current paper stock before doing printing operation
def check_current_stock():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT quantity FROM tbl_stock WHERE is_printing_material = 'Yes' AND status = 'ACTIVE' ")

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return result[0]
    return False

# ---------- Helper function —> Saving printing job
def save_print_job(cursor, customer_id, pages_required, print_type_selected, printing_cost):
    cursor.execute(
        """
        INSERT INTO tbl_print_jobs
        (customer_id, print_type, pages, cost)
        VALUES (?, ?, ?, ?)
        """,
        (customer_id, print_type_selected, pages_required, printing_cost)
    )

# ---------- Helper function —> Reducing the stock
def reduce_printing_stock(cursor, pages):
    cursor.execute(
        """
        UPDATE tbl_stock
        SET quantity = quantity - ?
        WHERE is_printing_material = ?
        AND status = ?
        """,
        (pages, "Yes", "ACTIVE")
    )

    # verify that an actual row was updated
    if cursor.rowcount == 0:
        raise Exception("Printing stock could not be updated.")

    return True

# ---------- for recording print jobs
def record_print_job(customer_id, pages_required, print_type_selected, printing_cost):
    conn = connect()
    cursor = conn.cursor()

    try:
        # Record printing transaction
        save_print_job(cursor, customer_id, pages_required, print_type_selected, printing_cost)

        # Reduce paper stock
        reduce_printing_stock(cursor, pages_required)

        conn.commit()
        return True

    except Exception as error:
        conn.rollback()
        print("Something went wrong:", error)
        return False

    finally:
        cursor.close()
        conn.close()

# ---------- fetch_financial_metrics after successful print operation
def fetch_financial_metrics():
    conn = connect()
    cursor = conn.cursor()

    # 1. Getting the current year and current week number (00 to 53)
    current_year = datetime.now().strftime('%Y')
    current_week = datetime.now().strftime('%W')  # %W treats Monday as the first day of the week

    # 2. Query for Weekly Revenue (SUM of the 'cost' column for this week)
    cursor.execute(
        """
            SELECT SUM(cost) 
            FROM tbl_print_jobs 
            WHERE strftime('%Y', date_created) = ? AND strftime('%W', date_created) = ?
        """,
        (current_year, current_week)
    )

    revenue_result = cursor.fetchone()
    weekly_revenue = revenue_result[0] if revenue_result[0] is not None else 0

    # 3. Query for Weekly Average (AVG of the 'cost' column per job this week)
    cursor.execute(
        """
            SELECT AVG(cost) 
            FROM tbl_print_jobs 
            WHERE strftime('%Y', date_created) = ? AND strftime('%W', date_created) = ?
        """, (current_year, current_week)
    )

    average_result = cursor.fetchone()
    weekly_average = average_result[0] if average_result[0] is not None else 0.0

    cursor.close()
    conn.close()

    # Return both calculations to your GUI controller as a tuple
    return weekly_revenue, weekly_average

# ---------- viewing available printing jobs
def view_print_job(sort_column="date_created", sort_order="ASC"):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(f"""      
        SELECT
            tbl_customers.fullname,
            tbl_print_jobs.print_type,
            tbl_print_jobs.pages,
            tbl_print_jobs.cost,
            strftime('%m-%d %H:%M', tbl_print_jobs.date_created)
        FROM tbl_print_jobs
        JOIN tbl_customers
        ON tbl_print_jobs.customer_id = tbl_customers.customer_id
        ORDER BY {sort_column} {sort_order}
        """, )

    get_result = cursor.fetchall()

    cursor.close()
    conn.close()

    return get_result

# ---------- searching for a specific printing job
def search_print_jobs(search_text):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            tbl_customers.fullname,
            tbl_print_jobs.print_type,
            tbl_print_jobs.pages,
            tbl_print_jobs.cost,
            tbl_print_jobs.date_created
        FROM tbl_print_jobs
        JOIN tbl_customers
        ON tbl_print_jobs.customer_id = tbl_customers.customer_id
        WHERE tbl_customers.fullname LIKE ? 
        """,
        (f"%{search_text}%",)
    )

    printing_jobs = cursor.fetchall()
    cursor.close()
    conn.close()

    return printing_jobs

# ---------- viewing current printing price
def current_printing_price(print_type_selected):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT price_per_page FROM printing_price
        WHERE price_type = ? """,
       (print_type_selected,))

    result = cursor.fetchone()
    cursor.close()
    conn.close()

    if result:
        return result
    return False

# ---------- saving the print price information
def save_print_price(printing_price, print_type_selected):
    conn = connect()
    cursor = conn.cursor()

    try:
        #  adding the new price
        cursor.execute(
            """INSERT INTO printing_price (price_per_page, price_type) VALUES (?, ?) """,
            (printing_price, print_type_selected)
        )

        # commit when Everything succeeded
        conn.commit()

        return True

    except Exception as error:
        # if anything goes wrong undo any change that was done
        conn.rollback()
        print("Something went wrong:", error)
        return False
    finally:
        cursor.close()
        conn.close()

# ---------- viewing available printing price information
def view_price_table():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT price_id, price_per_page, price_type FROM printing_price ")
    price = cursor.fetchall()

    cursor.close()
    conn.close()

    return price

# ---------- deleting available printing price information
def delete_price_in_database(price_id):
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """DELETE FROM printing_price 
            WHERE price_id = ? """,
            (price_id, )
        )

        conn.commit()

        return True

    except Exception as error:
        conn.rollback()
        print("Something went wrong:", error)
        return False
    finally:
        cursor.close()
        conn.close()

# ---------- updating available printing price information
def update_price_in_database(new_price, price_id):
    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute(
            """ UPDATE printing_price
                SET price_per_page = ?
                WHERE price_id = ? """,
            (new_price, price_id)
        )

        # verify if an actual row was updated
        if cursor.rowcount == 0:
            raise Exception("Price could not be updated.")

        # when Everything succeeded
        conn.commit()
        return True

    except Exception as error:
        conn.rollback()
        print("Something went wrong:", error)
        return False
    finally:
        cursor.close()
        conn.close()


# =============== [ 5. FUNCTIONS FOR REPORT MODULE ] ===============
# ---------- displaying sales summary report
def get_sales_summary():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT 
            COUNT(*), 
            SUM(pages), 
            SUM(cost),
            AVG(cost)
            FROM tbl_print_jobs
        """
    )

    sales = cursor.fetchone()
    conn.close()

    return sales

# ---------- Fetches and groups total printing for chart display
def get_sales_chart_data():
    conn = connect()
    cursor = conn.cursor()

    # Fetches and groups total printing revenue summarized by single days.
    # DATE(date_created) extracts just 'YYYY-MM-DD', ignoring hours/minutes
    # SUM(cost) totals all jobs processed on that specific calendar day
    # Restricts chart to the last 7 active printing days
    cursor.execute("""
        SELECT DATE(date_created) as sale_date, SUM(cost) as total_revenue
        FROM tbl_print_jobs
        GROUP BY DATE(date_created)
        ORDER BY sale_date DESC
        LIMIT 7
    """)

    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

# ---------- searching for a specific date report
def get_date_report(selected_date):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """SELECT COUNT(*), SUM(pages), SUM(cost) 
            FROM tbl_print_jobs
            WHERE date(date_created) = ?
        """, (selected_date,)
    )

    date_report = cursor.fetchone()
    conn.close()

    return date_report

# ---------- searching for a specific customer report
def search_specific_customer_report(search_text):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("""      
        SELECT
            tbl_print_jobs.job_id,
            tbl_customers.fullname,
            tbl_customers.phone_number, 
            tbl_customers.customer_status,
            tbl_print_jobs.print_type,
            tbl_print_jobs.pages,
            tbl_print_jobs.cost,
            strftime('%m-%d %H:%M', tbl_print_jobs.date_created)
        FROM tbl_print_jobs
        JOIN tbl_customers
        ON tbl_print_jobs.customer_id = tbl_customers.customer_id
        WHERE tbl_print_jobs.customer_id = ? 
        """, (search_text,)
    )

    customer_report = cursor.fetchall()
    cursor.close()
    conn.close()

    return customer_report



# ==================================================================================
# ============== CREATING FUNCTIONS NEEDED IN VERSION 1.0 APPLICATION  =============
# ==================================================================================
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

