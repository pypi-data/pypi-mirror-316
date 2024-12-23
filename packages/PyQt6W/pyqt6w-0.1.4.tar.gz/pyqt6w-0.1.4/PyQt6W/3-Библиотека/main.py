"""DROP DATABASE IF EXISTS LibraryDB;
CREATE DATABASE IF NOT EXISTS LibraryDB;
USE LibraryDB;

-- Таблица Книги
CREATE TABLE Books (
    BookID INT AUTO_INCREMENT PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Author VARCHAR(255) NOT NULL,
    Genre VARCHAR(100) NOT NULL,
    YearPublished INT NOT NULL
);

-- Таблица Читатели
CREATE TABLE Readers (
    ReaderID INT AUTO_INCREMENT PRIMARY KEY,
    LastName VARCHAR(100) NOT NULL,
    FirstName VARCHAR(100) NOT NULL,
    MiddleName VARCHAR(100),
    TicketNumber VARCHAR(20) NOT NULL UNIQUE
);

-- Таблица Выдача
CREATE TABLE BookIssues (
    IssueID INT AUTO_INCREMENT PRIMARY KEY,
    ReaderID INT NOT NULL,
    BookID INT NOT NULL,
    IssueDate DATE NOT NULL,
    FOREIGN KEY (ReaderID) REFERENCES Readers(ReaderID),
    FOREIGN KEY (BookID) REFERENCES Books(BookID)
);


-- Вставка данных в таблицу Books
INSERT INTO Books (Title, Author, Genre, YearPublished) VALUES
('Мастер и Маргарита', 'Михаил Булгаков', 'Роман', 1967),
('Война и мир', 'Лев Толстой', 'Роман', 1869),
('Преступление и наказание', 'Фёдор Достоевский', 'Роман', 1866),
('Евгений Онегин', 'Александр Пушкин', 'Поэма', 1833),
('Отцы и дети', 'Иван Тургенев', 'Роман', 1862);
-- Вставка данных в таблицу Readers
INSERT INTO Readers (LastName, FirstName, MiddleName, TicketNumber) VALUES
('Иванов', 'Иван', 'Иванович', 'TICKET001'),
('Петров', 'Петр', 'Петрович', 'TICKET002'),
('Сидоров', 'Алексей', 'Сергеевич', 'TICKET003'),
('Кузнецова', 'Мария', 'Игоревна', 'TICKET004');

-- Вставка данных в таблицу BookIssues
INSERT INTO BookIssues (ReaderID, BookID, IssueDate) VALUES
(1Автовокзал, 1Автовокзал, '2024-12-01'),
(1Автовокзал, 2, '2024-12-02'),
(2, 3, '2024-12-01'),
(3, 1Автовокзал, '2024-12-03'),
(4, 2, '2024-12-03'),
(1Автовокзал, 3, '2024-12-05'),
(2, 4, '2024-12-06'),
(3, 5, '2024-12-07'),
(4, 5, '2024-12-08');


DELIMITER //

CREATE PROCEDURE GetMostReadAuthor()
BEGIN
    SELECT
        b.Author AS MostReadAuthor,
        COUNT(bi.BookID) AS IssueCount
    FROM Books b
    JOIN BookIssues bi ON b.BookID = bi.BookID
    GROUP BY b.Author
    ORDER BY IssueCount DESC
    LIMIT 1Автовокзал;
END //

DELIMITER ;

DELIMITER //

CREATE PROCEDURE GetBooksByDates()
BEGIN
    SELECT
        bi.IssueDate AS Date,
        COUNT(bi.BookID) AS BookCount
    FROM BookIssues bi
    GROUP BY bi.IssueDate
    ORDER BY bi.IssueDate;
END //

DELIMITER ;"""









import sys
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QDialog,
    QHBoxLayout,
)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import db


class LibraryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Библиотека")
        self.setGeometry(100, 100, 900, 700)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # Стилизация
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QPushButton {
                background-color: #0078d7;
                color: white;
                border-radius: 8px;
                padding: 10px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #005a9e;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QTableWidget {
                background-color: white;
                border: 1px solid #ccc;
                border-radius: 8px;
                font-size: 14px;
            }
        """)

        # Кнопка для отображения наиболее читаемого автора
        self.most_read_author_button = QPushButton("Наиболее читаемый автор")
        self.most_read_author_button.clicked.connect(self.open_most_read_author_window)
        layout.addWidget(self.most_read_author_button)

        # Кнопка для отображения выдачи книг
        self.books_by_date_button = QPushButton("Выдача книг по датам")
        self.books_by_date_button.clicked.connect(self.open_books_by_date_window)
        layout.addWidget(self.books_by_date_button)

         # Таблица для всех книг
        self.books_table_label = QLabel("Список всех книг")
        self.books_table_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        self.books_table_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.books_table_label)

        self.books_table = QTableWidget()
        layout.addWidget(self.books_table)

        # Подключение к базе данных
        self.db_connection = db.connect_to_database()

        if not self.db_connection:
            error_label = QLabel("Не удалось подключиться к базе данных.")
            layout.addWidget(error_label)
        else:
            self.load_books_table()

    def load_books_table(self):
        """Загрузка всех книг в таблицу."""
        cursor = self.db_connection.cursor()
        query = "SELECT Title, Author, Genre, YearPublished FROM Books;"
        cursor.execute(query)
        books = cursor.fetchall()

        self.books_table.setRowCount(len(books))
        self.books_table.setColumnCount(4)
        self.books_table.setHorizontalHeaderLabels(["Название", "Автор", "Жанр", "Год издания"])

        self.header = self.books_table.horizontalHeader()
        self.header.setSectionResizeMode(0, self.header.ResizeMode.Stretch)
        self.header.setSectionResizeMode(1, self.header.ResizeMode.Stretch)
        self.header.setSectionResizeMode(2, self.header.ResizeMode.Stretch)
        self.header.setSectionResizeMode(3, self.header.ResizeMode.Stretch)

        for row_idx, book in enumerate(books):
            for col_idx, value in enumerate(book):
                self.books_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))
        
        self.books_table.resizeColumnsToContents()
        self.books_table.setSortingEnabled(True)
        cursor.close()

    def open_most_read_author_window(self):
        if not self.db_connection:
            self.info_label.setText("Нет подключения к базе данных")
            return

        window = MostReadAuthorWindow(self.db_connection)
        window.exec()

    def open_books_by_date_window(self):
        if not self.db_connection:
            self.info_label.setText("Нет подключения к базе данных")
            return

        window = BooksByDateWindow(self.db_connection)
        window.exec()


class MostReadAuthorWindow(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Наиболее читаемый автор")
        self.setGeometry(100, 100, 800, 400)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.result_table = QTableWidget()
        layout.addWidget(self.result_table)

        cursor = db_connection.cursor()
        cursor.callproc("GetMostReadAuthor")
        results = None

        for res in cursor.stored_results():
            results = res.fetchall()

        if results:
            self.result_table.setColumnCount(2)
            self.result_table.setRowCount(len(results))
            self.result_table.setHorizontalHeaderLabels(["Автор", "Количество выдач"])
            self.header = self.result_table.horizontalHeader()
            self.header.setSectionResizeMode(0, self.header.ResizeMode.Stretch)
            self.header.setSectionResizeMode(1, self.header.ResizeMode.ResizeToContents)

            for row_idx, row in enumerate(results):
                for col_idx, value in enumerate(row):
                    self.result_table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))

            self.result_table.setSortingEnabled(True)
        else:
            no_data_label = QLabel("Нет данных об авторах")
            layout.addWidget(no_data_label)

        cursor.close()


class BooksByDateWindow(QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.setWindowTitle("Выдача книг по датам")
        self.setGeometry(100, 100, 900, 500)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        layout.addWidget(self.canvas)

        cursor = db_connection.cursor()
        cursor.callproc("GetBooksByDates")
        results = None

        for res in cursor.stored_results():
            results = res.fetchall()

        if results:
            dates = [row[0] for row in results]
            counts = [row[1] for row in results]

            self.figure.clear()
            ax = self.figure.add_subplot(111)
            ax.plot(dates, counts, marker="o", color="#0078d7")
            ax.set_title("Выдача книг по датам")
            ax.set_xlabel("Дата")
            ax.set_ylabel("Количество выдач")
            self.canvas.draw()

        cursor.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LibraryApp()
    window.show()
    sys.exit(app.exec())
