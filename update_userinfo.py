from configparser import Error
import tkinter as tk
from tkinter import messagebox
from db_connection import get_db_connection

def run(main_app):
    """
    Entry point to run the "Update User Info" module.
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

    def update_user_info():
        """
        Handles the logic for updating the currently logged-in user's information.
        1. Validates user inputs for name and email.
        2. Updates the user details in the database.
        3. Provides feedback to the user on success or failure.
        """
        # Fetch user input from entry fields
        new_name = name_entry.get()
        new_email = email_entry.get()

        # Validate the email format
        if '@' not in new_email or '.' not in new_email.split('@')[-1]:
            show_error("Error", "Invalid email format.")  # Display error for invalid email format
            return

        # Update user details in the database
        try:
            cursor = main_app.conn.cursor()  # Create a database cursor
            query = """UPDATE users SET name = %s, email = %s WHERE user_id = %s"""
            cursor.execute(query, (new_name, new_email, main_app.current_user))
            main_app.conn.commit()  # Commit the transaction
            show_info("Success", "User information updated successfully!")  # Notify the user of success
            main_app.main_menu()  # Return to the main menu
        except Error as e:
            show_error("Error", f"Database error: {e}")  # Handle database errors

    # Set up the GUI for the "Update User Info" screen
    clear_screen()  # Clear any existing widgets on the screen
    tk.Label(root, text="Update User Information", font=("Arial", 24)).pack(pady=20)  # Title label

    # Input field for new user name
    tk.Label(root, text="New Name").pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    # Input field for new user email
    tk.Label(root, text="New Email").pack()
    email_entry = tk.Entry(root)
    email_entry.pack()

    # Button to submit the updates
    tk.Button(root, text="Update Info", command=update_user_info).pack(pady=10)

    # Button to return to the main menu
    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()