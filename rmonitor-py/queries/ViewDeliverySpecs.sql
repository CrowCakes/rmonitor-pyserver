SELECT D.DeliveryID, L.RentalNumber, C.CPU, C.PCType, C.OS, R.Name, R.PartType
FROM Delivery D
INNER JOIN RentalList L
ON D.DeliveryID = L.DeliveryID
INNER JOIN Rental B
ON L.RentalNumber = B.RentalNumber
INNER JOIN Computer C
ON B.RentalNumber = C.RentalNumber
INNER JOIN PartList P
ON C.RentalNumber = P.RentalNumber
INNER JOIN ParentList A
ON P.PartListID = A.ListID
INNER JOIN Parts R
ON A.PartID = R.PartID
WHERE B.Status <> "Deleted"
ORDER BY D.DeliveryID ASC, L.RentalNumber ASC