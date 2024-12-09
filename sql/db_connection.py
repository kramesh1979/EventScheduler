import mysql.connector  # Import the MySQL connector library to interact with MySQL databases

def get_db_connection():
    """
    Establishes and returns a connection to the MySQL database using the provided credentials.
    
    Prompts the user to enter the database username and password, then uses these credentials
    to connect to a MySQL database named "event_scheduler" running on the local host.
    
    Returns:
        A MySQL connection object.
    """
    # Prompt the user for the database username
    username = input("Enter username: ")
    
    # Prompt the user for the database password
    password = input("Enter Password: ")
    
    # Establish and return a connection to the MySQL database
    return mysql.connector.connect(
        host="localhost",  # Host address for the MySQL server
        user=username,  # Database username entered by the user
        password=password,  # Database password entered by the user
        database="event_scheduler"  # Database name
    )