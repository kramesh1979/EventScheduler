from main import EventScheduler  # Import the main application
from add_event import run as add_event  # Import the add_event script
from modify_event import run as modify_event  # Import the modify_event script
from view_events import run as view_events  # Import the view_events script
from delete_event import run as delete_event  # Import the delete_event script
from tkinter import Tk  # Import Tk directly from tkinter

if __name__ == "__main__":
    root = Tk()  # Correctly create the Tkinter root window
    main_app = EventScheduler(root)  # Create the main application instance

    # To call the respective functions
    main_app.view_events = lambda: view_events(main_app)
    main_app.delete_event = lambda: delete_event(main_app)

    main_app.root.mainloop()  # Start the Tkinter main loop