INSERT INTO RentalList(DeliveryID, RentalNumber) VALUES
(%(deliveryid)s, %(rentalnumber)s);

UPDATE Rental
SET Status = "Rental"
WHERE RentalNumber = %(rentalnumber)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID in 
(SELECT R.PartID
FROM Computer C 
INNER JOIN PartList P
ON C.RentalNumber = P.RentalNumber AND P.RentalNumber = %(rentalnumber)s
INNER JOIN ParentList L
ON P.PartListID = L.ListID
INNER JOIN Parts R
ON L.PartID = R.PartID);