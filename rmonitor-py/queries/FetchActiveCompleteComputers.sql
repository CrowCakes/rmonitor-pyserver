SELECT L.RentalNumber, B.PartID, C.Price
FROM Delivery D
INNER JOIN RentalList L
ON D.DeliveryID = L.DeliveryID
INNER JOIN Rental R
ON L.RentalNumber = R.RentalNumber
INNER JOIN Computer C
ON R.RentalNumber = C.RentalNumber
INNER JOIN PartList P 
ON C.RentalNumber = P.RentalNumber 
INNER JOIN ParentList A 
ON P.PartListID = A.ListID 
INNER JOIN Parts B 
ON A.PartID = B.PartID
WHERE D.DeliveryID = %(deliveryid)s AND R.Status = "Rental"
ORDER BY L.RentalNumber, B.PartID ASC
