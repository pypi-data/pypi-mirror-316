# 16.	Склад
# В базе данных содержатся сведения о грузах и размещении на стеллажах.
# Таблицы: Стеллажи (Код стеллажа, номер, количество ячеек, допустимая масса), Груз (Код груза, название), Позиция (Код груза, код стеллажа, номер ячейки, масса, дата укладки).
# Требуется:
# - определить количество свободных ячеек;
# - построить диаграмму сравнительного стеллажей заполнения (в процентах по массе).



# CREATE DATABASE Warehouse;
#
# USE Warehouse;
#
# -- Таблица для стеллажей
# CREATE TABLE Racks (
#     RackID INT PRIMARY KEY AUTO_INCREMENT,
# Number INT NOT NULL,
# CellCount INT NOT NULL,
# MaxWeight FLOAT NOT NULL
# );
#
# -- Таблица для грузов
# CREATE TABLE Cargo (
#     CargoID INT PRIMARY KEY AUTO_INCREMENT,
# Name VARCHAR(255) NOT NULL
# );
#
# -- Таблица для позиций
# CREATE TABLE Position (
#     PositionID INT PRIMARY KEY AUTO_INCREMENT,
# CargoID INT,
# RackID INT,
# CellNumber INT NOT NULL,
# Weight FLOAT NOT NULL,
# PlacementDate DATE NOT NULL,
# FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID),
# FOREIGN KEY (RackID) REFERENCES Racks(RackID)
# );
#
# -- Хранимая процедура для подсчета свободных ячеек
# DELIMITER //
# CREATE PROCEDURE GetFreeCells()
# BEGIN
# SELECT
# R.RackID,
# R.Number AS RackNumber,
# R.CellCount - COUNT(P.PositionID) AS FreeCells
# FROM
# Racks R
# LEFT JOIN
# Position P ON R.RackID = P.RackID
# GROUP BY
# R.RackID;
# END //
# DELIMITER ;
#
# -- Хранимая процедура для получения данных заполнения стеллажей
# DELIMITER //
# CREATE PROCEDURE GetRackUsage()
# BEGIN
# SELECT
# R.RackID,
# R.Number AS RackNumber,
# SUM(P.Weight) AS TotalWeight,
# R.MaxWeight AS MaxWeight,
# (SUM(P.Weight) / R.MaxWeight) * 100 AS UsagePercent
# FROM
# Racks R
# LEFT JOIN
# Position P ON R.RackID = P.RackID
# GROUP BY
# R.RackID;
# END //
# DELIMITER ;
#
#
# -- Очистка таблиц перед заполнением
# DELETE FROM Position;
# DELETE FROM Cargo;
# DELETE FROM Racks;
#
# -- Заполнение таблицы Racks (Стеллажи)
# INSERT INTO Racks (Number, CellCount, MaxWeight)
# VALUES
# (1, 10, 500.0),  -- Стеллаж 1: 10 ячеек, максимальная масса 500 кг
# (2, 8, 400.0),   -- Стеллаж 2: 8 ячеек, максимальная масса 400 кг
# (3, 12, 600.0);  -- Стеллаж 3: 12 ячеек, максимальная масса 600 кг
#
# -- Заполнение таблицы Cargo (Грузы)
# INSERT INTO Cargo (Name)
# VALUES
# ('Груз 1'),
# ('Груз 2'),
# ('Груз 3'),
# ('Груз 4');
#
# -- Заполнение таблицы Position (Размещение грузов)
# INSERT INTO Position (CargoID, RackID, CellNumber, Weight, PlacementDate)
# VALUES
# (1, 1, 1, 50.0, '2024-12-20'),  -- Груз 1, Стеллаж 1, Ячейка 1, Вес 50 кг
# (2, 1, 2, 30.0, '2024-12-21'),  -- Груз 2, Стеллаж 1, Ячейка 2, Вес 30 кг
# (3, 2, 1, 100.0, '2024-12-22'), -- Груз 3, Стеллаж 2, Ячейка 1, Вес 100 кг
# (4, 3, 1, 150.0, '2024-12-23'), -- Груз 4, Стеллаж 3, Ячейка 1, Вес 150 кг
# (1, 3, 2, 200.0, '2024-12-24'); -- Груз 1, Стеллаж 3, Ячейка 2, Вес 200 кг


import sys

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget,
    QTableWidgetItem, QWidget
)
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis
from mysql.connector import connect, Error


class WarehouseApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Склад - Управление")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.table_widget = QTableWidget()
        self.layout.addWidget(self.table_widget)

        self.load_free_cells_button = QPushButton("Показать свободные ячейки")
        self.load_free_cells_button.clicked.connect(self.show_free_cells)
        self.layout.addWidget(self.load_free_cells_button)

        self.load_usage_chart_button = QPushButton("Показать диаграмму заполнения")
        self.load_usage_chart_button.clicked.connect(self.show_usage_chart)
        self.layout.addWidget(self.load_usage_chart_button)

    def show_free_cells(self):
        """Показать количество свободных ячеек."""
        try:
            with connect(
                host="localhost",
                user="root",
                password="admin",
                database="Warehouse"
            ) as connection:
                cursor = connection.cursor()
                cursor.callproc("GetFreeCells")

                self.table_widget.setColumnCount(3)
                self.table_widget.setHorizontalHeaderLabels(["ID Стеллажа", "Номер Стеллажа", "Свободные Ячейки"])
                self.table_widget.setRowCount(0)

                for result in cursor.stored_results():
                    for i, row in enumerate(result.fetchall()):
                        self.table_widget.insertRow(i)
                        for j, value in enumerate(row):
                            self.table_widget.setItem(i, j, QTableWidgetItem(str(value)))

        except Error as e:
            print(f"Ошибка: {e}")

    def show_usage_chart(self):
        """Показать диаграмму заполнения стеллажей."""
        try:
            with connect(
                    host="localhost",
                    user="root",
                    password="admin",
                    database="Warehouse"
            ) as connection:
                cursor = connection.cursor()
                cursor.callproc("GetRackUsage")

                chart = QChart()
                chart.setTitle("Заполнение стеллажей (в процентах)")

                series = QBarSeries()

                for result in cursor.stored_results():
                    for row in result.fetchall():
                        rack_number = f"Стеллаж {row[1]}"
                        usage_percent = row[4]

                        bar_set = QBarSet(rack_number)
                        bar_set << usage_percent
                        series.append(bar_set)

                chart.addSeries(series)

                axis_x = QValueAxis()
                axis_x.setTitleText("Стеллажи")
                chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)

                axis_y = QValueAxis()
                axis_y.setTitleText("Процент заполнения")
                axis_y.setRange(0, 100)
                chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)

                chart_view = QChartView(chart)
                chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

                self.layout.addWidget(chart_view)

        except Error as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WarehouseApp()
    window.show()
    sys.exit(app.exec())
