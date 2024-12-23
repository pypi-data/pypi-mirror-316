# 19.	Управляющая компания жилищно-коммунального хозяйства.
# В базе данных содержатся сведения о проживающих гражданах, пользующихся услугами, видах услуг, тарифах, начисленных суммах.
# Таблицы: Улицы (Код улицы, название), Лицевые счета (Код счета, номер счета, Код улицы, дом, корпус, квартира, ФИО), Услуги (Код услуги, название, тариф), Начисления (Код начисления, код счета, код услуги, количество).
# Требуется:
# - отпечатать список лицевых счетов, упорядоченный по адресу:
# - отпечатать извещение на оплату по указанному счету.

# CREATE DATABASE housing_management;
#
# USE housing_management;
#
# CREATE TABLE Streets (
#     street_id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(255)
# );
#
# CREATE TABLE Accounts (
#     account_id INT AUTO_INCREMENT PRIMARY KEY,
# account_number VARCHAR(50),
# street_id INT,
# building VARCHAR(10),
# block VARCHAR(10),
# apartment VARCHAR(10),
# full_name VARCHAR(255),
# FOREIGN KEY (street_id) REFERENCES Streets(street_id)
# );
#
# CREATE TABLE Services (
#     service_id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(255),
# tariff DECIMAL(10, 2)
# );
#
# CREATE TABLE Charges (
#     charge_id INT AUTO_INCREMENT PRIMARY KEY,
# account_id INT,
# service_id INT,
# amount DECIMAL(10, 2),
# FOREIGN KEY (account_id) REFERENCES Accounts(account_id),
# FOREIGN KEY (service_id) REFERENCES Services(service_id)
# );
#
# -- Заполняем тестовыми данными
# INSERT INTO Streets (name) VALUES ('Main Street'), ('Elm Street');
# INSERT INTO Accounts (account_number, street_id, building, block, apartment, full_name) VALUES
# ('001', 1, '10', 'A', '101', 'Ivan Ivanov'),
# ('002', 1, '12', '', '202', 'Petr Petrov'),
# ('003', 2, '5', '', '303', 'Anna Sidorova');
# INSERT INTO Services (name, tariff) VALUES ('Electricity', 3.5), ('Water', 2.0), ('Gas', 1.5);
# INSERT INTO Charges (account_id, service_id, amount) VALUES (1, 1, 50), (1, 2, 30), (2, 1, 40), (3, 3, 25);



import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QPushButton,
    QLabel, QLineEdit, QMessageBox, QWidget
)
from PyQt6.QtCore import Qt
import mysql.connector


# Функция для подключения к базе данных MySQL
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",  # Замените на ваш пароль
            database="housing_management"
        )
        return connection
    except mysql.connector.Error as e:
        QMessageBox.critical(None, "Ошибка подключения", f"Ошибка при подключении к базе данных:\n{str(e)}")
        sys.exit(1)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управляющая компания ЖКХ")
        self.setGeometry(100, 100, 800, 600)

        # Подключение к базе данных
        self.connection = connect_to_db()

        # Инициализация интерфейса
        self.init_ui()

    def init_ui(self):
        try:
            layout = QVBoxLayout()

            # Таблица лицевых счетов
            self.accounts_table = QTableWidget()
            self.accounts_table.setColumnCount(6)
            self.accounts_table.setHorizontalHeaderLabels(["Номер счета", "Улица", "Дом", "Корпус", "Квартира", "ФИО"])
            layout.addWidget(self.accounts_table)

            # Кнопка загрузки данных
            self.load_button = QPushButton("Загрузить список лицевых счетов")
            self.load_button.clicked.connect(self.load_accounts)
            layout.addWidget(self.load_button)

            # Поле для ввода номера счета
            self.account_label = QLabel("Введите номер счета:")
            layout.addWidget(self.account_label)

            self.account_input = QLineEdit()
            layout.addWidget(self.account_input)

            # Кнопка для получения извещения
            self.get_notice_button = QPushButton("Показать извещение на оплату")
            self.get_notice_button.clicked.connect(self.show_notice)
            layout.addWidget(self.get_notice_button)

            # Центральный виджет
            central_widget = QWidget()
            central_widget.setLayout(layout)
            self.setCentralWidget(central_widget)
        except Exception as e:
            QMessageBox.critical(self, "Ошибка интерфейса", f"Ошибка при создании интерфейса:\n{str(e)}")
            sys.exit(1)

    def load_accounts(self):
        """Загрузка данных из базы данных в таблицу"""
        try:
            cursor = self.connection.cursor()
            query = """
            SELECT a.account_number, s.name, a.building, a.block, a.apartment, a.full_name
            FROM Accounts a
            JOIN Streets s ON a.street_id = s.street_id
            ORDER BY s.name, a.building, a.block, a.apartment;
            """
            cursor.execute(query)
            results = cursor.fetchall()

            self.accounts_table.setRowCount(len(results))
            for row_idx, row_data in enumerate(results):
                for col_idx, col_data in enumerate(row_data):
                    self.accounts_table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

            cursor.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Ошибка при загрузке данных из базы:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Неизвестная ошибка", f"Произошла ошибка:\n{str(e)}")

    def show_notice(self):
        """Отображение извещения на оплату"""
        account_number = self.account_input.text()
        if not account_number:
            QMessageBox.warning(self, "Ошибка", "Введите номер счета.")
            return

        try:
            cursor = self.connection.cursor()
            query = """
            SELECT a.full_name, s.name AS street_name, a.building, a.block, a.apartment,
                   sv.name AS service_name, sv.tariff, c.amount
            FROM Accounts a
            JOIN Streets s ON a.street_id = s.street_id
            JOIN Charges c ON a.account_id = c.account_id
            JOIN Services sv ON c.service_id = sv.service_id
            WHERE a.account_number = %s;
            """
            cursor.execute(query, (account_number,))
            results = cursor.fetchall()

            if not results:
                QMessageBox.warning(self, "Ошибка", "Лицевой счет не найден.")
                return

            # Создаем текст извещения
            notice_text = f"Извещение на оплату для счета {account_number}\n\n"
            notice_text += f"ФИО: {results[0][0]}\n"
            notice_text += f"Адрес: {results[0][1]}, дом {results[0][2]}, корпус {results[0][3]}, квартира {results[0][4]}\n\n"
            notice_text += "Услуги:\n"
            total = 0
            for row in results:
                service_name, tariff, amount = row[5], row[6], row[7]
                cost = tariff * amount
                total += cost
                notice_text += f"- {service_name}: {amount} x {tariff} = {cost:.2f} руб.\n"
            notice_text += f"\nИтого: {total:.2f} руб."

            QMessageBox.information(self, "Извещение на оплату", notice_text)
            cursor.close()
        except mysql.connector.Error as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка при получении данных:\n{str(e)}")
        except Exception as e:
            QMessageBox.critical(self, "Неизвестная ошибка", f"Произошла ошибка:\n{str(e)}")

    def closeEvent(self, event):
        """Закрытие приложения"""
        try:
            self.connection.close()
        except Exception:
            pass
        event.accept()


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        window = MainWindow()
        window.show()
        sys.exit(app.exec())
    except Exception as e:
        QMessageBox.critical(None, "Критическая ошибка", f"Ошибка запуска приложения:\n{str(e)}")
        sys.exit(1)
