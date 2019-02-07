SELECT A.Name, A.AccessoryType, A.RentalNumber, R.Status, A.Price
FROM Accessory A INNER JOIN Rental R
ON A.RentalNumber = R.RentalNumber
WHERE A.RentalNumber LIKE %(rentalnumber)s
ORDER BY A.AccessoryType ASC