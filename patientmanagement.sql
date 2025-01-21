create database patientmanagement;
use patientmanagement;
 CREATE TABLE adminsignup (
  name varchar(30) DEFAULT NULL,
  mobile bigint NOT NULL,
  email varchar(50) DEFAULT NULL,
  password varchar(40) DEFAULT NULL,
  PRIMARY KEY (mobile),
  UNIQUE KEY email (email)
);
 CREATE TABLE appoint (
  appointment_id int NOT NULL AUTO_INCREMENT,
  patientname varchar(30) NOT NULL,
  phone bigint NOT NULL,
  message text,
  date date NOT NULL,
  time time NOT NULL,
  PRIMARY KEY (appointment_id)
);

CREATE TABLE checkinout (
  appointment_id int NOT NULL,
  action enum('Check-In','Check-Out') DEFAULT 'Check-In',
  check_in_time datetime NOT NULL,
  check_out_time datetime DEFAULT NULL,
  KEY appointment_id (appointment_id),
  CONSTRAINT checkinout_ibfk_1 FOREIGN KEY (appointment_id) REFERENCES appoint (appointment_id) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE docsignup (
  name varchar(30) DEFAULT NULL,
  mobile bigint NOT NULL,
  email varchar(50) DEFAULT NULL,
  password varchar(40) DEFAULT NULL,
  PRIMARY KEY (mobile),
  UNIQUE KEY email (email)
);

 CREATE TABLE records (
  patientId varchar(30) NOT NULL,
  patientname varchar(30) DEFAULT NULL,
  records varchar(220) DEFAULT NULL,
  PRIMARY KEY (patientId)
);

CREATE TABLE `signup` (
  username varchar(12) DEFAULT NULL,
  mobile varchar(50) DEFAULT NULL,
  email varchar(50) DEFAULT NULL,
  address varchar(75) DEFAULT NULL,
  password text,
  KEY email (email),
  KEY idx_username (username)
);