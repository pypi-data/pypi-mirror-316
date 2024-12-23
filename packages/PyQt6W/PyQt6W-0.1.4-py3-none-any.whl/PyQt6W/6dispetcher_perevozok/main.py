"""CREATE DATABASE IF NOT EXISTS AutoDispatcher;

USE AutoDispatcher;

-- Points Table (Punkty)
CREATE TABLE Points (
                        PointID INT AUTO_INCREMENT PRIMARY KEY,
                        PointName VARCHAR(255)
);

-- Cargo Table (Gruzy)
CREATE TABLE Cargo (
                       CargoID INT AUTO_INCREMENT PRIMARY KEY,
                       CargoName VARCHAR(255),
                       Weight DECIMAL(10, 2)
);

-- Cars Table (Avtomobili)
CREATE TABLE Cars (
                      CarID INT AUTO_INCREMENT PRIMARY KEY,
                      CarMake VARCHAR(255),
                      LicensePlate VARCHAR(20),
                      Capacity DECIMAL(10, 2) -- Cargo capacity
);

-- Drivers Table (Voditeli)
CREATE TABLE Drivers (
                         DriverID INT AUTO_INCREMENT PRIMARY KEY,
                         FullName VARCHAR(255),
                         PhoneNumber VARCHAR(20)
);

-- Routes Table (Reisy)
CREATE TABLE Routes (
                        RouteID INT AUTO_INCREMENT PRIMARY KEY,
                        DriverID INT,
                        CarID INT,
                        PointID INT,
                        CargoID INT,
                        DepartureTime DATETIME,
                        TravelTime DECIMAL(10, 2), -- Travel time in hours
                        FOREIGN KEY (DriverID) REFERENCES Drivers(DriverID),
                        FOREIGN KEY (CarID) REFERENCES Cars(CarID),
                        FOREIGN KEY (PointID) REFERENCES Points(PointID),
                        FOREIGN KEY (CargoID) REFERENCES Cargo(CargoID)
);

DELIMITER //

CREATE PROCEDURE GetDriversInRoute(IN currentTime DATETIME)
BEGIN
SELECT
    d.FullName,
    r.DepartureTime,
    ADDTIME(r.DepartureTime, SEC_TO_TIME(r.TravelTime * 3600)) AS ArrivalTime
FROM Routes r
         JOIN Drivers d ON r.DriverID = d.DriverID
WHERE r.DepartureTime <= currentTime
  AND ADDTIME(r.DepartureTime, SEC_TO_TIME(r.TravelTime * 3600)) >= currentTime;
END //

DELIMITER ;


DELIMITER //

CREATE PROCEDURE GetAverageCarLoad()
BEGIN
SELECT
    c.CarMake,
    AVG(g.Weight) AS AverageLoad
FROM Routes r
         JOIN Cars c ON r.CarID = c.CarID
         JOIN Cargo g ON r.CargoID = g.CargoID
GROUP BY c.CarID;
END //

DELIMITER ;


-- Points (Punkty)
INSERT INTO Points (PointName) VALUES
                                   ('Moscow'),
                                   ('Saint Petersburg'),
                                   ('Kazan');

-- Cargo (Gruzy)
INSERT INTO Cargo (CargoName, Weight) VALUES
                                          ('Electronics', 500.00),
                                          ('Furniture', 1000.00),
                                          ('Clothing', 200.00);

-- Cars (Avtomobili)
INSERT INTO Cars (CarMake, LicensePlate, Capacity) VALUES
                                                       ('Volvo', 'A123BC', 1500.00),
                                                       ('Scania', 'B456DE', 2000.00),
                                                       ('Mercedes', 'C789FG', 1800.00);

-- Drivers (Voditeli)
INSERT INTO Drivers (FullName, PhoneNumber) VALUES
                                                ('John Doe', '123-456-7890'),
                                                ('Jane Smith', '987-654-3210'),
                                                ('Alex Johnson', '456-789-0123');

-- Routes (Reisy)
INSERT INTO Routes (DriverID, CarID, PointID, CargoID, DepartureTime, TravelTime) VALUES
                                                                                      (1Автовокзал, 1Автовокзал, 1Автовокзал, 1Автовокзал, '2024-12-01 08:00:00', 5.00),
                                                                                      (2, 2, 2, 2, '2024-12-01 09:00:00', 6.00),
                                                                                      (3, 3, 3, 3, '2024-12-01 10:00:00', 4.00);



"""




import sys
import pymysql
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QPushButton, QWidget, QMessageBox
)

class AutoDispatcherApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Dispatcher")
        self.resize(800, 600)

        self.connection = pymysql.connect(
            host="localhost",
            user="root",
            password="admin",
            database="AutoDispatcher"
        )

        layout = QVBoxLayout()

        self.drivers_button = QPushButton("Show Drivers in Route")
        self.drivers_button.clicked.connect(self.show_drivers_in_route)
        layout.addWidget(self.drivers_button)

        self.average_load_button = QPushButton("Show Average Car Load")
        self.average_load_button.clicked.connect(self.show_average_car_load)
        layout.addWidget(self.average_load_button)

        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def show_drivers_in_route(self):
        try:
            current_time = '2024-12-01 09:30:00'

            cursor = self.connection.cursor()
            cursor.callproc("GetDriversInRoute", (current_time,))
            drivers_data = cursor.fetchall()

            if not drivers_data:
                QMessageBox.information(self, "Drivers in Route", "No drivers are in route at the current time.")
                return

            self.table_widget.setRowCount(len(drivers_data))
            self.table_widget.setColumnCount(3)
            self.table_widget.setHorizontalHeaderLabels(["Driver Name", "Departure Time", "Arrival Time"])

            for i, row in enumerate(drivers_data):
                self.table_widget.setItem(i, 0, QTableWidgetItem(row[0]))
                self.table_widget.setItem(i, 1, QTableWidgetItem(str(row[1])))
                self.table_widget.setItem(i, 2, QTableWidgetItem(str(row[2])))

        except pymysql.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")
        finally:
            cursor.close()

    def show_average_car_load(self):
        try:
            cursor = self.connection.cursor()
            cursor.callproc("GetAverageCarLoad")
            load_data = cursor.fetchall()

            if not load_data:
                QMessageBox.information(self, "Average Car Load", "No data available.")
                return

            self.table_widget.setRowCount(len(load_data))
            self.table_widget.setColumnCount(2)
            self.table_widget.setHorizontalHeaderLabels(["Car Make", "Average Load"])

            for i, row in enumerate(load_data):
                self.table_widget.setItem(i, 0, QTableWidgetItem(row[0]))
                self.table_widget.setItem(i, 1, QTableWidgetItem(str(row[1])))

        except pymysql.Error as e:
            QMessageBox.critical(self, "Error", f"Database error: {e}")
        finally:
            cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AutoDispatcherApp()
    window.show()
    sys.exit(app.exec())
