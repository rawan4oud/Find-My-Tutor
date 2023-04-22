-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema fmt
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema fmt
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `fmt` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `fmt` ;

-- -----------------------------------------------------
-- Table `fmt`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fmt`.`student` (
  `studentID` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NULL DEFAULT NULL,
  `last_name` VARCHAR(50) NULL DEFAULT NULL,
  `age` INT NULL DEFAULT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  `languages` VARCHAR(100) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `password` VARCHAR(100) NULL DEFAULT NULL,
  `country` VARCHAR(50) NULL DEFAULT NULL,
  `city` VARCHAR(50) NULL DEFAULT NULL,
  `usertype` VARCHAR(20) NULL DEFAULT NULL,
  PRIMARY KEY (`studentID`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fmt`.`tutor`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fmt`.`tutor` (
  `tutorID` INT NOT NULL,
  `first_name` VARCHAR(50) NULL DEFAULT NULL,
  `last_name` VARCHAR(50) NULL DEFAULT NULL,
  `age` INT NULL DEFAULT NULL,
  `gender` VARCHAR(10) NULL DEFAULT NULL,
  `email` VARCHAR(100) NULL DEFAULT NULL,
  `password` VARCHAR(100) NULL DEFAULT NULL,
  `country` VARCHAR(50) NULL DEFAULT NULL,
  `city` VARCHAR(50) NULL DEFAULT NULL,
  `languages` VARCHAR(100) NULL DEFAULT NULL,
  `bio` TEXT NULL DEFAULT NULL,
  `education_background` TEXT NULL DEFAULT NULL,
  `subjects` VARCHAR(100) NULL DEFAULT NULL,
  `pricing_policy` TEXT NULL DEFAULT NULL,
  `availability` TEXT NULL DEFAULT NULL,
  `review` VARCHAR(500) NULL DEFAULT NULL,
  PRIMARY KEY (`tutorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fmt`.`rating`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fmt`.`rating` (
  `ratingID` INT NOT NULL,
  `tutorID` INT NULL DEFAULT NULL,
  `studentID` INT NULL DEFAULT NULL,
  `bookingID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`ratingID`),
  INDEX `FK_rating_tutorID` (`tutorID` ASC) VISIBLE,
  INDEX `FK_rating_bookingID` (`bookingID` ASC) VISIBLE,
  INDEX `FK_rating_studentID` (`studentID` ASC) VISIBLE,
  CONSTRAINT `FK_rating_bookingID`
    FOREIGN KEY (`bookingID`)
    REFERENCES `fmt`.`booking` (`bookingID`),
  CONSTRAINT `FK_rating_studentID`
    FOREIGN KEY (`studentID`)
    REFERENCES `fmt`.`student` (`studentID`),
  CONSTRAINT `FK_rating_tutorID`
    FOREIGN KEY (`tutorID`)
    REFERENCES `fmt`.`tutor` (`tutorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fmt`.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fmt`.`booking` (
  `bookingID` INT NOT NULL,
  `studentID` INT NULL DEFAULT NULL,
  `tutorID` INT NULL DEFAULT NULL,
  PRIMARY KEY (`bookingID`),
  INDEX `FK_booking_tutorID` (`tutorID` ASC) VISIBLE,
  INDEX `FK_booking_studentID` (`studentID` ASC) VISIBLE,
  CONSTRAINT `FK_booking_bookingID`
    FOREIGN KEY (`bookingID`)
    REFERENCES `fmt`.`rating` (`bookingID`),
  CONSTRAINT `FK_booking_studentID`
    FOREIGN KEY (`studentID`)
    REFERENCES `fmt`.`student` (`studentID`),
  CONSTRAINT `FK_booking_tutorID`
    FOREIGN KEY (`tutorID`)
    REFERENCES `fmt`.`tutor` (`tutorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `fmt`.`learning`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `fmt`.`learning` (
  `studentID` INT NULL DEFAULT NULL,
  `tutorID` INT NULL DEFAULT NULL,
  INDEX `FK_learning_tutorID` (`tutorID` ASC) VISIBLE,
  INDEX `FK_learning_studentID` (`studentID` ASC) VISIBLE,
  CONSTRAINT `FK_learning_studentID`
    FOREIGN KEY (`studentID`)
    REFERENCES `fmt`.`student` (`studentID`),
  CONSTRAINT `FK_learning_tutorID`
    FOREIGN KEY (`tutorID`)
    REFERENCES `fmt`.`tutor` (`tutorID`))
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
