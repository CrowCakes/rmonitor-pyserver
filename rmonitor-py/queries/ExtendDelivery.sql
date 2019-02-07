SET @olddeliveryid = <something>;
SET @newdeliveryid = <something>;
SET @so = <something>;
SET @si = <something>;
SET @ard = <something>;
SET @pos = <something>;
SET @customerid = <something>;
SET @releasedate = <something>;
SET @duedate = <something>;
SET @am = <something>;

INSERT INTO Delivery
		VALUES (@newdeliveryid, @so, @si,
		@ard, @pos, @customer, @releasedate,
		@duedate, @am, "Active",
		NULL);
		
UPDATE Delivery
SET ExtensionID = @newdeliveryid
WHERE DeliveryID = @olddeliveryid;