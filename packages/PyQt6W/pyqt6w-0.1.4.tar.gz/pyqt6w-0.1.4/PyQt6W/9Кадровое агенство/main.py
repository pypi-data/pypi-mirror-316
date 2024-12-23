"""DROP DATABASE IF EXISTS recruitment_agency;

CREATE DATABASE IF NOT EXISTS recruitment_agency;

USE recruitment_agency;

CREATE TABLE IF NOT EXISTS Positions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Professions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS EducationLevels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS ComputerSkills (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Vacancies (
    id INT AUTO_INCREMENT PRIMARY KEY,
    published_date DATE NOT NULL,
    title VARCHAR(255) NOT NULL,
    salary DECIMAL(10, 2) NOT NULL,
    is_active BOOLEAN NOT NULL,
    profession_id INT,
    education_id INT,
    computer_skill_id INT,
    FOREIGN KEY (profession_id) REFERENCES Professions(id),
    FOREIGN KEY (education_id) REFERENCES EducationLevels(id),
    FOREIGN KEY (computer_skill_id) REFERENCES ComputerSkills(id)
);

DELIMITER $$
CREATE PROCEDURE GetActiveVacancies()
BEGIN
    SELECT
        v.id, v.published_date, v.title, v.salary, v.is_active, p.name AS profession
    FROM Vacancies v
    JOIN Professions p ON v.profession_id = p.id
    WHERE v.is_active = TRUE;
END $$
DELIMITER ;

DELIMITER $$
CREATE PROCEDURE GetAverageSalariesByComputerSkill()
BEGIN
    SELECT
        cs.name AS skill_level, AVG(v.salary) AS average_salary
    FROM Vacancies v
    JOIN ComputerSkills cs ON v.computer_skill_id = cs.id
    GROUP BY cs.name;
END $$
DELIMITER ;

-- Данные для наполнения
INSERT INTO Professions (name) VALUES ('Программист'), ('Менеджер'), ('Аналитик');
INSERT INTO EducationLevels (name) VALUES ('Среднее'), ('Высшее');
INSERT INTO ComputerSkills (name) VALUES ('Начальный'), ('Средний'), ('Продвинутый');
INSERT INTO Vacancies (published_date, title, salary, is_active, profession_id, education_id, computer_skill_id)
VALUES
('2024-01-10', 'Вакансия 1Автовокзал', 60000, TRUE, 1Автовокзал, 2, 3),
('2024-01-12', 'Вакансия 2', 40000, FALSE, 2, 1Автовокзал, 2),
('2024-01-15', 'Вакансия 3', 70000, TRUE, 3, 2, 1Автовокзал),
('2024-01-18', 'Вакансия 4', 50000, FALSE, 1Автовокзал, 1Автовокзал, 3),
('2024-01-20', 'Вакансия 5', 80000, TRUE, 2, 2, 2),
('2024-01-23', 'Вакансия 6', 60000, FALSE, 3, 1Автовокзал, 1Автовокзал),
('2024-01-25', 'Вакансия 7', 70000, TRUE, 1Автовокзал, 2, 2),
('2024-01-28', 'Вакансия 8', 50000, FALSE, 2, 1Автовокзал, 3),
('2024-01-30', 'Вакансия 9', 80000, TRUE, 3, 2, 1Автовокзал),
('2024-02-01', 'Вакансия 10', 60000, FALSE, 1Автовокзал, 1Автовокзал, 2),
('2024-02-04', 'Вакансия 11', 70000, TRUE, 2, 2, 3),
('2024-02-06', 'Вакансия 12', 50000, FALSE, 3, 1Автовокзал, 1Автовокзал),
('2024-02-09', 'Вакансия 13', 80000, TRUE, 1Автовокзал, 2, 2),
('2024-02-11', 'Вакансия 14', 60000, FALSE, 2, 1Автовокзал, 3);

"""




