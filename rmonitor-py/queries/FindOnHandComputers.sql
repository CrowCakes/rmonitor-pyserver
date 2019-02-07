SELECT R.*, C.CPU, C.PCType, C.OS, C.PurchaseDate, C.IsUpgraded, C.Description, C.Price
FROM Rental R INNER JOIN Computer C
ON R.RentalNumber = C.RentalNumber
WHERE R.Status = "On Hand"
ORDER BY R.RentalNumber ASC