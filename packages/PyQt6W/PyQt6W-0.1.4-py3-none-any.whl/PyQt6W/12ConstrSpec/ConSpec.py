"""-- Создание базы данных и таблиц
CREATE DATABASE IF NOT EXISTS ConstructorDB;
USE ConstructorDB;

-- Таблица для разделов спецификации
CREATE TABLE IF NOT EXISTS SpecificationSections (
    SectionCode INT PRIMARY KEY,
    SectionName VARCHAR(255) NOT NULL
);

-- Таблица для предметов
CREATE TABLE IF NOT EXISTS Items (
    ItemCode INT PRIMARY KEY,
    Designation VARCHAR(255) NOT NULL,
    ItemName VARCHAR(255) NOT NULL,
    Unit VARCHAR(50) NOT NULL
);

-- Таблица для состава
CREATE TABLE IF NOT EXISTS Composition (
    CompositionCode INT PRIMARY KEY,
    NodeCode INT NOT NULL,
    SubNodeCode INT NOT NULL,
    Quantity INT NOT NULL,
    Position INT NOT NULL,
    FOREIGN KEY (NodeCode) REFERENCES Items(ItemCode),
    FOREIGN KEY (SubNodeCode) REFERENCES Items(ItemCode)
);

-- Хранимая процедура для печати спецификации по коду изделия
DELIMITER //
CREATE PROCEDURE GetSpecification(IN productCode INT)
BEGIN
    SELECT s.SectionCode, s.SectionName, i.ItemName, c.Quantity, c.Position
    FROM Composition c
    JOIN Items i ON c.SubNodeCode = i.ItemCode
    JOIN SpecificationSections s ON s.SectionCode = c.NodeCode
    WHERE c.NodeCode = productCode
    ORDER BY s.SectionCode, c.Position;
END //
DELIMITER ;

-- Хранимая процедура для получения списка стандартных изделий
DELIMITER //
CREATE PROCEDURE GetStandardItems()
BEGIN
    SELECT ItemName
    FROM Items
    WHERE Designation LIKE 'СТАНДАРТ%'
    ORDER BY ItemName;
END //
DELIMITER ;


USE ConstructorDB;

-- Заполнение таблицы разделов спецификации
INSERT INTO SpecificationSections (SectionCode, SectionName) VALUES
(1Автовокзал, 'Механика'),
(2, 'Электрика'),
(3, 'Гидравлика');

-- Заполнение таблицы предметов
INSERT INTO Items (ItemCode, Designation, ItemName, Unit) VALUES
(101, 'СТАНДАРТ-001', 'Шайба уплотнительная', 'шт'),
(102, 'СТАНДАРТ-002', 'Гайка М10', 'шт'),
(103, 'СТАНДАРТ-003', 'Болт М10х20', 'шт'),
(201, 'ДЕТАЛЬ-001', 'Корпус редуктора', 'шт'),
(202, 'ДЕТАЛЬ-002', 'Шестерня ведущая', 'шт'),
(203, 'ДЕТАЛЬ-003', 'Шестерня ведомая', 'шт'),
(301, 'УЗЕЛ-001', 'Редуктор', 'шт'),
(302, 'УЗЕЛ-002', 'Электродвигатель', 'шт'),
(303, 'УЗЕЛ-003', 'Насос гидравлический', 'шт');

-- Заполнение таблицы состава
INSERT INTO Composition (CompositionCode, NodeCode, SubNodeCode, Quantity, Position) VALUES
(1Автовокзал, 301, 201, 1Автовокзал, 1Автовокзал), -- Редуктор включает Корпус редуктора
(2, 301, 202, 1Автовокзал, 2), -- Редуктор включает Шестерню ведущую
(3, 301, 203, 1Автовокзал, 3), -- Редуктор включает Шестерню ведомую
(4, 302, 101, 10, 1Автовокзал), -- Электродвигатель включает Шайбу уплотнительную
(5, 302, 102, 10, 2), -- Электродвигатель включает Гайку М10
(6, 303, 103, 5, 1Автовокзал), -- Насос гидравлический включает Болт М10х20
(7, 303, 202, 1Автовокзал, 2); -- Насос гидравлический включает Шестерню ведущую

"""




import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QTextEdit, QWidget, QLineEdit, QLabel, QHBoxLayout
import mysql.connector

class ConstructorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конструкторская спецификация")
        self.setGeometry(100, 100, 800, 600)

        # Основной виджет
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Основной макет
        layout = QVBoxLayout()
        self.central_widget.setLayout(layout)

        # Поле ввода для кода изделия
        self.input_layout = QHBoxLayout()
        self.input_label = QLabel("Код изделия:")
        self.product_code_input = QLineEdit()
        self.get_spec_button = QPushButton("Печать спецификации")
        self.get_spec_button.clicked.connect(self.print_specification)
        self.input_layout.addWidget(self.input_label)
        self.input_layout.addWidget(self.product_code_input)
        self.input_layout.addWidget(self.get_spec_button)
        layout.addLayout(self.input_layout)

        # Кнопка для получения списка стандартных изделий
        self.get_standard_items_button = QPushButton("Алфавитный список стандартных изделий")
        self.get_standard_items_button.clicked.connect(self.print_standard_items)
        layout.addWidget(self.get_standard_items_button)

        # Поле вывода результата
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)

        # Подключение к базе данных
        self.db_connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="admin",  # Замените на ваш пароль
            database="ConstructorDB"
        )

    def print_specification(self):
        """Вывод спецификации по коду изделия"""
        product_code = self.product_code_input.text()
        if not product_code.isdigit():
            self.result_text.setText("Введите корректный числовой код изделия.")
            return

        cursor = self.db_connection.cursor()
        cursor.callproc("GetSpecification", [int(product_code)])
        self.result_text.clear()

        for result in cursor.stored_results():
            rows = result.fetchall()
            if rows:
                self.result_text.append("Спецификация:\n")
                for row in rows:
                    self.result_text.append(f"Раздел: {row[0]} ({row[1]}), "
                                            f"Изделие: {row[2]}, Количество: {row[3]}, Позиция: {row[4]}")
            else:
                self.result_text.setText("Данные не найдены.")

    def print_standard_items(self):
        """Вывод списка стандартных изделий"""
        cursor = self.db_connection.cursor()
        cursor.callproc("GetStandardItems")
        self.result_text.clear()

        for result in cursor.stored_results():
            rows = result.fetchall()
            if rows:
                self.result_text.append("Алфавитный список стандартных изделий:\n")
                for row in rows:
                    self.result_text.append(row[0])
            else:
                self.result_text.setText("Стандартные изделия не найдены.")

    def closeEvent(self, event):
        """Закрытие подключения при выходе"""
        self.db_connection.close()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ConstructorApp()
    window.show()
    sys.exit(app.exec())
