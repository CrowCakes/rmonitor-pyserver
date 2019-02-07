SELECT ClientID, 1
FROM Client
WHERE Name LIKE %(name)s
LIMIT 1