import tkinter
from tkinter import ttk
from tkinter import messagebox
from tkinter.simpledialog import askstring
from database import view_stock
from database import view_history
from database import search_stock
from database import get_last_stock_id
from database import get_stock_by_name
from database import get_active_printing_material
from database import save_stock_to_database
from database import update_stock_record_info
from database import delete_stock_from_database

# ====================[ Shared Variables ]===================
parent_window = None   # Parent window reference
close_callback = None  # Create a place to store the function that should be called when this window closes.
active_button = None   # What is currently selected? Initially Nothing
selected_stock = None  # Which stock is currently selected? Initially it should be None

# ============================================================
# =================== [ Open Stock Window ] ==================
# ============================================================
def open_stock_window(parent, on_close):
    # ---------- 1. This window receives two things everytime its opens:
    # Dashboard/root reference and Closing function reference.
    global parent_window, close_callback
    parent_window = parent
    close_callback = on_close

    # ---------- [ 2. Initializing this Window ]
    stock_window_interface = tkinter.Toplevel(parent)

    # ---------- [ 3. Title and size ]
    stock_window_interface.title("Printing Shop Management System")
    stock_window_interface.resizable(False, False)
    window_width = 900  # windows width
    window_height = 600  # widows height

    # ---------- [ 4. Actual Screen Size ]
    screen_width = stock_window_interface.winfo_screenwidth()
    screen_height = stock_window_interface.winfo_screenheight()

    # ---------- [ 5. Coordinates for centering the window ]
    x = (screen_width - window_width) // 2  # splits the answer/space equally into left/right
    y = (screen_height - window_height) // 2  # splits the answer/space equally into top/bottom

    # ---------- [ 6. Center the window using X/Y coordinates ]
    stock_window_interface.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # ---------- [ 7. Closing the window ]
    def close_stock_window():
        parent_window.deiconify()          # notify => Dashboard
        close_callback()                   # refer => closing function
        stock_window_interface.withdraw()  # hide this window

    # ---------- [ 7. Tie Closing function to X button ]
    stock_window_interface.protocol("WM_DELETE_WINDOW", close_stock_window)

    # ===================[ 1. Title Label ]=================
    header_frame = tkinter.Frame(stock_window_interface, height=50)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    title_label = tkinter.Label(header_frame, text="STOCK MANAGEMENT", font=("Segoe UI", 16, "bold"))
    title_label.pack(side="left", padx=20, pady=15)

    # ====================[ 2. Main Body ]===================
    body_frame = tkinter.Frame(stock_window_interface)
    body_frame.pack(fill="both", expand=True)

    # ===================[ 3. Left Frame ]===================
    navigation_frame = tkinter.Frame(body_frame, width=190, bg="#EAEAEA")
    navigation_frame.pack(side="left", fill="y")
    navigation_frame.pack_propagate(False)

    # Navigation Buttons & their functions
    def set_active_button(button):
        global active_button                             # Which button is active.

        if active_button is not None:                    # If nothing is selected Nothing happens.
            active_button.config(bg="SystemButtonFace")  # Return previously selected button back to normal appearance.

        button.config(bg="#D6EAF8")                      # Highlight the selected button
        active_button = button                           # Remember this button next time

    def show_page(page):
        view_page.pack_forget()              # Means => Hide Overview.
        manage_page.pack_forget()            # Means => Hide Register.
        history_page.pack_forget()           # Means => Hide View.
        page.pack(fill="both", expand=True)  # Means => Show whichever page I receive.

    # Navigation buttons
    overview_button = tkinter.Button(navigation_frame, text="view Stock", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(overview_button), show_page(view_page), load_stock()))
    overview_button.pack(pady=(30, 15))

    manage_button = tkinter.Button(navigation_frame, text="Manage Stock", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(manage_button), show_page(manage_page)))
    manage_button.pack(pady=15)

    history_button = tkinter.Button(navigation_frame, text="Stock History", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(history_button), show_page(history_page), load_stock_history()))
    history_button.pack(pady=15)

    # ===================[ 4. Right Frame ]===================
    right_frame = tkinter.Frame(body_frame, bg="white")
    right_frame.pack(side="left", fill="both", expand=True)

    # ========== Creating Workspace Container ==========
    workspace_frame = tkinter.Frame(right_frame, bg="white")
    workspace_frame.pack(fill="both", expand=True)

    # ====================================================
    # 01. First Page => overview
    # ====================================================
    view_page = tkinter.Frame(workspace_frame, bg="white")

    # 1. Load all the available stock into the table
    def load_stock():
        for row in stock_table.get_children():
            stock_table.delete(row)  # Before writing anything new first erase what's in the table (Refreshing)

        stock = view_stock()  # Get available stock from the database

        # Add each stock to the table
        for record in stock:
            stock_table.insert("", "end", values=record)

    # 2. Search for a specific stock
    def search_specific_stock():
        global selected_stock
        search_text = search_entry.get().strip()  # Read what the receptionist typed.

        if search_text == "":  # Check whether they typed something.
            messagebox.showerror("Missing Information", "Please enter Stock ID or Stock Name")
            search_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
            return

        # New search = previous selection is no longer valid
        selected_stock = None

        stock = search_stock(search_text)  # pass the info to the database file

        if not stock:  # if the stock is not available
            messagebox.showinfo("Search Result", "No Stock found.")
            search_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
            return

        for row in stock_table.get_children():
            stock_table.delete(row)  # Clear the table first (Refresh)

        for record in stock:  # Database returns matching stock.
            stock_table.insert("", "end", values=record)


    # 3. Select details of a specific stock
    def select_stock(event):
        global selected_stock

        selected = stock_table.focus()

        if selected:
            selected_stock = stock_table.item(selected)["values"]  # Store info of the selected row
        else:
            selected_stock = None  # when there is no row selected anymore

    # 4. Delete details of a specific stock
    def delete_selected_stock():
        global selected_stock

        # Check whether any stock is actually selected.
        if selected_stock is None:
            messagebox.showerror("Selection Required", "Please select any record first.")
            return

        # If selected → Ask for confirmation
        confirm = messagebox.askyesno("Confirm the operation", "Do you want to Delete the selected stock?")

        if not confirm:  # If option is not yes, stop the operation
            return

        # Get the reason for deleting
        reason = askstring("Reason for Deleting", "Type the reason to proceed: ")

        # if cancel was clicked or ok was clicked typing anything, stop the operation
        if reason is None or reason.strip() == "":
            messagebox.showinfo("Cancelled", "Process aborted.")
            return

        stock_id = selected_stock[0]  # get stock id
        success = delete_stock_from_database(stock_id, reason)  # call delete function from the database

        # When everything is okay give this feedback
        if success:
            messagebox.showinfo("Deletion Successful", "Stock deleted successfully.")

            selected_stock = None  # return selected stock to none/default
            show_page(view_page)  # switch back to view page
            load_stock()  # Reload stock info
        else:
            # When something goes wrong give this feedback
            messagebox.showerror(
                "Deletion Failed", "The stock could not be deleted.")

    def open_update_stock():
        # Check whether any stock is selected.
        if selected_stock is None:
            messagebox.showerror("Selection Required", "Please select any record first.")
            return

        show_page(manage_page)  # reuse the registration form interface
        load_selected_item()  # load the info of the selected stock into that form

    # ======= [ 5. load info of the selected stock ]
    def load_selected_item():
        global selected_stock

        if selected_stock is None:
            return

        # Switch Registration form => Update mode
        stock_manage_title.config(text="Update Stock Item")
        stock_info.config(text="Edit the Stock information below")

        stock_id_label.config(text=selected_stock[0])

        name_entry.delete(0, tkinter.END)
        name_entry.insert(0, selected_stock[1])

        quantity_entry.delete(0, tkinter.END)
        quantity_entry.insert(0, selected_stock[2])

        printing_type.set(selected_stock[3])

        save_button.config(text="Update")
        save_button.config(command=update_selected_stock)

    def update_selected_stock():
        # getting new info from the form
        stock_id = stock_id_label.cget("text")
        stock_name = name_entry.get()
        stock_quantity = quantity_entry.get().strip()
        printing_material = printing_type.get()
        confirm_replace = False
        old_stock_id = None

        # 2. Validation
        if not validate_name(stock_name): return
        if not validate_quantity(stock_quantity): return

        if printing_material == "Yes":
            current_printing = get_active_printing_material()

            # An existing printing material was found
            if current_printing:
                old_stock_id, old_stock_name = current_printing

                # Is it the SAME stock I'm editing?  YES → no replacement required
                if not stock_name == old_stock_name:
                    # NO → Confirm replacement
                    confirm_replace = messagebox.askyesno(
                        "Confirm replacement",
                        f"{old_stock_name} is the printing material. Do you want to replace it?"
                    )

                    if not confirm_replace:
                        return

        # Get the reason for adding
        reason = askstring("Remarks", "Type the remarks to proceed: ")

        # if cancel was clicked or ok was clicked without typing anything, stop the operation
        if reason is None or reason.strip() == "":
            messagebox.showinfo("Cancelled", "Process aborted.")
            return

        # ========= [Update the record]
        success = update_stock_record_info(stock_id, stock_name, stock_quantity, printing_material, reason, confirm_replace, old_stock_id)

        # When everything is okay give this feedback
        if success:
            messagebox.showinfo("Success", "Stock Updated successfully.")

            # ----- reset program to normal state
            reset_register_form()  # Restore form to Register Mode
            clear_form()  # Clear form
            show_page(view_page)  # switch to view page
            load_stock()  # Reload stock info
        else:
            # When something goes wrong give this feedback
            messagebox.showerror("Operation Failed", "The stock could not be Updated.")

    # Switch Registration form => register mode
    def reset_register_form():
        # Everything that changed when entering Update Mode to be reversed back to register mode
        stock_manage_title.config(text="Register Stock")
        stock_info.config(text="Complete the information below to register a new stock")

        stock_id_label.config(text=generate_stock_id())  # generating a new ID
        name_entry.delete(0, tkinter.END)  # clear this field
        quantity_entry.delete(0, tkinter.END)  # clear this field
        printing_type.current(0)  # reset the selection

        save_button.config(text="Save")  # button label
        save_button.config(command=save_stock)  # button command

    # ---------- [ 1. First Page => Frame for the table ]
    table_frame = tkinter.Frame(view_page, bg="white")

    # ---------- [ 2. First Page => Search & Sort Utility ]
    search_frame = tkinter.Frame(view_page, bg="white")
    search_frame.pack(fill="x", padx=20, pady=10)

    # Search Label
    search_label = tkinter.Label(search_frame, text="Search Stock:", font=("Segoe UI", 11), bg="white")
    search_label.pack(side="left")

    # Search Entry
    search_entry = tkinter.Entry(search_frame, font=("Segoe UI", 11), width=22)
    search_entry.pack(side="left", padx=10)

    # Search Button
    search_button = tkinter.Button(search_frame, text="Search", width=11, command=search_specific_stock)
    search_button.pack(side="left")

    # Update Button
    update_button = tkinter.Button(search_frame, text="Update Stock", width=15, command=open_update_stock)
    update_button.pack(side="left", padx=10)

    # Delete Button
    delete_button = tkinter.Button(search_frame, text="Delete Stock", width=15, command=delete_selected_stock)
    delete_button.pack(side="left", padx=0)

    # ---------- [ 3. First Page => Display the table area ]
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------- [ 4. First Page => Creating the Treeview ]
    stock_table = ttk.Treeview(table_frame, columns=("ID", "Name", "Quantity", "Printing Material", "Status"), show="headings")
    stock_table.bind("<<TreeviewSelect>>", select_stock)

    # ---------- [ 5. First Page => Creating table headings ]
    stock_table.heading("ID", text="Stock ID")
    stock_table.heading("Name", text="Name")
    stock_table.heading("Quantity", text="Quantity")
    stock_table.heading("Printing Material", text="Printing Material")
    stock_table.heading("Status", text="Status")

    # ---------- [ 6. First Page => Set the column widths ]
    stock_table.column("ID", width=50)
    stock_table.column("Name", width=200)
    stock_table.column("Quantity", width=50)
    stock_table.column("Printing Material", width=100)
    stock_table.column("Status", width=120)

    # display the table
    stock_table.pack(fill="both", expand=True)

    # ====================================================
    # 02. Second Page => Manage
    # ====================================================
    manage_page = tkinter.Frame(workspace_frame, bg="white")

    def generate_stock_id():
        last_stock = get_last_stock_id()  # Read the last stock_id

        if last_stock is None:  # No Stock?
            return "S0001"  # Return S0001

        last_stock_id = last_stock[0]  # take last stock info from the tuple then access the 1st item
        number = int(last_stock_id[1:])  # slice operation to remove first letter (S) keeping everything else (004)
        number += 1  # Add 1 to get a new id
        return f"S{number:04d}"  # Put the S back in front and If the number is small, add enough zeros so every ID has the same length

    # ---------- [ Second Page => Frame for the form ]
    form_frame = tkinter.Frame(manage_page, bg="white")
    form_frame.pack(padx=40, pady=30, anchor="nw")

    # ---------- [ Second Page => form title ]
    stock_manage_title = tkinter.Label(form_frame, text="Add New Stock", font=("Segoe UI", 20, "bold"), bg="white")

    # Form grid
    stock_manage_title.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 25))
    stock_info = tkinter.Label(form_frame, text="Complete the information below to add a new stock", font=("Segoe UI", 12), bg="white")
    stock_info.grid(row=1, column=0, columnspan=2, sticky="w", pady=(5, 20))

    # Stock ID
    tkinter.Label(form_frame, text="Stock ID", font=("Segoe UI", 11), bg="white").grid(row=2, column=0, sticky="w", pady=5)
    stock_id_label = tkinter.Label(form_frame, text=generate_stock_id(), font=("Segoe UI", 11), fg="gray", bg="white")
    stock_id_label.grid(row=2, column=1, sticky="w", padx=15)

    # Stock Item
    name_label = tkinter.Label(form_frame, text="Item Name", font=("Segoe UI", 11), bg="white")
    name_label.grid(row=3, column=0, sticky="w", pady=8)

    # Stock Item => Entry
    name_entry = tkinter.Entry(form_frame, font=("Segoe UI", 11), width=35)
    name_entry.grid(row=3, column=1, padx=(20, 0), pady=8, sticky="w")

    # Quantity
    quantity_label = tkinter.Label(form_frame, text="Quantity", font=("Segoe UI", 11), bg="white")
    quantity_label.grid(row=4, column=0, sticky="w", pady=8)

    # Quantity => Entry
    quantity_entry = tkinter.Entry(form_frame, font=("Segoe UI", 11), width=35)
    quantity_entry.grid(row=4, column=1, padx=(20, 0), pady=8, sticky="w")

    # Printing Material
    printing_type_label = tkinter.Label(form_frame, text="Printing Material", font=("Segoe UI", 11), bg="white")
    printing_type_label.grid(row=5, column=0, sticky="w", pady=8)

    # Printing Material => Dropdown menu
    printing_type = ttk.Combobox(form_frame, width=43, state="readonly")
    printing_type["values"] = ("Yes", "No")
    printing_type.current(0)
    printing_type.grid(row=5, column=1, padx=(20, 0), pady=8, sticky="w")

    # ---------- [ Second Page => button frame ]
    button_frame = tkinter.Frame(form_frame, bg="white")
    button_frame.grid(row=6, column=1, sticky="w", pady=(25, 0))

    # validation
    def validate_name(item_name):
        if item_name == "":
            messagebox.showerror("Missing Information", "Please enter the Item name.")
            return False

        if not item_name.replace(" ", ""):  # Prevent names containing only spaces/unnecessary spaces
            messagebox.showerror("Incorrect Naming", "Please enter the item name correctly.")
            return False
        return True

    def validate_quantity(item_quantity):
        if item_quantity == "":
            messagebox.showerror("Missing Information", "Please enter the item quantity.")
            return False

        if not item_quantity.isdigit():
            messagebox.showerror("Incorrect Format", "item quantity is incorrect format")
            return False

        if int(item_quantity) <= 0:
            messagebox.showerror("Incorrect Quantity", "Quantity has to be more than zero")
            return False
        return True

    # function for saving stock info
    def save_stock():
        # 1. Get user input
        stock_id = generate_stock_id()
        name = name_entry.get().strip()
        quantity = quantity_entry.get().strip()
        printing_material = printing_type.get()
        confirm_reactivate = False
        confirm_replace = False
        stock_id_exist = None
        old_stock_id = None

        # 2. Validation
        if not validate_name(name): return
        if not validate_quantity(quantity): return

        stock = get_stock_by_name(name)

        if stock:
            stock_id_exist = stock[0]

            confirm_reactivate = messagebox.askyesno(
                "Confirm reactivation",
                "This stock is currently inactive. Would you like to Activate it back?"
            )

            if not confirm_reactivate:
                return

        if printing_material == "Yes":
            current_printing = get_active_printing_material()

            # An existing printing material was found
            if current_printing:
                old_stock_id, old_stock_name = current_printing

                confirm_replace = messagebox.askyesno(
                    "Confirm replacement",
                    f"{old_stock_name} is the printing material. Do you want to replace it?"
                )

                if not confirm_replace:
                    return

        # Get the reason for adding
        reason = askstring("Remarks", "Type the remarks to proceed: ")

        # if cancel was clicked or ok was clicked without typing anything, stop the operation
        if reason is None or reason.strip() == "":
            messagebox.showinfo("Cancelled", "Process aborted.")
            return

        # ========= [Save the info]
        success = save_stock_to_database(stock_id, name, quantity, printing_material, reason, confirm_replace, old_stock_id, confirm_reactivate, stock_id_exist)

        # When everything is okay give this feedback
        if success:
            messagebox.showinfo("Success", "Stock added successfully.")

            clear_form()
            stock_id_label.config(text=generate_stock_id())
            show_page(view_page)  # switch to view page
            load_stock()  # Reload stock info
        else:
            # When something goes wrong give this feedback
            messagebox.showerror("Operation Failed", "The stock could not be Added.")

    # Save Button
    save_button = tkinter.Button(button_frame, text="Save", width=12, command=save_stock)
    save_button.pack(side="left", padx=(0, 30))

    # function for clearing the form
    def clear_form():
        name_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
        quantity_entry.delete(0, tkinter.END)  # erase everything from position 0 to the end
        printing_type.current(0)

    # Clear Button
    clear_button = tkinter.Button(button_frame, text="Clear", width=12, command=clear_form)
    clear_button.pack(side="left")

    # ====================================================
    # 03. Third Page => History
    # ====================================================
    history_page = tkinter.Frame(workspace_frame, bg="white")

    # 1. Load Stock History into the table
    def load_stock_history():
        for row in history_table.get_children():
            history_table.delete(row)  # Before writing anything new first erase what's in the table (Refreshing)

        history = view_history()  # Get stock history from the database

        # Add each stock history to the table
        for record in history:
            history_table.insert("", "end", values=record)

    # 2. Sorting function that uses any column
    def sort_stock():
        selected_option = sort_options.get()  # Ask the Combobox => What did the receptionist choose?
        selected_order = order_options.get()  # Ask the Combobox => What direction did the receptionist choose?

        column = sort_columns[selected_option]  # The dictionary translates the first choice
        order = sort_orders[selected_order]  # The dictionary translates the second choice

        stock_history = view_history(column, order)  # Send the translated info to the Database

        for row in history_table.get_children():
            history_table.delete(row)  # Clear the old table.

        for record in stock_history:  # Put the newly sorted records into the table.
            history_table.insert("", "end", values=record)

    # message label
    history_label = tkinter.Label(history_page, text="View every stock transaction history", font=("Segoe UI", 15), bg="white")
    history_label.pack(anchor="w", padx=20, pady=(10, 2))

    # ------------- start sort functionality -----------------
    sort_frame = tkinter.Frame(history_page, bg="white")
    sort_frame.pack(fill="x", padx=20, pady=(0, 10))

    sort_label = tkinter.Label(sort_frame, text="Sort History:", font=("Segoe UI", 11), bg="white")
    sort_label.pack(side="left")

    # Sort Options
    sort_options = ttk.Combobox(sort_frame, width=15, state="readonly")
    sort_options["values"] = ("History ID", "Stock ID", "Action", "Date/Time")

    sort_options.current(3)
    sort_options.pack(side="left", padx=5)

    # Create translation dictionary => sort_columns["Full Name"] produces fullname
    # what the receptionist see (left side) and what the database knows (right side)
    sort_columns = {
        "History ID": "history_id",
        "Stock ID": "stock_id",
        "Action": "action",
        "Date/Time": "date_created"
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
    sort_button = tkinter.Button(sort_frame, text="Sort", width=10, command=sort_stock)
    sort_button.pack(side="left", padx=5)
    # ------------- end sort functionality

    # ---------- [ 1. History => Frame for the table ]
    table_history_frame = tkinter.Frame(history_page, bg="white")
    table_history_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # ---------- [ 2 History => Creating the Treeview ]
    history_table = ttk.Treeview(table_history_frame, columns=("ID", "Stock ID", "Action", "Quantity", "Remark", "Date"), show="headings")

    # ---------- [ 5. First Page => Creating table headings ]
    history_table.heading("ID", text="History ID")
    history_table.heading("Stock ID", text="Stock ID")
    history_table.heading("Action", text="Action")
    history_table.heading("Quantity", text="Quantity")
    history_table.heading("Remark", text="Remark")
    history_table.heading("Date", text="Date")

    # ---------- [ 6. First Page => Set the column widths ]
    history_table.column("ID", width=50)
    history_table.column("Stock ID", width=50)
    history_table.column("Action", width=50)
    history_table.column("Quantity", width=50)
    history_table.column("Remark", width=200)
    history_table.column("Date", width=100)

    # display the table
    history_table.pack(fill="both", expand=True)

    # ===================[ Show this page only after all the others exist  ]===================
    show_page(view_page)

    # Load stock automatically when the window opens
    load_stock()