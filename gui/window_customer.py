import tkinter
import datetime
from tkinter import ttk
from tkinter import messagebox
from database import get_last_customer_id
from database import save_customer_to_database
from database import fetch_customer_metrics
from database import fetch_financial_metrics
from database import recent_activity_history
from database import get_all_customers
from database import get_customer_existence
from database import search_customers
from database import update_customer_in_database
from database import delete_customer_in_database
from database import view_customer_history

# ====================[ Shared Variables ]===================
parent_window = None      # Parent window reference
close_callback = None     # Create a place to store the function that should be called when this window closes.
active_button = None      # What is currently selected? Initially Nothing
selected_customer = None  # Which record is selected? Initially it should be None

# ============================================================
# ================== [ Open Customer Window ] ================
# ============================================================
def open_customer_window(parent, on_close):
    # ---------- 1. This window receives two things everytime its opens:
    # Dashboard/root reference and Closing function reference.
    global parent_window, close_callback
    parent_window = parent
    close_callback = on_close

    # ---------- [ 2. Initializing this Window ]
    customer_window_interface = tkinter.Toplevel(parent)

    # ---------- [ 3. Title and size ]
    customer_window_interface.title("Printing Shop Management System")
    customer_window_interface.resizable(False, False)
    window_width = 900  # windows width
    window_height = 600  # widows height

    # ---------- [ 4. Actual Screen Size ]
    screen_width = customer_window_interface.winfo_screenwidth()
    screen_height = customer_window_interface.winfo_screenheight()

    # ---------- [ 5. Coordinates for centering the window ]
    x = (screen_width - window_width) // 2  # splits the answer/space equally into left/right
    y = (screen_height - window_height) // 2  # splits the answer/space equally into top/bottom

    # ---------- [ 6. Center the window using X/Y coordinates ]
    customer_window_interface.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # ---------- [ 7. Closing the window ]
    def close_customer_window():
        parent_window.deiconify()             # notify => Dashboard
        close_callback()                      # refer => closing function
        customer_window_interface.withdraw()  # hide this window

    # ---------- [ 8. Tie Closing function to X button ]
    customer_window_interface.protocol("WM_DELETE_WINDOW", close_customer_window)

    # ===================[ 1. Title Label ]=================
    header_frame = tkinter.Frame(customer_window_interface, height=50)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    title_label = tkinter.Label(header_frame, text="CUSTOMER MANAGEMENT", font=("Segoe UI", 16, "bold"))
    title_label.pack(side="left", padx=20, pady=15)

    # ====================[ 2. Main Body ]===================
    body_frame = tkinter.Frame(customer_window_interface)
    body_frame.pack(fill="both", expand=True)

    # ===================[ 3. Left Frame ]===================
    navigation_frame = tkinter.Frame(body_frame, width=190, bg="#EAEAEA")
    navigation_frame.pack(side="left", fill="y")
    navigation_frame.pack_propagate(False)

    # Navigation Buttons & their functions
    def set_active_button(button):
        global active_button  # Change which sidebar button is active.

        if active_button is not None:      # has a button already been selected? If the answer is No Nothing happens.
            active_button.config(bg="SystemButtonFace")  # Return the previously selected button back to its normal appearance.

        button.config(bg="#D6EAF8")  # Highlight the newly selected button
        active_button = button  # Remember this button for next time

    def show_page(page):
        overview_page.pack_forget()  # Means => Hide Overview.
        register_page.pack_forget()  # Means => Hide Register.
        view_page.pack_forget()      # Means => Hide View.
        history_page.pack_forget()      # Means => Hide View.
        page.pack(fill="both", expand=True)  # Means => Show whichever page I receive.

    # Home Button
    overview_button = tkinter.Button(
        navigation_frame, text="Overview", font=("Segoe UI", 11), width=18,
        command=lambda: (set_active_button(overview_button),
                         show_page(overview_page),
                         customer_metrics_controller_display(),
                         financial_metrics_controller_display(),
                         load_recent_activity_history()
                         )
    )
    overview_button.pack(pady=(30, 15))

    # Register Button
    register_button = tkinter.Button(navigation_frame, text="Register Customer", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(register_button), show_page(register_page)) )
    register_button.pack(pady=15)

    #View Button
    view_button = tkinter.Button(navigation_frame, text="View Customers", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(view_button), show_page(view_page), load_customers()))
    view_button.pack(pady=15)

    #History Button
    history_button = tkinter.Button(navigation_frame, text="History Customers", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(history_button), show_page(history_page), load_customer_history()))
    history_button.pack(pady=15)

    # ===================[ 4. Right Frame ]===================
    right_frame = tkinter.Frame(body_frame, bg="white")
    right_frame.pack(side="left", fill="both", expand=True)

    # ========== Creating Workspace Container ==========
    workspace_frame = tkinter.Frame(right_frame, bg="white")
    workspace_frame.pack(fill="both", expand=True)

    # ====================================================
    # 01. Create the First Page => overview
    # ====================================================
    overview_page = tkinter.Frame(workspace_frame, bg="white")

    current_time = datetime.datetime.now()
    hour = current_time.hour

    if hour < 12: greeting = "Good Morning 👋"
    elif hour < 18: greeting = "Good Afternoon ☀️"
    else: greeting = "Good Evening 🌙"
    today = current_time.strftime("%A, %d %B %Y")

    # welcome message
    welcome_label = tkinter.Label(overview_page, text="Welcome back to Printing Shop Management System", font=("Segoe UI", 14, "bold"), bg="white")
    welcome_label.pack(anchor="w", padx=20, pady=(35, 0))

    # 1. Main Header Row Container
    header_container = tkinter.Frame(overview_page, bg="white")
    header_container.pack(fill="x", padx=20, pady=(0, 5))

    # 2. Left Side Content (Greeting)
    greeting_label = tkinter.Label(header_container, text=greeting, font=("Segoe UI", 11, "bold"), fg="#2D3748", bg="white")
    greeting_label.pack(side="left", anchor="w")

    # 3. Right Side Content (Date)
    date_label = tkinter.Label(header_container, text=today, font=("Segoe UI", 10), fg="gray", bg="white")
    date_label.pack(side="right", anchor="e")

    # =================== [ Customer Overview Section ]
    cards_label = tkinter.Frame(overview_page, bg="white")
    cards_label.pack(fill="x", padx=20, pady=(20, 0))

    # =========== [ Display Controller => Customer Metrics ]
    def customer_metrics_controller_display():
        metrics_controller = fetch_customer_metrics()

        if metrics_controller:
            # Unpack the row into descriptive variables
            db_total, db_active, db_inactive = metrics_controller

            # Safe fallback to 0 if the table is empty and returns None
            metrics_total = db_total or 0
            metrics_active = db_active or 0
            metrics_inactive = db_inactive or 0

            # displaying the values into the labels
            lbl_total_val.config(text=str(metrics_total))
            lbl_active_val.config(text=str(metrics_active))
            lbl_inactive_val.config(text=str(metrics_inactive))

    # =========== [ Display Controller => Financial Performance ]
    def financial_metrics_controller_display():
        financial_controller = fetch_financial_metrics()

        if financial_controller:
            # Unpack the row into descriptive variables
            db_revenue, db_average = financial_controller

            # Safe fallback to 0 if the table is empty and returns None
            weekly_revenue = f"{db_revenue}" if db_revenue else "0"
            weekly_average = f"{db_average:.2f}" if db_average else "0.00"

            # displaying the values into the labels
            lbl_revenue_val.config(text=str(weekly_revenue))
            lbl_average_val.config(text=str(weekly_average))

    # --- LEFT Column Container ---
    left_side_label = tkinter.Frame(cards_label, bg="white")
    left_side_label.pack(side="left", anchor="nw")

    tkinter.Label(left_side_label, text="Customer Metrics", font=("Segoe UI", 12, "bold"), fg="#1A202C", bg="white").pack(anchor="w", padx=8, pady=(5,8))

    # --- RIGHT Column Container ---
    right_side_frame = tkinter.Frame(cards_label, bg="white")
    right_side_frame.pack(side="right", anchor="ne")

    tkinter.Label(right_side_frame, text="Weekly Financial Performance", font=("Segoe UI", 12, "bold"), fg="#1A202C", bg="white").pack(anchor="e", padx=8, pady=(5,8))

    # Container background matches your page background
    cards_container = tkinter.Frame(overview_page, bg="white")
    cards_container.pack(fill="x", padx=20)

    # --- LEFT GROUP: Customer Metrics ---
    left_side_frame = tkinter.Frame(cards_container, bg="white")
    left_side_frame.pack(side="left", anchor="nw")

    # 1. Total Customers Card
    card_total = tkinter.Frame(left_side_frame, bg="#F5F5F5", width=107, height=80)
    card_total.pack(side="left", padx=8)
    card_total.pack_propagate(False)

    lbl_total_val = tkinter.Label(card_total, text=" ", font=("Segoe UI", 13, "bold"), bg="#F5F5F5")
    lbl_total_val.pack(anchor="w", padx=15, pady=(6, 2))
    tkinter.Label(card_total, text="Total", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=15)

    # 2. Active Customers Card
    card_active = tkinter.Frame(left_side_frame, bg="#F5F5F5", width=107, height=80)
    card_active.pack(side="left", padx=8)
    card_active.pack_propagate(False)

    lbl_active_val = tkinter.Label(card_active, text=" ", font=("Segoe UI", 13, "bold"), bg="#F5F5F5")
    lbl_active_val.pack(anchor="w", padx=15, pady=(6, 2))
    tkinter.Label(card_active, text="Active", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=15)

    # 3. Inactive Customers Card
    card_inactive = tkinter.Frame(left_side_frame, bg="#F5F5F5", width=107, height=80)
    card_inactive.pack(side="left", padx=8)
    card_inactive.pack_propagate(False)

    lbl_inactive_val = tkinter.Label(card_inactive, text="-", font=("Segoe UI", 13, "bold"), bg="#F5F5F5")
    lbl_inactive_val.pack(anchor="w", padx=15, pady=(6, 2))
    tkinter.Label(card_inactive, text="Inactive", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=15)

    # --- RIGHT GROUP: Financial Performance ---
    right_side_frame = tkinter.Frame(cards_container, bg="white")
    right_side_frame.pack(side="right", anchor="ne")

    # 4. Weekly Revenue Card
    card_revenue = tkinter.Frame(right_side_frame, bg="#F5F5F5", width=107, height=80)
    card_revenue.pack(side="left", padx=8)
    card_revenue.pack_propagate(False)

    lbl_revenue_val = tkinter.Label(card_revenue, text=" ", font=("Segoe UI", 11, "bold"), bg="#F5F5F5")
    lbl_revenue_val.pack(anchor="w", padx=15, pady=(6, 2))
    tkinter.Label(card_revenue, text="Revenue", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=15)

    # 5. Weekly Average Card
    card_average = tkinter.Frame(right_side_frame, bg="#F5F5F5", width=107, height=80)
    card_average.pack(side="left", padx=8)
    card_average.pack_propagate(False)

    lbl_average_val = tkinter.Label(card_average, text=" ", font=("Segoe UI", 11, "bold"), bg="#F5F5F5")
    lbl_average_val.pack(anchor="w", padx=15, pady=(6, 2))
    tkinter.Label(card_average, text="Average", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=15)

    # ================== [ Recent Activities ]
    overview_frame = tkinter.Frame(overview_page, bg="white")
    overview_frame.pack(fill="x", padx=20, pady=5)

    recent_activity_title = tkinter.Label(overview_page,  text="Recent Activity", font=("Segoe UI", 12, "bold"), fg="#1A202C",  bg="white")
    recent_activity_title.pack(anchor="w", padx=20, pady=(30, 0))

    activities_frame = tkinter.Frame(overview_page, bg="white", relief="solid", bd=0)
    activities_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20) )


    def load_recent_activity_history():
        # Clear any old items inside the frame first to prevent overlapping data
        for child in activities_frame.winfo_children():
            child.destroy()

        show_recent_activity = recent_activity_history()  # Fetch history from database

        for activity in show_recent_activity:
            name, action, date = activity

            # 1. Create a row container frame for each individual activity log
            row_frame = tkinter.Frame(activities_frame, bg="white")
            row_frame.pack(fill="x", padx=20, pady=6, anchor="w")

            # 2. Left side: The Action Text (Bold Name + Normal Action Description)
            # Using functional emojis as a visual anchor makes it look like a log feed
            full_log_text = f"👤 {name} {action.lower()}"

            log_label = tkinter.Label(row_frame, text=full_log_text, font=("Segoe UI", 10), fg="#2D3748", bg="white")
            log_label.pack(side="left", anchor="w")

            # 3. Right side: The Muted Timestamp
            # Forcing the timestamp to the right keeps the layout clean and readable
            date_label = tkinter.Label(row_frame, text=date, font=("Segoe UI", 9, "italic"), fg="#A0AEC0", bg="white")
            date_label.pack(side="right", anchor="e", padx=(10, 0))

            # 4. Optional: Add a very faint horizontal separator line between entries
            separator = tkinter.Frame(activities_frame, height=1, bg="#EDF2F7")
            separator.pack(fill="x", padx=20, pady=(2, 0))

    # ====================================================
    # 02. Create the Second Page => Register
    # ====================================================
    register_page = tkinter.Frame(workspace_frame, bg="white")

    # Generating Customer ID for the next customer
    def generate_customer_id():
        last_customer = get_last_customer_id()  # Read the last customer_id

        if last_customer is None:  # No customer?
            return "C0001"  # Return C0001

        last_customer_id = last_customer[0]  # take last customer info from the tuple then access the 1st item
        number = int(last_customer_id[1:])  # slice operation to remove first letter (C) and keeping everything else (004)
        number += 1  # Add 1 to get a new customer id
        return f"C{number:04d}"  # Put the C back in front and If the number is small, add enough zeros so every ID has the same length


    # Creating Form Container
    form_frame = tkinter.Frame(register_page, bg="white")
    form_frame.pack(padx=40, pady=30, anchor="nw")

    # Page Title
    register_title = tkinter.Label(form_frame, text="Register Customer", font=("Segoe UI", 20, "bold"), bg="white")
    register_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 25))

    customer_info = tkinter.Label(form_frame, text="Complete the information below to register a new customer", font=("Segoe UI", 12), bg="white")
    customer_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 20))

    # Customer ID
    tkinter.Label(form_frame, text="Customer ID", font=("Segoe UI", 11), bg="white").grid(row=2, column=0, sticky="w", pady=5)
    customer_id_label = tkinter.Label(form_frame, text=generate_customer_id(), font=("Segoe UI", 11), fg="gray", bg="white")
    customer_id_label.grid(row=2, column=1, sticky="w", padx=15)

    # Full Name
    fullname_label = tkinter.Label(form_frame, text="Full Name", font=("Segoe UI", 11), bg="white")
    fullname_label.grid(row=3, column=0, sticky="w", pady=8)

    # Full Name => Entry
    fullname_entry = tkinter.Entry(form_frame, font=("Segoe UI", 11), width=35)
    fullname_entry.grid(row=3, column=1, padx=(20, 0), pady=8, sticky="w")

    # Phone Number
    phone_label = tkinter.Label(form_frame, text="Phone Number", font=("Segoe UI", 11), bg="white")
    phone_label.grid(row=4, column=0, sticky="w", pady=8)

    # Phone Number => Entry
    phone_entry = tkinter.Entry(form_frame, font=("Segoe UI", 11), width=35)
    phone_entry.grid(row=4, column=1, padx=(20, 0), pady=8, sticky="w")

    # Customer Type
    customer_type_label = tkinter.Label(form_frame, text="Customer Type", font=("Segoe UI", 11), bg="white")
    customer_type_label.grid(row=5, column=0, sticky="w", pady=8)

    # Customer Type => Dropdown menu
    customer_type = ttk.Combobox(form_frame, width=43, state="readonly")
    customer_type["values"] = ("Individual", "Business", "School", "Organization")
    customer_type.current(0)
    customer_type.grid(row=5, column=1, padx=(20, 0), pady=8, sticky="w")

    # ======== Button Frame
    button_frame = tkinter.Frame(form_frame, bg="white")
    button_frame.grid(row=6, column=1, sticky="w", pady=(25, 0))

    # validate the fullname
    def validate_fullname(fullname):
        if fullname == "":
            messagebox.showerror("Missing Information", "Please enter the customer's full name.")
            return False

        if not fullname.replace(" ", "").isalpha():  # Remove spaces and Check if everything left is alphabetic.
            messagebox.showerror("Incorrect Naming", "Please enter the customer's full name correctly.")
            return False
        return True

    # validate the phone number
    def validate_phone(phone):
        if phone == "":
            messagebox.showerror("Missing Information", "Please enter the customer's phone number.")
            return False

        if not phone.isdigit():
            messagebox.showerror("Incorrect Format", "Customer's phone number is incorrect format")
            return False

        if len(phone) != 10:
            messagebox.showerror("Incorrect Format", "Please complete the customer's phone number")
            return False

        if not phone.startswith("0"):
            messagebox.showerror("Incorrect Format", "Customer's phone number is expected to start with 0")
            return False
        return True

    # function for saving customer info
    def save_customer():
        # 1. Get user input
        customer_id = generate_customer_id()
        fullname = fullname_entry.get().strip()
        phone = phone_entry.get().strip()
        customer_type_selected = customer_type.get()
        old_id = None
        confirm_reactivate = False

        # 2. Validation
        if not validate_fullname(fullname): return
        if not validate_phone(phone): return

        # 3. Check if an inactive customer already exists
        existing_customer = get_customer_existence(fullname, phone, customer_type_selected)

        if existing_customer :
            # database returned a tuple, so we extract the ID from it (id, name, phone, type)
            old_id = existing_customer[0]
            old_fullname = existing_customer[1]

            confirm_reactivate = messagebox.askyesno(
                "Confirm reactivation",
                f"{old_fullname} is currently inactive. Would you like to perform Reactivation?"
            )

            if not confirm_reactivate:
                # If they click NO, stop everything and do nothing
                return

        # 4. Save the info
        success = save_customer_to_database(customer_id, fullname, phone, customer_type_selected, confirm_reactivate, old_id)

        if success:
            # 4. If everything is okay
            messagebox.showinfo("Success", "Customer information saved successfully")
            clear_form()
            customer_id_label.config(text=generate_customer_id())
            show_page(view_page)  # switch to view page
            load_customers()  # Reload customers info
        else:
            messagebox.showerror("Error", "Customer information could not be saved")

    # Save Button
    save_button = tkinter.Button(button_frame, text="Save", width=12, command=save_customer)
    save_button.pack(side="left", padx=(0, 30))

    # function for clearing the form
    def clear_form():
        fullname_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
        phone_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
        customer_type.current(0)

    # Clear Button
    clear_button = tkinter.Button(button_frame, text="Clear", width=12, command=clear_form)
    clear_button.pack(side="left")

    # ====================================================
    # 03. Create the Third Page => View
    # ====================================================
    view_page = tkinter.Frame(workspace_frame, bg="white")

    # ======= [ 1. load all the available customers into the table ]
    def load_customers():
        # Before writing today's names first erase everything
        for row in customer_table.get_children():
            customer_table.delete(row)

        customers = get_all_customers()  # Get customers from SQLite

        # Add each customer to the table
        for customer in customers:
            customer_table.insert("", "end", values=customer)

    # ======= [ 2. be able to search for a specific customer ]
    def search_specific_customer():
        global selected_customer
        search_text = search_entry.get().strip()  # Read what the receptionist typed.

        if search_text == "":  # Check whether they typed something.
            messagebox.showerror("Missing Information", "Please enter Customer ID, Full Name or Phone Number.")
            return

        # New search = previous selection is no longer valid
        selected_customer = None

        customers = search_customers(search_text)  # Ask the database to search.

        if not customers:  # if the customer is not there display a message
            messagebox.showinfo("Search Result", "No customer found.")
            search_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
            return

        for row in customer_table.get_children():  # Clear the table first
            customer_table.delete(row)

        for customer in customers:  # Database returns matching customers.
            customer_table.insert("", "end", values=customer)

    # ======= [ 3. be able to select details of a specific customer ]
    def select_customer(event):
        global selected_customer

        selected = customer_table.focus()

        if selected:
            # When a specific row is being clicked the program quietly remembers it
            selected_customer = customer_table.item(selected)["values"]
        else:
            # when there is no row selected anymore
            selected_customer = None

    # ======= [ 4. open registration form in updating mode ]
    def open_update_customer():
        if selected_customer is None:
            messagebox.showerror("Selection Required", "Please select a customer first.")
            return

        show_page(register_page)  # reuse the registration form interface
        load_selected_customer()  # load the info of the selected customer into that form

    # ======= [ 5. load info of the selected customer ]
    def load_selected_customer():
        global selected_customer

        if selected_customer is None:
            return

        register_title.config(text="Update Customer")
        customer_info.config(text="Edit the customer information below")

        customer_id_label.config(text=selected_customer[0])  # Assume the .config(text=...) is a name tag, simply replaces the text written on it.

        fullname_entry.delete(0, tkinter.END)
        fullname_entry.insert(0, selected_customer[1])

        phone_entry.delete(0, tkinter.END)
        phone_entry.insert(0, selected_customer[2])

        customer_type.set(selected_customer[3])

        save_button.config(text="Update")
        save_button.config(command=update_selected_customer)

    # ======= [ 6. send updated info to the database ]
    def update_selected_customer():
        # getting new info from the form
        customer_id = customer_id_label.cget("text")
        fullname = fullname_entry.get().strip()
        phone = phone_entry.get()
        customer_type_selected = customer_type.get()

        # call the database function that will connect this info to the database
        success = update_customer_in_database(customer_id, fullname, phone, customer_type_selected)

        if success:
            # If everything is okay give a feedback
            messagebox.showinfo("Update Successful", "Customer information updated successfully.")

            # ----- reset program to normal state
            reset_register_form()  # Restore form to Register Mode
            clear_form()  # Clear form
            show_page(view_page)  # switch to view page
            load_customers()  # Reload customers info
        else:
            messagebox.showerror("Update Error", "Customer information could not be updated.")


    # ======= [ 7. Return the form to normal Register Mode ]
    def reset_register_form():
        # Everything that changed when entering Update Mode to be reversed back to register mode
        register_title.config(text="Register Customer")
        customer_info.config(text="Complete the information below to register a new customer")

        customer_id_label.config(text=generate_customer_id())  # generating a new ID
        fullname_entry.delete(0, tkinter.END)  # clear this field
        phone_entry.delete(0, tkinter.END)  # clear this field
        customer_type.current(0)  # reset the selection

        save_button.config(text="Save")  # button label
        save_button.config(command=save_customer)  # button command

    # ======= [ 8. be able to delete a specific customer ]
    def delete_selected_customer():
        global selected_customer

        if selected_customer is None:  # Check whether a customer is actually selected.
            messagebox.showerror("Selection Required", "Please select a customer first.")
            return

        confirm = messagebox.askyesno("Confirm the operation",
                                      "Do you want to Delete the selected customer?")  # If selected → Ask for confirmation

        if not confirm:  # If option yes was not clicked, stop the operation
            return

        customer_id = selected_customer[0]  # get customer id
        confirm = delete_customer_in_database(customer_id)  # calling deleting function from the database

        if confirm:
            messagebox.showinfo("Deletion Successful",
                                "Customer record deleted successfully.")  # If everything is okay give a feedback
            selected_customer = None
            show_page(view_page)  # switch back to view page
            load_customers()  # Reload customers info
        else:
            messagebox.showerror("Deletion Error", "Customer record could not be deleted.")

    # ======= [ 9. Sorting function that uses any column ]
    def sort_customers():
        select_option = sort_options_combobox.get()  # Ask What did the receptionist choose?
        select_order = order_options_combobox.get()  # Ask What direction did the receptionist choose?

        column_info = sort_customer_dict[select_option]  # The dictionary translates the first choice
        order_info = sort_orders_dict[select_order]  # The dictionary translates the second choice

        customers_info = get_all_customers(column_info, order_info)  # Send the translated info to the Database

        for row in customer_table.get_children():
            customer_table.delete(row)          # Clear the old table.

        for record in customers_info:  # Put the newly sorted records into the table.
            customer_table.insert("", "end", values=record)

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
    search_button = tkinter.Button(search_frame, text="Search", width=11, command=search_specific_customer)
    search_button.pack(side="left")

    # Update Button
    update_button = tkinter.Button(search_frame, text="Update Customer", width=15, command=open_update_customer)
    update_button.pack(side="left", padx=10)

    # Delete Button
    delete_button = tkinter.Button(search_frame, text="Delete Customer", width=15, command=delete_selected_customer)
    delete_button.pack(side="left", padx=0)

    # ---------- [ Sort Utility ]
    # Sort frame
    sort_frame = tkinter.Frame(view_page, bg="white")
    sort_frame.pack(fill="x", padx=20, pady=(0, 10))

    sort_label = tkinter.Label(sort_frame, text="Sort Customers:", font=("Segoe UI", 11), bg="white")
    sort_label.pack(side="left")

    # Sort Options
    sort_options_combobox = ttk.Combobox(sort_frame, width=15, state="readonly")
    sort_options_combobox["values"] = ("Customer ID", "Full Name", "Customer Type")

    sort_options_combobox.current(0)  # Start with Customer ID
    sort_options_combobox.pack(side="left", padx=5)

    # This is our translation dictionary
    # what the receptionist see (left side) and what the database knows (right side)
    sort_customer_dict = {
        "Customer ID": "customer_id",
        "Full Name": "fullname",
        "Customer Type": "customer_type"
    }

    # Create the order dictionary
    # The receptionist sees Ascending and  SQLite understands ASC
    sort_orders_dict = {
        "Ascending": "ASC",
        "Descending": "DESC"
    }

    # ascending/descending combo box
    order_options_combobox = ttk.Combobox(sort_frame, width=12, state="readonly")
    order_options_combobox["values"] = ("Ascending", "Descending")

    order_options_combobox.current(0)
    order_options_combobox.pack(side="left", padx=5)

    # sort button
    sort_button = tkinter.Button(sort_frame, text="Sort", width=10, command=sort_customers)
    sort_button.pack(side="left", padx=5)

    # Display the table area
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Create the Treeview
    customer_table = ttk.Treeview(table_frame, columns=("ID", "Name", "Phone", "Type"), show="headings")
    customer_table.bind("<<TreeviewSelect>>", select_customer)

    # Create the headings
    customer_table.heading("ID", text="Customer ID")
    customer_table.heading("Name", text="Full Name")
    customer_table.heading("Phone", text="Phone Number")
    customer_table.heading("Type", text="Customer Type")

    # Set the column widths
    customer_table.column("ID", width=100)
    customer_table.column("Name", width=220)
    customer_table.column("Phone", width=150)
    customer_table.column("Type", width=120)

    # display the table
    customer_table.pack(fill="both", expand=True)

    # ====================================================
    # 04. Create the Fourth Page => History
    # ====================================================
    history_page = tkinter.Frame(workspace_frame, bg="white")

    # ======= History Page Functions
    # 1. Load Customer History into the table
    def load_customer_history():
        for row in history_table.get_children():
            history_table.delete(row)  # Before writing anything new first erase what's in the table (Refreshing)

        history = view_customer_history()  # Get history info from the database

        # Add each record to the table
        for record in history:
            history_table.insert("", "end", values=record)

    # 2. Sorting function that uses any column
    def sort_history():
        selected_option = sort_options.get()  # Ask What did the receptionist choose?
        selected_order = order_options.get()  # Ask What direction did the receptionist choose?

        which_column = sort_columns[selected_option]  # The dictionary translates the first choice
        order_of = sort_orders[selected_order]  # The dictionary translates the second choice

        history_sort  = view_customer_history(which_column, order_of)  # Send the translated info to the Database

        for row in history_table.get_children():
            history_table.delete(row)  # Clear the old table.

        for history in history_sort:  # Put the newly sorted records into the table.
            history_table.insert("", "end", values=history)

    # message label
    history_label = tkinter.Label(history_page, text="View all customer activity history", font=("Segoe UI", 15), bg="white")
    history_label.pack(anchor="w", padx=20, pady=(10, 2))

    # ------------- start sort functionality -----------------
    # Sort frame
    sort_frame = tkinter.Frame(history_page, bg="white")
    sort_frame.pack(fill="x", padx=20, pady=(0, 10))

    sort_label = tkinter.Label(sort_frame, text="Sort History:", font=("Segoe UI", 11), bg="white")
    sort_label.pack(side="left")

    # Sort Options
    sort_options = ttk.Combobox(sort_frame, width=15, state="readonly")
    sort_options["values"] = ("Customer ID", "Fullname", "Action", "Date")

    sort_options.current(3)  # Start with Date
    sort_options.pack(side="left", padx=5)

    # Translation dictionary
    # what the receptionist see (left side) and what the database knows (right side)
    sort_columns = {
        "Customer ID": "tbl_customers_history.customer_id",
        "Fullname": "fullname",
        "Action": "action",
        "Date": "date_created"
    }

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
    sort_button = tkinter.Button(sort_frame, text="Sort", width=10, command=sort_history)
    sort_button.pack(side="left", padx=5)

    # ---------- [ 1. History => Frame for the table ]
    table_history_frame = tkinter.Frame(history_page, bg="white")
    table_history_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------- [ 2 History => Creating the Treeview ]
    history_table = ttk.Treeview(table_history_frame, columns=("Customer ID", "Fullname", "Action", "Date"), show="headings")

    # ---------- [ 5. First Page => Creating table headings ]
    history_table.heading("Customer ID", text="Customer ID")
    history_table.heading("Fullname", text="Fullname")
    history_table.heading("Action", text="Action")
    history_table.heading("Date", text="Date")

    # ---------- [ 6. First Page => Set the column widths ]
    history_table.column("Customer ID", width=50)
    history_table.column("Fullname", width=100)
    history_table.column("Action", width=50)
    history_table.column("Date", width=100)

    # display the table
    history_table.pack(fill="both", expand=True)

    # ===================[ Show this page only after all the others exist  ]===================
    show_page(overview_page)
    customer_metrics_controller_display()
    financial_metrics_controller_display()
    load_recent_activity_history()

