# Building the “customer brain” here so that it remembers
# importing database file here so that anything to do with the database will use this reference
import database

# Setting printing price
def printing_price():
    # ==========[ 1. Get User Input ]==========
    setting_name = "price_per_page"
    price_tag = int(input("Set printing price per page: "))

    if price_tag <= 0:
        print("Price tag must be greater than 0")
        return

    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 2. Check if the item exist ]==========
    cursor.execute("SELECT 1 FROM settings_price WHERE settings_name = ?", (setting_name,))
    exists = cursor.fetchone()

    if exists:
        # ==========[ 3. Proceed with the update ]==========
        cursor.execute("UPDATE settings_price SET price_tag = ? WHERE settings_name = ?", (price_tag, setting_name))
    else:
        # ==========[ 4. Insert new record ]==========
        cursor.execute("""
            INSERT INTO settings_price (settings_name, price_tag) 
            VALUES (?, ?)""",
            (setting_name, price_tag))

    # ==========[ 5. Commit N Save Changes ]==========
    conn.commit()
    conn.close()

    print("Printing Price has been set successfully!")

# Read printing_price from the database
def get_print_price():
    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ Fetching price column ]==========
    cursor.execute("SELECT price_tag FROM settings_price WHERE settings_name = ?", ("price_per_page",))
    current_price = cursor.fetchone()[0]

    cursor.close()
    conn.close()
    return current_price






