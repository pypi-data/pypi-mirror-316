# -- Частная клиника.Врачи частной клиники ведут прием пациентов по определенному расписанию. В результате приема ставится диагноз.
# -- Таблицы: Врачи (Код врача, ФИО, специализация), Пациенты (Код пациента, ФИО, адрес), Диагнозы (Код диагноза, название, лечение), Приемы (Код приема, код врача, код пациента, дата, время, код диагноза).Требуется:
# -- определить пациентов, побывавших у врача более одного раза;- относительную загрузку врачей по специализациям.
# CREATE DATABASE IF NOT EXISTS PrivateClinic;
# USE PrivateClinic;
# -- Таблицы
# CREATE TABLE Doctors (
#     doctor_id INT AUTO_INCREMENT PRIMARY KEY,    full_name VARCHAR(100) NOT NULL,
# specialization VARCHAR(100));
# CREATE TABLE Patients (
#     patient_id INT AUTO_INCREMENT PRIMARY KEY,    full_name VARCHAR(100) NOT NULL,
# address VARCHAR(200));
# CREATE TABLE Diagnoses (
#     diagnosis_id INT AUTO_INCREMENT PRIMARY KEY,    diagnosis_name VARCHAR(100),
# treatment TEXT);
# CREATE TABLE Appointments (
#     appointment_id INT AUTO_INCREMENT PRIMARY KEY,    doctor_id INT,
# patient_id INT,    appointment_date DATE,
# appointment_time TIME,    diagnosis_id INT,
# FOREIGN KEY (doctor_id) REFERENCES Doctors(doctor_id),    FOREIGN KEY (patient_id) REFERENCES Patients(patient_id),
# FOREIGN KEY (diagnosis_id) REFERENCES Diagnoses(diagnosis_id));
#
# -----------------------------------------ё
#
# -- Вставка данных в таблицу Doctors
# INSERT INTO Doctors (full_name, specialization) VALUES
# ('Иванов Иван Иванович', 'Терапевт'),
# ('Петров Петр Петрович', 'Хирург'),
# ('Сидорова Анна Сергеевна', 'Кардиолог');
#
# -- Вставка данных в таблицу Patients
# INSERT INTO Patients (full_name, address) VALUES
# ('Смирнов Алексей Викторович', 'Москва, ул. Ленина, д. 1'),
# ('Кузнецова Ольга Павловна', 'Санкт-Петербург, пр. Невский, д. 2'),
# ('Попов Сергей Николаевич', 'Екатеринбург, ул. Уральская, д. 3');
#
# -- Вставка данных в таблицу Diagnoses
# INSERT INTO Diagnoses (diagnosis_name, treatment) VALUES
# ('Грипп', 'Постельный режим, противовирусные препараты'),
# ('Перелом руки', 'Иммобилизация, операция при необходимости'),
# ('Гипертония', 'Изменение образа жизни, медикаментозное лечение');
#
# -- Вставка данных в таблицу Appointments
# INSERT INTO Appointments (doctor_id, patient_id, appointment_date, appointment_time, diagnosis_id) VALUES
# (1, 1, '2023-10-01', '10:00:00', 1), -- Иванов И.И. принимает Смирнова А.В. с диагнозом Грипп
# (2, 2, '2023-10-02', '11:00:00', 2), -- Петров П.П. принимает Кузнецову О.П. с диагнозом Перелом руки
# (3, 3, '2023-10-03', '12:00:00', 3); -- Сидорова А.С. принимает Попова С.Н. с диагнозом Гипертония
#
# ---------------------------------------------
#
# -- Процедуры:sql
# -- Копировать код-- Пациенты, посетившие врача более одного раза
# DELIMITER $$CREATE PROCEDURE GetFrequentPatients()
# BEGIN    SELECT p.full_name, d.full_name AS doctor_name, COUNT(a.appointment_id) AS visit_count
# FROM Appointments a    JOIN Patients p ON a.patient_id = p.patient_id
# JOIN Doctors d ON a.doctor_id = d.doctor_id    GROUP BY p.patient_id, d.doctor_id
# HAVING visit_count > 1;END$$
# DELIMITER ;
# -- Относительная загрузка врачей по специализациямDELIMITER $$
# CREATE PROCEDURE GetDoctorLoadBySpecialization()BEGIN
# SELECT d.specialization,           COUNT(a.appointment_id) AS total_appointments,
# ROUND(COUNT(a.appointment_id) / (SELECT COUNT(*) FROM Appointments) * 100, 2) AS load_percentage    FROM Appointments a
# JOIN Doctors d ON a.doctor_id = d.doctor_id    GROUP BY d.specialization;
# END$$DELIMITER ;

import sys
import mysql.connector
from PyQt6 import QtWidgets, QtGui

class Database:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host='localhost',
            user='admin',  # Замените на ваше имя пользователя
            password='admin',  # Замените на ваш пароль
            database='PrivateClinic'  # Замените на ваше имя базы данных
        )
        self.cursor = self.connection.cursor()

    def call_procedure(self, procedure_name):
        self.cursor.callproc(procedure_name)
        results = []
        for result in self.cursor.stored_results():
            results.append(result.fetchall())
        return results

    def close(self):
        self.cursor.close()
        self.connection.close()


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Medical Database")
        self.setGeometry(100, 100, 600, 400)

        self.layout = QtWidgets.QVBoxLayout()
        
        self.button_frequent_patients = QtWidgets.QPushButton("Get Frequent Patients")
        self.button_frequent_patients.clicked.connect(self.get_frequent_patients)
        
        self.button_doctor_load = QtWidgets.QPushButton("Get Doctor Load by Specialization")
        self.button_doctor_load.clicked.connect(self.get_doctor_load_by_specialization)

        self.table = QtWidgets.QTableWidget()
        
        self.layout.addWidget(self.button_frequent_patients)
        self.layout.addWidget(self.button_doctor_load)
        self.layout.addWidget(self.table)

        self.setLayout(self.layout)

        self.database = Database()

    def get_frequent_patients(self):
        results = self.database.call_procedure('GetFrequentPatients')
        self.display_results(results[0], ["Patient Name", "Doctor Name", "Visit Count"])

    def get_doctor_load_by_specialization(self):
        results = self.database.call_procedure('GetDoctorLoadBySpecialization')
        self.display_results(results[0], ["Specialization", "Total Appointments", "Load Percentage"])

    def display_results(self, data, headers):
        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)

        for i, row in enumerate(data):
            for j, value in enumerate(row):
                self.table.setItem(i, j, QtWidgets.QTableWidgetItem(str(value)))

    def closeEvent(self, event):
        self.database.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())