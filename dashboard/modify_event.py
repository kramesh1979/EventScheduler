from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from db_connection import get_db_connection

def modify_event():
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

    def load_event_details():
        """Load details of the selected event into the form for modification."""
        selected_item = tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select an event to modify.")
            return

        event_id = tree.item(selected_item, "values")[0]
        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM events WHERE id = %s", (event_id,))
            event = cursor.fetchone()
            if event:
                event_id_entry.config(state=NORMAL)
                event_id_entry.delete(0, END)
                event_id_entry.insert(0, event[0])
                event_id_entry.config(state=DISABLED)

                event_name_entry.delete(0, END)
                event_name_entry.insert(0, event[1])

                event_date_entry.delete(0, END)
                event_date_entry.insert(0, event[2])

                event_time_entry.delete(0, END)
                event_time_entry.insert(0, event[3])

                description_entry.delete(0, END)
                description_entry.insert(0, event[4])
        except Exception as e:
            status_label.config(text=f"Error: {e}", fg="red")
        finally:
            conn.close()

    def update_event():
        """Update the selected event in the database."""
        event_id = event_id_entry.get()
        event_name = event_name_entry.get()
        event_date = event_date_entry.get()
        event_time = event_time_entry.get()
        description = description_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = """
                UPDATE events 
                SET event_name = %s, event_date = %s, event_time = %s, description = %s
                WHERE id = %s
            """
            cursor.execute(query, (event_name, event_date, event_time, description, event_id))
            conn.commit()
            messagebox.showinfo("Success", f"Event ID {event_id} updated successfully.")
            fetch_events()
        except Exception as e:
            messagebox.showerror("Error", f"Error updating event: {e}")
        finally:
            conn.close()

    # Tkinter window setup
    root = Tk()
    root.title("Modify Event")

    # Treeview for displaying events
    columns = ("ID", "Event Name", "Date", "Time", "Description")
    tree = ttk.Treeview(root, columns=columns, show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Event Name", text="Event Name")
    tree.heading("Date", text="Date")
    tree.heading("Time", text="Time")
    tree.heading("Description", text="Description")
    tree.pack(fill=BOTH, expand=True)

    # Form to update event
    Label(root, text="Event ID").pack()
    event_id_entry = Entry(root, state=DISABLED)
    event_id_entry.pack()

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

    Button(root, text="Load Selected Event", command=load_event_details).pack()
    Button(root, text="Update Event", command=update_event).pack()

    # Status label
    status_label = Label(root, text="")
    status_label.pack()

    # Fetch button
    fetch_button = Button(root, text="Fetch Events", command=fetch_events)
    fetch_button.pack()

    # Run the Tkinter loop
    root.mainloop()