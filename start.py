# Import the main EventScheduler class, which is the central application.
from main import EventScheduler

# Import individual functionalities from their respective scripts. These are modular functions that
# handle specific parts of the application, like adding, modifying, viewing, and deleting events.
from add_event import run as add_event
from modify_event import run as modify_event
from view_events import run as view_events
from delete_event import run as delete_event

# Import the Tk class from tkinter, which is used to create the graphical user interface (GUI).
from tkinter import Tk

# Entry point of the application.
if __name__ == "__main__":
    # Step 1: Create the root Tkinter window.
    # This serves as the main window for the application where all GUI components will reside.
    root = Tk()

    # Step 2: Initialize the EventScheduler application with the root Tkinter window.
    # The EventScheduler class handles the core application functionality, such as user login,
    # navigating between menus, and interacting with the database.
    main_app = EventScheduler(root)

    # Step 3: Dynamically link additional functionalities to the main application instance.
    # The `view_events` function will now be callable from the main application menu.
    main_app.view_events = lambda: view_events(main_app)

    # Similarly, the `delete_event` function is linked to the application for deleting events.
    main_app.delete_event = lambda: delete_event(main_app)

    # Step 4: Start the main Tkinter event loop.
    # This keeps the application running and listens for user interactions like button clicks.
    # Without this line, the GUI would not function.
    main_app.root.mainloop()