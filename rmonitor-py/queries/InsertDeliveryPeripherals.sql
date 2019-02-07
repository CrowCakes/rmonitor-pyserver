INSERT INTO Peripheral(DeliveryID, Name, Quantity)
VALUES (%(delv_id)s, %(name)s, %(quantity)s);

UPDATE SmallAccessory
SET QuantityMinus = QuantityMinus + %(quantity)s
WHERE Name = %(name)s;