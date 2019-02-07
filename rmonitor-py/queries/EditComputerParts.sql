UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid)s
);

UPDATE ParentList
SET PartID = %(part)s
WHERE ListID = %(listid)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part)s