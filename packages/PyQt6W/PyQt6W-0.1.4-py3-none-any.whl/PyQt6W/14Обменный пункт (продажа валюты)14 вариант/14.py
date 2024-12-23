"""CREATE DATABASE ExchangeDB;
USE ExchangeDB;
CREATE TABLE Клиенты (
    Код_клиента INT AUTO_INCREMENT PRIMARY KEY,
    ФИО VARCHAR(255) NOT NULL,
    Паспорт VARCHAR(50) NOT NULL
);

CREATE TABLE Валюта (
    Код_валюты INT AUTO_INCREMENT PRIMARY KEY,
    Название VARCHAR(50) NOT NULL,
    Курс_продажи DECIMAL(10, 2) NOT NULL
);

CREATE TABLE Сделки (
    Код_сделки INT AUTO_INCREMENT PRIMARY KEY,
    Код_клиента INT NOT NULL,
    Код_валюты INT NOT NULL,
    Сумма DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (Код_клиента) REFERENCES Клиенты(Код_клиента),
    FOREIGN KEY (Код_валюты) REFERENCES Валюта(Код_валюты)
);
INSERT INTO Клиенты (ФИО, Паспорт) VALUES
('Иван Иванов', '1234 567890'),
('Мария Смирнова', '2345 678901'),
('Анна Петрова', '3456 789012');

INSERT INTO Валюта (Название, Курс_продажи) VALUES
('USD', 75.50),
('EUR', 85.30),
('GBP', 95.40);

INSERT INTO Сделки (Код_клиента, Код_валюты, Сумма) VALUES
(1Автовокзал, 1Автовокзал, 1000),
(2, 2, 500),
(3, 3, 300),
(1Автовокзал, 2, 200);
"""



import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import ttk, messagebox

def calculate_share_and_max_deal():
    try:
        # Подключение к базе данных
        connection = mysql.connector.connect(
            host="localhost",
            user="root",  # Замените на свой MySQL логин
            password="root",  # Замените на свой MySQL пароль
            database="ExchangeDB"  # Название базы данных в MySQL
        )
        cursor = connection.cursor()

        # 1Автовокзал. Доля сделок по каждой валюте
        query1 = """
        SELECT 
            v.Название AS Валюта,
            SUM(s.Сумма * v.Курс_продажи) AS Сделки_в_рублях,
            (SUM(s.Сумма * v.Курс_продажи) / (SELECT SUM(s1.Сумма * v1.Курс_продажи) 
                                            FROM Сделки s1
                                            JOIN Валюта v1 ON s1.Код_валюты = v1.Код_валюты)) * 100 AS Доля_в_процентах
        FROM Сделки s
        JOIN Валюта v ON s.Код_валюты = v.Код_валюты
        GROUP BY v.Название
        ORDER BY Доля_в_процентах DESC;
        """
        cursor.execute(query1)
        result1 = cursor.fetchall()

        # 2. Максимальный размер сделки в рублях
        query2 = """
        SELECT 
            s.Код_сделки,
            c.ФИО AS Клиент,
            v.Название AS Валюта,
            s.Сумма * v.Курс_продажи AS Сделка_в_рублях
        FROM Сделки s
        JOIN Валюта v ON s.Код_валюты = v.Код_валюты
        JOIN Клиенты c ON s.Код_клиента = c.Код_клиента
        ORDER BY Сделка_в_рублях DESC
        LIMIT 1Автовокзал;
        """
        cursor.execute(query2)
        result2 = cursor.fetchone()

        return result1, result2

    except Error as e:
        messagebox.showerror("Ошибка", f"Ошибка при работе с MySQL: {e}")
        return None, None

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def show_results():
    result1, result2 = calculate_share_and_max_deal()
    if result1 and result2:
        # Очистка таблицы перед добавлением новых данных
        for row in tree.get_children():
            tree.delete(row)

        # Добавление данных в таблицу
        for row in result1:
            tree.insert("", tk.END, values=(row[0], f"{row[1]:.2f}", f"{row[2]:.2f}%"))

        # Отображение максимальной сделки
        max_deal_label.config(
            text=f"Код сделки: {result2[0]}, Клиент: {result2[1]}, "
                 f"Валюта: {result2[2]}, Сделка в рублях: {result2[3]:.2f}"
        )


# Создание главного окна
root = tk.Tk()
root.title("Расчеты по сделкам")
root.geometry("700x500")

# Заголовок
title_label = tk.Label(root, text="Расчеты по сделкам валютного обмена", font=("Arial", 16))
title_label.pack(pady=10)

# Создание таблицы для отображения данных
columns = ("Валюта", "Сделки в рублях", "Доля в процентах")
tree = ttk.Treeview(root, columns=columns, show="headings", height=10)
tree.pack(pady=10)

# Определение заголовков таблицы
tree.heading("Валюта", text="Валюта")
tree.heading("Сделки в рублях", text="Сделки в рублях")
tree.heading("Доля в процентах", text="Доля в процентах")

# Кнопка для выполнения расчетов
calc_button = tk.Button(root, text="Выполнить расчеты", command=show_results, bg="lightblue", font=("Arial", 12))
calc_button.pack(pady=10)

# Метка для отображения максимальной сделки
max_deal_label = tk.Label(root, text="", font=("Arial", 12), fg="blue")
max_deal_label.pack(pady=20)

# Запуск интерфейса
root.mainloop()
