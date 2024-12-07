import tkinter as tk
from tkinter import ttk, messagebox
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
                self.main_screen()
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
    def main_screen(self):
        self.clear_screen()
        tk.Label(self.root, text="Event Scheduler", font=("Arial", 24)).pack(pady=20)
        tk.Button(self.root, text="Add Event", command=self.add_event_screen).pack(pady=5)
        tk.Button(self.root, text="View Events", command=self.view_events_screen).pack(pady=5)
        tk.Button(self.root, text="Logout", command=self.login_screen).pack(pady=5)

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
        tk.Button(self.root, text="Back", command=self.main_screen).pack()

    def add_event(self):
        event_name = self.event_name_entry.get()
        event_date = self.event_date_entry.get()
        event_time = self.event_time_entry.get()
        description = self.description_entry.get()
        try:
            cursor = self.conn.cursor()
            query = """INSERT INTO events (user_id, event_name, event_date, event_time, description)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (self.current_user, event_name, event_date, event_time, description))
            self.conn.commit()
            self.show_info("Success", "Event added successfully!")
            self.main_screen()
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

        tk.Button(self.root, text="Delete Selected Event", command=lambda: self.delete_event(tree)).pack(pady=10)
        tk.Button(self.root, text="Back", command=self.main_screen).pack()

    # Delete Event
    def delete_event(self, tree):
        selected_item = tree.selection()
        if not selected_item:
            self.show_error("Error", "No event selected!")
            return

        try:
            event_values = tree.item(selected_item)["values"]
            event_name, event_date = event_values[0], event_values[1]

            cursor = self.conn.cursor()
            query = """DELETE FROM events WHERE user_id = %s AND event_name = %s AND event_date = %s"""
            cursor.execute(query, (self.current_user, event_name, event_date))
            self.conn.commit()
            self.show_info("Success", "Event deleted successfully!")
            self.view_events_screen()
        except Error as e:
            self.show_error("Error", f"Database error: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = EventScheduler(root)
    root.mainloop()
    
    