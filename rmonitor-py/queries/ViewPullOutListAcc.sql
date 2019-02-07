SELECT B.RentalNumber, R.Status, A.Name, A.AccessoryType, A.Price
FROM PullOut O
INNER JOIN PullOutList B
ON (O.DeliveryID = B.DeliveryID AND O.FormNumber = B.FormNumber)
INNER JOIN Rental R
ON B.RentalNumber = R.RentalNumber
INNER JOIN Accessory A
ON R.RentalNumber = A.RentalNumber
WHERE O.DeliveryID = %(deliveryid)s AND 
O.FormNumber = %(formnumber)s
ORDER BY B.RentalNumber ASC