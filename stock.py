# Building the “Stock brain” here so that it remembers
# importing database file here so that anything to do with the database will use this reference
import database

def view_stock():
    # setting connection to the database
    conn = database.connect()
    cursor = conn.cursor()

    # displaying records that are inside the table
    cursor.execute("SELECT stock_id, item_name, quantity, is_printing_material FROM stock WHERE status = 'ACTIVE' ")
    stock = cursor.fetchall()

    if stock:
        print("\n===== Available STOCK =====")
        for row in stock:
            # ==========[ Unpack the tuple ]==========
            stock_id, name, quantity, is_printing = row
            print(f"Item ID ({stock_id}) : {name}, Remaining Quantity: {quantity} => Printing Material: {is_printing} ")
    else:
        print("No Available Stock yet.")

    conn.close()


def add_update_stock():
    # ==========[ 1. Get User Input ]==========
    item_name = " ".join(input("Enter Item Name: ").split())
    quantity = int(input("Enter Quantity: "))

    if quantity <= 0:
        print("Quantity must be greater than zero.")
        return

    print(f"\nIs '{item_name}' used for printing?")
    print("1. Yes")
    print("2. No")

    choice = input("Select Option: ")
    remarks = input("Remarks (Optional): ")

    if choice not in ("1", "2"):
        print("Invalid option.")
        return

    is_printing_material = "Yes" if choice == "1" else "No"

    conn = database.connect()
    cursor = conn.cursor()

    continue_saving = True

    # ==========[ 2. Check if this item already exists ]==========
    cursor.execute("SELECT stock_id, status FROM stock WHERE item_name = ?", (item_name,))
    existing_item = cursor.fetchone()

    # ==========[ 3. Only one ACTIVE printing material allowed ]==========
    if is_printing_material == "Yes":
        cursor.execute("SELECT stock_id, item_name FROM stock WHERE is_printing_material = 'Yes' AND status = 'ACTIVE' ")
        current_printing = cursor.fetchone()

        if current_printing:
            printing_id, printing_name = current_printing

            if printing_name.lower() != item_name.lower():

                print(f"\nCurrent printing material is: {printing_name}")
                print("Replace it?")
                print("1. Yes")
                print("2. No")

                answer = input("Select Option: ")

                if answer == "1":
                    cursor.execute("UPDATE stock SET is_printing_material = 'No' WHERE stock_id = ?", (printing_id,))
                else:
                    continue_saving = False

    if not continue_saving:
        print("\nOperation cancelled.")
        conn.close()
        return

    # ==========[ 4. Insert / Restock / Reactivate item where necessary ]==========
    if not existing_item:
        # ---------- Inserting Brand New Item ----------
        cursor.execute("INSERT INTO stock (item_name, quantity, is_printing_material) VALUES (?, ?, ?)", (item_name, quantity, is_printing_material))

        stock_id = cursor.lastrowid
        action = "ADD"              # -------- Action Performed
    else:
        stock_id, status = existing_item
        if status == 'ACTIVE':
            # ---------- Updating existing active Item (Restock) ----------
            cursor.execute("UPDATE stock SET quantity = stock.quantity + ?, is_printing_material = ? WHERE stock_id = ?",
                (quantity, is_printing_material, stock_id))

            action = "RESTOCK"     # -------- Action Performed
        else:
            # ---------- Reactivating existing INACTIVE Item (Reactivate) ----------
            cursor.execute("UPDATE stock SET quantity = ?, is_printing_material = ?, status = 'ACTIVE' WHERE stock_id = ? ",
                (quantity, is_printing_material, stock_id))

            action = "REACTIVATE"   # -------- Action Performed

    # ---------- calling log function and passing cursor in it ----------
    log_stock_history(cursor, stock_id, action, quantity, remarks)
    conn.commit()

    print("\nStock saved successfully.")
    view_stock()

    conn.close()


