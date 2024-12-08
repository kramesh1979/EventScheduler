import tkinter as tk
from tkinter import messagebox
from mysql.connector import Error
from db_connection import get_db_connection
from datetime import datetime

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

        tk.Button(self.root, text="Add Event", command=self.add_event_screen).pack(pady=5)
        tk.Button(self.root, text="View Events", command=self.view_events_screen).pack(pady=5)
        tk.Button(self.root, text="Modify Event", command=self.modify_event_screen).pack(pady=5)
        tk.Button(self.root, text="Delete Event", command=self.delete_event_screen).pack(pady=5)
        tk.Button(self.root, text="Update User Info", command=self.update_user_screen).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=10)

    # Add Event
    def add_event_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Add Event", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Event Name").pack()
        self.event_name_entry = tk.Entry(self.root)
        self.event_name_entry.pack()

        tk.Label(self.root, text="Event Date (YYYY-MM-DD)").pack()
        self.event_date_entry = tk.Entry(self.root)
        self.event_date_entry.pack()

        tk.Label(self.root, text="Event Time (HH:MM)").pack()
        self.event_time_entry = tk.Entry(self.root)
        self.event_time_entry.pack()

        tk.Label(self.root, text="Description").pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.pack()

        tk.Button(self.root, text="Add Event", command=self.add_event).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack()

    def add_event(self):
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_time = self.event_time_entry.get()
        description = self.description_entry.get()

        # Check if the date is a future date
        try:
            event_date_dt = datetime.strptime(event_date, "%Y-%m-%d")
            if event_date_dt < datetime.now().date():
                self.show_error("Error", "Event date must be in the future!")
                return
        except ValueError:
            self.show_error("Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        try:
            cursor = self.conn.cursor()
            query = """INSERT INTO events (user_id, event_name, event_date, event_time, description)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (self.current_user, event_name, event_date, event_time, description))
            self.conn.commit()
            self.show_info("Success", "Event added successfully!")
            self.main_menu()
        except Error as e:
            self.show_error("Error", f"Database error: {e}")

    # View Events
    def view_events_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="My Events", font=("Arial", 24)).pack(pady=20)
        frame = tk.Frame(self.root)
        frame.pack()

        tree = ttk.Treeview(frame, columns=("Name", "Date", "Time", "Description"), show="headings")
        tree.heading("Name", text="Event Name")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Description", text="Description")
        tree.pack()

        try:
            cursor = self.conn.cursor()
            query = "SELECT event_name, event_date, event_time, description FROM events WHERE user_id = %s"
            cursor.execute(query, (self.current_user,))
            events = cursor.fetchall()
            for event in events:
                tree.insert("", "end", values=event)
        except Error as e:
            self.show_error("Error", f"Database error: {e}")

        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=10)

    # Modify Event Screen
    def modify_event_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Modify Event", font=("Arial", 24)).pack(pady=20)
        
        frame = tk.Frame(self.root)
        frame.pack()

        tree = ttk.Treeview(frame, columns=("Name", "Date", "Time", "Description"), show="headings")
        tree.heading("Name", text="Event Name")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Description", text="Description")
        tree.pack()

        try:
            cursor = self.conn.cursor()
            query = "SELECT event_id, event_name, event_date, event_time, description FROM events WHERE user_id = %s"
            cursor.execute(query, (self.current_user,))
            events = cursor.fetchall()
            self.event_map = {tree.insert("", "end", values=(event[1], event[2], event[3], event[4])): event[0] for event in events}
        except Error as e:
            self.show_error("Error", f"Database error: {e}")
            return

        tk.Button(self.root, text="Modify Selected Event", command=lambda: self.load_event_details(tree)).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=10)

    # Load Selected Event Details for Modification
    def load_event_details(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            self.show_error("Error", "No event selected!")
            return
        
        event_id = self.event_map[selected_item[0]]

        try:
            cursor = self.conn.cursor()
            query = "SELECT event_name, event_date, event_time, description FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()
            if event:
                self.edit_event_screen(event_id, event[0], event[1], event[2], event[3])
        except Error as e:
            self.show_error("Error", f"Database error: {e}")

    # Edit Event Screen
    def edit_event_screen(self, event_id, event_name, event_date, event_time, description):
        self.clear_screen()
        tk.Label(self.root, text="Edit Event", font=("Arial", 24)).pack(pady=20)

        tk.Label(self.root, text="Event Name").pack()
        self.event_name_entry = tk.Entry(self.root)
        self.event_name_entry.insert(0, event_name)
        self.event_name_entry.pack()

        tk.Label(self.root, text="Event Date (YYYY-MM-DD)").pack()
        self.event_date_entry = tk.Entry(self.root)
        self.event_date_entry.insert(0, event_date)
        self.event_date_entry.pack()

        tk.Label(self.root, text="Event Time (HH:MM)").pack()
        self.event_time_entry = tk.Entry(self.root)
        self.event_time_entry.insert(0, event_time)
        self.event_time_entry.pack()

        tk.Label(self.root, text="Description").pack()
        self.description_entry = tk.Entry(self.root)
        self.description_entry.insert(0, description)
        self.description_entry.pack()

        tk.Button(self.root, text="Update Event", command=lambda: self.update_event(event_id)).pack(pady=10)
        tk.Button(self.root, text="Back to Modify Events", command=self.modify_event_screen).pack()

    def update_event(self, event_id):
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_time = self.event_time_entry.get()
        description = self.description_entry.get()

        # Check if the date is a future date
        try:
            event_date_dt = datetime.strptime(event_date, "%Y-%m-%d")
            if event_date_dt < datetime.now().date():
                self.show_error("Error", "Event date must be in the future!")
                return
        except ValueError:
            self.show_error("Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        try:
            cursor = self.conn.cursor()
            query = """UPDATE events SET event_name = %s, event_date = %s, event_time = %s, description = %s
                       WHERE event_id = %s"""
            cursor.execute(query, (event_name, event_date, event_time, description, event_id))
            self.conn.commit()
            self.show_info("Success", "Event updated successfully!")
            self.modify_event_screen()
        except Error as e:
            self.show_error("Error", f"Database error: {e}")

    # Delete Event Screen
    def delete_event_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Delete Event", font=("Arial", 24)).pack(pady=20)
        
        frame = tk.Frame(self.root)
        frame.pack()

        tree = ttk.Treeview(frame, columns=("Name", "Date", "Time", "Description"), show="headings")
        tree.heading("Name", text="Event Name")
        tree.heading("Date", text="Date")
        tree.heading("Time", text="Time")
        tree.heading("Description", text="Description")
        tree.pack()

        try:
            cursor = self.conn.cursor()
            query = "SELECT event_id, event_name, event_date, event_time, description FROM events WHERE user_id = %s"
            cursor.execute(query, (self.current_user,))
            events = cursor.fetchall()
            self.event_map = {tree.insert("", "end", values=(event[1], event[2], event[3], event[4])): event[0] for event in events}
        except Error as e:
            self.show_error("Error", f"Database error: {e}")
            return

        tk.Button(self.root, text="Delete Selected Event", command=lambda: self.delete_event(tree)).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack(pady=10)

    # Delete Selected Event
    def delete_event(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            self.show_error("Error", "No event selected!")
            return
        
        event_id = self.event_map[selected_item[0]]

        try:
            cursor = self.conn.cursor()
            query = "DELETE FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            self.conn.commit()
            self.show_info("Success", "Event deleted successfully!")
            self.delete_event_screen()
        except Error as e:
            self.show_error("Error", f"Database error: {e}")

    # Update User Screen
    def update_user_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Update User Info", font=("Arial", 24)).pack(pady=20)
        tk.Label(self.root, text="New Username").pack()
        self.username_entry = tk.Entry(self.root)
        self.username_entry.pack()

        tk.Label(self.root, text="New Password").pack()
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.pack()

        tk.Button(self.root, text="Update Info", command=self.update_user_info).pack(pady=10)
        tk.Button(self.root, text="Back to Menu", command=self.main_menu).pack()

    def update_user_info(self):
        new_username = self.username_entry.get()
        new_password = self.password_entry.get()

        try:
            cursor = self.conn.cursor()
            query = """UPDATE users SET username = %s, password = %s WHERE user_id = %s"""
            cursor.execute(query, (new_username, new_password, self.current_user))
            self.conn.commit()
            self.show_info("Success", "User info updated successfully!")
            self.main_menu()
        except Error as e:
            self.show_error("Error", f"Database error: {e}")



if __name__ == "__main__":
    root = tk.Tk()
    app = EventScheduler(root)
    root.mainloop()