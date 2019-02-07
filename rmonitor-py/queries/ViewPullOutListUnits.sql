SELECT B.RentalNumber, R.PartID, C.Price
FROM PullOut O
INNER JOIN PullOutList B 
on (O.DeliveryID = B.DeliveryID AND O.FormNumber = B.FormNumber)
INNER JOIN Rental A 
on B.RentalNumber = A.RentalNumber
INNER JOIN Computer C  
ON A.RentalNumber = C.RentalNumber
INNER JOIN PartList P 
ON C.RentalNumber = P.RentalNumber 
INNER JOIN ParentList L 
ON P.PartListID = L.ListID 
INNER JOIN Parts R 
ON L.PartID = R.PartID
WHERE O.DeliveryID = %(deliveryid)s AND O.FormNumber = %(formnumber)s
ORDER BY B.RentalNumber, R.PartID ASC