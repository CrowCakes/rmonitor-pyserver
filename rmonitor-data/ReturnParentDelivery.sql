DELIMITER //
CREATE PROCEDURE return_parent_delivery
(IN delv int)
BEGIN
	DECLARE ext int;
	DECLARE new_delv int;
	
	UPDATE Delivery
	SET Status = "Returned"
	WHERE DeliveryID = delv;
	
	SET ext = 0;
	
	SELECT DeliveryID INTO ext
	FROM Delivery
	WHERE ExtensionID = delv;
	
	WHILE (ext <> 0) DO
		UPDATE Delivery 
		SET Status = 'Returned' 
		WHERE DeliveryID = ext;
		
		SET new_delv = ext;
		
		SELECT DeliveryID INTO ext
		FROM Delivery
		WHERE ExtensionID = new_delv;
	END WHILE;
END //
DELIMITER ;