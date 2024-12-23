from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QMessageBox
import sys

# Локальное хранилище данных (вместо базы данных)
tt = [
    {"id": 1, "name": "Станция А", "trips": 0},
    {"id": 2, "name": "Станция Б", "trips": 0},
]

torts = [
    {"id": 1, "brand": "Кузьминки", "capacity": 1},
    {"id": 2, "brand": "Текстильщики", "capacity": 1},
]

# Список рейсов, где каждый рейс — это словарь
trips = []

# Функция для расчёта общего количества рейсов
def calculate_total_capacity():
    total_capacity = sum(
        tort["capacity"] for trip in trips for tort in torts if tort["id"] == trip["tort_id"]
    )
    QMessageBox.information(None, "Общее количество рейсов", f"Общее количество рейсов: {total_capacity}")

# Главное окно
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Управление рейсами")
        self.setGeometry(100, 100, 700, 500)
        self.initUI()

    def initUI(self):
        # Основной макет
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title_label = QtWidgets.QLabel(" Управление рейсами")
        title_label.setFont(QtGui.QFont("Arial", 22, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #444; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Список станций
        self.station_list = QtWidgets.QListWidget()
        self.station_list.setFont(QtGui.QFont("Arial", 14))
        self.station_list.setStyleSheet("""
            background-color: #ffffff;
            color: #555555;
            border: 2px solid #D3D3D3;
            border-radius: 10px;
            padding: 10px;
        """)
        layout.addWidget(self.station_list)

        # Кнопки
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(20)

        calc_button = self.create_button("\ud83d\udcca Рассчитать количество рейсов", calculate_total_capacity, "#4CAF50")
        button_layout.addWidget(calc_button)

        add_trip_button = self.create_button("\u2795 Добавить торт", self.open_add_trip_window, "#007BFF")
        button_layout.addWidget(add_trip_button)

        exit_button = self.create_button("\u274c Выход", self.close, "#FF3B3B")
        button_layout.addWidget(exit_button)

        layout.addLayout(button_layout)

        self.setLayout(layout)
        self.show_station_trips()

    # Функция для отображения станций и количества рейсов
    def show_station_trips(self):
        self.station_list.clear()
        for station in tt:
            self.station_list.addItem(f"{station['name']}: {station['trips']} рейсов")
        if not tt:
            self.station_list.addItem("Нет данных о станциях.")

    # Функция для создания окна добавления рейса
    def open_add_trip_window(self):
        self.add_trip_window = AddTripWindow(self)
        self.add_trip_window.show()

    # Создание кнопки с иконками и стилем
    def create_button(self, text, callback, color):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #2a9d8f;
            }}
        """)
        return button

# Окно добавления рейса
class AddTripWindow(QtWidgets.QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Добавление рейса")
        self.setGeometry(200, 200, 450, 400)
        self.initUI()

    def initUI(self):
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)

        # Заголовок
        title_label = QtWidgets.QLabel("\u2795 Добавить рейс")
        title_label.setFont(QtGui.QFont("Arial", 18, QtGui.QFont.Weight.Bold))
        title_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: #444; margin-bottom: 20px;")
        layout.addWidget(title_label)

        # Поля ввода
        form_layout = QtWidgets.QFormLayout()
        self.station_combo = QtWidgets.QComboBox()
        self.station_combo.setStyleSheet("background-color: #f5f5f5; border: 2px solid #D3D3D3; padding: 5px;")
        for station in tt:
            self.station_combo.addItem(f"{station['id']} - {station['name']}")
        form_layout.addRow(" Кондитерская:", self.station_combo)

        self.tort_combo = QtWidgets.QComboBox()
        self.tort_combo.setStyleSheet("background-color: #f5f5f5; border: 2px solid #D3D3D3; padding: 5px;")
        for tort in torts:
            self.tort_combo.addItem(f"{tort['id']} - {tort['brand']} (порций: {tort['capacity']})")
        form_layout.addRow(" Торт:", self.tort_combo)

        self.time_input = QtWidgets.QLineEdit()
        self.time_input.setPlaceholderText("Формат: HH:MM")
        self.time_input.setStyleSheet("background-color: #ffffff; border: 2px solid #D3D3D3; padding: 5px;")
        form_layout.addRow("\u23f0 Время приезда:", self.time_input)

        layout.addLayout(form_layout)

        # Кнопки
        button_layout = QtWidgets.QHBoxLayout()
        save_button = self.create_button("\ud83d\udcbe Сохранить", self.save_trip, "#007BFF")
        button_layout.addWidget(save_button)

        back_button = self.create_button("\u21a9 Назад", self.close, "#FF3B3B")
        button_layout.addWidget(back_button)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    # Сохранение нового рейса
    def save_trip(self):
        station_text = self.station_combo.currentText()
        tort_text = self.tort_combo.currentText()
        time = self.time_input.text()

        if not station_text or not tort_text or not time:
            QMessageBox.critical(self, "Ошибка", "Все поля должны быть заполнены!")
            return

        try:
            # Конвертируем ID станции и торта в числа
            station_id = int(station_text.split(" - ")[0])
            tort_id = int(tort_text.split(" - ")[0])

            # Проверяем корректность времени (в формате HH:MM)
            if len(time) != 5 or time[2] != ":" or not time.replace(":", "").isdigit():
                raise ValueError("Некорректный формат времени. Используйте HH:MM.")

            # Добавляем рейс
            trips.append({"station_id": station_id, "tort_id": tort_id, "time": time})

            # Увеличиваем счётчик рейсов для станции
            for station in tt:
                if station["id"] == station_id:
                    station["trips"] += 1

            QMessageBox.information(self, "Успех", "Рейс добавлен!")
            self.close()
            self.parent.show_station_trips()  # Обновление списка
        except ValueError as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка: {e}")

    # Создание кнопки с иконками и стилем
    def create_button(self, text, callback, color):
        button = QtWidgets.QPushButton(text)
        button.clicked.connect(callback)
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 16px;
            }}
            QPushButton:hover {{
                background-color: #0056b3;
            }}
        """)
        return button


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    # Установка общей темы для приложения
    app.setStyleSheet("""
        QWidget {
            background-color: #F0F4F8;
        }
        QLabel {
            color: #333333;
        }
    """)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
