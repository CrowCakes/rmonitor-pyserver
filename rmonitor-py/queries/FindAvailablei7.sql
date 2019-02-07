SELECT R.*, C.CPU, C.PCType, C.OS, C.PurchaseDate, C.IsUpgraded, C.Description, C.Price
FROM Rental R, Computer C
WHERE R.Status = "On Hand" AND C.CPU = "i7" AND R.RentalNumber = C.RentalNumber
ORDER BY R.RentalNumber ASC