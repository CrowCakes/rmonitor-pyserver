SELECT DISTINCT R.*, C.CPU, C.PCType, C.OS, C.PurchaseDate, C.IsUpgraded, C.Description, C.Price
FROM Delivery D
INNER JOIN RentalList L
ON D.DeliveryID = L.DeliveryID
INNER JOIN Rental R
ON L.RentalNumber = R.RentalNumber
INNER JOIN Computer C
ON R.RentalNumber = C.RentalNumber
WHERE D.DueDate < %(date)s AND D.Status <> "Returned" AND D.ExtensionID is NULL
ORDER BY R.RentalNumber ASC