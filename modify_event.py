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

    def load_event_details(event_id):
        try:
            cursor = main_app.conn.cursor()
            query = "SELECT event_name, event_date, event_time, description FROM events WHERE event_id = %s"
            cursor.execute(query, (event_id,))
            event = cursor.fetchone()
            if event:
                edit_event_screen(event_id, event[0], event[1], event[2], event[3])
        except Error as e:
            show_error("Error", f"Database error: {e}")

    def edit_event_screen(event_id, event_name, event_date, event_time, description):
        def update_event():
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

        clear_screen()
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

        tk.Button(root, text="Update Event", command=update_event).pack(pady=10)
        tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()

    clear_screen()
    tk.Label(root, text="Modify Event", font=("Arial", 24)).pack(pady=20)

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
        tree.bind("<Double-1>", lambda event: load_event_details(event_map[event.widget.selection()[0]]))
    except Error as e:
        show_error("Error", f"Database error: {e}")

    tk.Button(root, text="Back to Menu", command=main_app.main_menu).pack()