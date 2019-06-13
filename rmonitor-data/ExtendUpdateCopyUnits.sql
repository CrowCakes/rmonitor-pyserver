delimiter //
 
CREATE TRIGGER extend_update_copyunits 
BEFORE UPDATE ON Delivery
FOR EACH ROW
BEGIN
	IF NEW.ExtensionID <> 0 AND OLD.ExtensionID = 0 THEN
		INSERT INTO RentalList(DeliveryID, RentalNumber) 
		SELECT NEW.ExtensionID, RentalNumber 
		FROM RentalList 
		WHERE DeliveryID = OLD.DeliveryID;
	END IF;
END;//
 
delimiter ;