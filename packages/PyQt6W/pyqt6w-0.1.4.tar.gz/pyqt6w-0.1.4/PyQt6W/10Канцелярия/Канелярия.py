"""CREATE DATABASE enterprise_documents;
USE enterprise_documents;

-- Создание таблицы "Виды документов"
CREATE TABLE document_types (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создание таблицы "Отделы"
CREATE TABLE departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Создание таблицы "Документы"
CREATE TABLE documents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    number VARCHAR(255) NOT NULL,
    document_type_id INT,
    sender_department_id INT,
    recipient_department_id INT,
    registration_date DATE,
    FOREIGN KEY (document_type_id) REFERENCES document_types(id),
    FOREIGN KEY (sender_department_id) REFERENCES departments(id),
    FOREIGN KEY (recipient_department_id) REFERENCES departments(id)
);

-- Пример хранимой процедуры для получения служебных записок планового отдела
DELIMITER //
CREATE PROCEDURE get_planning_department_notes()
BEGIN
    SELECT d.name, d.number, d.registration_date
    FROM documents d
    JOIN departments dep ON dep.id = d.sender_department_id
    JOIN document_types dt ON dt.id = d.document_type_id
    WHERE dep.name = 'Плановый отдел' AND dt.name = 'Служебная записка';
END //
DELIMITER ;

-- Пример хранимой процедуры для получения сравнительной диаграммы количества документов по видам
DELIMITER //
CREATE PROCEDURE get_document_counts_by_type()
BEGIN
    SELECT dt.name AS document_type, COUNT(d.id) AS document_count
    FROM documents d
    JOIN document_types dt ON dt.id = d.document_type_id
    GROUP BY dt.name;
END //
DELIMITER ;


-- Вставка данных в таблицу "Виды документов"
INSERT INTO document_types (name) VALUES
('Служебная записка'),
('Приказ'),
('Отчёт');

-- Вставка данных в таблицу "Отделы"
INSERT INTO departments (name) VALUES
('Плановый отдел'),
('Отдел кадров'),
('Юридический отдел'),
('Финансовый отдел');

-- Вставка данных в таблицу "Документы"
INSERT INTO documents (name, number, document_type_id, sender_department_id, recipient_department_id, registration_date) VALUES
('Служебная записка 1Автовокзал', '001', 1Автовокзал, 1Автовокзал, 2, '2024-12-01'),
('Приказ 1Автовокзал', '002', 2, 3, 1Автовокзал, '2024-12-05'),
('Отчёт 1Автовокзал', '003', 3, 4, 3, '2024-12-10'),
('Служебная записка 2', '004', 1Автовокзал, 1Автовокзал, 4, '2024-12-12'),
('Приказ 2', '005', 2, 2, 4, '2024-12-15');

"""


import sys
import mysql.connector
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QTableWidget, QTableWidgetItem
from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis
from PyQt6.QtCore import Qt

# Подключение к базе данных MySQL
def create_connection():
    connection = mysql.connector.connect(
        host='localhost',  # Замените на ваш хост
        user='root',  # Замените на ваше имя пользователя
        password='admin',  # Замените на ваш пароль
        database='enterprise_documents'
    )
    return connection

# Получение служебных записок планового отдела
def get_planning_department_notes():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.callproc('get_planning_department_notes')  # Вызов хранимой процедуры
    result = []
    for res in cursor.stored_results():
        result = res.fetchall()
    conn.close()
    return result

# Получение данных для диаграммы
def get_document_counts_by_type():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.callproc('get_document_counts_by_type')  # Вызов хранимой процедуры
    result = []
    for res in cursor.stored_results():
        result = res.fetchall()
    conn.close()
    return result

# Класс для главного окна
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Канцелярия')
        self.setGeometry(100, 100, 800, 600)

        # Основной виджет
        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        # Макет для размещения элементов
        self.layout = QVBoxLayout(self.central_widget)

        # Кнопка для поиска служебных записок
        self.notes_button = QPushButton('Показать служебные записки планового отдела', self)
        self.notes_button.clicked.connect(self.show_notes)
        self.layout.addWidget(self.notes_button)

        # Таблица для отображения служебных записок
        self.notes_table = QTableWidget(self)
        self.layout.addWidget(self.notes_table)

        # Кнопка для построения диаграммы
        self.chart_button = QPushButton('Построить диаграмму количества документов по видам', self)
        self.chart_button.clicked.connect(self.show_chart)
        self.layout.addWidget(self.chart_button)

        # Виджет для отображения диаграммы
        self.chart_view = QChartView(self)
        self.layout.addWidget(self.chart_view)

    def show_notes(self):
        notes = get_planning_department_notes()
        self.notes_table.setRowCount(len(notes))
        self.notes_table.setColumnCount(3)
        self.notes_table.setHorizontalHeaderLabels(['Название', 'Номер', 'Дата регистрации'])

        for row, note in enumerate(notes):
            for col, data in enumerate(note):
                self.notes_table.setItem(row, col, QTableWidgetItem(str(data)))

    from PyQt6.QtCharts import QChart, QChartView, QBarSet, QBarSeries, QBarCategoryAxis
    from PyQt6.QtCore import Qt

    # Метод для построения диаграммы
    def show_chart(self):
        data = get_document_counts_by_type()
        categories = [item[0] for item in data]
        counts = [item[1] for item in data]

        # Создание набора данных для диаграммы
        bar_set = QBarSet('Количество документов')
        bar_set.append(counts)

        # Создание серии и диаграммы
        series = QBarSeries()
        series.append(bar_set)

        chart = QChart()
        chart.addSeries(series)
        chart.setTitle('Количество документов по видам')
        chart.setAnimationOptions(QChart.AnimationOption.SeriesAnimations)

        # Создание оси X (категориальная ось)
        axis = QBarCategoryAxis()
        axis.append(categories)

        # Создание оси Y (по умолчанию будет автоматически)
        chart.addAxis(axis, Qt.AlignmentFlag.AlignBottom)

        # Добавляем ось к серии
        series.attachAxis(axis)

        # Отображение диаграммы
        self.chart_view.setChart(chart)


# Запуск приложения
def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
