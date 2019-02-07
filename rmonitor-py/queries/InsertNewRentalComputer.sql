INSERT INTO Rental(RentalNumber, Status) VALUES (%(rental_number)s, "On Hand");

INSERT INTO Computer(RentalNumber, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price) 
VALUES (%(rental_number)s, %(cpu)s, %(pctype)s, %(os)s, %(purchasedate)s, %(status)s, %(description)s, %(price)s);

INSERT INTO Original(RentalNumber) VALUES (%(rental_number)s);
SET @last_id_original := LAST_INSERT_ID();

/* partid goes to the insert query directly below */
INSERT INTO ParentList(PartID) VALUES (%(part1)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part2)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part3)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part4)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part5)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part6)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part7)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part8)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

INSERT INTO ParentList(PartID) VALUES (%(part9)s);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, %(rental_number)s);

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part1)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part2)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part3)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part4)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part5)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part6)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part7)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part8)s;

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = %(part9)s;