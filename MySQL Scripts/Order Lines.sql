CREATE TABLE `WMS`.`_orderLines` (
	`OrderLineID` BIGINT NOT NULL AUTO_INCREMENT,
	`OrderID` BIGINT NOT NULL,
	`ProductID` BIGINT NOT NULL,
	`QTY` BIGINT NOT NULL,
  PRIMARY KEY (`OrderLineID`),
  FOREIGN KEY (`ProductID`) REFERENCES `_product`(`ProductID`),
  FOREIGN KEY (`OrderID`) REFERENCES `_order`(`OrderID`));
