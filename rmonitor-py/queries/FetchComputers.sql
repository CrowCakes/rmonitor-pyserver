SELECT L.RentalNumber, 1
FROM Delivery D
INNER JOIN RentalList L
ON D.DeliveryID = L.DeliveryID
INNER JOIN Rental R
ON L.RentalNumber = R.RentalNumber
WHERE D.DeliveryID = %(deliveryid)s AND R.Status <> "Deleted"