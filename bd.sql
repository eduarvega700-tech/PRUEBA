CREATE DATABASE par_impar;

USE par_impar;

CREATE TABLE resultados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL,
    resultado VARCHAR(50) NOT NULL
);

CREATE TABLE tablas_multiplicar (
    id INT AUTO_INCREMENT PRIMARY KEY,
    numero INT NOT NULL,
    tabla_generada TEXT NOT NULL
);

CREATE TABLE adivina_numero (
    id INT AUTO_INCREMENT PRIMARY KEY,
    intento INT NOT NULL,
    numero_secreto INT NOT NULL,
    mensaje VARCHAR(100) NOT NULL
);