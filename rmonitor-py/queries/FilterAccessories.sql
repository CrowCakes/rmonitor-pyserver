SELECT A.Name, A.AccessoryType, A.RentalNumber, R.Status, A.Price, A.Remarks
FROM Accessory A INNER JOIN Rental R
ON A.RentalNumber = R.RentalNumber
WHERE A.RentalNumber REGEXP %(rentalnumber)s
ORDER BY A.AccessoryType ASC