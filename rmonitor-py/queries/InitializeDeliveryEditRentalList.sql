UPDATE Parts
SET Status = "On Hand"
WHERE PartID in 
(SELECT L.PartID
FROM RentalList A
INNER JOIN Rental R
ON A.RentalNumber = R.RentalNumber
INNER JOIN Computer C
ON R.RentalNumber = C.RentalNumber
INNER JOIN PartList P
ON C.RentalNumber = P.RentalNumber
INNER JOIN ParentList L
ON P.PartListID = L.ListID
WHERE A.DeliveryID = %(deliveryid)s);

UPDATE Rental
SET Status = "On Hand"
WHERE RentalNumber in 
(SELECT RentalNumber
FROM RentalList
WHERE DeliveryID = %(deliveryid)s);

DELETE FROM RentalList
WHERE DeliveryID = %(deliveryid)s;