CREATE DATABASE concerts;
CREATE TABLE concerts.event (
  id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(50) NOT NULL,
  venue VARCHAR(50) NOT NULL,
  date TIMESTAMP NOT NULL
)
