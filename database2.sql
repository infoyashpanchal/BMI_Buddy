USE BMI;


DELIMITER $$

select "delimiter changes" $$
show warnings $$

DROP TRIGGER IF EXISTS insert_validation;
DROP TRIGGER IF EXISTS update_validation;

select "triggers deleted" $$
show warnings $$
-- INSERT VALIDATION
CREATE TRIGGER insert_validation BEFORE INSERT ON user FOR EACH ROW
BEGIN
DECLARE EXIT HANDLER FOR 12345 BEGIN END;	-- First Name not alpha
DECLARE EXIT HANDLER FOR 23456 BEGIN END;	-- Last Name not alpha

IF REGEXP_LIKE(NEW.f_name, '[^a-zA-Z]') THEN
	SIGNAL SQLSTATE '12345'
	SET MESSAGE_TEXT = 'Invalid First Name';
END IF;

IF NEW.l_name REGEXP '[^a-zA-Z]' THEN
	SIGNAL SQLSTATE '23456'
	SET MESSAGE_TEXT = 'Inavlid Last Name';
END IF;
END $$

select "insert validation created" $$
show warnings $$

-- UPDATE VALIDATION
CREATE TRIGGER update_validation BEFORE UPDATE ON user FOR EACH ROW
BEGIN
DECLARE EXIT HANDLER FOR 34567 BEGIN END;	-- First Name not alpha
DECLARE EXIT HANDLER FOR 45678 BEGIN END;	-- Last Name not alpha

IF REGEXP_LIKE(NEW.f_name, '[^a-zA-Z]') THEN
	SIGNAL SQLSTATE '34567'
	SET MESSAGE_TEXT = 'Invalid First Name';
END IF;

IF NEW.l_name REGEXP '[^a-zA-Z]' THEN
	SIGNAL SQLSTATE '45678'
	SET MESSAGE_TEXT = 'Inavlid Last Name';
END IF;
END $$ 

select "update validation created" $$
show warnings $$
DELIMITER ;

select "delimiter changed";
show warnings;
