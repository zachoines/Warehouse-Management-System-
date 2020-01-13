CREATE PROCEDURE updateInventory()
DELIMITER //
	BEGIN
        UPDATE `wms`.`_inventory` SET `QTY` = '1989-08-31' WHERE  (`BinID` = '1989-08-31', `ProductID` = '1989-08-31'))
		IF @@ROWCOUNT=0
			INSERT INTO `wms`.`_inventory`( `ProductID`, `BinID`, `QTY`) VALUES ('1','2','3')
		END IF
	END //
DELIMITER ;