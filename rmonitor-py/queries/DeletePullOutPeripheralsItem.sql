DELETE FROM PullOutPeripheral
WHERE DeliveryID = %(deliveryid)s AND 
FormNumber = %(formnumber)s AND
Name = %(name)s