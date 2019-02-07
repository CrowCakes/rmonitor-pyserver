SELECT R.*
FROM Computer C 
INNER JOIN Original O
ON C.RentalNumber = O.RentalNumber
INNER JOIN OriginalList P
ON O.OriginalID = P.OriginalID
INNER JOIN ParentList L
ON P.OriginalListID = L.ListID
INNER JOIN Parts R
ON L.PartID = R.PartID
WHERE C.RentalNumber = %(rentalnumber)s
ORDER BY R.PartID