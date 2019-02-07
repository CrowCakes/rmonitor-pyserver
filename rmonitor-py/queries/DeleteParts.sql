UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(partid)s;