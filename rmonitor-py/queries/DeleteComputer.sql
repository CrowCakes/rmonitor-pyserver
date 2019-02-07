UPDATE Rental
SET Status = "Deleted"
WHERE RentalNumber = %(rental_number)s;

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList INNER JOIN PartList
ON ParentList.ListID = PartList.PartListID
WHERE RentalNumber = %(rental_number)s
);