import tkinter
from tkinter import ttk

# linking other windows to the dashboard
from database import initialize_database
from gui import window_customer
from gui import window_stock
from gui import window_print
from gui import window_report

# ========== [ 1. When program starts, no Child window is open ] ==========
window_customer_open = False
window_stock_open = False
window_print_open = False
window_report_open = False

# ========== [ 2. Dashboard Interface Settings ] ==========
root = tkinter.Tk()    # identifying it as root/main window
initialize_database()  # initialize database connection

# ---------- Title and size
root.title("Printing Shop Management System")
root.resizable(False, False)
window_width = 900  # windows width
window_height = 600  # widows height

# ---------- Actual Screen Size
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# ---------- Coordinates for centering the window
x = (screen_width - window_width) // 2    # splits the answer/space equally into left/right
y = (screen_height - window_height) // 2  # splits the answer/space equally into top/bottom

# ---------- Center the window using X/Y coordinates
root.geometry(f"{window_width}x{window_height}+{x}+{y}")


# ========== [ 3. Splash Screen Controller ] ==========
# ---------- Instantly hide dashboard window on startup
root.withdraw()

# ---------- Builds a temporary borderless splash screen with a linear 0-100% progress bar.
def show_splash_screen():
    global splash_window, progress, current_progress_value

    splash_window = tkinter.Toplevel()
    splash_window.overrideredirect(True)
    splash_window.config(bg="#F5F5F5")

    # Size and Center the splash window specifically
    splash_w, splash_h = 550, 320
    splash_x = (screen_width - splash_w) // 2
    splash_y = (screen_height - splash_h) // 2
    splash_window.geometry(f"{splash_w}x{splash_h}+{splash_x}+{splash_y}")

    # Splash Contents
    tkinter.Label(
        splash_window,
        text="🖨️ Printing Shop Management System",
        font=("Segoe UI", 18, "bold"),
        fg="#1A202C",
        bg="#F5F5F5"
    ).pack(expand=True, pady=(50, 5))

    tkinter.Label(
        splash_window,
        text="Version 2.0  •  Application Loading Interface ...",
        font=("Segoe UI", 10),
        fg="gray",
        bg="#F5F5F5"
    ).pack(expand=True, pady=(0, 20))

    # Custom loading bar layout
    style = ttk.Style()
    style.theme_use('default')
    style.configure(
        "Splash.Horizontal.TProgressbar",
        thickness=2,
        background="#1A202C",
        troughcolor="#E2E8F0"
    )

    # Changed mode to 'determinate' for fixed left-to-right filling
    progress = ttk.Progressbar(
        splash_window,
        style="Splash.Horizontal.TProgressbar",
        orient="horizontal",
        length=420,
        mode="determinate"
    )
    progress.pack(pady=(0, 50))

    # Track progress value manually
    current_progress_value = 0
    progress['value'] = 0

    # Start the smooth filling loop
    animate_progress_bar()

# ---------- Increments the progress bar smoothly. Reaches 100% in exactly 3 seconds.
def animate_progress_bar():
    global current_progress_value, splash_window

    # Total time = 3000ms. We update every 30ms.
    # 3000ms / 30ms = 100 steps total. Each step adds exactly 1% to the bar.
    if current_progress_value < 100:
        current_progress_value += 1
        progress['value'] = current_progress_value

        # Schedule the next incremental step in 30 milliseconds
        splash_window.after(30, animate_progress_bar)
    else:
        # The moment it reaches exactly 100%, trigger the transition immediately!
        hide_splash_and_show_dashboard()

# ---------- Destroys splash overlay structure safely and launches the main window.
def hide_splash_and_show_dashboard():
    global splash_window
    splash_window.destroy()  # Close loading window completely
    root.deiconify()         # Make your primary main dashboard visible to the user


# ========== [ 4. Title Label (Main Dashboard Elements) ] ==========
tkinter.Label(root, text="PRINTING SHOP MANAGEMENT SYSTEM", font=("Segoe UI", 20, "bold")).pack(pady=60)


