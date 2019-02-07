INSERT INTO RentalList(DeliveryID, RentalNumber) 
VALUES (%(deliveryid)s, %(rentalnumber)s);

UPDATE Rental
SET Status = "Unavailable"
WHERE RentalNumber = %(rentalnumber)s;