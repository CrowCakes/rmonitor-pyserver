SELECT * FROM
(SELECT A.DeliveryID, B.DeliveryID
FROM Delivery A, Delivery B
WHERE A.ExtensionID = B.Delivery
ORDER BY A.DeliveryID ASC
LIMIT 1)
UNION
SELECT * FROM
(SELECT A.DeliveryID, B.DeliveryID
FROM Delivery A, Delivery B
WHERE A.ExtensionID = B.Delivery
ORDER BY A.DeliveryID DESC
LIMIT 1);