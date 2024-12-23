# 17.	Справочник филателиста.
# В базе данных содержатся сведения о личной коллекции марок.
# Таблицы базы данных: Жанры (код жанра, название), Страны (код страны, название), марки(код марки, код страны, код жанра, год выпуска, цена, номер альбома).
# Требуется:
# - найти самую дорогую марку;
# - построить сравнительную диаграмму количества марок по годам выпуска.


#!!!!!!!!!!!!!!!!!!  SQL в файле db


import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QPushButton, QLabel, QTableWidget, QTableWidgetItem, QWidget, QDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import db
import utils
import mysql.connector

class PhilatelyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Справочник филателиста")
        self.setGeometry(100, 100, 800, 600)
        utils.center_window(self)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.most_expensive_button = QPushButton("Найти самую дорогую марку")
        self.most_expensive_button.clicked.connect(self.find_most_expensive_stamp)
        layout.addWidget(self.most_expensive_button)

        self.diagram_button = QPushButton("Построить диаграмму")
        self.diagram_button.clicked.connect(self.show_diagram)
        layout.addWidget(self.diagram_button)

        self.all_stamps_button = QPushButton("Показать все марки")
        self.all_stamps_button.clicked.connect(self.show_all_stamps)
        layout.addWidget(self.all_stamps_button)

        self.info_label = QLabel("Выберите действие")
        layout.addWidget(self.info_label)

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        self.db_connection = db.connect_to_database()

        if not self.db_connection:
            self.info_label.setText("Нет подключения к базе данных")

    def show_all_stamps(self):
        if not self.db_connection:
            self.info_label.setText("Нет подключения к базе данных")
            return

        dialog = QDialog(self)
        dialog.setWindowTitle("Все марки")
        dialog.resize(600, 400)

        layout = QVBoxLayout(dialog)

        table = QTableWidget()
        layout.addWidget(table)

        cursor = self.db_connection.cursor()
        query = """
            SELECT s.id, c.name AS country, g.name AS genre, s.release_year, s.price, s.album_number
            FROM stamps s
            JOIN countries c ON s.country_id = c.id
            JOIN genres g ON s.genre_id = g.id;
        """
        cursor.execute(query)
        results = cursor.fetchall()

        table.setColumnCount(6)
        table.setRowCount(len(results))
        table.setHorizontalHeaderLabels(["ID", "Страна", "Жанр", "Год выпуска", "Цена", "Альбом"])

        for row_idx, row in enumerate(results):
            for col_idx, value in enumerate(row):
                table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

        cursor.close()
        dialog.exec()
    def find_most_expensive_stamp(self):
        if not self.db_connection:
            self.info_label.setText("Нет подключения к базе данных")
            return

        cursor = self.db_connection.cursor()
        cursor.callproc("GetMostExpensiveStamp")
        result = None

        for res in cursor.stored_results():
            result = res.fetchone()

        if result:
            self.result_table.setColumnCount(6)
            self.result_table.setRowCount(1)
            self.result_table.setHorizontalHeaderLabels(["ID", "Цена", "Страна", "Жанр", "Год выпуска", "Альбом"])
            for i, value in enumerate(result):
                self.result_table.setItem(0, i, QTableWidgetItem(str(value)))
        else:
            self.info_label.setText("Марки не найдены")
        cursor.close()

    def show_diagram(self):
        if not self.db_connection:
            self.info_label.setText("Нет подключения к базе данных")
            return

        cursor = self.db_connection.cursor()
        query = "SELECT release_year, COUNT(*) AS count FROM stamps GROUP BY release_year ORDER BY release_year;"
        cursor.execute(query)
        results = cursor.fetchall()

        years = [row[0] for row in results]
        counts = [row[1] for row in results]

        self.figure.clear()
        ax = self.figure.add_subplot(111)
        ax.bar(years, counts)
        ax.set_title("Количество марок по годам выпуска")
        ax.set_xlabel("Год выпуска")
        ax.set_ylabel("Количество марок")
        self.canvas.draw()

        cursor.close()



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PhilatelyApp()
    window.show()
    sys.exit(app.exec())