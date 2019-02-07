SELECT Name, Quantity
FROM PullOutPeripheral
WHERE DeliveryID = %(deliveryid)s AND FormNumber = %(formnumber)s