# ========== [ 5. Dashboard Navigation Buttons ] ==========
# ----- Opening customer window -----
def open_customer_window():
    global window_customer_open

    # preventing opening duplicate windows
    if window_customer_open:  # Translation => "Is this window already open?"
        return  # simply => Stop, No same window will open
    window_customer_open = True  # Translation => "this window is now officially open."

    root.withdraw()  # hide dashboard (parent window stays hidden)

    # Open Customer window
    window_customer.open_customer_window(
        root,  # give it the Dashboard as its parent
        customer_closed  # tell it to call this function when it closes.
    )

# ----- Closing customer window -----
def customer_closed():  # Refer to this function when this window closes.
    global window_customer_open  # refer to this existing variable instead of creating a new one
    window_customer_open = False  # Dashboard notified that this window is closed
    root.deiconify()  # Dashboard window Opens


# ----- Opening stock window -----
def open_stock_window():
    global window_stock_open

    # preventing opening duplicate windows
    if window_stock_open:  # Translation => "Is this window already open?"
        return  # simply => Stop, No same window will open
    window_stock_open = True  # Translation => "this window is now officially open."

    root.withdraw()  # hide dashboard (parent window stays hidden)

    # Open stock window
    window_stock.open_stock_window(
        root,  # give it the Dashboard as its parent
        stock_closed  # tell it to call this function when it closes.
    )


# --------- Closing stock window
def stock_closed():  # Refer to this function when this window closes.
    global window_stock_open   # refer to this existing variable instead of creating a new one
    window_stock_open = False  # Dashboard notified that this window is closed
    root.deiconify()  # Dashboard window Opens


# ----- Opening print window -----
def open_print_window():
    global window_print_open

    # preventing opening duplicate windows
    if window_print_open:  # Translation => "Is this window already open?"
        return  # simply => Stop, No same window will open
    window_print_open = True  # Translation => "this window is now officially open."

    root.withdraw()  # hide dashboard (parent window stays hidden)

    # Open Print window
    window_print.open_print_window(
        root,  # give it the Dashboard as its parent
        print_closed  # tell it to call this function when it closes.
    )


# --------- Closing print window
def print_closed():  # Refer to this function when this window closes.
    global window_print_open  # refer to this existing variable instead of creating a new one
    window_print_open = False  # Dashboard notified that this window is closed
    root.deiconify()  # Dashboard window Opens


# ----- Opening report window -----
def open_report_window():
    global window_report_open

    # preventing opening duplicate windows
    if window_report_open:  # Translation => "Is this window already open?"
        return  # simply => Stop, No same window will open
    window_report_open = True  # Translation => "this window is now officially open."

    root.withdraw()  # hide dashboard (parent window stays hidden)

    # Open report window
    window_report.open_report_window(
        root,  # give it the Dashboard as its parent
        report_closed  # tell it to call this function when it closes.
    )


# --------- Closing report window
def report_closed():  # Refer to this function when this window closes.
    global window_report_open  # refer to this existing variable instead of creating a new one
    window_report_open = False  # Dashboard notified that Stock window is closed
    root.deiconify()  # Dashboard window Opens


# --------- navigation buttons
# Manage Customer
tkinter.Button(root, text="Manage Customers", font=("Segoe UI", 12), width=20, command=open_customer_window).pack(
    pady=10)

# Manage Stock
tkinter.Button(root, text="Manage Stock", font=("Segoe UI", 12), width=20, command=open_stock_window).pack(pady=10)

# Manage Printing Jobs
tkinter.Button(root, text="Manage Printing Jobs", font=("Segoe UI", 12), width=20, command=open_print_window).pack(
    pady=10)

# Generate Reports
tkinter.Button(root, text="Generate Reports", font=("Segoe UI", 12), width=20, command=open_report_window).pack(pady=10)

# Program's Version Label
tkinter.Label(root, text="Version 2.0", font=("Segoe UI", 10)).pack(side="bottom", pady=50)

# ========== [ START LOADING ORDER RUN ] ==========
show_splash_screen()

root.mainloop()
