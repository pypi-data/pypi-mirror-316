import mysql.connector

def create_conn():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="user",
            password="root",
            database="exam",
        )
        
        return conn if conn.is_connected() else None
    except Exception as err:
        print(err)
        print(f"Не получилось подключиться к баззе даннных")
        return None

def init_db():
    """Создание и заполнение таблиц тестовыми данными."""
    conn = create_conn()
    if conn is None:
        return
    
    cursor = conn.cursor()
    try:   
        # Заполнение таблиц тестовыми данными
        cursor.executemany(
            "INSERT INTO buses_marks (mark_name) VALUES (%s);",
            [("Mercedes",), ("Volvo",), ("MAN",)]
        )

        cursor.executemany(
            "INSERT INTO buses (gos_number, mark_id, capacity) VALUES (%s, %s, %s);",
            [
                ("AA1234BB", 1, 50),
                ("CC5678DD", 2, 60),
                ("EE9101FF", 3, 55)
            ]
        )

        cursor.executemany(
            "INSERT INTO stations (name) VALUES (%s);",
            [("Station A",), ("Station B",), ("Station C",)]
        )

        cursor.executemany(
            "INSERT INTO flights (station_id, bus_id, departure_time) VALUES (%s, %s, %s);",
            [
                (1, 1, "2024-12-22 10:00:00"),
                (2, 2, "2024-12-22 12:00:00"),
                (3, 3, "2024-12-22 14:00:00"),
                (1, 2, "2024-12-22 16:00:00"),
                (2, 3, "2024-12-22 18:00:00")
            ]
        )


        conn.commit()
        print("База данных инициализирована успешно.")
    except mysql.connector.Error as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()


def get_flights():
    """Получение данных о рейсах из представления."""
    conn = create_conn()
    if conn is None:
        return []
    
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM total_flights_capacity;")
        flights = cursor.fetchall()
        return flights
    except mysql.connector.Error as e:
        print(f"Ошибка при получении данных о рейсах: {e}")
        return []
    finally:
        cursor.close()
        conn.close()