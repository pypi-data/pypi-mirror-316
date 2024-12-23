"""CREATE DATABASE WarrantyWorkshop;

USE WarrantyWorkshop;

CREATE TABLE Manufacturers (
    manufacturer_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE EquipmentTypes (
    equipment_type_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Clients (
    client_id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    address VARCHAR(255) NOT NULL
);

CREATE TABLE RepairCategories (
    repair_category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE Repairs (
    repair_id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT,
    equipment_type_id INT,
    repair_category_id INT,
    equipment_name VARCHAR(255),
    request_date DATE,
    completion_date DATE,
    FOREIGN KEY (client_id) REFERENCES Clients(client_id),
    FOREIGN KEY (equipment_type_id) REFERENCES EquipmentTypes(equipment_type_id),
    FOREIGN KEY (repair_category_id) REFERENCES RepairCategories(repair_category_id)
);


DELIMITER $$

CREATE PROCEDURE GetPendingRepairs()
BEGIN
    SELECT r.repair_id, c.full_name, e.name AS equipment_type, r.equipment_name, r.request_date
    FROM Repairs r
    JOIN Clients c ON r.client_id = c.client_id
    JOIN EquipmentTypes e ON r.equipment_type_id = e.equipment_type_id
    WHERE r.completion_date IS NULL;
END $$

DELIMITER ;


DELIMITER $$

CREATE PROCEDURE GetComplexRepairsByManufacturer()
BEGIN
    SELECT m.name AS manufacturer, COUNT(r.repair_id) AS complex_repairs
    FROM Repairs r
    JOIN Manufacturers m ON r.equipment_type_id = m.manufacturer_id
    JOIN RepairCategories rc ON r.repair_category_id = rc.repair_category_id
    WHERE rc.name = 'Сложный'
    GROUP BY m.name;
END $$

DELIMITER ;


INSERT INTO Manufacturers (name) VALUES ('Samsung'), ('LG'), ('Sony');

INSERT INTO EquipmentTypes (name) VALUES ('Телевизор'), ('Холодильник'), ('Стиральная машина');

INSERT INTO Clients (full_name, address) VALUES ('Иван Иванов', 'Москва, ул. Ленина, 1Автовокзал'), ('Петр Петров', 'Санкт-Петербург, ул. Мира, 2');

INSERT INTO RepairCategories (name) VALUES ('Простой'), ('Сложный');

-- Пример ремонтов
INSERT INTO Repairs (client_id, equipment_type_id, repair_category_id, equipment_name, request_date, completion_date)
VALUES
(1Автовокзал, 1Автовокзал, 2, 'Телевизор Samsung', '2024-12-01', NULL),
(2, 2, 1Автовокзал, 'Холодильник LG', '2024-12-05', '2024-12-10');"""





import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem
import matplotlib.pyplot as plt

# Создание подключения к базе данных
def create_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",  # Укажите ваш сервер MySQL
            user="root",  # Ваше имя пользователя
            password="admin",  # Ваш пароль
            database="WarrantyWorkshop"  # Убедитесь, что база данных существует
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Ошибка подключения: {err}")
        sys.exit(1)

# Получение невыполненных ремонтов
def get_pending_repairs():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.callproc('GetPendingRepairs')
    result = []
    for res in cursor.stored_results():
        result = res.fetchall()
    conn.close()
    return result

# Получение данных для диаграммы
def get_complex_repairs_by_manufacturer():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.callproc('GetComplexRepairsByManufacturer')
    result = []
    for res in cursor.stored_results():
        result = res.fetchall()
    conn.close()
    return result

# GUI для отображения данных
class WarrantyWorkshopApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Гарантийная мастерская')
        self.setGeometry(100, 100, 800, 600)
        layout = QVBoxLayout()

        # Кнопка для отображения невыполненных ремонтов
        self.pending_repairs_button = QPushButton('Показать невыполненные ремонты', self)
        self.pending_repairs_button.clicked.connect(self.show_pending_repairs)
        layout.addWidget(self.pending_repairs_button)

        # Кнопка для построения диаграммы
        self.chart_button = QPushButton('Построить диаграмму сложных ремонтов', self)
        self.chart_button.clicked.connect(self.show_complex_repairs_chart)
        layout.addWidget(self.chart_button)

        # Таблица для отображения данных
        self.table = QTableWidget(self)
        layout.addWidget(self.table)

        self.setLayout(layout)

    def show_pending_repairs(self):
        repairs = get_pending_repairs()
        self.table.setRowCount(len(repairs))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID Ремонта', 'Клиент', 'Тип техники', 'Название техники', 'Дата обращения'])

        for row, repair in enumerate(repairs):
            for col, value in enumerate(repair):
                self.table.setItem(row, col, QTableWidgetItem(str(value)))

    def show_complex_repairs_chart(self):
        data = get_complex_repairs_by_manufacturer()
        manufacturers = [item[0] for item in data]
        counts = [item[1] for item in data]

        plt.bar(manufacturers, counts)
        plt.xlabel('Производитель')
        plt.ylabel('Количество сложных ремонтов')
        plt.title('Сравнительная диаграмма сложных ремонтов по производителям')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = WarrantyWorkshopApp()
    window.show()
    sys.exit(app.exec())
