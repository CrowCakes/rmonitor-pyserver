SELECT Computer.RentalNumber, 1
FROM 
Computer INNER JOIN PartList 
ON Computer.RentalNumber = PartList.RentalNumber
INNER JOIN ParentList 
ON PartList.PartListID = ParentList.ListID
WHERE PartID = %(partid)s
LIMIT 1