create database dbname;
CREATE TABLE `dbname`.`login_details` (
  `email` VARCHAR(45) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `psw` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`email`),
  UNIQUE INDEX `email_UNIQUE` (`email` ASC) VISIBLE);