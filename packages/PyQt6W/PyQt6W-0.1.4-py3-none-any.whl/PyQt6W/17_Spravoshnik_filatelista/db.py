# -- SQLBook: Code
# DROP DATABASE IF EXISTS philately;
# CREATE DATABASE philately;
#
# USE philately;
#
# CREATE TABLE genres (
#     id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(255) NOT NULL UNIQUE
# );
#
# CREATE TABLE countries (
#     id INT AUTO_INCREMENT PRIMARY KEY,
# name VARCHAR(255) NOT NULL UNIQUE
# );
#
# CREATE TABLE stamps (
#     id INT AUTO_INCREMENT PRIMARY KEY,
# country_id INT NOT NULL,
# genre_id INT NOT NULL,
# release_year INT NOT NULL,
# price DECIMAL(10, 2) NOT NULL,
# FOREIGN KEY (country_id) REFERENCES countries(id),
# FOREIGN KEY (genre_id) REFERENCES genres(id)
# );
#
# # Список жанров филателиста
# INSERT INTO genres (name) VALUES
# ('Советские'),
# ('Современные'),
# ('Восточные'),
# ('Индийские'),
# ('Азиатские');
#
# # Список стран филателиста
# INSERT INTO countries (name) VALUES
# ('Австралия'),
# ('Австрия'),
# ('Азербайджан'),
# ('Албания'),
# ('Англия'),
# ('Ангола'),
# ('Антарктика'),
# ('Аргентина'),
# ('Армения'),
# ('Афганистан'),
# ('Бангладеш'),
# ('Беларусь'),
# ('Бельгия'),
# ('Болгария'),
# ('Бразилия'),
# ('Великобритания'),
# ('Венгрия'),
# ('Венесуэла'),
# ('Вьетнам'),
# ('Германия'),
# ('Греция'),
# ('Дания'),
# ('Египет'),
# ('Израиль'),
# ('Индия'),
# ('Индонезия'),
# ('Иордания'),
# ('Ирак'),
# ('Иран'),
# ('Италия'),
# ('Казахстан'),
# ('Канада'),
# ('Китаи'),
# ('Колумбия'),
# ('Корея'),
# ('Куба'),
# ('Латвия'),
# ('Литва'),
# ('Люксембург'),
# ('Малайзия'),
# ('Мексика'),
# ('Молдавия'),
# ('Нидерланды');
#
# # Список стикеров
# INSERT INTO stamps (country_id, genre_id, release_year, price, album_number) VALUES
# (1, 1, YEAR(NOW()) - FLOOR(RAND()*100), FLOOR(RAND()*1000) + 1, FLOOR(RAND()*1000) + 1),
# (2, 1, YEAR(NOW()) - FLOOR(RAND()*100), FLOOR(RAND()*1000) + 1, FLOOR(RAND()*1000) + 1),
# (3, 1, YEAR(NOW()) - FLOOR(RAND()*100), FLOOR(RAND()*1000) + 1, FLOOR(RAND()*1000) + 1),
# (4, 1, YEAR(NOW()) - FLOOR(RAND()*100), FLOOR(RAND()*1000) + 1, FLOOR(RAND()*1000) + 1),
# (5, 1, YEAR(NOW()) - FLOOR(RAND()*100), FLOOR(RAND()*1000) + 1, FLOOR(RAND()*1000) + 1);
#
#
# DELIMITER //
#
# CREATE PROCEDURE GetMostExpensiveStamp()
# BEGIN
# SELECT
# s.id,
# s.price,
# c.name AS country,
# g.name AS genre,
# s.release_year,
# s.album_number
# FROM stamps s
# JOIN countries c ON s.country_id = c.id
# JOIN genres g ON s.genre_id = g.id
# ORDER BY s.price DESC
# LIMIT 1;
# END //
#
# DELIMITER ;


import mysql.connector

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="philately"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Ошибка при подключении к базе данных: {err}")
        return None