import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QWidget, QDialog
)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import db

class SalaryChartWindow(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Диаграмма среднего оклада")
        self.setGeometry(300, 50, 800, 800)
        self.setStyleSheet("""
            
        """)
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        self.db_connection = db_connection
        self.show_salary_chart()

    def show_salary_chart(self):
        if not self.db_connection:
            return

        cursor = self.db_connection.cursor()
        cursor.callproc("GetAverageSalariesByComputerSkill")
        results = None
        
        for res in cursor.stored_results():
            results = res.fetchall()

        if not results:
            self.show_error("Нет данных")
            return
        
        levels = [row[0] for row in results]
        salaries = [row[1] for row in results]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(levels, salaries, color='skyblue')
        ax.set_title("Средний оклад в зависимости от уровня владения компьютером", fontsize=14, weight='bold')
        ax.set_xlabel("Уровень владения компьютером", fontsize=12)
        ax.set_ylabel("Средний оклад", fontsize=12)
        self.canvas.draw()

        cursor.close()


class RecruitmentAgencyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Кадровое агентство")
        self.setGeometry(100, 100, 900, 700)

        # Центральный виджет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Основной макет
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
      
        self.salary_chart_button = QPushButton("Диаграмма среднего оклада")
        self.salary_chart_button.setFont(QFont("Calibri", 12))
        self.salary_chart_button.setStyleSheet("""
            QPushButton {
                background-color: #008CBA;
                color: white;
                border: none;
                padding: 10px 20px;
                font-size: 14px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #007bb5;
            }
        """)
        self.salary_chart_button.clicked.connect(self.show_salary_chart_window)
        layout.addWidget(self.salary_chart_button)

        # Таблица для отображения данных
        self.result_table = QTableWidget()
        self.result_table.setFont(QFont("Calibri", 10))
        self.result_table.setStyleSheet("""
           
        """)
        layout.addWidget(self.result_table)

        # Подключение к базе данных
        self.db_connection = db.connect_to_database()
        if not self.db_connection:
            self.show_error("Нет подключения к базе данных")
        else:
            self.show_active_vacancies() 

    def show_error(self, message):
        error_label = QLabel(message)
        error_label.setFont(QFont("Calibri", 12))
        error_label.setStyleSheet("color: red;")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout().addWidget(error_label)

    def show_active_vacancies(self):
        if not self.db_connection:
            return

        self.result_table.clearContents()
        self.result_table.setRowCount(0)
        
        cursor = self.db_connection.cursor()
        cursor.callproc("GetActiveVacancies")

        results = None
        
        for res in cursor.stored_results():
            results = res.fetchall()

        if not results:
            self.show_error("Нет активных вакансий")
            return
        
        
        self.result_table.setRowCount(len(results))
        self.result_table.setColumnCount(6)
        self.result_table.setHorizontalHeaderLabels([
            "Код", "Дата", "Название", "Оклад", "Актуальность", "Профессия"
        ])

        self.header = self.result_table.horizontalHeader()
        self.header.setSectionResizeMode(0, self.header.ResizeMode.ResizeToContents)
        self.header.setSectionResizeMode(1, self.header.ResizeMode.ResizeToContents)
        self.header.setSectionResizeMode(2, self.header.ResizeMode.Stretch)
        self.header.setSectionResizeMode(3, self.header.ResizeMode.Stretch)
        self.header.setSectionResizeMode(4, self.header.ResizeMode.ResizeToContents)
        self.header.setSectionResizeMode(5, self.header.ResizeMode.Stretch)

        for row_idx, row_data in enumerate(results):
            for col_idx, value in enumerate(row_data):
                self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        cursor.close()
    def show_salary_chart_window(self):
        if not self.db_connection:
            return
        self.salary_window = SalaryChartWindow(self.db_connection)
        self.salary_window.exec()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RecruitmentAgencyApp()
    window.show()
    sys.exit(app.exec())
