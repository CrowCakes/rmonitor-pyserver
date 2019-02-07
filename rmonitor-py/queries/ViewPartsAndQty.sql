SELECT Name, PartType, COUNT(*)
FROM Parts
GROUP BY Name, PartType