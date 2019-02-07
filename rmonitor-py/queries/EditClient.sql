UPDATE Client
SET Name = %(name)s,
Address = %(address)s,
ContactPerson = %(contactp)s,
ContactNumber = %(contactn)s
WHERE Name = %(old_name)s