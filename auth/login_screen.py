from tkinter import *
from db_connection import get_db_connection

def login_screen():
    def authenticate_user():
        username = username_entry.get()
        password = password_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        
        if user:
            login_status_label.config(text="Login successful!", fg="green")
            # Call main menu function (from dashboard/main_menu.py)
        else:
            login_status_label.config(text="Invalid credentials!", fg="red")
        
        conn.close()

    # Tkinter UI for login
    root = Tk()
    root.title("Login")
    
    Label(root, text="Username").pack()
    username_entry = Entry(root)
    username_entry.pack()

    Label(root, text="Password").pack()
    password_entry = Entry(root, show="*")
    password_entry.pack()

    Button(root, text="Login", command=authenticate_user).pack()
    login_status_label = Label(root, text="")
    login_status_label.pack()

    root.mainloop()