UPDATE SmallAccessory
SET Name = %(name)s,
AccessoryType = %(type)s,
Price = %(price)s,
Quantity = %(quantity)s,
QuantityMinus = %(minus)s
WHERE Name = %(old_name)s and AccessoryType = %(old_type)s