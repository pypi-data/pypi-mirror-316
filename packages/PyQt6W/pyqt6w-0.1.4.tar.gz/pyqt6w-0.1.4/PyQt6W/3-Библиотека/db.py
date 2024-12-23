import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="LibraryDB"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Ошибка при подключении к базе данных: {err}")
        return None

