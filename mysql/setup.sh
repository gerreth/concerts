#!/bin/bash
set -e

mysql --user=root --password=root mysql <<-EOSQL
  CREATE DATABASE IF NOT EXISTS concerts;
  DROP TABLE IF EXISTS concerts.event;
  CREATE TABLE concerts.event (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL,
    venue VARCHAR(80) NOT NULL,
    date TIMESTAMP NOT NULL,
    UNIQUE KEY name (name,venue,date)
  )
EOSQL
