import tkinter
from tkinter import ttk
from tkinter import messagebox

from database import check_customer_id
from database import check_current_stock
from database import current_printing_price
from database import save_print_price
from database import view_price_table
from database import delete_price_in_database
from database import update_price_in_database
from database import record_print_job
from database import view_print_job
from database import search_print_jobs

# ====================[ Shared Variables ]===================
parent_window = None   # Parent window reference
close_callback = None  # Create a place to store the function that should be called when this window closes.
active_button = None   # What is currently selected? Initially Nothing
selected_price = None  # Which Price is selected? Initially it should be None

# ============================================================
# =================== [ Open Print Window ] ==================
# ============================================================
def open_print_window(parent, on_close):
    # ---------- 1. This window receives two things everytime its opens:
    # Dashboard/root reference and Closing function reference.
    global parent_window, close_callback
    parent_window = parent
    close_callback = on_close

    # ---------- [ 2. Initializing this Window ]
    print_window_interface = tkinter.Toplevel(parent)

    # ---------- [ 3. Title and size ]
    print_window_interface.title("Printing Shop Management System")
    print_window_interface.resizable(False, False)
    window_width = 900  # windows width
    window_height = 600  # widows height

    # ---------- [ 4. Actual Screen Size ]
    screen_width = print_window_interface.winfo_screenwidth()
    screen_height = print_window_interface.winfo_screenheight()

    # ---------- [ 5. Coordinates for centering the window ]
    x = (screen_width - window_width) // 2  # splits the answer/space equally into left/right
    y = (screen_height - window_height) // 2  # splits the answer/space equally into top/bottom

    # ---------- [ 6. Center the window using X/Y coordinates ]
    print_window_interface.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # ---------- [ 7. Closing the window ]
    def close_print_window():
        parent_window.deiconify()          # notify => Dashboard
        close_callback()                   # refer => closing function
        print_window_interface.withdraw()  # hide this window

    # ---------- [ 8. Tie Closing function to X button ]
    print_window_interface.protocol("WM_DELETE_WINDOW", close_print_window)

    # ===================[ 1. Title Label ]=================
    header_frame = tkinter.Frame(print_window_interface, height=50)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    title_label = tkinter.Label(header_frame, text="PRINTING MANAGEMENT", font=("Segoe UI", 16, "bold"))
    title_label.pack(side="left", padx=20, pady=15)

    # ====================[ 2. Main Body ]===================
    body_frame = tkinter.Frame(print_window_interface)
    body_frame.pack(fill="both", expand=True)

    # ===================[ 3. Left Frame ]===================
    navigation_frame = tkinter.Frame(body_frame, width=190, bg="#EAEAEA")
    navigation_frame.pack(side="left", fill="y")
    navigation_frame.pack_propagate(False)

    # Navigation Buttons & their functions
    def set_active_button(button):
        global active_button  # Which button is active.

        if active_button is not None:  # If nothing is selected Nothing happens.
            active_button.config(bg="SystemButtonFace")  # Return previously selected button back to normal appearance.

        button.config(bg="#D6EAF8")  # Highlight the selected button
        active_button = button  # Remember this button next time

    def show_page(page):
        job_page.pack_forget()
        view_page.pack_forget()
        price_page.pack_forget()
        manage_price_page.pack_forget()
        page.pack(fill="both", expand=True)  # Means => Show whichever page I receive.

    # Navigation buttons
    job_button = tkinter.Button(navigation_frame, text="New Job", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(job_button), show_page(job_page)))
    job_button.pack(pady=(30, 15))

    view_button = tkinter.Button(navigation_frame, text="View Jobs", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(view_button), show_page(view_page), load_print_job()))
    view_button.pack(pady=15)

    price_button = tkinter.Button(navigation_frame, text="Printing Price", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(price_button), show_page(price_page)))
    price_button.pack(pady=15)

    manage_price_button = tkinter.Button(navigation_frame, text="Manage Print Price", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(manage_price_button), show_page(manage_price_page), load_printing_price()))
    manage_price_button.pack(pady=15)

    # ===================[ 4. Right Frame ]===================
    right_frame = tkinter.Frame(body_frame, bg="white")
    right_frame.pack(side="left", fill="both", expand=True)

    # ========== Creating Workspace Container ==========
    workspace_frame = tkinter.Frame(right_frame, bg="white")
    workspace_frame.pack(fill="both", expand=True)

    # ====================================================
    # 01. First Page => Print New Job
    # ====================================================
    job_page = tkinter.Frame(workspace_frame, bg="white")

    # Creating Form Container
    form_frame = tkinter.Frame(job_page, bg="white")
    form_frame.pack(padx=40, pady=30, anchor="nw")

    # Page Title
    print_title = tkinter.Label(form_frame, text="CREATE PRINTING JOB", font=("Segoe UI", 20, "bold"), bg="white")
    print_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 25))

    print_info = tkinter.Label(form_frame, text="Complete the information below to print a new job", font=("Segoe UI", 12), bg="white")
    print_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 20))

    # Customer ID => Label
    customer_label = tkinter.Label(form_frame, text="Enter Customer ID", font=("Segoe UI", 11), bg="white")
    customer_label.grid(row=2, column=0, sticky="w", pady=8)

    # Customer ID => Entry
    customer_entry = tkinter.Entry(form_frame, font=("Segoe UI", 11), width=35)
    customer_entry.grid(row=2, column=1, padx=(20, 0), pady=8, sticky="w")

    # Number of Pages => Label
    pages_label = tkinter.Label(form_frame, text="Number of Pages", font=("Segoe UI", 11), bg="white")
    pages_label.grid(row=3, column=0, sticky="w", pady=8)

    # Number of Pages => Entry
    pages_entry = tkinter.Entry(form_frame, font=("Segoe UI", 11), width=35)
    pages_entry.grid(row=3, column=1, padx=(20, 0), pady=8, sticky="w")

    # Printing Material => Label
    print_type_label = tkinter.Label(form_frame, text="Printing Type", font=("Segoe UI", 11), bg="white")
    print_type_label.grid(row=4, column=0, sticky="w", pady=8)

    # Printing Material => Dropdown menu
    printing_type = ttk.Combobox(form_frame, width=43, state="readonly")
    printing_type["values"] = ("Coloured", "Black & White")
    printing_type.current(0)
    printing_type.grid(row=4, column=1, padx=(20, 0), pady=8, sticky="w")

    # function and logic for printing
    def validate_customer_id(customer):
        if customer == "":
            messagebox.showerror("Missing Information", "Please enter the customer's ID.")
            return False
        return True

    def validate_page_numbers(pages):
        if pages == "":
            messagebox.showerror("Missing Information", "Please enter number of pages.")
            return False

        if not pages.isdigit():
            messagebox.showerror("Incorrect Format", "Page Number is incorrect format")
            return False
        pages = int(pages)

        if pages <= 0:
            messagebox.showerror("Incorrect Format", "Page Number cannot be Less than or Zero")
            return False
        return True

    def printing_process():
        # getting info from the form
        customer_id = customer_entry.get().strip()
        number_of_pages = pages_entry.get().strip()
        print_type_selected = printing_type.get()

        # 2. Validation
        if not validate_customer_id(customer_id): return
        if not validate_page_numbers(number_of_pages): return

        # 01. check existence of the customer id
        confirm_id = check_customer_id(customer_id)

        if not confirm_id:
            messagebox.showerror("Error", "This Customer ID is not recognised")
            return

        # 02. getting stock quantity from the database
        current_stock = check_current_stock()

        pages_required = int(number_of_pages)
        if pages_required > current_stock:
            messagebox.showerror("Error", "Insufficient Paper Stock")
            return

        # 03 type of printing & price calculation
        check_result = current_printing_price(print_type_selected)

        if check_result:
            price = check_result[0]
            printing_cost = price * pages_required

            # 05. Record transaction
            print_successful = record_print_job(customer_id, pages_required, print_type_selected, printing_cost)

            # 06. Give feedback
            if print_successful:
                messagebox.showinfo("Success", "Printing Operation completed successfully.")

                # ----- reset program to normal state
                clear_form()  # Clear form
                show_page(view_page)  # switch to view page
                load_print_job()  # Reload available printing job
            else:
                # When something goes wrong give this feedback
                messagebox.showerror("Operation Failed", "Printing Operation could not be completed.")
        else:
            # if price and print_type are not available
            messagebox.showerror("Error", "Pricing information is not available.")
            return

    # function for clearing the form
    def clear_form():
        customer_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
        pages_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
        printing_type.current(0)

    # ======== Button Frame
    button_frame = tkinter.Frame(form_frame, bg="white")
    button_frame.grid(row=5, column=1, sticky="w", pady=(25, 0))

    # Print Button
    save_button = tkinter.Button(button_frame, text="Print", width=12, command=printing_process)
    save_button.pack(side="left", padx=(0, 30))

    # ====================================================
    # 02. Second Page => View All Job
    # ====================================================
    view_page = tkinter.Frame(workspace_frame, bg="white")

    # ======= [ 1. load available print jobs into the table ]
    def load_print_job():
        for row in print_job_table.get_children():  # Clear the current table before loading fresh records
            print_job_table.delete(row)

        printing_jobs = view_print_job()  # Get customers from SQLite

        # Add each record to the table
        for job in printing_jobs:
            print_job_table.insert("", "end", values=job)

    # ======= [ 2. search print job for a specific customer ]
    def search_for_specific_customer():
        search_text = search_entry.get().strip()  # Read what the receptionist typed.

        if search_text == "":  # Check whether they typed something.
            messagebox.showerror("Missing Information", "Please enter Customer Name.")
            return

        printing_jobs = search_print_jobs(search_text)  # Ask the database to search.

        if not printing_jobs:  # if the customer is not there display a message
            messagebox.showinfo("Search Result", "No customer found.")
            return

        for row in print_job_table.get_children():  # Clear the table first
            print_job_table.delete(row)

        for job in printing_jobs:  # Database returns matching customers.
            print_job_table.insert("", "end", values=job)

    # ======= [ 3. Sorting based on Name, print type or date column ]
    def sort_print_jobs():
        selected_option = sort_options.get()  # Ask What did the receptionist choose?
        selected_order = order_options.get()  # Ask What direction did the receptionist choose?

        column = sort_columns[selected_option]  # The dictionary translates the first choice
        order = sort_orders[selected_order]  # The dictionary translates the second choice

        customer_sort = view_print_job(column, order)  # Send the translated info to the Database

        for row in print_job_table.get_children():
            print_job_table.delete(row)  # Clear the old table.

        for print_job in customer_sort:  # Put the newly sorted records into the table.
            print_job_table.insert("", "end", values=print_job)

    # ========= Create frame for the table
    table_frame = tkinter.Frame(view_page, bg="white")

    # ---------- [ Search Utility ]
    search_frame = tkinter.Frame(view_page, bg="white")
    search_frame.pack(fill="x", padx=20, pady=10)

    # Search Label
    search_label = tkinter.Label(search_frame, text="Search Customer:", font=("Segoe UI", 11), bg="white")
    search_label.pack(side="left")

    # Search Entry
    search_entry = tkinter.Entry(search_frame, font=("Segoe UI", 11), width=22)
    search_entry.pack(side="left", padx=10)

    # Search Button
    search_button = tkinter.Button(search_frame, text="Search", width=11, command=search_for_specific_customer)
    search_button.pack(side="left")

    # ---------- [ Sort Utility ]
    # Sort frame
    sort_frame = tkinter.Frame(view_page, bg="white")
    sort_frame.pack(fill="x", padx=20, pady=(0, 10))

    sort_label = tkinter.Label(sort_frame, text="Sort Customers:", font=("Segoe UI", 11), bg="white")
    sort_label.pack(side="left")

    # Sort Options
    sort_options = ttk.Combobox(sort_frame, width=15, state="readonly")
    sort_options["values"] = ("Full Name", "Type", "Date")

    sort_options.current(2)  # Start with Date
    sort_options.pack(side="left", padx=5)

    # This is our translation dictionary => sort_columns["Full Name"] produces fullname
    # what the receptionist see (left side) and what the database knows (right side)
    sort_columns = {
        "Full Name": "fullname",
        "Type": "print_type",
        "Date": "date_created"
    }

    # Create the order dictionary
    # The receptionist sees Ascending and  SQLite understands ASC
    sort_orders = {
        "Ascending": "ASC",
        "Descending": "DESC"
    }

    # ascending/descending combo box
    order_options = ttk.Combobox(sort_frame, width=12, state="readonly")
    order_options["values"] = ("Ascending", "Descending")

    order_options.current(0)
    order_options.pack(side="left", padx=5)

    # sort button
    sort_button = tkinter.Button(sort_frame, text="Sort", width=10, command=sort_print_jobs)
    sort_button.pack(side="left", padx=5)

    # Display the table area
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Create the Treeview
    print_job_table = ttk.Treeview(table_frame, columns=("Customer Name", "Type", "Pages", "Cost", "Date"), show="headings")

    # Create the headings
    print_job_table.heading("Customer Name", text="Customer Name")
    print_job_table.heading("Type", text="Type")
    print_job_table.heading("Pages", text="Pages")
    print_job_table.heading("Cost", text="Cost")
    print_job_table.heading("Date", text="Date")

    # Set the column widths
    print_job_table.column("Customer Name", width=100)
    print_job_table.column("Type", width=150)
    print_job_table.column("Pages", width=50)
    print_job_table.column("Cost", width=50)
    print_job_table.column("Date", width=100)

    # display the table
    print_job_table.pack(fill="both", expand=True)


    # ====================================================
    # 03. Third Page => Printing Price
    # ====================================================
    price_page = tkinter.Frame(workspace_frame, bg="white")

    # Creating Form Container
    form_frame = tkinter.Frame(price_page, bg="white")
    form_frame.pack(padx=40, pady=30, anchor="nw")

    # Page Title
    price_title = tkinter.Label(form_frame, text="Set Printing Price", font=("Segoe UI", 20, "bold"), bg="white")
    price_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 25))

    price_info = tkinter.Label(form_frame, text="Use the form below to set the printing price", font=("Segoe UI", 12), bg="white")
    price_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 20))

    price_label = tkinter.Label(form_frame, text="Price Per Page", font=("Segoe UI", 11), bg="white")
    price_label.grid(row=2, column=0, sticky="w", pady=8)

    price_entry = tkinter.Entry(form_frame, font=("Segoe UI", 11), width=35)
    price_entry.grid(row=2, column=1, padx=(20, 0), pady=8, sticky="w")

    print_type_label = tkinter.Label(form_frame, text="Print Type", font=("Segoe UI", 11), bg="white")
    print_type_label.grid(row=3, column=0, sticky="w", pady=8)

    # Customer Type => Dropdown menu
    print_type = ttk.Combobox(form_frame, width=43, state="readonly")
    print_type["values"] = ("Black & White", "Coloured")
    print_type.current(0)
    print_type.grid(row=3, column=1, padx=(20, 0), pady=8, sticky="w")

    # ======== Button Frame
    button_frame = tkinter.Frame(form_frame, bg="white")
    button_frame.grid(row=4, column=1, sticky="w", pady=(25, 0))

    # validate the price
    def validate_price(set_price):
        if set_price == "":
            messagebox.showerror("Missing Information", "Please enter Printing Price")
            return False

        if not set_price.isdigit():
            messagebox.showerror("Incorrect Format", "Printing Price is incorrect format")
            return False

        price_number = int(set_price)

        if price_number <= 0:
            messagebox.showerror("Incorrect Format", "Price cannot be Less than or Zero")
            return False
        return True

    # function for saving info
    def save_price():
        # 1. Get user input
        printing_price = price_entry.get().strip()
        print_type_selected = print_type.get()

        # 2. Validation
        if not validate_price(printing_price): return

        # 3. Save the info
        success = save_print_price(printing_price, print_type_selected)

        if success:
            # If everything is okay
            messagebox.showinfo("Success", "Printing Price saved successfully")
            clear_price_form()
            load_printing_price()
            show_page(manage_price_page)
        else:
            messagebox.showerror("Error", "Printing Price could not be saved")

    # Save Button
    save_button = tkinter.Button(button_frame, text="Save", width=12, command=save_price)
    save_button.pack(side="left", padx=(0, 30))

    # function for clearing the form
    def clear_price_form():
        price_entry.delete(0, tkinter.END)
        printing_type.current(0)

    # Clear Button
    clear_button = tkinter.Button(button_frame, text="Clear", width=12, command=clear_price_form)
    clear_button.pack(side="left")

    # ====================================================
    # 04. Fourth Page => Printing Price Manage
    # ====================================================
    manage_price_page = tkinter.Frame(workspace_frame, bg="white")

    def select_price(event):
        global selected_price

        selected = view_price.focus()

        if selected:
            selected_price = view_price.item(selected)["values"]
        else:
            selected_price = None

    def load_printing_price():
        for row in view_price.get_children():
            view_price.delete(row)  # Before writing anything new first erase what's in the table (Refreshing)

        history = view_price_table()  # Get history info from the database

        # Add each record to the table
        for record in history:
            view_price.insert("", "end", values=record)

    def delete_selected_price():
        global selected_price

        if selected_price is None:  # Check whether anything is selected.
            messagebox.showerror("Selection Required", "Please select any price first.")
            return

        confirm = messagebox.askyesno("Confirm the operation", "Do you want to Delete the selected Price?")

        if not confirm:  # If option was not yes, stop the operation
            return

        price_id = selected_price[0]  # get price id
        confirm = delete_price_in_database(price_id)  # calling deleting function from the database

        if confirm:
            messagebox.showinfo("Deletion Successful", "Printing Price deleted successfully.")  # If everything is okay give a feedback
            selected_price = None
            load_printing_price()
            show_page(manage_price_page)
        else:
            messagebox.showerror("Error", "Printing Price could not be deleted")

    # open registration form in updating mode
    def open_selected_price():
        if selected_price is None:
            messagebox.showerror("Selection Required", "Please select any price first.")
            return

        show_page(price_page)     # reuse the existing form interface
        load_selected_price()  # load the info of the selected price into that form

    # loading selected info into the form => update mode
    def load_selected_price():
        global selected_price

        if selected_price is None:
            return

        price_title.config(text="Update Price")
        price_info.config(text="Edit the Printing Price information below")

        price_entry.delete(0, tkinter.END)
        price_entry.insert(0, selected_price[1])
        print_type.set(selected_price[2])

        save_button.config(text="Update")
        save_button.config(command=update_selected_price)

    # Updating the printing price
    def update_selected_price():
        global selected_price

        price_id = selected_price[0]
        new_price = price_entry.get()

        if not validate_price(new_price): return

        # call the database function that will update this info
        feedback = update_price_in_database(new_price, price_id)

        if feedback:
            messagebox.showinfo("Update Successful", "Printing Price has been Updated successfully.")  # If everything is okay give a feedback
            # ----- reset program to normal state
            selected_price = None
            reset_price_form()     # Restore form to Add Mode
            clear_price_form()     # Clear form
            show_page(manage_price_page)  # switch to view page
            load_printing_price()  # Reload customers info
        else:
            messagebox.showerror("Error", "Printing Price could not be Updated")

    # Revert anything that changed when switching to Update Mode
    def reset_price_form():
        price_title.config(text="Set Printing Price")
        price_info.config(text="Use the form below to set the printing price")

        price_entry.delete(0, tkinter.END)  # clear this field
        print_type.current(0)                     # reset the selection

        save_button.config(text="Save")  # button label
        save_button.config(command=save_price)  # button command

    # ---------- [ update/delete Utility ]
    button_frame = tkinter.Frame(manage_price_page, bg="white")
    button_frame.pack(fill="x", padx=20, pady=10)

    # Update Button
    update_button = tkinter.Button(button_frame, text="Update Price", width=15, command=open_selected_price)
    update_button.pack(side="left", padx=10)

    # Delete Button
    delete_button = tkinter.Button(button_frame, text="Delete Price", width=15, command=delete_selected_price)
    delete_button.pack(side="left", padx=0)

    # ---------- [ Frame for the table ]
    price_frame = tkinter.Frame(manage_price_page, bg="white")
    price_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------- [ Creating the Treeview ]
    view_price = ttk.Treeview(price_frame, columns=("ID", "Price Per Page", "Print Type"), show="headings")
    view_price.bind("<<TreeviewSelect>>", select_price)

    # ---------- [ Creating table headings ]
    view_price.heading("ID", text="Price ID")
    view_price.heading("Price Per Page", text="Price Per Page")
    view_price.heading("Print Type", text="Print Type")

    # ---------- [ Set the column widths ]
    view_price.column("ID", width=100)
    view_price.column("Price Per Page", width=100)
    view_price.column("Print Type", width=100)

    # display the table
    view_price.pack(fill="both", expand=True)

    # ===================[ Show this page only after all the others exist  ]===================
    show_page(job_page)