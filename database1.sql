DROP DATABASE IF EXISTS BMI;
CREATE DATABASE IF NOT EXISTS BMI;
USE BMI;


CREATE TABLE IF NOT EXISTS user(
	id INT AUTO_INCREMENT PRIMARY KEY,
	f_name VARCHAR(20) NOT NULL,
	l_name VARCHAR(20) NOT NULL,
	height DECIMAL(3,2) NOT NULL,
	weight DECIMAL(5,2) NOT NULL,
	BMI DECIMAL(5,2),
	CONSTRAINT valid_name CHECK( LENGTH(f_name) >=2 AND LENGTH(l_name) >= 2 )
	);


-- BMI Calculation
DROP TRIGGER IF EXISTS bmi_insert;
CREATE TRIGGER bmi_insert BEFORE INSERT ON user 
FOR EACH ROW 
SET NEW.bmi = NEW.weight / (NEW.height * NEW.height);


DROP TRIGGER IF EXISTS bmi_update;
CREATE TRIGGER bmi_update BEFORE UPDATE ON user 
FOR EACH ROW 
SET NEW.bmi = NEW.weight / (NEW.height * NEW.height);


