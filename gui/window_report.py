import tkinter
import matplotlib.pyplot as plt
from tkinter import messagebox
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from tkcalendar import DateEntry

from database import get_sales_summary
from database import get_sales_chart_data
from database import search_specific_customer_report
from database import get_date_report

# ====================[ Shared Variables ]===================
parent_window = None  # Parent window reference
close_callback = None # Create a place to store the function that should be called when this window closes.
active_button = None  # What is currently selected? Initially Nothing

# ============================================================
# =================== [ Open Report Window ] ==================
# ============================================================
def open_report_window(parent, on_close):
    # ---------- 1. This window receives two things everytime its opens:
    # Dashboard/root reference and Closing function reference.
    global parent_window, close_callback
    parent_window = parent
    close_callback = on_close

    # ---------- [ 2. Initializing this Window ]
    report_window_interface = tkinter.Toplevel(parent)

    # ---------- [ 3. Title and size ]
    report_window_interface.title("Printing Shop Management System")
    report_window_interface.resizable(False, False)
    window_width = 900  # windows width
    window_height = 600  # widows height

    # ---------- [ 4. Actual Screen Size ]
    screen_width = report_window_interface.winfo_screenwidth()
    screen_height = report_window_interface.winfo_screenheight()

    # ---------- [ 5. Coordinates for centering the window ]
    x = (screen_width - window_width) // 2  # splits the answer/space equally into left/right
    y = (screen_height - window_height) // 2  # splits the answer/space equally into top/bottom

    # ---------- [ 6. Center the window using X/Y coordinates ]
    report_window_interface.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # ---------- [ 7. Closing the window ]
    def close_report_window():
        parent_window.deiconify()           # notify => Dashboard
        close_callback()                    # refer => closing function
        report_window_interface.withdraw()  # hide this window

    # ---------- [ 7. Tie Closing function to X button ]
    report_window_interface.protocol("WM_DELETE_WINDOW", close_report_window)

    # ===================[ 1. Title Label ]=================
    header_frame = tkinter.Frame(report_window_interface, height=50)
    header_frame.pack(fill="x")
    header_frame.pack_propagate(False)

    title_label = tkinter.Label(header_frame, text="REPORT SUMMARY", font=("Segoe UI", 16, "bold"))
    title_label.pack(side="left", padx=20, pady=15)

    # ====================[ 2. Main Body ]===================
    body_frame = tkinter.Frame(report_window_interface)
    body_frame.pack(fill="both", expand=True)

    # ===================[ 3. Left Frame ]===================
    navigation_frame = tkinter.Frame(body_frame, width=190, bg="#EAEAEA")
    navigation_frame.pack(side="left", fill="y")
    navigation_frame.pack_propagate(False)

    # Navigation Buttons & their functions
    def set_active_button(button):
        global active_button  # Which button is active.

        if active_button is not None:                    # If nothing is selected Nothing happens.
            active_button.config(bg="SystemButtonFace")  # Return previously selected button back to normal appearance.

        button.config(bg="#D6EAF8")  # Highlight the selected button
        active_button = button       # Remember this button next time

    def show_page(page):
        sales_summary_page.pack_forget()
        date_report_page.pack_forget()
        customer_report_page.pack_forget()
        page.pack(fill="both", expand=True)  # Means => Show whichever page I receive.

    # Navigation buttons
    sales_button = tkinter.Button(navigation_frame, text="Sales Summary", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(sales_button), show_page(sales_summary_page), refresh_dashboard_chart(chart_frame)))
    sales_button.pack(pady=(30, 15))

    date_button = tkinter.Button(navigation_frame, text="Date Report", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(date_button), show_page(date_report_page)))
    date_button.pack(pady=15)

    customer_button = tkinter.Button(navigation_frame, text="Customer Report", font=("Segoe UI", 11), width=18, command=lambda: (set_active_button(customer_button), show_page(customer_report_page)))
    customer_button.pack(pady=15)

    # ===================[ 4. Right Frame ]===================
    right_frame = tkinter.Frame(body_frame, bg="white")
    right_frame.pack(side="left", fill="both", expand=True)

    # ========== Creating Workspace Container ==========
    workspace_frame = tkinter.Frame(right_frame, bg="white")
    workspace_frame.pack(fill="both", expand=True)

    # ====================================================
    # 01. First Page => Sales Summary
    # ====================================================
    sales_summary_page = tkinter.Frame(workspace_frame, bg="white")

    # ======= [ 1. display Summary Report ]
    sales = get_sales_summary()  # Get customers from SQLite

    if sales:
        # Unpack the row into descriptive variables
        total_jobs, total_pages, total_cost, avg_cost = sales

        # Safe fallback to 0 if the table is empty and returns None
        jobs = total_jobs or 0
        pages = total_pages or 0
        total = total_cost or 0
        average = f"{avg_cost:.2f}" if avg_cost else "0.00"

    # ======== Summary Frame
    summary_frame = tkinter.Frame(sales_summary_page, bg="white")
    summary_frame.pack(fill="x", padx=20, pady=15)

    # dashboard label
    summary_label = tkinter.Label(summary_frame, text="Sales Summary Report", font=("Segoe UI", 16, "bold"), bg="white")
    summary_label.pack(anchor="nw", padx=20, pady=(15, 5))

    note_label = tkinter.Label(summary_frame, text="Summary Report of all operations of Printing Shop Management System", font=("Segoe UI", 11), fg="gray", bg="white")
    note_label.pack(anchor="w", padx=20, pady=(0, 25))

    # ---------- [ Total Jobs Card ]
    total_jobs = tkinter.Frame(summary_frame, bg="#F5F5F5", width=140, height=100, relief="solid", bd=0)
    total_jobs.pack(side="left", padx=14)
    total_jobs.pack_propagate(False)

    tkinter.Label(total_jobs, text=jobs, font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 15))
    tkinter.Label(total_jobs, text="Total Jobs", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 12))

    # ---------- [ Total Pages Card ]
    total_pages = tkinter.Frame(summary_frame, bg="#F5F5F5", width=140, height=100, relief="solid", bd=0)
    total_pages.pack(side="left", padx=14)
    total_pages.pack_propagate(False)

    tkinter.Label(total_pages, text=pages, font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 15))
    tkinter.Label(total_pages, text="Total Pages", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 12))

    # ---------- [ Total Revenue Card ]
    total_revenue = tkinter.Frame(summary_frame, bg="#F5F5F5", width=140, height=100, relief="solid", bd=0)
    total_revenue.pack(side="left", padx=14)
    total_revenue.pack_propagate(False)

    tkinter.Label(total_revenue, text=total, font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 15))
    tkinter.Label(total_revenue, text="Total Revenue", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 12))

    # ---------- [  Average Revenue Card ]
    average_revenue = tkinter.Frame(summary_frame, bg="#F5F5F5", width=140, height=100, relief="solid", bd=0)
    average_revenue.pack(side="left", padx=14)
    average_revenue.pack_propagate(False)

    tkinter.Label(average_revenue, text=average, font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 15))
    tkinter.Label(average_revenue, text="Average Revenue", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 12))

    # ======= [ Display Graphical Analytics Chart ] =======
    # chart Frame
    chart_frame = tkinter.Frame(sales_summary_page, bg="white")
    chart_frame.pack(fill="x", padx=20, pady=15)

    # ======= [ 2. Display Graphical Analytics Chart ] =======
    def refresh_dashboard_chart(container_frame):
        # A. Clear out the previous chart canvas
        for widget in container_frame.winfo_children():
            if isinstance(widget, FigureCanvasTkAgg):
                widget.destroy()
            elif isinstance(widget, tkinter.Label) and widget.cget("text") == "":
                widget.destroy()

        # B. Fetch the grouped day-by-day dataset from the database
        chart_data = get_sales_chart_data()

        if chart_data:
            # Extract and cleanly format the date axis titles
            dates = []

            for row in chart_data:
                try:
                    # Convert '2026-09-27' string into a cleaner '27 Sep' text format
                    clean_date = datetime.strptime(row[0], "%Y-%m-%d").strftime("%d %b")
                    dates.append(clean_date)
                except Exception:
                    dates.append(row[0]) # Fallback to original text if error occurs

            # Extract daily aggregated revenues
            daily_revenues = [row[1] for row in chart_data]

            # Create a Matplotlib Figure window matching your card aesthetics
            fig, ax = plt.subplots(figsize=(6, 3.2), dpi=100)
            fig.patch.set_facecolor("#F5F5F5")
            ax.set_facecolor("#F5F5F5")

            # Plot visual bars
            bars = ax.bar(dates, daily_revenues, color="#4A90E2", width=0.45)

            # Clean layout styling - Title updated to match the grouping choice
            ax.set_title("Daily Revenue Breakdown", fontname="Segoe UI", fontsize=11, color="#1F2937", pad=15)

            # 1. REMOVE ALL OUTLINE BORDERS (SPINES)
            for spine in ax.spines.values():
                spine.set_visible(False)

            # 2. HIDE THE Y-AXIS MEASUREMENTS
            ax.get_yaxis().set_visible(False)

            # 3. STYLE THE X-AXIS LABELS
            ax.tick_params(axis="x", colors="#6B7280", labelsize=9, length=0)
            for label in ax.get_xticklabels():
                label.set_fontname("Segoe UI")

            # 4. RENDER NEAT VALUE LABELS ON TOP OF BARS
            # Adjusted vertical spacing offset based on currency numbers
            max_y = max(daily_revenues) if daily_revenues else 1
            y_offset = max_y * 0.05 # Dynamic 5% offset headroom above bars

            for bar in bars:
                yval = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    yval + y_offset,
                    f"Kes {yval:,.2f}", # Forces professional currency string formatting on the bars
                    ha="center",
                    va="bottom",
                    fontname="Segoe UI",
                    fontsize=8,
                    color="#374151"
                )

            # Give extra headroom at the top of the graph so currency text labels never clip
            ax.set_ylim(0, max_y + (y_offset * 3))

            plt.tight_layout()

            # --- Canvas Layer Integration ---
            canvas = FigureCanvasTkAgg(fig, master=container_frame)
            canvas_widget = canvas.get_tk_widget()

            # Configure background block to blend completely
            canvas_widget.configure(bg="#F5F5F5", highlightthickness=0)
            canvas_widget.pack(fill=tkinter.BOTH, expand=True, padx=20, pady=10)
            canvas.draw()


    # ====================================================
    # 02. Second Page => Date Report
    # ====================================================
    date_report_page = tkinter.Frame(workspace_frame, bg="white")

    # ======== Summary Frame
    date_summary_frame = tkinter.Frame(date_report_page, bg="white")
    date_summary_frame.pack(fill="x", padx=20, pady=15)

    # dashboard label
    summary_label = tkinter.Label(date_summary_frame, text="Sales Summary By Date", font=("Segoe UI", 16, "bold"), bg="white")
    summary_label.pack(anchor="nw", padx=20, pady=(15, 5))

    note_label = tkinter.Label(date_summary_frame, text="Get summary report for a specific date in Printing Shop Management System", font=("Segoe UI", 11), fg="gray", bg="white")
    note_label.pack(anchor="w", padx=20, pady=0)

    # ======== Date Report Frame
    date_entry_frame = tkinter.Frame(date_report_page, bg="white")
    date_entry_frame.pack(fill="x", padx=35, pady=15)

    # Date Entry
    get_date_entry = DateEntry(date_entry_frame, date_pattern='yyyy-mm-dd', font=("Segoe UI", 11), width=22)
    get_date_entry.pack(side="left", padx=10)

    # ======== Date Report Frame
    date_report_frame = tkinter.Frame(date_report_page, bg="white")
    date_report_frame.pack(fill="x", padx=35, pady=15)

    def show_date():
        # Use .get_date() to return a datetime.date object, then convert it to a string
        selected_date = get_date_entry.get_date().strftime('%Y-%m-%d')

        # Call database function
        this_date_report = get_date_report(selected_date)

        # Clear existing cards first
        for child in date_report_frame.winfo_children():
            child.destroy()

        # Unpack the row into descriptive variables
        today_total_jobs, today_total_pages, today_total_cost = this_date_report

        # Safe fallback to 0 if the table is empty and returns None
        show_jobs = today_total_jobs or 0
        show_pages = today_total_pages or 0
        show_total = today_total_cost or 0

        # ---------- [ Total Jobs Card ]
        today_jobs = tkinter.Frame(date_report_frame, bg="#F5F5F5", width=160, height=100, relief="solid", bd=0)
        today_jobs.pack(side="left", padx=14)
        today_jobs.pack_propagate(False)

        tkinter.Label(today_jobs, text=show_jobs, font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 15))
        tkinter.Label(today_jobs, text="Total Jobs", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 12))

        # ---------- [ Total Pages Card ]
        today_pages = tkinter.Frame(date_report_frame, bg="#F5F5F5", width=160, height=100, relief="solid", bd=0)
        today_pages.pack(side="left", padx=14)
        today_pages.pack_propagate(False)

        tkinter.Label(today_pages, text=show_pages, font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 15))
        tkinter.Label(today_pages, text="Total Pages", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 12))

        # ---------- [ Total Revenue Card ]
        today_revenue = tkinter.Frame(date_report_frame, bg="#F5F5F5", width=160, height=100, relief="solid", bd=0)
        today_revenue.pack(side="left", padx=14)
        today_revenue.pack_propagate(False)

        tkinter.Label(today_revenue, text=show_total, font=("Segoe UI", 16, "bold"), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 15))
        tkinter.Label(today_revenue, text="Total Revenue", font=("Segoe UI", 10), bg="#F5F5F5").pack(anchor="w", padx=20, pady=(2, 12))

    # Show Button
    search_button = tkinter.Button(date_entry_frame, text="Search", font=("Segoe UI", 10), width=11, command=show_date)
    search_button.pack(side="left")

    # ====================================================
    # 03. Third Page => Customer Report
    # ====================================================
    customer_report_page = tkinter.Frame(workspace_frame, bg="white")

    # 1. validate user id
    def validate_customer_id(customer):
        if customer == "":
            messagebox.showerror("Missing Information", "Please enter the customer's ID.")
            return False
        return True

    # 2. search print job for a specific customer
    def search_customer_report():
        # 3. Get the raw text from the search box
        search_text = search_entry.get().strip()  # Read what the receptionist typed.

        # 4. Perform Validation
        if not validate_customer_id(search_text): return

        # 5. Run database retrieval
        customer_report = search_specific_customer_report(search_text)  # Ask the database to search.

        # 6. if the customer isn't there display this message
        if not customer_report:
            messagebox.showerror("Search Result", "Customer not found.")
            clear_search_box()
            return

        # 7. Remove previous results from the table to display new ones
        for row in customer_report_table.get_children():
            customer_report_table.delete(row)

        total_jobs = 0
        total_pages = 0
        total_cost = 0

        for report in customer_report:
            # 8. Unpack and display matching entries in a loop
            job_id, fullname, phone_number, customer_status, print_type, pages, cost, date_created = report

            total_jobs += 1              # Count each job row
            total_pages += (pages or 0)  # Accumulate total pages safely
            total_cost += (cost or 0)    # Accumulate total cost safely

            # 9. FORMAT DATA INDIVIDUALLY FOR THE TABLE ROW
            formatted_cost = f"Kes {cost:.2f}" if cost else "Kes 0.00"

            # 10. DISPLAY INTO THE TABLE ROWS
            customer_report_table.insert("", "end", values=(job_id, print_type, pages, formatted_cost, date_created))

        # 11. UPDATE THE LABELS AFTER THE LOOP FINISHES
        report_fullname_label.config(text=f"Customer: {fullname}")
        report_phone_label.config(text=f"Phone: {phone_number}")
        report_status_label.config(text=f"Status: {customer_status}")

        total_jobs_label.config(text=f"Total Jobs: {total_jobs}")
        total_pages_label.config(text=f"Total Pages: {total_pages}")
        total_revenue_label.config(text=f"Total Cost: Kes {total_cost:.2f}")

    # ---------- [ Search Utility ]
    search_frame = tkinter.Frame(customer_report_page, bg="white")
    search_frame.pack(fill="x", padx=20, pady=10)

    # Search Label
    search_label = tkinter.Label(search_frame, text="Search Customer ID:", font=("Segoe UI", 11), bg="white")
    search_label.pack(side="left")

    # Search Entry
    search_entry = tkinter.Entry(search_frame, font=("Segoe UI", 11), width=22)
    search_entry.pack(side="left", padx=10)

    # Search Button
    search_button = tkinter.Button(search_frame, text="Search", width=11, command=search_customer_report)
    search_button.pack(side="left", padx=(0, 30))

    # clear function
    def clear_search_box():
        # Wipes out all text inside the entry box
        search_entry.delete(0, "end")
        report_fullname_label.config(text=f"Customer: ")
        report_phone_label.config(text=f"Phone: ")
        report_status_label.config(text=f"Status: ")

        total_jobs_label.config(text=f"Total Jobs: 0")
        total_pages_label.config(text=f"Total Pages: 0")
        total_revenue_label.config(text=f"Total Cost: Kes 0")

        # refresh the labels & table
        for row in customer_report_table.get_children():
            customer_report_table.delete(row)

    # Clear Button
    clear_button = tkinter.Button(search_frame, text="Clear", width=11, command=clear_search_box)
    clear_button.pack(side="left")

    # ======== Specific Customer's Summary Frame
    get_summary_frame = tkinter.Frame(customer_report_page, bg="white")
    get_summary_frame.pack(fill="x", padx=20, pady=15)

    # Heading label
    summary_label = tkinter.Label(get_summary_frame, text="Specific Customer's Summary", font=("Segoe UI", 12, "bold"), bg="white")
    summary_label.pack(anchor="nw", padx=20, pady=(15, 5))

    # --- NEW CONTAINER FOR THE TWO CARDS ---
    # This holds both cards horizontally inside the main summary frame
    cards_container = tkinter.Frame(get_summary_frame, bg="white")
    cards_container.pack(fill="x", padx=20, pady=(0, 15))

    # Left side card
    left_side_frame = tkinter.Frame(cards_container, bg="white")

    # side="left" places it on the left; expand creates spacing
    left_side_frame.pack(side="left", anchor="nw", padx=(0, 20), pady=0)

    # left side elements
    report_fullname_label = tkinter.Label(left_side_frame, text="Customer: ", font=("Segoe UI", 11), bg="white")
    report_fullname_label.pack(anchor="w", pady=(0, 5))

    report_phone_label = tkinter.Label(left_side_frame, text="Phone: ", font=("Segoe UI", 11), bg="white")
    report_phone_label.pack(anchor="w", pady=(0, 5))

    report_status_label = tkinter.Label(left_side_frame, text="Status: ", font=("Segoe UI", 11), bg="white")
    report_status_label.pack(anchor="w", pady=(0, 5))

    # Right side card
    right_side_frame = tkinter.Frame(cards_container, bg="white")

    # side="left" makes it sit immediately to the right of the first frame
    right_side_frame.pack(side="left", anchor="nw", padx=20, pady=0)

    # right side elements
    total_jobs_label = tkinter.Label(right_side_frame, text="Total Jobs: 0", font=("Segoe UI", 11), bg="white")
    total_jobs_label.pack(anchor="w", pady=(0, 5))

    total_pages_label = tkinter.Label(right_side_frame, text="Total Pages: 0", font=("Segoe UI", 11), bg="white")
    total_pages_label.pack(anchor="w", pady=(0, 5))

    total_revenue_label = tkinter.Label(right_side_frame, text="Total Cost: 0", font=("Segoe UI", 11), bg="white")
    total_revenue_label.pack(anchor="w", pady=(0, 5))

    # ========= Create frame for the table
    table_frame = tkinter.Frame(customer_report_page, bg="white")
    table_frame.pack(fill="both", expand=True, padx=20, pady=10)

    # Create the Treeview
    customer_report_table = ttk.Treeview(table_frame, columns=("Job ID", "Type", "Pages", "Cost", "Date"), show="headings")

    # Create the headings
    customer_report_table.heading("Job ID", text="Job ID")
    customer_report_table.heading("Type", text="Type")
    customer_report_table.heading("Pages", text="Pages")
    customer_report_table.heading("Cost", text="Cost")
    customer_report_table.heading("Date", text="Date")

    # Set the column widths
    customer_report_table.column("Job ID", width=50)
    customer_report_table.column("Type", width=100)
    customer_report_table.column("Pages", width=50)
    customer_report_table.column("Cost", width=50)
    customer_report_table.column("Date", width=100)

    # display the table
    customer_report_table.pack(fill="both", expand=True)

    # ===================[ Show this page only after all the others exist  ]===================
    show_page(sales_summary_page)
    refresh_dashboard_chart(chart_frame)