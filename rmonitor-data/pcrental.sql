DROP DATABASE IF EXISTS PCRental;

CREATE DATABASE PCRental;
USE PCRental;

CREATE TABLE Login (
	Username varchar(50) PRIMARY KEY,
	Password char(128),
	Salt char(76),
	Role varchar(20)
);

CREATE TABLE LoginStatus (
	Username varchar(50),
	
	FOREIGN KEY (Username) REFERENCES Login(Username)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

INSERT INTO Login
VALUES ("user", 
"17ebd78d536492e5048df5139a11ecb67ef6907b5a944764b1cc69a46b6dce5e0b1c1f7ef39a9fb315a2df5e6b9606329b70db925c6863701424d616038637ec", 
"lVj+4IzTIIQGIr6RlZNZLc4Wpe+TxndU7of3CLRWZXM=", 
"Admin");

INSERT INTO Login
VALUES ("viewer", 
"0c9b9ccfb6bea1fe39eff7190236a0453a48d0a8e252c83e06cd7c9216ecd79e00aba52cb74e32a2f73d0f6bafa1483872a70cfa47962d96985a47ab3da58423", 
"B6pCsF5PJn+QfCB9QulnR+QA88z0Gkkjp9MBTJ2m6E8=", 
"Viewer");

INSERT INTO Login
VALUES ("report",
"7db4545978298cdca3cb44297c4e447421868ee04313b373e65a925b7468e2fe7bf1b04ac40fc552c891b10f7a41b92da641560f54cec8ea304bbb684fa265e5", 
"QTgPIPg73QLEmyMhT36v9/pLuxyyg2AJLrfK/EdfbiA=", 
"Reports");

INSERT INTO Login
VALUES ("root", 
"f9c191e3d837d390c1c91192f2542227103333fe43ba239849f141dede9efcf1df2f87833c4d967f3e9621caf75d89535104864fa7b4f5bb97b2986155ce319c", 
"qA3MXL+gX4fVNwIQWoWfYDqttIDiV/PSEBWTJC8kldo=", 
"Super");

CREATE TABLE Client (
	ClientID int AUTO_INCREMENT PRIMARY KEY,
	Name varchar(100),
	Address varchar(255),
	ContactPerson varchar(30),
	ContactNumber int
);

CREATE TABLE Parts (
	PartID int AUTO_INCREMENT PRIMARY KEY,
	Name varchar(100),
	PartType varchar(20),
	Status varchar(20),
	Price float
);

CREATE TABLE Rental (
	RentalNumber varchar(30) PRIMARY KEY,
	Status varchar(20)
);

CREATE TABLE ParentList (
	ListID int AUTO_INCREMENT PRIMARY KEY,
	PartID int,
	
	FOREIGN KEY (PartID) REFERENCES Parts (PartID)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE PartList (
	PartListID int PRIMARY KEY,
	RentalNumber varchar(30),
	
	FOREIGN KEY (PartListID) REFERENCES ParentList (ListID)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	FOREIGN KEY (RentalNumber) REFERENCES Rental (RentalNumber)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE Accessory (
	RentalNumber varchar(30) PRIMARY KEY,
	Name varchar(100),
	AccessoryType varchar(50),
	Price float,
	
	FOREIGN KEY (RentalNumber) REFERENCES Rental (RentalNumber)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE TABLE SmallAccessory (
	Name varchar(100) NOT NULL PRIMARY KEY,
	AccessoryType varchar(50),
	Price float,
	Quantity int,
	QuantityMinus int
);


CREATE TABLE Computer (
	RentalNumber varchar(30) PRIMARY KEY,
	CPU varchar(10),
	PCType varchar(10),
	OS varchar(30),
	PurchaseDate date,
	Description varchar(1000),
	Price float,

	IsUpgraded boolean,
	
	FOREIGN KEY (RentalNumber) REFERENCES Rental (RentalNumber)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE TABLE Original (
	OriginalID int AUTO_INCREMENT PRIMARY KEY,
	RentalNumber varchar(30),
	
	FOREIGN KEY (RentalNumber) REFERENCES Rental (RentalNumber)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE TABLE OriginalList (
	OriginalListID int,
	OriginalID int,
	
	FOREIGN KEY (OriginalListID) REFERENCES ParentList (ListID)
	ON UPDATE CASCADE
	ON DELETE CASCADE,
	FOREIGN KEY (OriginalID) REFERENCES Original (OriginalID)
	ON UPDATE CASCADE
	ON DELETE CASCADE
);

CREATE TABLE Delivery (
	DeliveryID int AUTO_INCREMENT PRIMARY KEY,
	SalesOrder varchar(30),
	SalesInvoice varchar(30),
	ARD varchar(30),
	POS varchar(30),
	CustomerID int,
	ReleaseDate date,
	DueDate date,
	AccountManager varchar(10),
	Status varchar(20),
	ExtensionID int DEFAULT NULL,
	Comments varchar(255),
	Frequency int,
	
	FOREIGN KEY (CustomerID) REFERENCES Client (ClientID)
	ON UPDATE CASCADE,
	FOREIGN KEY (ExtensionID) REFERENCES Delivery (DeliveryID)
	ON UPDATE CASCADE
);

CREATE TABLE RentalList (
	ListId int AUTO_INCREMENT PRIMARY KEY,
	DeliveryID int,
	RentalNumber varchar(30),
	
	FOREIGN KEY (DeliveryID) REFERENCES Delivery (DeliveryID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE,
	FOREIGN KEY (RentalNumber) REFERENCES Rental (RentalNumber)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);
ALTER TABLE RentalList ADD UNIQUE OneComputerOnly(DeliveryID, RentalNumber);

CREATE TABLE Peripheral (
	ListId int AUTO_INCREMENT PRIMARY KEY,
	DeliveryID int,
	Name varchar(100) NOT NULL,
	Quantity int,
	
	FOREIGN KEY (DeliveryID) REFERENCES Delivery (DeliveryID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE,
	FOREIGN KEY (Name) REFERENCES SmallAccessory (Name)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE TABLE PullOut (
	ListId int AUTO_INCREMENT PRIMARY KEY,
	DeliveryID int,
	FormNumber varchar(20),
	DateCreated date,
	Status varchar(20),
	
	FOREIGN KEY (DeliveryID) REFERENCES Delivery (DeliveryID)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE INDEX pullout ON PullOut(DeliveryID, FormNumber);

CREATE TABLE PullOutList (
	ListId int AUTO_INCREMENT PRIMARY KEY,
	DeliveryID int,
	FormNumber varchar(20),
	RentalNumber varchar(30),
	
	FOREIGN KEY (DeliveryID, FormNumber) REFERENCES PullOut (DeliveryID, FormNumber)
	ON UPDATE CASCADE 
	ON DELETE CASCADE,
	FOREIGN KEY (RentalNumber) REFERENCES Rental (RentalNumber)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

CREATE TABLE PullOutPeripheral (
	ListId int AUTO_INCREMENT PRIMARY KEY,
	DeliveryID int,
	FormNumber varchar(20),
	Name varchar(100),
	Quantity int,
	
	FOREIGN KEY (DeliveryID, FormNumber) REFERENCES PullOut (DeliveryID, FormNumber)
	ON UPDATE CASCADE 
	ON DELETE CASCADE,
	FOREIGN KEY (Name) REFERENCES Peripheral (Name)
	ON UPDATE CASCADE 
	ON DELETE CASCADE
);

INSERT INTO Client(Name, Address, ContactPerson, ContactNumber) 
VALUES ("Test Company 1","Test Address 1","Test Contact 1",1234567);
INSERT INTO Client(Name, Address, ContactPerson, ContactNumber) 
VALUES ("Test Company 2","Test Address 2","Test Contact 2",1234568);

INSERT INTO Parts(Name, PartType, Status) VALUES ("N/A", "N/A", "N/A");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 1", "HDD", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 2", "HDD", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 3", "HDD", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 4", "Memory", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 5", "Memory", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 6", "Memory", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 7", "Processor", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 8", "Processor", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 9", "Processor", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 10", "Motherboard", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 11", "Motherboard", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 12", "Motherboard", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 13", "Test Part A", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 14", "Test Part A", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 15", "Test Part A", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 16", "Test Part B", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 17", "Test Part B", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 18", "Test Part B", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 19", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 20", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 21", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 22", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 23", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 24", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 25", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 26", "Test Part C", "On Hand");
INSERT INTO Parts(Name, PartType, Status) VALUES ("Test Part 27", "Test Part C", "On Hand");

/* First sample rental unit */
INSERT INTO Rental(RentalNumber, Status) VALUES ("ABC-012345", "On Hand");
INSERT INTO Computer(RentalNumber, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price) 
VALUES ("ABC-012345", "i7", "Computer", "Windows 10", '2015-01-01', FALSE, '', 0);
INSERT INTO Original(RentalNumber) VALUES ("ABC-012345");
SET @last_id_original := LAST_INSERT_ID();

INSERT INTO ParentList(PartID) VALUES (2);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 2;

INSERT INTO ParentList(PartID) VALUES (5);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 5;

INSERT INTO ParentList(PartID) VALUES (8);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 8;

INSERT INTO ParentList(PartID) VALUES (11);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 11;

INSERT INTO ParentList(PartID) VALUES (14);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 14;

INSERT INTO ParentList(PartID) VALUES (17);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 17;

INSERT INTO ParentList(PartID) VALUES (20);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 20;

INSERT INTO ParentList(PartID) VALUES (23);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 23;

INSERT INTO ParentList(PartID) VALUES (26);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012345");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 26;

/* Second sample rental unit */
INSERT INTO Rental(RentalNumber, Status) VALUES ("ABC-012346", "On Hand");
INSERT INTO Computer(RentalNumber, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price) 
VALUES ("ABC-012346", "i7", "Computer", "Windows 10", "2015-01-01", FALSE, '', 0);
INSERT INTO Original(RentalNumber) VALUES ("ABC-012346");
SET @last_id_original := LAST_INSERT_ID();

INSERT INTO ParentList(PartID) VALUES (3);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 3;

INSERT INTO ParentList(PartID) VALUES (6);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 6;

INSERT INTO ParentList(PartID) VALUES (9);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 9;

INSERT INTO ParentList(PartID) VALUES (12);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 12;

INSERT INTO ParentList(PartID) VALUES (15);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 15;

INSERT INTO ParentList(PartID) VALUES (18);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 18;

INSERT INTO ParentList(PartID) VALUES (21);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 21;

INSERT INTO ParentList(PartID) VALUES (24);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 24;

INSERT INTO ParentList(PartID) VALUES (27);
SET @last_id_list := LAST_INSERT_ID();
INSERT INTO OriginalList VALUES (@last_id_list, @last_id_original);
INSERT INTO PartList VALUES (@last_id_list, "ABC-012346");

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID = 27;

/* test accesories */

INSERT INTO Rental VALUES ("001", "On Hand");
INSERT INTO Accessory VALUES ("001", "Test Accessory 1", "Mouse", 0);

INSERT INTO Rental VALUES ("002", "On Hand");
INSERT INTO Accessory VALUES ("002", "Test Accessory 2", "Mouse", 0);

INSERT INTO Rental VALUES ("003", "On Hand");
INSERT INTO Accessory VALUES ("003", "Test Accessory 3", "Mouse", 0);

INSERT INTO Rental VALUES ("004", "On Hand");
INSERT INTO Accessory VALUES ("004", "Test Accessory 4", "Keyboard", 0);

INSERT INTO Rental VALUES ("005", "On Hand");
INSERT INTO Accessory VALUES ("005", "Test Accessory 5", "Keyboard", 0);

INSERT INTO Rental VALUES ("006", "On Hand");
INSERT INTO Accessory VALUES ("006", "Test Accessory 6", "Keyboard", 0);

/* Sample deliveries */
INSERT INTO Delivery(SalesOrder, SalesInvoice,
ARD, POS, CustomerID, ReleaseDate, DueDate,
AccountManager, Status, ExtensionID, Comments, Frequency) VALUES 
(NULL,NULL,NULL,NULL,1,'2018-06-15','2018-11-30',"ABC","Active",NULL,NULL,30);

INSERT INTO RentalList(DeliveryID, RentalNumber) VALUES
(1, "ABC-012345");

UPDATE Rental
SET Status = "Unavailable"
WHERE RentalNumber = "ABC-012345";

UPDATE Parts
SET Status = "Unavailable"
WHERE PartID in 
(SELECT L.PartID
FROM Computer C 
INNER JOIN PartList P
ON C.RentalNumber = P.RentalNumber AND P.RentalNumber = "ABC-012345"
INNER JOIN ParentList L
ON P.PartListID = L.ListID);
