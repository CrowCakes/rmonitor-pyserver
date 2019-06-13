/*UPDATE Delivery
SET Status = "Returned"
WHERE DeliveryID = %(deliveryid)s*/

CALL return_parent_delivery(%(deliveryid)s)