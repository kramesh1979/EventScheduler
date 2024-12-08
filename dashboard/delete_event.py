from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connection import get_db_connection

def delete_event():
    def fetch_events():
        """Fetch and display all events in the tree view."""
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

    def delete_selected_event():
        """Delete the selected event by ID."""
        selected_item = tree.selection()

        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an event to delete.")
            return

        # Get the event ID of the selected item
        event_id = tree.item(selected_item, "values")[0]

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            # Confirm deletion
            confirmation = messagebox.askyesno("Confirm Deletion", f"Are you sure you want to delete Event ID {event_id}?")
            if confirmation:
                cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
                conn.commit()
                messagebox.showinfo("Success", f"Event ID {event_id} deleted successfully.")
                fetch_events()  # Refresh the tree view
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting event: {e}")
        finally:
            conn.close()

    # Tkinter window setup
    root = Tk()
    root.title("Delete Event")

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

    # Buttons
    fetch_button = Button(root, text="Fetch Events", command=fetch_events)
    fetch_button.pack()

    delete_button = Button(root, text="Delete Selected Event", command=delete_selected_event)
    delete_button.pack()

    # Status label
    status_label = Label(root, text="")
    status_label.pack()

    # Run the Tkinter loop
    root.mainloop()