from configparser import Error  # Import Error class for handling configuration errors
import tkinter as tk  # Import tkinter for GUI creation
from tkinter import messagebox  # Import messagebox for pop-up alerts
from db_connection import get_db_connection  # Import the database connection utility
from datetime import datetime  # Import datetime for handling and validating date and time

def run(main_app):
    """
    Entry point to run the "Add Event" module.
    Accepts the main application object to ensure access to its resources like root, database connection, and current user.
    """
    root = main_app.root  # Reference the main application window

    def clear_screen():
        """
        Clears the current screen by destroying all widgets.
        Ensures a clean slate for displaying new content.
        """
        for widget in root.winfo_children():
            widget.destroy()

    def show_error(title, message):
        """
        Displays an error message using a messagebox.
        Used for notifying users about issues like invalid input or database errors.
        """
        messagebox.showerror(title, message)

    def show_info(title, message):
        """
        Displays an informational message using a messagebox.
        Used for positive feedback like successful operations.
        """
        messagebox.showinfo(title, message)

    def add_event():
        """
        Handles the logic for adding a new event to the database.
        1. Validates user inputs for the event name, date, time, and description.
        2. Ensures the event date is in the future.
        3. Inserts the event details into the database.
        4. Provides feedback to the user on success or failure.
        """
        # Fetch user input from entry fields
        event_name = event_name_entry.get()
        event_date = event_date_entry.get()
        event_time = event_time_entry.get()
        description = description_entry.get()

        # Validate the event date to ensure it is in the future
        try:
            event_date_dt = datetime.strptime(event_date, "%Y-%m-%d")  # Parse date string into a datetime object
            event_date_only = event_date_dt.date()  # Extract only the date portion
            if event_date_only < datetime.now().date():  # Check if the date is in the past
                raise ValueError("Kindly choose future dates to schedule an event.")  # Custom error message
        except ValueError as ve:
            show_error("Error", str(ve))  # Display the custom error message for invalid or past dates
            return

        # Insert event details into the database
        try:
            cursor = main_app.conn.cursor()  # Create a database cursor
            query = """INSERT INTO events (user_id, event_name, event_date, event_time, description)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (main_app.current_user, event_name, event_date, event_time, description))
            main_app.conn.commit()  # Commit the transaction
            show_info("Success", "Event added successfully!")  # Notify the user of success
            main_app.main_menu()  # Return to the main menu
        except Error as e:
            show_error("Error", f"Database error: {e}")  # Handle database errors

    # Set up the GUI for the "Add Event" screen
    clear_screen()  # Clear any existing widgets on the screen
    tk.Label(root, text="Add Event", font=("Arial", 24)).pack(pady=20)  # Title label

    # Input field for event name
    tk.Label(root, text="Event Name").pack()
    event_name_entry = tk.Entry(root)
    event_name_entry.pack()

    # Input field for event date
    tk.Label(root, text="Event Date (YYYY-MM-DD)").pack()
    event_date_entry = tk.Entry(root)
    event_date_entry.pack()

    # Input field for event time
    tk.Label(root, text="Event Time (HH:MM)").pack()
    event_time_entry = tk.Entry(root)
    event_time_entry.pack()

    # Input field for event description
    tk.Label(root, text="Description").pack()
    description_entry = tk.Entry(root)
    description_entry.pack()

    # Button to submit the event
    tk.Button(root, text="Add Event", command=add_event).pack(pady=10)

    # Button to return to the main menu
    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()