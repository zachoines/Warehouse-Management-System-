CREATE TABLE `WMS`.`_order` (
	`OrderID` BIGINT NULL AUTO_INCREMENT,
	`OrderNumber` VARCHAR(45) NULL unique,
	`DateOrdered` DATETIME,
	`CustomerName` VARCHAR(45) NULL,
	`CustomerAddress` VARCHAR(45) NULL,
  PRIMARY KEY (`OrderID`));