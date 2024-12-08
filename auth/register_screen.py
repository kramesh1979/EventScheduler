from tkinter import *
from db_connection import get_db_connection

def register_screen():
    def register_user():
        username = username_entry.get()
        password = password_entry.get()

        conn = get_db_connection()
        cursor = conn.cursor()

        query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        try:
            cursor.execute(query, (username, password))
            conn.commit()
            register_status_label.config(text="Registration successful!", fg="green")
        except:
            register_status_label.config(text="Error! Username may already exist.", fg="red")
        
        conn.close()

    # Tkinter UI for registration
    root = Tk()
    root.title("Register")
    
    Label(root, text="Username").pack()
    username_entry = Entry(root)
    username_entry.pack()

    Label(root, text="Password").pack()
    password_entry = Entry(root, show="*")
    password_entry.pack()

    Button(root, text="Register", command=register_user).pack()
    register_status_label = Label(root, text="")
    register_status_label.pack()

    root.mainloop()