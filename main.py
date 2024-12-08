from tkinter import messagebox, Tk, Label, Entry, Button, Frame
from db_connection import get_db_connection  # Import the database connection utility

class EventScheduler:
    def __init__(self, root):
        """
        Initializes the EventScheduler with a root Tk instance, sets the title,
        geometry, establishes the database connection, and starts the login screen.
        """
        self.root = root
        self.root.title("Event Alchemy")
        self.root.geometry("800x600")
        self.conn = get_db_connection()  # Establish database connection
        self.current_user = None  # To store the ID of the current user
        self.login_screen()  # Display the login screen initially

    # Utility Functions
    def clear_screen(self):
        """
        Clears all widgets from the current screen to prepare for a new screen.
        """
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_error(self, title, message):
        """
        Displays an error message using a messagebox.
        """
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        """
        Displays an informational message using a messagebox.
        """
        messagebox.showinfo(title, message)

    # Authentication Screens
    def login_screen(self):
        """
        Displays the login screen with fields for username and password, and buttons
        for logging in or registering a new account.
        """
        self.clear_screen()
        
        Label(self.root, text="Login", font=("Arial", 24)).pack(pady=20)
        Label(self.root, text="Username").pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        Label(self.root, text="Password").pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        Button(self.root, text="Login", command=self.login).pack(pady=10)
        Button(self.root, text="Register", command=self.register_screen).pack()

    def register_screen(self):
        """
        Displays the registration screen with fields for a new username and password,
        and buttons for submitting registration or going back to the login screen.
        """
        self.clear_screen()
        Label(self.root, text="Register", font=("Arial", 24)).pack(pady=20)
        Label(self.root, text="Username").pack()
        self.username_entry = Entry(self.root)
        self.username_entry.pack()

        Label(self.root, text="Password").pack()
        self.password_entry = Entry(self.root, show="*")
        self.password_entry.pack()

        Button(self.root, text="Register", command=self.register).pack(pady=10)
        Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def login(self):
        """
        Authenticates the user by checking the entered username and password against
        the database records. If valid, transitions to the main menu; otherwise, shows an error.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            cursor = self.conn.cursor()
            query = "SELECT user_id FROM users WHERE username = %s AND password = %s"
            cursor.execute(query, (username, password))
            result = cursor.fetchone()
            if result:
                self.current_user = result[0]
                self.main_menu()
            else:
                self.show_error("Login Failed", "Invalid credentials!")
        except Exception as e:  # Catch all exceptions for database error
            self.show_error("Error", f"Database error: {e}")

    def register(self):
        """
        Registers a new user by inserting the provided username and password into the database.
        If successful, transitions back to the login screen; otherwise, shows an error.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            self.conn.commit()
            self.show_info("Success", "Registration successful!")
            self.login_screen()
        except Exception as e:  # Catch all exceptions for database error
            self.show_error("Error", f"Database error: {e}")

    # Main Menu
    def main_menu(self):
        """
        Displays the main menu with options for adding, viewing, modifying, and deleting events,
        updating user information, and logging out. All elements are centered on the screen.
        """
        self.clear_screen()
    
        # Use a frame to help manage the layout
        frame = Frame(self.root)
        frame.pack(expand=True, fill='both')

        # Centering the title
        Label(frame, text="Event Alchemy", font=("Arial", 24)).pack(pady=10, side='top')
        Label(frame, text="Transforming Events into Experiences", font=("Arial", 10)).pack(pady=5, side='top')
    
        # Buttons to manage events, centered horizontally
        button_frame = Frame(frame)
        button_frame.pack(pady=20)  # Padding around the frame

        Button(button_frame, text="Add Event", command=self.add_event).pack(pady=5, side='left', padx=10)
        Button(button_frame, text="View Events", command=self.view_events).pack(pady=5, side='left', padx=10)
        Button(button_frame, text="Modify Event", command=self.modify_event).pack(pady=5, side='left', padx=10)
        Button(button_frame, text="Delete Event", command=self.delete_event).pack(pady=5, side='left', padx=10)
        Button(button_frame, text="Update User Info", command=self.update_user_info).pack(pady=5, side='left', padx=10)

        Button(frame, text="Logout", command=self.login_screen).pack(pady=10, side='top')
    # Load each module from separate scripts
    def add_event(self):
        """
        Imports the 'add_event' script and runs the 'run' function within it.
        """
        import add_event  # Import add_event script
        add_event.run(self)

    def modify_event(self):
        """
        Imports the 'modify_event' script and runs the 'run' function within it.
        """
        import modify_event  # Import modify_event script
        modify_event.run(self)

    def view_events(self):
        """
        Imports the 'view_events' script and runs the 'run' function within it.
        """
        import view_events  # Import view_events script
        view_events.run(self)

    def delete_event(self):
        """
        Imports the 'delete_event' script and runs the 'run' function within it.
        """
        import delete_event  # Import delete_event script
        delete_event.run(self)

    def update_user_info(self):
        """
        Placeholder function for updating user information. Implement logic as needed.
        """
        pass

if __name__ == "__main__":
    root = Tk()
    app = EventScheduler(root)
    root.mainloop()