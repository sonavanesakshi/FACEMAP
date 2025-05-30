CREATE DATABASE  IF NOT EXISTS `project`;
USE `project`;


CREATE TABLE skin_analysis (
    id INT PRIMARY KEY AUTO_INCREMENT,
    gender VARCHAR(20),
    age VARCHAR(30),
    acne_type VARCHAR(50),
    suggestions JSON,
    filename VARCHAR(60),
    analyzed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);