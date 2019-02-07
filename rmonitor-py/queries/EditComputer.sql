UPDATE Rental
SET RentalNumber = %(rental_number)s
WHERE RentalNumber = %(old_rental)s;

UPDATE Computer
SET CPU = %(cpu)s,
PCType = %(pctype)s,
OS = %(os)s, 
PurchaseDate = %(purchasedate)s,
IsUpgraded = %(up_status)s,
Description = %(description)s,
Price = %(price)s
WHERE RentalNumber = %(rental_number)s;

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid1)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid2)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid3)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid4)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid5)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid6)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid7)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid8)s
);

UPDATE Parts
SET Status = "On Hand"
WHERE PartID IN (
SELECT PartID
FROM ParentList
WHERE ListID = %(listid9)s
);

UPDATE ParentList
SET PartID = %(part1)s
WHERE ListID = %(listid1)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part1)s;

UPDATE ParentList
SET PartID = %(part2)s
WHERE ListID = %(listid2)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part2)s;

UPDATE ParentList
SET PartID = %(part3)s
WHERE ListID = %(listid3)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part3)s;

UPDATE ParentList
SET PartID = %(part4)s
WHERE ListID = %(listid4)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part4)s;

UPDATE ParentList
SET PartID = %(part5)s
WHERE ListID = %(listid5)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part5)s;

UPDATE ParentList
SET PartID = %(part6)s
WHERE ListID = %(listid6)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part6)s;

UPDATE ParentList
SET PartID = %(part7)s
WHERE ListID = %(listid7)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part7)s;

UPDATE ParentList
SET PartID = %(part8)s
WHERE ListID = %(listid8)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part8)s;

UPDATE ParentList
SET PartID = %(part9)s
WHERE ListID = %(listid9)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part9)s;