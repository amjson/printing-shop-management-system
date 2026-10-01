# Building the “sales brain” here so that it remembers
# importing database file here so that anything to do with the database will use this reference
import database

def view_sales_menu():
    # ==========[ 1. Setting up the Menu ]==========
    print("1. Sales Summary")
    print("2. View All Sales")
    print("3. Sales for specific date")
    print("4. View Sales for specific customer")

    choice = input("\nSelect Option: ")

    if choice == "1":
        sales_summary()

    elif choice == "2":
        view_sales()

    elif choice == "3":
        specific_date_report()

    elif choice == "4":
        specific_customer_report()

    else:
        print("Invalid option.")

def view_sales():
    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 1. Retrieving all sales record ]==========
    cursor.execute("""      
        SELECT
            print_jobs.job_id,
            customers.name,
            print_jobs.pages,
            print_jobs.cost
        FROM print_jobs
        JOIN customers
        ON print_jobs.customer_id = customers.customer_id
    """)

    # ==========[ 2. Get all the records ]==========
    all_sales = cursor.fetchall()

    if not all_sales:
        print("No Sales have been done yet.")
        conn.close()
        return

    total_revenue = 0

    # ==========[ 4. looping through all the records ]==========
    print("\n==================== PRINT JOB HISTORY ====================")
    for sale in all_sales:
        job_id, customer_name, pages_printed, cost = sale
        print(f"Job ID: ({job_id}) | Customer: {customer_name} | Pages: {pages_printed} | Cost: {cost} KES \n")

        # adding the cost of each job as the loop continues
        total_revenue = total_revenue + cost

    print("\n-----------------------------------------------------------")

    # ==========[ 5. display the total revenue ]==========
    print(f"Total Revenue: {total_revenue} KES")

    conn.close()

def sales_summary():
    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 1. Counting total number of sales ]==========
    cursor.execute("SELECT COUNT(*) FROM print_jobs")
    total_jobs = cursor.fetchone()[0]

    # ==========[ 2. Calculating number of pages used in printing ]==========
    cursor.execute("SELECT SUM(pages) FROM print_jobs")
    total_pages = cursor.fetchone()[0]

    # ==========[ 3. Calculating the total revenue ]==========
    cursor.execute("SELECT SUM(cost) FROM print_jobs")
    total_revenue = cursor.fetchone()[0]

    # ==========[ 4. Calculating the average revenue ]==========
    cursor.execute("SELECT AVG(cost) FROM print_jobs")
    average_revenue = cursor.fetchone()[0]

    # ==========[ 5. If there is nothing in the table use => 0 ]==========
    total_pages = total_pages or 0
    total_revenue = total_revenue or 0
    average_revenue = average_revenue or 0

    # ==========[ 6. displaying sales summary ]==========
    print("\n====================================")
    print("SALES SUMMARY REPORT")
    print("====================================")

    print(f"Total Jobs: {total_jobs}")
    print(f"Total Pages Printed: {total_pages}")
    print(f"Total Revenue: {total_revenue} KES")
    print(f"Average Revenue Per Job: {average_revenue:.2f} KES")

    # Close the connection
    conn.close()

def specific_date_report():
    # ==========[ 1. Get User Input ]==========
    search_by_date = " ".join(input("Enter Date (YYYY-MM-DD): ").split())

    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 2. Counting total number of sales for a specific date ]==========
    cursor.execute("SELECT COUNT(job_id) FROM print_jobs WHERE DATE(date_created) = ?", (search_by_date,))
    jobs_on_this_day = cursor.fetchone()[0]

    # ==========[ 3. Calculating number of pages used on a specific date ]==========
    cursor.execute("SELECT SUM(pages) FROM print_jobs WHERE DATE(date_created) = ?", (search_by_date,))
    pages_on_this_day = cursor.fetchone()[0]

    # ==========[ 4. Calculating Total Revenue generated on a specific date ]==========
    cursor.execute("SELECT SUM(cost) FROM print_jobs WHERE DATE(date_created) = ?", (search_by_date,))
    revenue_on_this_day = cursor.fetchone()[0]

    # ==========[ 5. If there is nothing in the table use => 0 ]==========
    total_jobs = jobs_on_this_day or 0
    total_pages = pages_on_this_day or 0
    total_revenue = revenue_on_this_day or 0

    # ==========[ 6. display sales for the selected date ]==========
    print("\n====================================")
    print(f"SUMMARY REPORT OF {search_by_date} ")
    print("====================================")

    print(f"Total Jobs: {total_jobs}")
    print(f"Total Pages Printed: {total_pages}")
    print(f"Total Revenue: {total_revenue} KES")

    conn.close()

def specific_customer_report():
    # ==========[ 1. Get User Input ]==========
    customer_id = int(input("Enter customer ID: "))

    conn = database.connect()
    cursor = conn.cursor()

    # ==========[ 2. Confirm if the customer already exists ]==========
    cursor.execute("SELECT 1 FROM customers WHERE customer_id = ?", (customer_id,))
    customer_exist = cursor.fetchone()

    # ==========[ 3. when customer record dont exist ]==========
    if not customer_exist:
        print(f"Customer with ID {customer_id} does not exist.")
        conn.close()
        return

    # ==========[ 4. Show all print jobs for customer of this ID ]==========
    cursor.execute("""      
        SELECT
            customers.name,
            print_jobs,
            print_jobs.pages,
            print_jobs.cost
        FROM print_jobs
        JOIN customers
        ON print_jobs.customer_id = customers.customer_id
        WHERE customers.customer_id = ? 
        """, (customer_id,))

    customer_jobs = cursor.fetchall()

    # ==========[ 5. The customer has no print jobs yet ]==========
    if not customer_jobs:
        print("This customer has no print jobs yet.")
        conn.close()
        return

    total_pages = 0
    total_cost = 0

    print(f"\n==================== PRINTING REPORT HISTORY ==============\n")
    for print_job in customer_jobs:
        # ==========[ 6. loop through all the records ]==========
        customer_name, job_id, pages, cost = print_job

        print(f"Customer Name: {customer_name}")
        print(f"Job ID: {job_id}")
        print(f"Pages Printed: {pages}")
        print(f"Charges {cost} KES\n")

        total_pages = total_pages + pages   # add total pages as the loop continues
        total_cost = total_cost + cost      # add total cost of each job as the loop continues

    # ==========[ 8. displaying summary for specific customer ]==========
    print(f"Total Jobs: {len(customer_jobs)}")
    print(f"Total Page: {total_pages}")
    print(f"Total Revenue: {total_cost} KES")

    conn.close()