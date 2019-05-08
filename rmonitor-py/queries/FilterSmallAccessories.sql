SELECT *
FROM SmallAccessory
WHERE Name REGEXP %(partid)s
ORDER BY Name