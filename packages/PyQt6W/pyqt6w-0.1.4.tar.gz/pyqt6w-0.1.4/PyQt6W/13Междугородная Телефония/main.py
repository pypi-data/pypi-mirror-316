"""CREATE DATABASE PhoneStation;

USE PhoneStation;

CREATE TABLE Tariffs (
                         TariffID INT PRIMARY KEY,
                         MinDistance INT NOT NULL,
                         MaxDistance INT NOT NULL,
                         PricePerMinute DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Cities (
                        CityID INT PRIMARY KEY,
                        Distance INT NOT NULL,
                        TariffID INT NOT NULL,
                        FOREIGN KEY (TariffID) REFERENCES Tariffs(TariffID)
);

CREATE TABLE Calls (
                       CallID INT PRIMARY KEY,
                       CityID INT NOT NULL,
                       StartTime DATETIME NOT NULL,
                       DurationMinutes INT NOT NULL,
                       FOREIGN KEY (CityID) REFERENCES Cities(CityID)
);

DELIMITER //

CREATE PROCEDURE GetCallsSortedByStartTime()
BEGIN
SELECT
    Calls.CallID,
    Cities.CityID,
    Calls.StartTime,
    Calls.DurationMinutes
FROM Calls
         JOIN Cities ON Calls.CityID = Cities.CityID
ORDER BY Calls.StartTime ASC;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE GetCostDistributionByCity()
BEGIN
    SELECT Cities.CityID, SUM(Calls.DurationMinutes * Tariffs.PricePerMinute) AS TotalCost
    FROM Calls
    JOIN Cities
        ON Calls.CityID = Cities.CityID
    JOIN Tariffs
        ON Cities.TariffID = Tariffs.TariffID
    GROUP BY Cities.CityID;
END //

DELIMITER ;


INSERT INTO Tariffs (TariffID, MinDistance, MaxDistance, PricePerMinute)
VALUES
    (1Автовокзал, 0, 100, 0.50),
    (2, 101, 500, 1Автовокзал.00),
    (3, 501, 1000, 1Автовокзал.50);

INSERT INTO Cities (CityID, Distance, TariffID)
VALUES
    (1Автовокзал, 50, 1Автовокзал),
    (2, 300, 2),
    (3, 700, 3);

INSERT INTO Calls (CallID, CityID, StartTime, DurationMinutes)
VALUES
    (1Автовокзал, 1Автовокзал, '2024-12-25 10:00:00', 10),
    (2, 2, '2024-12-25 11:30:00', 20),
    (3, 3, '2024-12-25 12:00:00', 15),
    (4, 1Автовокзал, '2024-12-25 13:00:00', 25),
    (5, 2, '2024-12-25 14:30:00', 30);
"""


import sys

import pymysql
from PyQt6.QtCharts import QChart, QPieSeries, QChartView
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPainter
from PyQt6.QtWidgets import (
    QApplication, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QPushButton, QWidget, QMessageBox, QMainWindow
)


class PhoneStationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Intercity Phone Station")
        self.resize(800, 600)

        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="admin",
            database="PhoneStation"
        )

        layout = QVBoxLayout()
        self.call_table = QTableWidget()
        layout.addWidget(self.call_table)

        self.load_calls_button = QPushButton("Show Calls (Sorted by Start Time)")
        self.load_calls_button.clicked.connect(self.show_calls)
        layout.addWidget(self.load_calls_button)

        self.show_cost_distribution_button = QPushButton("Show Cost Distribution by City")
        self.show_cost_distribution_button.clicked.connect(self.show_cost_distribution)
        layout.addWidget(self.show_cost_distribution_button)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_calls(self):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("GetCallsSortedByStartTime")  # Вызов хранимой процедуры
            data = cursor.fetchall()

            if not data:
                QMessageBox.information(self, "Info", "No calls found.")
                return

            self.call_table.setRowCount(len(data))
            self.call_table.setColumnCount(4)
            self.call_table.setHorizontalHeaderLabels(["Call ID", "City ID", "Start Time", "Duration (Minutes)"])

            for row_idx, row_data in enumerate(data):
                for col_idx, value in enumerate(row_data):
                    self.call_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        except pymysql.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")
        finally:
            cursor.close()

    def show_cost_distribution(self):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("GetCostDistributionByCity")  # Вызов хранимой процедуры
            city_costs = cursor.fetchall()

            if not city_costs:
                QMessageBox.information(self, "Info", "No data found for cost distribution.")
                return

            total_cost = sum(row[1] for row in city_costs)
            if total_cost == 0:
                QMessageBox.information(self, "Info", "Total cost is zero, cannot calculate distribution.")
                return

            series = QPieSeries()
            for city_id, cost in city_costs:
                percentage = (cost / total_cost) * 100
                series.append(f"City {city_id} ({percentage:.2f}%)", cost)

            chart = QChart()
            chart.addSeries(series)
            chart.setTitle("Cost Distribution by City")
            chart.legend().setVisible(True)
            chart.legend().setAlignment(Qt.AlignmentFlag.AlignBottom)

            chart_view = QChartView(chart)
            chart_view.setRenderHint(QPainter.RenderHint.Antialiasing)

            chart_window = QMainWindow(self)
            chart_window.setWindowTitle("Cost Distribution Chart")
            chart_window.setCentralWidget(chart_view)
            chart_window.resize(600, 400)
            chart_window.show()

        except pymysql.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")
        finally:
            cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhoneStationApp()
    window.show()
    sys.exit(app.exec())
