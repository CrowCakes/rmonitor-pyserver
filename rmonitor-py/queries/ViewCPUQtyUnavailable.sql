SELECT CPU, COUNT(*)
FROM Computer INNER JOIN Rental
ON Computer.RentalNumber = Rental.RentalNumber
WHERE Rental.Status = "Unavailable"
GROUP BY CPU
ORDER BY CPU ASC
