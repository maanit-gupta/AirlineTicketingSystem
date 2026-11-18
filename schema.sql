CREATE DATABASE IF NOT EXISTS airline_db;
USE airline_db;

CREATE TABLE IF NOT EXISTS flights (
    code   VARCHAR(10) PRIMARY KEY,
    route  VARCHAR(100) NOT NULL,
    dep_time VARCHAR(20) NOT NULL,
    price  INT NOT NULL,
    seats  INT NOT NULL
);

CREATE TABLE IF NOT EXISTS bookings (
    pnr           CHAR(6) PRIMARY KEY,
    passenger_name VARCHAR(100) NOT NULL,
    age           INT NOT NULL,
    flight_code   VARCHAR(10) NOT NULL,
    travel_class  VARCHAR(10) NOT NULL,
    fare          INT NOT NULL,
    booked_at     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (flight_code) REFERENCES flights(code)
);

INSERT IGNORE INTO flights (code, route, dep_time, price, seats) VALUES
 ('AI101', 'New York -> Chicago', '08:00 AM', 180, 5),
 ('UA202', 'Chicago -> Dallas',   '11:30 AM', 150, 4),
 ('DL303', 'Atlanta -> Miami',    '02:15 PM', 130, 3),
 ('AA404', 'Dallas -> Denver',    '05:45 PM', 170, 2),
 ('WN505', 'Denver -> Las Vegas', '08:10 PM', 110, 6);
