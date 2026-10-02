# Printing Shop Management System

## Version 2.0

## 1. Introduction
The Printing Shop Management System is a Python-based desktop application designed to help manage the daily operations of a printing shop.

The system provides a graphical user interface (GUI) that allows users to manage customers, printing materials, printing jobs, printing prices, and business reports from a central dashboard.

Version 2.0 was developed using Python, Tkinter, and SQLite. The system is designed to improve the organization of printing shop records, reduce manual record keeping, and provide easier access to customer, stock, printing, and sales information.


## 2. Project Objectives
The main objectives of the Printing Shop Management System are:
1. To provide a centralized system for managing printing shop operations.
2. To maintain organized customer records, including customer registration, updates, status management, and printing history.
3. To manage printing materials and monitor stock quantities used during printing operations.
4. To manage printing prices and use the current printing price when calculating the cost of a printing job.
5. To record printing jobs and maintain a history of completed printing operations.
6. To provide reports that allow the user to review sales, printing activity, and customer-specific information.
7. To reduce reliance on manual record keeping and make business information easier to access.
8. To provide a user-friendly graphical interface for performing common printing shop operations.


## 3. System Features
The Printing Shop Management System provides the following main features:

### 3.1 Customer Management
The Customer Management module allows the user to:

- Register new customers.
- Update customer information.
- Search for customers.
- View customer information and printing history.
- Deactivate customers when they are no longer active.
- Reactivate previously deactivated customers.
- Maintain customer history for important customer-related actions.

### 3.2 Stock Management
The Stock Management module allows the user to:

- Register printing shop stock items.
- Update stock information.
- Search for stock items.
- Monitor available stock quantities.
- Designate a stock item as the active printing material.
- Replace the currently selected printing material.
- Deactivate stock items without permanently removing their records.
- Reactivate previously deactivated stock items.
- Maintain a history of stock-related activities.

### 3.3 Printing Management
The Printing Management module allows the user to:

- Create new printing jobs.
- Validate customer information before creating a job.
- Check the availability of printing material.
- Validate the number of pages being printed.
- Calculate the cost of a printing job using the current printing price.
- Automatically reduce printing material stock after a successful printing job.
- View completed printing jobs.
- Search printing job records.
- Sort printing job records.
- Manage printing prices by adding, updating, and deleting prices.

### 3.4 Reports
The Reports module provides access to business information through:

- Sales summary reports.
- Date-based reports.
- Customer-specific reports.
- Total jobs and pages.
- Total revenue.
- Average revenue.
- Sales charts.

### 3.5 Dashboard
The Dashboard provides the main navigation interface for the system.

From the dashboard, the user can access:

- Customer Management
- Stock Management
- Printing Management
- Reports

The system also provides a splash screen when the application starts.


## 4. System Requirements
#### Python Libraries
The project uses the following Python libraries:

| Library | Purpose |
|---|---|
| Tkinter | Building the graphical user interface |
| SQLite3 | Connecting to and managing the SQLite database |
| Matplotlib | Displaying sales charts |
| TkCalendar | Providing date selection controls |
| Datetime | Working with dates and times |


## 5. System Architecture
The Printing Shop Management System Version 2.0 uses a modular desktop application architecture. 
The system separates the graphical user interface from the database operations and organizes 
the main functions of the application into separate modules.

### 5.1 Overall Architecture
The main flow of the application is:

User
↓
Dashboard
↓
GUI Modules
↓
Database Functions
↓
SQLite Database

The dashboard acts as the main navigation point of the application. From the dashboard, the user 
can access the Customer Management, Stock Management, Printing Management, and Reports modules.

### 5.2 Application Flow
A typical interaction with the system follows this general process:

1. The application starts through `dashboard.py`.
2. The database is initialized.
3. The splash screen is displayed.
4. The dashboard is displayed.
5. The user selects a required module.
6. The selected GUI module is opened.
7. The GUI collects and validates user input.
8. Database functions are called when information needs to be stored, updated, searched, or retrieved.
9. The SQLite database processes the requested operation.
10. The result is returned to the GUI and displayed to the user.


## 6. Database Design
The Printing Shop Management System uses SQLite as its database management system.

SQLite was selected because it provides a lightweight, file-based database
that can be used directly by the Python application without requiring a
separate database server.

The `database.py` module contains the SQL functions responsible for
creating tables and performing database operations such as inserting,
retrieving, updating, searching, and recording historical information.

### 6.1 Database Relationships
The main relationships between the Version 2 tables are:

- A customer can have multiple printing jobs.
- A customer can have multiple customer history records.
- A stock item can have multiple stock history records.
- A printing job is associated with the customer who requested it.

The relationships allow the system to connect operational records with
their associated customers and stock items.

### 6.2 Version 1 Database
Version 1 of the system was developed as a console-based application
before the Tkinter GUI version was created.

The original database structures and database functions were retained in
`database.py` as part of the Version 1 implementation.

Version 1 uses its own SQLite database file located in the main
application's `data` directory.

The Version 2 implementation was developed separately from these
structures while continuing to use the shared `database.py` module.


## 7. Business Rules and Validation
The system applies validation and business rules to ensure that operations
are performed using valid information and that important records remain
consistent.

### 7.1 Customer Rules
- Only active customers can be used to create new printing jobs.
- Deactivated customers cannot create new printing jobs.
- Deactivated customers can be reactivated.
- Previous printing records of deactivated customers remain available in reports and history.
- Customer-related actions are recorded in the customer history.

### 7.2 Stock Rules
- Stock items can be deactivated without permanently deleting their records.
- Deactivated stock items can be reactivated.
- Only an active stock item can be selected as the current printing material.
- The system prevents multiple materials that are active to considered as printing materials at the same time.
- Printing reduces the available quantity of the active printing material.
- Stock-related actions are recorded in the stock history.

### 7.3 Printing Rules
- A valid active customer must be provided before a printing job can be created.
- The number of pages must be valid before printing can proceed.
- Sufficient printing material must be available.
- The current printing price is used when calculating the printing cost.
- A successful printing job is recorded in the database.
- The required printing material is reduced after a successful printing operation.


## 8. Installation and Setup
The project can be run directly from the Python source code or packaged as a Windows executable.

### 8.1 Python Version
#### Project Setup
1. Copy or clone the project folder to the computer.
2. Ensure Python is installed and available on the system.
3. Install any required external Python packages.
4. Open the project in a Python development environment such as PyCharm.
5. Run the Version 2 application from `dashboard.py`.

### 8.2 Executable Version
When packaged as an executable, the application can be launched directly
without requiring the user to run the Python source files manually.

The application automatically creates its required database directory
and SQLite database file when the database is initialized.


## 9. Limitations and Future Improvements
The current version focuses on the core operations of a small printing
shop, including customer management, stock management, printing jobs,
printing prices, and reporting.

Future versions could expand the system with additional features such as
user accounts and access control, automated backups, or additional
business and reporting features.

## 10. Conclusion
The Printing Shop Management System provides a centralized solution for
managing the core operations of a small printing shop. The system brings
together customer management, stock management, printing operations,
pricing, and reporting within a single application. Version 2 extends the
original console-based system with a graphical interface designed to make
the system easier to operate and navigate. The project demonstrates the
use of Python, Tkinter, and SQLite to develop a practical desktop
application for managing business records and day-to-day operations.