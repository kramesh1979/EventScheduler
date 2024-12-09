from configparser import Error
import tkinter as tk
from tkinter import ttk, messagebox
from sql.db_connection import get_db_connection  # Import the database connection function

def run(main_app):
    """
    Main function to display the 'View Events' screen in the event scheduling application.
    
    Args:
        main_app: An instance of the EventScheduler class containing database connection and user information.
    """
    root = main_app.root

    # Utility function to clear the current screen
    def clear_screen():
        """
        Removes all widgets from the current screen to prepare for a new view.
        """
        for widget in root.winfo_children():
            widget.destroy()

    # Utility function to show an error message
    def show_error(title, message):
        """
        Displays an error message box with the given title and message.
        
        Args:
            title (str): The title of the error message box.
            message (str): The error message to be displayed.
        """
        messagebox.showerror(title, message)

    # Utility function to show an informational message
    def show_info(title, message):
        """
        Displays an informational message box with the given title and message.
        
        Args:
            title (str): The title of the informational message box.
            message (str): The informational message to be displayed.
        """
        messagebox.showinfo(title, message)

    # Clear the current screen to start displaying events
    clear_screen()

    # Label for the 'View Events' title
    tk.Label(root, text="View Events", font=("Arial", 24)).pack(pady=20)

    # Frame to hold the Treeview widget
    frame = tk.Frame(root)
    frame.pack()

    # Treeview widget to display events
    tree = ttk.Treeview(frame, columns=("Name", "Date", "Time", "Description"), show="headings")
    tree.heading("Name", text="Event Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Description", text="Description")
    tree.pack()

    try:
        # Establish a database cursor
        cursor = main_app.conn.cursor()
        
        # SQL query to fetch events for the current user
        query = "SELECT event_id, event_name, event_date, event_time, description FROM events WHERE user_id = %s"
        cursor.execute(query, (main_app.current_user,))
        
        # Fetch all events
        events = cursor.fetchall()
        
        # Map events to the Treeview items
        event_map = {tree.insert("", "end", values=(event[1], event[2], event[3], event[4])): event[0] for event in events}
    except Error as e:
        # Display an error message if there's a database error
        show_error("Error", f"Database error: {e}")

    # Button to return to the main menu
    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()