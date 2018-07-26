DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS student CASCADE;
DROP TABLE IF EXISTS preferredname;
DROP TABLE IF EXISTS session;
DROP TABLE IF EXISTS studentsession;
DROP TABLE IF EXISTS faculty;
DROP TABLE IF EXISTS facultyteam;

DROP TYPE IF EXISTS session_kind;

CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(40) UNIQUE NOT NULL,
	password VARCHAR(128) NOT NULL
);


CREATE TABLE IF NOT EXISTS student(
       anum CHAR(9) NOT NULL PRIMARY KEY,
       firstname VARCHAR(64),
       lastname VARCHAR(64)
); 

CREATE TABLE IF NOT EXISTS preferredname(
      anum CHAR(9) REFERENCES student(anum),
      preferredfirstname VARCHAR(64),
      pronouns VARCHAR(24)
);

CREATE TYPE session_kind AS ENUM('mandatory', 'affinity', 'c2c', 'seminar');
CREATE TABLE IF NOT EXISTS session(
       id SERIAL NOT NULL PRIMARY KEY,
       name VARCHAR(128),
       seats INT,
       location VARCHAR(128),
       starttime TIMESTAMPTZ,
       length FLOAT,
       kind session_kind
);

CREATE TABLE IF NOT EXISTS studentsession(
       id SERIAL NOT NULL PRIMARY KEY,
       anum char(9) NOT NULL,
       session_id INT NOT NULL
);

CREATE TABLE IF NOT EXISTS faculty (
       id SERIAL NOT NULL PRIMARY KEY,
       name VARCHAR(128)
);
CREATE TABLE IF NOT EXISTS facultyteam (
       id SERIAL NOT NULL PRIMARY KEY,
       session_id INT,
       faculty_id INT
);

COMMIT;

INSERT INTO student(anum, firstname, lastname) values 
	('A4','Adam','King'),
	('A5', 'Jacob','Lambert');
INSERT INTO preferredname(anum, pronouns) values
	('A5', 'he/his');

INSERT INTO session(name, location) values
	('Orientation Seminar', 'SEM II A1107'),
	('First Peoples Reception','LIB 4300'),
	('Trans and Queer Cetner Reception','LIB 4300'),
	('Better Reading Through Writing','LIB 3301');
