from tkinter import *
from tkinter import ttk
from db_connection import get_db_connection

def view_events():
    def fetch_events():
        # Connect to the database and fetch events
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM events")
            rows = cursor.fetchall()
            # Clear the tree view
            for row in tree.get_children():
                tree.delete(row)
            # Insert rows into the tree view
            for row in rows:
                tree.insert("", END, values=row)
        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="red")
        finally:
            conn.close()

    # Tkinter window setup
    root = Tk()
    root.title("View Events")

    # Treeview for displaying events
    columns = ("ID", "Event Name", "Date", "Time", "Description")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Event Name", text="Event Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Description", text="Description")
    tree.column("ID", width=50)
    tree.column("Event Name", width=150)
    tree.column("Date", width=100)
    tree.column("Time", width=100)
    tree.column("Description", width=200)
    tree.pack(fill=BOTH, expand=True)

    # Status label for messages
    status_label = Label(root, text="")
    status_label.pack()

    # Fetch events button
    fetch_button = Button(root, text="Fetch Events", command=fetch_events)
    fetch_button.pack()

    # Run the Tkinter loop
    root.mainloop()