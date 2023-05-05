-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema newdb
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema newdb
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `newdb` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `newdb` ;

-- -----------------------------------------------------
-- Table `newdb`.`user`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`user` (
  `username` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `picture` VARCHAR(255) NULL DEFAULT NULL,
  `fullname` VARCHAR(255) NULL DEFAULT NULL,
  `age` INT NULL DEFAULT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  `languages` VARCHAR(255) NULL DEFAULT NULL,
  `contact` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `newdb`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`student` (
  `username` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `picture` VARCHAR(255) NULL DEFAULT NULL,
  `fullname` VARCHAR(255) NULL DEFAULT NULL,
  `age` INT NULL DEFAULT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  `languages` VARCHAR(255) NULL DEFAULT NULL,
  `contact` VARCHAR(255) NULL DEFAULT NULL,
  `interests` VARCHAR(255) NULL DEFAULT NULL,
  `useruser` VARCHAR(100) NULL DEFAULT NULL,
  `userpass` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`username`),
  INDEX `useruser` (`useruser` ASC) VISIBLE,
  CONSTRAINT `student_ibfk_1`
    FOREIGN KEY (`useruser`)
    REFERENCES `newdb`.`user` (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `newdb`.`tutor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`tutor` (
  `username` VARCHAR(100) NOT NULL,
  `password` VARCHAR(100) NOT NULL,
  `picture` VARCHAR(255) NULL DEFAULT NULL,
  `fullname` VARCHAR(255) NULL DEFAULT NULL,
  `age` INT NULL DEFAULT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  `languages` VARCHAR(255) NULL DEFAULT NULL,
  `contact` VARCHAR(255) NULL DEFAULT NULL,
  `bio` VARCHAR(255) NULL DEFAULT NULL,
  `education` VARCHAR(255) NULL DEFAULT NULL,
  `yearsofexperience` INT NULL DEFAULT NULL,
  `location` VARCHAR(255) NULL DEFAULT NULL,
  `subjects` VARCHAR(255) NULL DEFAULT NULL,
  `availability` VARCHAR(255) NULL DEFAULT NULL,
  `minprice` INT NULL DEFAULT NULL,
  `maxprice` INT NULL DEFAULT NULL,
  `deliverymethod` VARCHAR(255) NULL DEFAULT NULL,
  `avgrating` FLOAT NULL DEFAULT NULL,
  `cv` VARCHAR(255) NULL DEFAULT NULL,
  `docs` VARCHAR(255) NULL DEFAULT NULL,
  `useruser` VARCHAR(100) NULL DEFAULT NULL,
  `userpass` VARCHAR(100) NULL DEFAULT NULL,
  PRIMARY KEY (`username`),
  INDEX `useruser` (`useruser` ASC) VISIBLE,
  CONSTRAINT `tutor_ibfk_1`
    FOREIGN KEY (`useruser`)
    REFERENCES `newdb`.`user` (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `newdb`.`session`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`session` (
  `sessionid` INT NOT NULL,
  `platform` VARCHAR(255) NULL DEFAULT NULL,
  `tutfeedback` VARCHAR(255) NULL DEFAULT NULL,
  `username` VARCHAR(100) NULL DEFAULT NULL,
  `password` VARCHAR(100) NULL DEFAULT NULL,
  `rating` FLOAT NULL DEFAULT NULL,
  PRIMARY KEY (`sessionid`),
  INDEX `username` (`username` ASC) VISIBLE,
  CONSTRAINT `session_ibfk_1`
    FOREIGN KEY (`username`)
    REFERENCES `newdb`.`student` (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `newdb`.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`booking` (
  `usid` VARCHAR(100) NOT NULL,
  `uspass` VARCHAR(100) NOT NULL,
  `tutorid` VARCHAR(100) NOT NULL,
  `tutpass` VARCHAR(100) NOT NULL,
  `sessid` INT NOT NULL,
  `platform` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY (`usid`, `tutorid`, `sessid`),
  INDEX `tutorid` (`tutorid` ASC) VISIBLE,
  INDEX `sessid` (`sessid` ASC) VISIBLE,
  CONSTRAINT `booking_ibfk_1`
    FOREIGN KEY (`usid`)
    REFERENCES `newdb`.`student` (`username`),
  CONSTRAINT `booking_ibfk_2`
    FOREIGN KEY (`tutorid`)
    REFERENCES `newdb`.`tutor` (`username`),
  CONSTRAINT `booking_ibfk_3`
    FOREIGN KEY (`sessid`)
    REFERENCES `newdb`.`session` (`sessionid`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `newdb`.`chat`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`chat` (
  `chatid` INT NOT NULL,
  `timestamp` TIMESTAMP NOT NULL,
  `message` VARCHAR(200) NOT NULL,
  `tutuser` VARCHAR(100) NOT NULL,
  `studuser` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`chatid`),
  INDEX `tutuser` (`tutuser` ASC) VISIBLE,
  INDEX `studuser` (`studuser` ASC) VISIBLE,
  CONSTRAINT `chat_ibfk_1`
    FOREIGN KEY (`tutuser`)
    REFERENCES `newdb`.`tutor` (`username`),
  CONSTRAINT `chat_ibfk_2`
    FOREIGN KEY (`studuser`)
    REFERENCES `newdb`.`student` (`username`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `newdb`.`learning`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`learning` (
  `learningid` INT NOT NULL AUTO_INCREMENT,
  `studuser` VARCHAR(100) NOT NULL,
  `tutuser` VARCHAR(100) NOT NULL,
  `coursename` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`learningid`),
  INDEX `studuser` (`studuser` ASC) VISIBLE,
  INDEX `tutuser` (`tutuser` ASC) VISIBLE,
  CONSTRAINT `learning_ibfk_1`
    FOREIGN KEY (`studuser`)
    REFERENCES `newdb`.`student` (`username`),
  CONSTRAINT `learning_ibfk_2`
    FOREIGN KEY (`tutuser`)
    REFERENCES `newdb`.`tutor` (`username`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `newdb`.`review`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `newdb`.`review` (
  `revid` INT NOT NULL AUTO_INCREMENT,
  `review` VARCHAR(100) NULL DEFAULT NULL,
  `tutuser` VARCHAR(100) NOT NULL,
  `studuser` VARCHAR(100) NOT NULL,
  `coursename` VARCHAR(100) NOT NULL,
  PRIMARY KEY (`revid`),
  INDEX `tutuser` (`tutuser` ASC) VISIBLE,
  INDEX `studuser` (`studuser` ASC) VISIBLE,
  CONSTRAINT `review_ibfk_1`
    FOREIGN KEY (`tutuser`)
    REFERENCES `newdb`.`tutor` (`username`),
  CONSTRAINT `review_ibfk_2`
    FOREIGN KEY (`studuser`)
    REFERENCES `newdb`.`student` (`username`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
