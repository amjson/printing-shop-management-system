# Building the “customer brain” here so that it remembers
# importing database file here so that anything to do with the database will use this reference
import database

# Registering a new customer
def register_customer():
    # ==========[ 1. Get User Input ]==========
    name = " ".join(input("Enter Customer name: ").split())                # remove leading/trailing spaces immediately
    phone = input("Enter Phone number: ").strip()

    # ==========[ 2. Validate Business Rules ]==========
    if not name and not phone:                                             # avoid accepting blank user input
        print("Error: Customer name and Phone cannot be empty.")

    # ==========[ 3. Set Database Connection ]==========
    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 4. Saving customer record ]==========
    cursor.execute("INSERT INTO customers (name, phone) VALUES (?, ?)", (name, phone))

    # ==========[ 5. Commit Changes ]==========
    conn.commit()
    conn.close()

    # ==========[ 6. Display Customers ]==========
    print("Customer registered successfully!")
    view_customers()

# Viewing customers records
def view_customers():
    # ==========[ 1. Set Database Connection ]==========
    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 2. Retrieving customers record ]==========
    cursor.execute("SELECT customer_id, name, phone, date_registered FROM customers")
    customers = cursor.fetchall()

    # ==========[ 2. Display records if there is any ]==========
    if customers:
        print("\n===== CUSTOMERS LIST =====\n")
        for customer in customers:
            # ==========[ 3. unpacking the tuple inside the loop ]==========
            customer_id, name, phone, date = customer
            print(f"Customer ID: ({customer_id}) Name: {name} | Phone: {phone} | Date: {date}")
    else:
        # ==========[ 4. Display this message if there is no record ]==========
        print("No customers Registered yet.")

    # ==========[ 5. Close the database connection ]==========
    conn.close()


# Searching for a specific customer
def search_customer():
    # ==========[ 1. Get User Input ]==========
    search_name = " ".join(input("Enter customer name: ").split())

    # ==========[ 2. Validate Business Rules ]==========
    if not search_name:  # avoid accepting blank user input
        print("Enter Customer name.")

    # ==========[ 3. Set Database Connection ]==========
    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 4. Retrieving customers record ]==========
    cursor.execute("SELECT * FROM customers WHERE name LIKE ? ", (f"%{search_name}%",))
    rows = cursor.fetchall()

    # ==========[ 5. Display records if there is any ]==========
    if rows:
        print("\n===== SEARCH RESULTS =====")
        for row in rows:
            print(f"Customer ID: ({row[0]}) Name: {row[1]} | Phone: {row[2]}")
    else:
        # ==========[ 6. Display this message if there is no record ]==========
        print("No matching customers found.")

    # ==========[ 7. Close the database connection ]==========
    conn.close()


# Updating customer records
def update_customer():
    # ==========[ 1. Get User Input ]==========
    customer_id = int(input("Enter customer ID to update: "))

    # ==========[ 2. Validate Business Rules ]==========
    if customer_id < 1:
        print("Error: Invalid Customer with ID")
    else:
        # ==========[ 3. Set Database Connection ]==========
        conn = database.connect()
        cursor = conn.cursor()

        # ==========[ 4. Checking if record with this ID exist ]==========
        cursor.execute("SELECT name, phone FROM customers WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()

        if customer:
            # ==========[ 5. Display current info and input to allow new info ]==========
            current_name, current_phone = customer  # Only unpack after you've confirmed something was returned.
            new_name = " ".join(input("New Name/Leave blank to keep current: ").split())
            new_phone =  input("New Phone/Leave blank to keep current: ").strip()

            # ==========[ 6. Validate or confirm the info to use in the database ]==========
            updated_name = current_name if new_name == "" else new_name    # if this input is blank use the current info
            updated_phone = current_phone if new_phone == "" else new_phone    # if this input is blank use the current info

            # ==========[ 7. Replace records in the database with the updated one ]==========
            cursor.execute("UPDATE customers SET name = ?, phone = ? WHERE customer_id = ?",
                (updated_name, updated_phone, customer_id))
        else:
            # ==========[ 8. If the record is not there ]==========
            print(f"Error: Customer with ID {customer_id} does not exist.")
            conn.close()
            return

        # ==========[ 9. Commit Changes ]==========
        conn.commit()

        print("Customer updated successfully!")
        view_customers()

        # ==========[ 10. Close the database connection ]==========
        conn.close()


# deleting customer record
def delete_customer():
    # ==========[ 1. Get User Input ]==========
    customer_id = int(input("Enter customer ID you want to Delete: "))

    # ==========[ 2. Validate Business Rules ]==========
    if customer_id < 1:
        print("Error: Invalid Customer with ID")
    else:
        # ==========[ 3. Set Database Connection ]==========
        conn = database.connect()
        cursor = conn.cursor()

        # ==========[ 4. Checking if record with this ID exist ]==========
        cursor.execute("SELECT 1 FROM customers WHERE customer_id = ?", (customer_id,))
        customer = cursor.fetchone()

        # ==========[ 5. If the record is not there ]==========
        if not customer:
            print(f"Error: Customer with ID {customer_id} does not exist.")
            conn.close()
            return

        # ==========[ 6. Confirmation message ]==========
        print("Do you want to DELETE this customer!\n")
        print("1. Proceed")
        print("2. Cancel")

        choice = input("\nSelect Option: ")

        # ==========[ 7. Early exit ]==========
        if choice not in ("1", "2"):
            print("Invalid option.")
            conn.close()
            return

        proceed = "Yes" if choice == "1" else "No"

        # ==========[ 8. Remove the record from the program ]==========
        if proceed == "Yes":
            cursor.execute("DELETE FROM customers WHERE customer_id = ?", (customer_id,))

            print("Customer deleted successfully!")
            conn.commit()
            view_customers()

        else:
            print("Process has been cancelled!")

        # ==========[ 10. Commit changes and Close connection ]==========
        conn.close()