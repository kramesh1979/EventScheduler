from tkinter import *
from tkinter import messagebox
from db_connection import get_db_connection

def update_user():
    def update_user_details():
        """Update the user details in the database."""
        current_username = current_username_entry.get()
        new_username = new_username_entry.get()
        new_password = new_password_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()

        try:
            query = """
                UPDATE users
                SET username = %s, password = %s
                WHERE username = %s
            """
            cursor.execute(query, (new_username, new_password, current_username))
            if cursor.rowcount == 0:
                messagebox.showwarning("Error", "Current username not found.")
            else:
                conn.commit()
                messagebox.showinfo("Success", "User details updated successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Error updating user: {e}")
        finally:
            conn.close()

    # Tkinter window setup
    root = Tk()
    root.title("Update User Details")

    Label(root, text="Current Username").pack()
    current_username_entry = Entry(root)
    current_username_entry.pack()

    Label(root, text="New Username").pack()
    new_username_entry = Entry(root)
    new_username_entry.pack()

    Label(root, text="New Password").pack()
    new_password_entry = Entry(root, show="*")
    new_password_entry.pack()

    Button(root, text="Update Details", command=update_user_details).pack()

    # Run the Tkinter loop
    root.mainloop()