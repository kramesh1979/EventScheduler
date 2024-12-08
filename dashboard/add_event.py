from tkinter import *
from db_connection import get_db_connection

def add_event():
    def save_event():
        event_name = event_name_entry.get()
        event_date = event_date_entry.get()
        event_time = event_time_entry.get()
        description = description_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO events (event_name, event_date, event_time, description) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (event_name, event_date, event_time, description))
        conn.commit()
        conn.close()

        status_label.config(text="Event added successfully!", fg="green")

    # Tkinter UI for adding events
    root = Tk()
    root.title("Add Event")

    Label(root, text="Event Name").pack()
    event_name_entry = Entry(root)
    event_name_entry.pack()

    Label(root, text="Event Date (YYYY-MM-DD)").pack()
    event_date_entry = Entry(root)
    event_date_entry.pack()

    Label(root, text="Event Time (HH:MM)").pack()
    event_time_entry = Entry(root)
    event_time_entry.pack()

    Label(root, text="Description").pack()
    description_entry = Entry(root)
    description_entry.pack()

    Button(root, text="Save", command=save_event).pack()
    status_label = Label(root, text="")
    status_label.pack()

    root.mainloop()