from auth.login_screen import login_screen
from auth.register_screen import register_screen
from dashboard.main_menu import main_menu

def main():
    def app_entry():
        print("Welcome to Event Scheduler!")
        print("1. Login")
        print("2. Register")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("Launching Login Screen...")
            login_screen()
        elif choice == "2":
            print("Launching Registration Screen...")
            register_screen()
        else:
            print("Invalid choice. Please try again.")
            app_entry()

    # Start the application
    app_entry()

if __name__ == "__main__":
    main()