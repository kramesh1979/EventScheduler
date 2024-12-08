import tkinter as tk
from tkinter import messagebox
from db_connection import get_db_connection

class EventScheduler:
    def __init__(self, root):
        self.root = root
        self.root.title("Event Scheduler")
        self.root.geometry("800x600")
        self.conn = get_db_connection()
        self.current_user = None
        self.login_screen()

    # Utility Functions
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_error(self, title, message):
        messagebox.showerror(title, message)

    def show_info(self, title, message):
        messagebox.showinfo(title, message)

    # Authentication Screens
    def login_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Login", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register", command=self.register_screen).pack()

    def register_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Register", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Register", command=self.register).pack(pady=10)
        tk.Button(self.root, text="Back to Login", command=self.login_screen).pack()

    def login(self):
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
        except Error as e:
            self.show_error("Error", f"Database error: {e}")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        try:
            cursor = self.conn.cursor()
            query = "INSERT INTO users (username, password) VALUES (%s, %s)"
            cursor.execute(query, (username, password))
            self.conn.commit()
            self.show_info("Success", "Registration successful!")
            self.login_screen()
        except Error as e:
            self.show_error("Error", f"Database error: {e}")

    # Main Menu
    def main_menu(self):
        self.clear_screen()
        tk.Label(self.root, text="Event Scheduler", font=("Arial", 24)).pack(pady=20)

        tk.Button(self.root, text="Add Event", command=self.add_event).pack(pady=5)
        tk.Button(self.root, text="View Events", command=self.view_events).pack(pady=5)
        tk.Button(self.root, text="Modify Event", command=self.modify_event).pack(pady=5)
        tk.Button(self.root, text="Delete Event", command=self.delete_event).pack(pady=5)
        tk.Button(self.root, text="Update User Info", command=self.update_user_info).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)

    # Load each module from separate scripts
    def add_event(self):
        import add_event  # Import add_event script
        add_event.run(self)

    def modify_event(self):
        import modify_event  # Import modify_event script
        modify_event.run(self)

    def view_events(self):
        # Placeholder for view events
        pass

    def delete_event(self):
        # Placeholder for delete event
        pass

    def update_user_info(self):
        # Placeholder for updating user info
        pass


if __name__ == "__main__":
    root = tk.Tk()
    app = EventScheduler(root)
    root.mainloop()