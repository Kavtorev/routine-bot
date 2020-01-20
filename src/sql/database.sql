CREATE TABLE students(
	id INT PRIMARY KEY AUTO_INCREMENT,
	uid INT unique,
	first_name VARCHAR(40),
	last_name VARCHAR(40),
	user_name VARCHAR(40),
	login VARCHAR(10) DEFAULT 'unknown',
	password VARCHAR(40) DEFAULT 'unknown'

);


