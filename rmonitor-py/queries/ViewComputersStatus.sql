SELECT C.RentalNumber, R.Status
FROM Computer C INNER JOIN Rental R
ON C.RentalNumber = R.RentalNumber
ORDER BY C.RentalNumber ASC