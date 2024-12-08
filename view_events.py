from configparser import Error
import tkinter as tk
from tkinter import ttk, messagebox
from db_connection import get_db_connection

def run(main_app):
    root = main_app.root

    def clear_screen():
        for widget in root.winfo_children():
            widget.destroy()

    def show_error(title, message):
        messagebox.showerror(title, message)

    def show_info(title, message):
        messagebox.showinfo(title, message)

    clear_screen()
    tk.Label(root, text="View Events", font=("Arial", 24)).pack(pady=20)

    frame = tk.Frame(root)
    frame.pack()

    tree = ttk.Treeview(frame, columns=("Name", "Date", "Time", "Description"), show="headings")
    tree.heading("Name", text="Event Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Description", text="Description")
    tree.pack()

    try:
        cursor = main_app.conn.cursor()
        query = "SELECT event_id, event_name, event_date, event_time, description FROM events WHERE user_id = %s"
        cursor.execute(query, (main_app.current_user,))
        events = cursor.fetchall()
        event_map = {tree.insert("", "end", values=(event[1], event[2], event[3], event[4])): event[0] for event in events}
    except Error as e:
        show_error("Error", f"Database error: {e}")

    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()