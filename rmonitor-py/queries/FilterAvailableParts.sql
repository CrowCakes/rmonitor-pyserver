SELECT *
FROM Parts
WHERE CAST(PartID as CHAR) LIKE %(partid)s AND Status = "On Hand"
ORDER BY PartID ASC