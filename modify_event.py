from configparser import Error
import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_db_connection

def run(main_app):
    """
    The `run` function manages the 'Modify Event' feature, allowing the user to view, edit, and update their events.
    This function integrates with the main application (`main_app`) and interacts with the database to fetch
    and update event details.

    Args:
        main_app (EventScheduler): The main application instance, which provides access to the database connection
        and root Tkinter window.
    """
    root = main_app.root  # The main Tkinter window passed from the main application.

    # Utility Functions
    def clear_screen():
        """
        Removes all widgets from the current root window. This is used to refresh the interface when navigating
        between screens.
        """
        for widget in root.winfo_children():
            widget.destroy()

    def show_error(title, message):
        """
        Displays an error message in a popup window.
        Args:
            title (str): The title of the error popup.
            message (str): The error message to display.
        """
        messagebox.showerror(title, message)

    def show_info(title, message):
        """
        Displays an informational message in a popup window.
        Args:
            title (str): The title of the information popup.
            message (str): The message to display.
        """
        messagebox.showinfo(title, message)

    # Core Functionality
    def load_event_details(event_id):
        """
        Fetches details for a specific event by its ID and navigates to the event editing screen.

        Args:
            event_id (int): The ID of the event to fetch from the database.
        """
        try:
            cursor = main_app.conn.cursor()
            query = "SELECT event_name, event_date, event_time, description FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()  # Fetch the event details
            if event:
                edit_event_screen(event_id, event[0], event[1], event[2], event[3])
        except Error as e:
            show_error("Error", f"Database error: {e}")

    def edit_event_screen(event_id, event_name, event_date, event_time, description):
        """
        Displays the screen to edit a selected event's details.

        Args:
            event_id (int): The ID of the event being edited.
            event_name (str): The name of the event.
            event_date (str): The date of the event (in YYYY-MM-DD format).
            event_time (str): The time of the event (in HH:MM format).
            description (str): The description of the event.
        """
        def update_event():
            """
            Updates the event details in the database and navigates back to the main menu.
            """
            new_name = event_name_entry.get()
            new_date = event_date_entry.get()
            new_time = event_time_entry.get()
            new_description = description_entry.get()

            try:
                cursor = main_app.conn.cursor()
                query = """UPDATE events SET event_name = %s, event_date = %s, event_time = %s, description = %s
                           WHERE event_id = %s"""
                cursor.execute(query, (new_name, new_date, new_time, new_description, event_id))
                main_app.conn.commit()
                show_info("Success", "Event updated successfully!")
                main_app.main_menu()
            except Error as e:
                show_error("Error", f"Database error: {e}")

        clear_screen()  # Refresh the screen for editing

        # Create labels and input fields for each event attribute
        tk.Label(root, text="Edit Event", font=("Arial", 24)).pack(pady=20)

        tk.Label(root, text="Event Name").pack()
        event_name_entry = tk.Entry(root)
        event_name_entry.insert(0, event_name)
        event_name_entry.pack()

        tk.Label(root, text="Event Date (YYYY-MM-DD)").pack()
        event_date_entry = tk.Entry(root)
        event_date_entry.insert(0, event_date)
        event_date_entry.pack()

        tk.Label(root, text="Event Time (HH:MM)").pack()
        event_time_entry = tk.Entry(root)
        event_time_entry.insert(0, event_time)
        event_time_entry.pack()

        tk.Label(root, text="Description").pack()
        description_entry = tk.Entry(root)
        description_entry.insert(0, description)
        description_entry.pack()

        # Add buttons for updating the event or returning to the main menu
        tk.Button(root, text="Update Event", command=update_event).pack(pady=10)
        tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()

    # Main 'Modify Event' Screen
    clear_screen()
    tk.Label(root, text="Modify Event", font=("Arial", 24)).pack(pady=20)

    # Create a frame to display events in a table format
    frame = tk.Frame(root)
    frame.pack()

    # Create a Treeview widget to display event details
    tree = ttk.Treeview(frame, columns=("Name", "Date", "Time", "Description"), show="headings")
    tree.heading("Name", text="Event Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Description", text="Description")
    tree.pack()

    try:
        # Fetch all events for the logged-in user from the database
        cursor = main_app.conn.cursor()
        query = "SELECT event_id, event_name, event_date, event_time, description FROM events WHERE user_id = %s"
        cursor.execute(query, (main_app.current_user,))
        events = cursor.fetchall()  # Retrieve all events

        # Populate the Treeview with the retrieved events
        event_map = {
            tree.insert("", "end", values=(event[1], event[2], event[3], event[4])): event[0]
            for event in events
        }

        # Bind a double-click event to load the selected event for editing
        tree.bind("<Double-1>", lambda event: load_event_details(event_map[event.widget.selection()[0]]))
    except Error as e:
        show_error("Error", f"Database error: {e}")

    # Add a button to return to the main menu
    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()