SELECT R.RentalNumber, R.Status, A.Name, A.AccessoryType, A.Price
FROM Delivery D
INNER JOIN RentalList L
ON D.DeliveryID = L.DeliveryID
INNER JOIN Rental R
ON L.RentalNumber = R.RentalNumber
INNER JOIN Accessory A
ON R.RentalNumber = A.RentalNumber
WHERE D.DeliveryID = %(deliveryid)s AND R.Status = "Pending"
ORDER BY R.RentalNumber ASC