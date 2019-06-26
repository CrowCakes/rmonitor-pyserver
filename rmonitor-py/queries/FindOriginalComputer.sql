SELECT A.*, C.CPU, C.PCType, C.OS, C.PurchaseDate, C.IsUpgraded, C.Description, C.Price
FROM Rental A 
INNER JOIN Computer C 
ON A.RentalNumber = C.RentalNumber 
INNER JOIN Original P 
ON C.RentalNumber = P.RentalNumber 
INNER JOIN OriginalList O
ON P.OriginalID = O.OriginalID
INNER JOIN ParentList L 
ON O.OriginalListID = L.ListID 
INNER JOIN Parts R 
ON L.PartID = R.PartID
WHERE R.PartID = %(partid)s