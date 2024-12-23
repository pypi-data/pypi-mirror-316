# 18.	Туристский клуб
# Туристский клуб организует одно – и многодневные пешеходные туры в группах с руководителем по разным маршрутам и разной категории сложности.
# Таблицы: Маршруты (Код маршрута, название, продолжительность, категория сложности),Руководители (Код руководителя, ФИО, телефон), Группы (Код группы, название группы, код маршрута, код руководителя, количество туристов, дата отправления).
# Требуется:
# - определить перечень групп на маршруте;
# - построить сравнительную диаграмму количества туристов по уровню сложности маршрутов.


# CREATE DATABASE TouristClub;
#
# USE TouristClub;
#
# CREATE TABLE Routes (
#     RouteID INT AUTO_INCREMENT PRIMARY KEY,
# Name VARCHAR(100),
# Duration INT,
# DifficultyLevel VARCHAR(50)
# );
#
# CREATE TABLE Leaders (
#     LeaderID INT AUTO_INCREMENT PRIMARY KEY,
# FullName VARCHAR(100),
# Phone VARCHAR(20)
# );
#
# CREATE TABLE `groups` (
#     GroupID INT AUTO_INCREMENT PRIMARY KEY,
# GroupName VARCHAR(100),
# RouteID INT,
# LeaderID INT,
# TouristCount INT,
# DepartureDate DATE,
# FOREIGN KEY (RouteID) REFERENCES Routes(RouteID),
# FOREIGN KEY (LeaderID) REFERENCES Leaders(LeaderID)
# );
#
# INSERT INTO Routes (RouteID, Name, Duration, DifficultyLevel)
# VALUES
# (1, 'Mountain Adventure', 7, 'Hard'),
# (2, 'River Walk', 3, 'Medium'),
# (3, 'Forest Trail', 2, 'Easy'),
# (4, 'Desert Expedition', 5, 'Hard'),
# (5, 'Coastal Journey', 4, 'Medium');
#
# INSERT INTO Leaders (LeaderID, FullName, Phone)
# VALUES
# (1, 'John Smith', '123-456-7890'),
# (2, 'Emily Johnson', '987-654-3210'),
# (3, 'Michael Brown', '555-123-4567'),
# (4, 'Sarah Davis', '444-987-6543'),
# (5, 'David Wilson', '333-555-7890');
#
#
# INSERT INTO Groups (GroupID, GroupName, RouteID, LeaderID, TouristCount, DepartureDate)
# VALUES
# (1, 'Adventure Enthusiasts', 1, 1, 15, '2024-12-25'),
# (2, 'Nature Explorers', 3, 2, 12, '2024-12-27'),
# (3, 'Desert Travelers', 4, 3, 10, '2024-12-30'),
# (4, 'Coastal Adventurers', 5, 4, 8, '2024-12-29'),
# (5, 'River Wanderers', 2, 5, 20, '2024-12-28');




import sys
import pymysql
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem, QPushButton
)
from PyQt6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QBarCategoryAxis, QValueAxis
from PyQt6.QtGui import QPainter
from PyQt6.QtCore import Qt


class TouristClubApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tourist Club")
        self.setGeometry(100, 100, 800, 600)

        # Подключение к базе данных MySQL
        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="admin",
            database="TouristClub"
        )

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # Таблица для отображения данных
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # Кнопка загрузки списка групп
        self.load_groups_button = QPushButton("Show Groups by Route")
        self.load_groups_button.clicked.connect(self.load_groups)
        layout.addWidget(self.load_groups_button)

        # Кнопка для отображения диаграммы
        self.chart_button = QPushButton("Show Tourists Chart")
        self.chart_button.clicked.connect(self.show_chart)
        layout.addWidget(self.chart_button)

        # Контейнер для компоновки
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def load_groups(self):
        """Загрузка списка групп из базы данных"""
        cursor = self.connection.cursor()
        query = """
            SELECT g.GroupName, Routes.Name, Leaders.FullName, g.TouristCount, g.DepartureDate
            FROM `groups` g 
            JOIN Routes ON g.RouteID = Routes.RouteID
            JOIN Leaders ON g.LeaderID = Leaders.LeaderID;
        """
        cursor.execute(query)
        rows = cursor.fetchall()

        self.table.setRowCount(len(rows))
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Group", "Route", "Leader", "Tourists", "Departure Date"])

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

    def show_chart(self):
        cursor = self.connection.cursor()
        query = """
            SELECT Routes.DifficultyLevel, SUM(g.TouristCount)
            FROM `groups` g
            JOIN Routes ON g.RouteID = Routes.RouteID
            GROUP BY Routes.DifficultyLevel;
        """

        cursor.execute(query)
        data = cursor.fetchall()

        if not data:  # Проверка на пустой результат
            print("No data available to display the chart.")
            return

        # Создание диаграммы
        chart = QChart()
        series = QBarSeries()

        categories = []
        for row in data:
            difficulty, tourists = row
            bar_set = QBarSet(difficulty)
            bar_set << tourists
            series.append(bar_set)
            categories.append(difficulty)

        chart.addSeries(series)
        chart.setTitle("Tourists by Route Difficulty Level")
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # Настройка оси X
        axisX = QBarCategoryAxis()
        axisX.append(categories)
        chart.addAxis(axisX, Qt.AlignmentFlag.AlignBottom)
        series.attachAxis(axisX)

        # Настройка оси Y
        axisY = QValueAxis()
        axisY.setRange(0, max(row[1] for row in data) + 10)
        chart.addAxis(axisY, Qt.AlignmentFlag.AlignLeft)
        series.attachAxis(axisY)

        # Виджет для отображения диаграммы
        chart_view = QChartView(chart)
        chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Окно с диаграммой
        chart_window = QMainWindow(self)
        chart_window.setWindowTitle("Tourists Chart")
        chart_window.setCentralWidget(chart_view)
        chart_window.resize(600, 400)
        chart_window.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TouristClubApp()
    window.show()
    sys.exit(app.exec())
