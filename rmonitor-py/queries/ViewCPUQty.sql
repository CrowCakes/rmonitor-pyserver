SELECT CPU, COUNT(*)
FROM Computer INNER JOIN Rental
ON Computer.RentalNumber = Rental.RentalNumber
WHERE Rental.Status = "On Hand"
GROUP BY CPU
ORDER BY CPU ASC
