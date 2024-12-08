import tkinter as tk
from tkinter import messagebox
from db_connection import get_db_connection
from datetime import datetime

def run(main_app):
    root = main_app.root

    def clear_screen():
        for widget in root.winfo_children():
            widget.destroy()

    def show_error(title, message):
        messagebox.showerror(title, message)

    def show_info(title, message):
        messagebox.showinfo(title, message)

    def add_event():
        event_name = event_name_entry.get()
        event_date = event_date_entry.get()
        event_time = event_time_entry.get()
        description = description_entry.get()

        # Check if the date is a future date
        try:
            event_date_dt = datetime.strptime(event_date, "%Y-%m-%d")
            event_date_only = event_date_dt.date()
            if event_date_only < datetime.now().date():
                show_error("Error", "Event date must be in the future!")
                return
        except ValueError:
            show_error("Error", "Invalid date format! Use YYYY-MM-DD.")
            return

        try:
            cursor = main_app.conn.cursor()
            query = """INSERT INTO events (user_id, event_name, event_date, event_time, description)
                       VALUES (%s, %s, %s, %s, %s)"""
            cursor.execute(query, (main_app.current_user, event_name, event_date, event_time, description))
            main_app.conn.commit()
            show_info("Success", "Event added successfully!")
            main_app.main_menu()
        except Error as e:
            show_error("Error", f"Database error: {e}")

    # GUI for adding event
    clear_screen()
    tk.Label(root, text="Add Event", font=("Arial", 24)).pack(pady=20)

    tk.Label(root, text="Event Name").pack()
    event_name_entry = tk.Entry(root)
    event_name_entry.pack()

    tk.Label(root, text="Event Date (YYYY-MM-DD)").pack()
    event_date_entry = tk.Entry(root)
    event_date_entry.pack()

    tk.Label(root, text="Event Time (HH:MM)").pack()
    event_time_entry = tk.Entry(root)
    event_time_entry.pack()

    tk.Label(root, text="Description").pack()
    description_entry = tk.Entry(root)
    description_entry.pack()

    tk.Button(root, text="Add Event", command=add_event).pack(pady=10)
    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()