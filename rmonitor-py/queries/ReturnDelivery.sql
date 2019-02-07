UPDATE PullOut
SET Status = "Returned"
WHERE DeliveryID = %(deliveryid)s AND FormNumber = %(formnumber)s;

UPDATE Parts
SET Status = "On Hand"
WHERE PartID in 
(SELECT L.PartID
FROM PullOut O
INNER JOIN PullOutList A
ON (O.DeliveryID = A.DeliveryID AND O.FormNumber = A.FormNumber)
INNER JOIN Rental R
ON A.RentalNumber = R.RentalNumber
INNER JOIN Computer C
ON R.RentalNumber = C.RentalNumber
INNER JOIN PartList P
ON C.RentalNumber = P.RentalNumber
INNER JOIN ParentList L
ON P.PartListID = L.ListID
WHERE O.DeliveryID = %(deliveryid)s AND O.FormNumber = %(formnumber)s);

UPDATE Rental
SET Status = "On Hand"
WHERE RentalNumber in 
(SELECT L.RentalNumber
FROM PullOut O
INNER JOIN PullOutList L
ON (O.DeliveryID = L.DeliveryID AND O.FormNumber = L.FormNumber)
WHERE O.DeliveryID = %(deliveryid)s AND O.FormNumber = %(formnumber)s);

UPDATE SmallAccessory AS A INNER JOIN PullOutPeripheral AS B
ON A.Name = B.Name
SET A.QuantityMinus = A.QuantityMinus - B.Quantity
WHERE B.DeliveryID = %(deliveryid)s AND 
B.FormNumber = %(formnumber)s AND 
A.Name = B.Name;
