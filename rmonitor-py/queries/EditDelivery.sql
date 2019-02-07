UPDATE Delivery
SET SalesOrder = %(so)s,
SalesInvoice = %(si)s,
ARD = %(ard)s,
POS = %(pos)s,
CustomerID = %(clientid)s,
ReleaseDate = %(releasedate)s,
DueDate = %(duedate)s,
AccountManager = %(am)s,
Status = %(status)s,
ExtensionID = %(extension)s,
Frequency = %(frequency)s
WHERE DeliveryID = %(deliveryid)s;

UPDATE Parts
SET Status = "On Hand"
WHERE PartID in 
(SELECT L.PartID
FROM RentalList A
INNER JOIN Rental R
ON A.RentalNumber = R.RentalNumber
INNER JOIN Computer C
ON R.RentalNumber = C.RentalNumber
INNER JOIN PartList P
ON C.RentalNumber = P.RentalNumber
INNER JOIN ParentList L
ON P.PartListID = L.ListID
WHERE A.DeliveryID = %(deliveryid)s);

UPDATE Rental
SET Status = "On Hand"
WHERE RentalNumber in 
(SELECT RentalNumber
FROM RentalList
WHERE DeliveryID = %(deliveryid)s);

DELETE FROM RentalList
WHERE DeliveryID = %(deliveryid)s;

UPDATE SmallAccessory INNER JOIN Peripheral 
ON SmallAccessory.Name = Peripheral.Name
SET SmallAccessory.QuantityMinus = SmallAccessory.QuantityMinus - Peripheral.Quantity
WHERE Peripheral.DeliveryID = %(deliveryid)s AND
SmallAccessory.Name = Peripheral.Name;

DELETE FROM Peripheral
WHERE DeliveryID = %(deliveryid)s;
