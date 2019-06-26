SELECT R.*, A.Name, A.AccessoryType, A.Remarks, A.Price
FROM Rental R, Accessory A
WHERE R.Status = "On Hand" AND R.RentalNumber = A.RentalNumber
ORDER BY R.RentalNumber