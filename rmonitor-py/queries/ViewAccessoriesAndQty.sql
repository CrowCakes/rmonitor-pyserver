SELECT Name, AccessoryType, COUNT(*)
FROM Accessory
GROUP BY Name, AccessoryType