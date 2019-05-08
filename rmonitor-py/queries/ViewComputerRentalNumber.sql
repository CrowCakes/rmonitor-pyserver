SELECT C.RentalNumber, A.Status, C.CPU, 
C.PCType, C.OS, C.PurchaseDate, C.IsUpgraded, C.Description, C.Price,
R.PartID, R.Name, R.PartType, R.Price
FROM Rental A INNER JOIN Computer C  
ON A.RentalNumber = C.RentalNumber
INNER JOIN PartList P 
ON C.RentalNumber = P.RentalNumber 
INNER JOIN ParentList L 
ON P.PartListID = L.ListID 
INNER JOIN Parts R 
ON L.PartID = R.PartID
WHERE C.RentalNumber REGEXP %(rentalnumber)s
ORDER BY C.RentalNumber, R.PartID ASC
