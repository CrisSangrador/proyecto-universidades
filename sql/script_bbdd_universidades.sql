-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema universidades
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema universidades
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `universidades` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
USE `universidades` ;

-- -----------------------------------------------------
-- Table `universidades`.`países`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `universidades`.`países` (
  `idestado` INT NOT NULL AUTO_INCREMENT,
  `nombre_país` VARCHAR(45) NOT NULL,
  `nombre_provincia` VARCHAR(45) NOT NULL,
  `latitud` DECIMAL(10,7) NULL DEFAULT NULL,
  `longitud` DECIMAL(10,7) NULL DEFAULT NULL,
  PRIMARY KEY (`idestado`))
ENGINE = InnoDB
AUTO_INCREMENT = 54
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


-- -----------------------------------------------------
-- Table `universidades`.`universidades`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `universidades`.`universidades` (
  `id_universidad` INT NOT NULL AUTO_INCREMENT,
  `nombre_universidad` VARCHAR(100) NULL DEFAULT NULL,
  `pagina_web` VARCHAR(100) NULL DEFAULT NULL,
  `países_idestado` INT NOT NULL,
  PRIMARY KEY (`id_universidad`),
  INDEX `fk_universidades_países_idx` (`países_idestado` ASC) VISIBLE,
  CONSTRAINT `fk_universidades_países`
    FOREIGN KEY (`países_idestado`)
    REFERENCES `universidades`.`países` (`idestado`))
ENGINE = InnoDB
AUTO_INCREMENT = 2487
DEFAULT CHARACTER SET = utf8mb4
COLLATE = utf8mb4_0900_ai_ci;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
