UPDATE Rental
SET RentalNumber = %(rental_number)s
WHERE RentalNumber = %(old_rental)s;

UPDATE Accessory
SET Name = %(name)s,
AccessoryType = %(acctype)s,
Remarks = %(remarks)s,
Price = %(price)s
WHERE RentalNumber = %(rental_number)s;