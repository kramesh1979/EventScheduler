from tkinter import *
from dashboard.add_event import add_event
from dashboard.view_event import view_events
from dashboard.delete_event import delete_event

def main_menu():
    def open_add_event():
        add_event()

    def open_view_events():
        view_events()

    def open_delete_event():
        delete_event()

    # Tkinter UI for main menu
    root = Tk()
    root.title("Main Menu")

    Button(root, text="Add Event", command=open_add_event).pack()
    Button(root, text="View Events", command=open_view_events).pack()
    Button(root, text="Delete Event", command=open_delete_event).pack()

    root.mainloop()