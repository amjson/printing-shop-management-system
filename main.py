# importing file names at the top so that anything to do with that specific file will use this reference,
# main.py acts as a receptionist that direct you to where you need to go
import database
import customer
import printing
import reports
import set_price
import stock

# function for handling registration of customers
def register_customer():
    customer.register_customer()

# function for handling viewing of customers
def view_customers():
    customer.view_customers()

# function for handling searching specific customer
def search_customer():
    customer.search_customer()

# function for handling updating existing customer record
def update_customer():
    customer.update_customer()

# function for handling deleting customers record
def delete_customer():
    customer.delete_customer()

# function for handling printing Price
def new_price():
    set_price.printing_price()

# function for handling printing jobs
def new_print_job():
    printing.new_print_job()

# function for handling adding/updating stock
def add_stock():
    stock.add_update_stock()

# function for handling viewing stock
def view_stock():
    stock.view_stock()

# function that handles viewing stock history
def view_stock_history():
    stock.view_stock_history()

# function that handles deleting stock
def delete_stock():
    stock.delete_stock()

# function for handling viewing sales
def view_sales():
    reports.view_sales_menu()

# Initializing the database whenever the program starts
database.create_tables()

# ======================================================================================================================
# creating the menu for displaying all the options
while True:
    print("\n====================================")
    print("PRINTING SHOP MANAGEMENT SYSTEM")
    print("====================================")

    print("1. Register Customer")
    print("2. View Customers")
    print("3. Search Customer")
    print("4. Update Customer")
    print("5. Delete Customer")
    print("6. Set Printing Price")
    print("7. Print Job")
    print("8. Add Stock")
    print("9. View Stock")
    print("10. View Stock History")
    print("11. Delete Stock")
    print("12. View Sales")
    print("13. Exit")

    choice = input("\nSelect Option: ")

    if choice == "1":
        register_customer()

    elif choice == "2":
        view_customers()

    elif choice == "3":
        search_customer()

    elif choice == "4":
        update_customer()

    elif choice == "5":
        delete_customer()

    elif choice == "6":
        new_price()

    elif choice == "7":
        new_print_job()

    elif choice == "8":
        add_stock()

    elif choice == "9":
        view_stock()

    elif choice == "10":
        view_stock_history()

    elif choice == "11":
        delete_stock()

    elif choice == "12":
        view_sales()

    elif choice == "13":
        print("Thank you for using the Printing Shop Management System.")
        print("Goodbye!!")
        break

    else:
        print("Invalid option.")