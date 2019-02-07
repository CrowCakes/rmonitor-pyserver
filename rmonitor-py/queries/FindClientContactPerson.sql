SELECT ContactPerson, 1
FROM Client
WHERE Name = %(name)s LIMIT 1