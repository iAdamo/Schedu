-- prepares a MySQL server for the project

DROP DATABASE IF EXISTS schedu_db;

CREATE DATABASE IF NOT EXISTS schedu_db;
CREATE USER IF NOT EXISTS 'schedu_dev'@'localhost' IDENTIFIED BY 'password';
GRANT ALL PRIVILEGES ON `schedu_db`.* TO 'schedu_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'schedu_dev'@'localhost';
FLUSH PRIVILEGES;

use schedu_db;

DROP TABLE IF EXISTS `admins`;

CREATE TABLE admins (
    id VARCHAR(60) NOT NULL,
    password VARCHAR(128) NOT NULL,
    first_name VARCHAR(60) NOT NULL,
    last_name VARCHAR(60) NOT NULL,
    date_of_birth VARCHAR(10) NOT NULL,
    nin INT NOT NULL UNIQUE,
    phone_number INT NOT NULL UNIQUE,
    email VARCHAR(128) NOT NULL UNIQUE,
    role VARCHAR(128) NOT NULL,
    PRIMARY KEY (id)
);

INSERT INTO admins VALUES
('schedu-admin-ali-0000', '$2b$12$ggLlP8CFrScNpGcEV8D0YOMrHx3Nb.USpm3MUSuEFV7pk1vFcw1ma', 'John', 'Doe', '1990-01-01', 123456089, 967654321, 'john.doe@eample.com', 'admin'),
('student2', 'hashed_password_2', 'Jane', 'Smith', '1995-05-15', 987684321, 123406789, 'jane.sith@example.com', 'student');
