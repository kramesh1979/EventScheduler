import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user=input("Enter username: "),
        password=input("Enter Password: "),
        database="event_scheduler"
    )