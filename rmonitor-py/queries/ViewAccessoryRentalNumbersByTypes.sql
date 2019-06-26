SELECT A.Name, A.AccessoryType, A.RentalNumber, R.Status, A.Price, A.Remarks
FROM Accessory A INNER JOIN Rental R
ON A.RentalNumber = R.RentalNumber
ORDER BY A.AccessoryType ASC