"""CREATE DATABASE Hotel;

USE Hotel;

CREATE TABLE Categories (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    category_name VARCHAR(255) NOT NULL
);

CREATE TABLE Rooms (
    room_id INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT,
    room_number INT NOT NULL,
    capacity INT NOT NULL,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);

CREATE TABLE Citizens (
    citizen_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    passport_number VARCHAR(20) NOT NULL
);

CREATE TABLE Accommodation (
    accommodation_id INT AUTO_INCREMENT PRIMARY KEY,
    citizen_id INT,
    room_id INT,
    check_in_date DATE NOT NULL,
    duration INT NOT NULL,  -- in days
    FOREIGN KEY (citizen_id) REFERENCES Citizens(citizen_id),
    FOREIGN KEY (room_id) REFERENCES Rooms(room_id)
);

-- Вставка тестовых данных
INSERT INTO Categories (category_name) VALUES ('Single'), ('Double'), ('Suite');

INSERT INTO Rooms (category_id, room_number, capacity) VALUES
(1Автовокзал, 101, 1Автовокзал), (1Автовокзал, 102, 1Автовокзал), (2, 201, 2), (2, 202, 2), (3, 301, 4);

INSERT INTO Citizens (full_name, passport_number) VALUES
('John Doe', '12345678'), ('Jane Smith', '23456789');





DELIMITER $$

-- Процедура для подсчета свободных номеров
CREATE PROCEDURE GetFreeRooms()
BEGIN
    SELECT r.room_id, r.room_number, c.category_name, r.capacity
    FROM Rooms r
    LEFT JOIN Accommodation a ON r.room_id = a.room_id
    LEFT JOIN Categories c ON r.category_id = c.category_id
    WHERE a.room_id IS NULL;
END $$

-- Процедура для расчета процента занятости по категориям
CREATE PROCEDURE GetOccupancyPercentage()
BEGIN
    SELECT c.category_name,
           ROUND((COUNT(a.room_id) / (SELECT COUNT(*) FROM Rooms r WHERE r.category_id = c.category_id)) * 100, 2) AS occupancy_percentage
    FROM Categories c
    LEFT JOIN Rooms r ON c.category_id = r.category_id
    LEFT JOIN Accommodation a ON r.room_id = a.room_id
    GROUP BY c.category_name, c.category_id;  -- добавлен c.category_id в GROUP BY
END $$

DELIMITER ;
"""



import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt6.QtCore import Qt


class HotelApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление Гостиницей")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QVBoxLayout()

        # Текстовое поле для отображения результатов
        self.result_text = QTextEdit(self)
        self.result_text.setReadOnly(True)
        self.layout.addWidget(self.result_text)

        # Кнопки для выполнения запросов
        self.btn_free_rooms = QPushButton('Показать Свободные Номера', self)
        self.btn_occupancy = QPushButton('Показать Занятость по Категориям', self)

        self.layout.addWidget(self.btn_free_rooms)
        self.layout.addWidget(self.btn_occupancy)

        # Подключение кнопок к методам
        self.btn_free_rooms.clicked.connect(self.show_free_rooms)
        self.btn_occupancy.clicked.connect(self.show_occupancy)

        self.setLayout(self.layout)

        # Подключение к базе данных MySQL
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",
            database="Hotel"
        )
        self.cursor = self.db_connection.cursor()

    def show_free_rooms(self):
        """Показать свободные номера, вызывая хранимую процедуру"""
        self.cursor.callproc('GetFreeRooms')

        result = ""
        for result_set in self.cursor.stored_results():
            for row in result_set.fetchall():
                result += f"Номер ID: {row[0]}, Номер: {row[1]}, Категория: {row[2]}, Вместимость: {row[3]}\n"

        self.result_text.setText(result)

    def show_occupancy(self):
        """Показать процент занятости по категориям"""
        self.cursor.callproc('GetOccupancyPercentage')

        result = ""
        for result_set in self.cursor.stored_results():
            for row in result_set.fetchall():
                result += f"Категория: {row[0]}, Занятость: {row[1]}%\n"

        self.result_text.setText(result)

    def closeEvent(self, event):
        """Закрытие соединения с базой данных при выходе из приложения"""
        self.cursor.close()
        self.db_connection.close()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HotelApp()
    window.show()
    sys.exit(app.exec())
