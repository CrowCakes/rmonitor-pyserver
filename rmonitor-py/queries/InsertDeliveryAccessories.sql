INSERT INTO RentalList(DeliveryID, RentalNumber) 
VALUES (%(deliveryid)s, %(rentalnumber)s);

UPDATE Rental
SET Status = "Rental"
WHERE RentalNumber = %(rentalnumber)s;