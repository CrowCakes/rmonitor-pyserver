DELETE FROM PullOutList
WHERE DeliveryID = %(deliveryid)s AND 
FormNumber = %(formnumber)s AND
RentalNumber = %(rentalnumber)s