def delete_stock():
    # ==========[ 1. Get User Input ]==========
    stock_id = int(input("Enter Stock ID you want to Delete: "))

    print("Do you want to DELETE this Stock?")
    print("1. Yes")
    print("2. No")

    choice = input("Select Option: ")

    if choice not in ("1", "2"):
        print("Invalid option.")
        return

    confirm_delete = "Yes" if choice == "1" else "No"

    # ==========[ 2. Validate Business Rules ]==========
    if confirm_delete == "Yes":

        conn = database.connect()
        cursor = conn.cursor()

        # ==========[ 3. Check if the item exist ]==========
        cursor.execute("SELECT stock_id, quantity FROM stock WHERE stock_id = ? AND status = 'ACTIVE' ", (stock_id,))
        selected_stock = cursor.fetchone()

        if not selected_stock:
            print(f"\nNo Stock that matches ID No: {stock_id}")
            conn.close()
            return
        else:
            # ==========[ 4. Proceed with the process, Ask for the reason (optional) ]==========
            remarks = input("Reason for Deleting (optional): ")
            stock_id, quantity = selected_stock

            # ==========[ 5. Perform soft delete ]==========
            cursor.execute("""
                UPDATE stock SET
                status=?,
                is_printing_material=?
                WHERE stock_id = ? """,('INACTIVE', 'No', stock_id))

            # ==========[ 6. Log History ]=========
            action = "INACTIVE"

            # ---------- calling log function and passing cursor in it ----------
            log_stock_history(cursor, stock_id, action, quantity, remarks)
            conn.commit()

            print("\nStock deleted successfully.")
            view_stock()
            conn.close()
    else:
        print("\nOperation cancelled.")


# Read printing_material quantity from database for reduction after printing is done
def get_stock():
    # setting connection to the database
    conn = database.connect()
    cursor = conn.cursor()

    # Specify the exact columns you want, separated by commas
    cursor.execute("SELECT quantity FROM stock WHERE is_printing_material = 'Yes' AND status = 'ACTIVE' ")
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if row:
        return row[0]
    return 0

"""
When it comes to database connection think in terms of ownership, then ask Who should own the connection?
>>update_stock<< opens the db conn and since >>log_stock_history<< also need it but it happens to be inside the 1st function
there is no need to open a new one you borrow from the existing one => log_stock_history(cursor)
"""
# Update paper quantity after printing process
def update_stock(cursor, pages, new_stock, is_printing_material):
    cursor.execute("""
        UPDATE stock
        SET quantity = ?
        WHERE is_printing_material = ? AND status = 'ACTIVE'
        RETURNING stock_id;
    """, (new_stock, is_printing_material))

    # Get the returned row FIRST
    stock_id = cursor.fetchone()[0]

    # record the change in the stock history
    action = "PRINT"
    quantity = pages
    remarks = f"{pages} pages printed"

    # ---------- calling log function and passing cursor in it ----------
    log_stock_history(cursor, stock_id, action, quantity, remarks)


# Record any activity done that involves stock
def log_stock_history(cursor, stock_id, action, quantity, remarks):
    # Insert the record in the table
    cursor.execute("""
        INSERT INTO stock_history (stock_id, action, quantity, remarks) 
        VALUES (?, ?, ?, ?)""",
        (stock_id, action, quantity, remarks))

def view_stock_history():
    # setting connection to the database
    conn = database.connect()
    cursor = conn.cursor()

    # displaying records that are inside the table
    cursor.execute("""      
        SELECT
            stock_history.history_id,
            stock.item_name,
            stock_history.action,
            stock_history.quantity,
            stock_history.remarks,
            stock_history.date_created
        FROM stock_history
        JOIN stock
        ON stock_history.stock_id = stock.stock_id
        """)
    rows = cursor.fetchall()

    if len(rows) == 0:
        print("No History yet.")
    else:
        print("\n===== STOCK HISTORY =====")
        for row in rows:
            print(
                f"ID: ({row[0]}) | Item Name: {row[1]} | Action: {row[2]} | Quantity: {row[3]} | Remarks: {row[4]} | Date: {row[5]} ")

    conn.close()

