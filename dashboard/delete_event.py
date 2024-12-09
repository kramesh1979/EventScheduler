from configparser import Error  # Import Error class for handling configuration-related exceptions
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from sql.db_connection import get_db_connection  # Import the database connection utility

def run(main_app):
    root = main_app.root  # Reference to the root Tkinter window of the main application

    # Function to clear the current screen by removing all its widgets
    def clear_screen():
        for widget in root.winfo_children():
            widget.destroy()

    # Function to show an error message in a pop-up window
    def show_error(title, message):
        messagebox.showerror(title, message)

    # Function to show an informational message in a pop-up window
    def show_info(title, message):
        messagebox.showinfo(title, message)

    # Function to delete an event from the database
    def delete_event(event_id):
        if not event_id:
            show_info("Info", "No events to delete")  # Show info message if no event is selected
            return
        
        try:
            cursor = main_app.conn.cursor()  # Get a cursor object from the database connection
            query = "DELETE FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))  # Execute delete query with the provided event_id
            main_app.conn.commit()  # Commit the transaction to the database
            show_info("Success", "Event deleted successfully!")  # Notify user of success
            main_app.view_events()  # Refresh the event list on the main menu
        except Error as e:
            show_error("Error", f"Database error: {e}")  # Show error if a database issue occurs

    # Clear the screen and set up the UI for deleting an event
    clear_screen()
    tk.Label(root, text="Delete Event", font=("Arial", 24)).pack(pady=20)

    frame = tk.Frame(root)  # Create a frame to manage layout within the window
    frame.pack()

    # Set up a Treeview widget to display the list of events
    tree = ttk.Treeview(frame, columns=("Name", "Date", "Time", "Description"), show="headings")
    tree.heading("Name", text="Event Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Description", text="Description")
    tree.pack()

    try:
        cursor = main_app.conn.cursor()  # Get a cursor object from the database connection
        query = "SELECT event_id, event_name, event_date, event_time, description FROM events WHERE user_id = %s"
        cursor.execute(query, (main_app.current_user,))  # Execute query to fetch events for the current user
        events = cursor.fetchall()  # Fetch all events from the result set
        event_map = {tree.insert("", "end", values=(event[1], event[2], event[3], event[4])): event[0] for event in events}
        # Bind the Delete action to the selected event in the Treeview
        tree.bind("<Delete>", lambda e: delete_event(event_map.get(tree.selection(), None)))
    except Error as e:
        show_error("Error", f"Database error: {e}")

    # Add a Delete button to delete the selected event
    delete_button = tk.Button(root, text="Delete Selected Event", command=lambda: delete_event(event_map.get(tree.selection()[0], None)))
    delete_button.pack(pady=10)
    
    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()  # Button to return to the main menu