SELECT L.ListID, 1
FROM Computer C 
INNER JOIN PartList P 
ON C.RentalNumber = P.RentalNumber 
INNER JOIN ParentList L 
ON P.PartListID = L.ListID 
WHERE C.RentalNumber = %(rental_number)s