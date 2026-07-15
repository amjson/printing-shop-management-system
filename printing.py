# Building the “printing job brain” here so that it remembers
# importing database file here so that anything to do with the database will use this reference
import database
import set_price
import stock

def new_print_job():
    # ==========[ 1. Get User Input ]==========
    customer_id = input("Enter Customer ID: ")
    pages = int(input("Number of pages: "))

    # ==========[ 2. Initialize price to the price in the table ]==========
    current_price = set_price.get_print_price()

    # ==========[ 3. Initialize stock to the quantity in the table ]==========
    current_stock = stock.get_stock()

    # ==========[ 4. Compare Available stock with pages to be printed ]==========
    if pages > current_stock:
        print("Insufficient paper stock.")
    else:
        cost = pages * current_price         # calculating the cost

        # setting connection to the database
        conn = database.connect()
        cursor = conn.cursor()

        # validating the customer_id
        cursor.execute("SELECT 1 FROM customers WHERE customer_id = ? ", (customer_id,))
        row = cursor.fetchone()

        if not row:
            # display invalid customer id
            print("------------------------------- \n")
            print("Customer with this ID not found")
        else:
            # Proceed with the adding the details in printing_jobs table
            cursor.execute("""
                INSERT INTO print_jobs (customer_id, pages, cost) 
                VALUES (?, ?, ?)""",
                (customer_id, pages, cost))

            # if printing was successful reduce Stock
            new_stock = current_stock - pages                         # reduce current quantity by no. of pages printed

            print(f"\nPrinting process completed successfully.\n")
            print("------------------------------- \n")

            print("Initial paper stock: ", current_stock)             # display current paper stock
            print("No. of Papers used: ", pages)                      # display no. of pages used
            print("New stock: ", new_stock)                           # display the new paper stock

            # display feedback to the user
            print("\n------------------------------- \n")
            print(f"Job recorded successfully.")
            print(f"Total Cost: {cost} KES")

            if new_stock < 30:
                print("\nWARNING!! You need to do a restock")

            # Call the function from the other file
            stock.update_stock(cursor, pages, new_stock, "Yes")    # updating the stock table to match new paper stock

            # commit the changes and close the connection
            conn.commit()
            conn.close()
