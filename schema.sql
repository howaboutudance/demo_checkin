
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	username VARCHAR(40) UNIQUE NOT NULL,
	password VARCHAR(128) NOT NULL
)


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
CREATE TABLE IF NOT EXISTS form {
	id serial NOT NULL PRIMARY KEY,
	schema json,
	uischema json
}
COMMIT;

