INSERT INTO RentalList(DeliveryID, RentalNumber) 
VALUES (%(deliveryid)s, %(rentalnumber)s);

UPDATE Rental
SET Status = "Unavailable"
WHERE RentalNumber = %(rentalnumber)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID in 
(SELECT L.PartID
FROM Computer C 
INNER JOIN PartList P
ON C.RentalNumber = P.RentalNumber
INNER JOIN ParentList L
ON P.PartListID = L.ListID
WHERE P.RentalNumber = %(rentalnumber)s);