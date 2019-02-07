SELECT DeliveryID, FormNumber,
	RentalNumber
FROM PullOutList
WHERE DeliveryID = %(deliveryid)s AND 
FormNumber = %(formnumber)s