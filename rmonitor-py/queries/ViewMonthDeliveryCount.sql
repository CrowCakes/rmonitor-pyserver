SELECT MONTH(ReleaseDate), YEAR(ReleaseDate), COUNT(*)
FROM Delivery
GROUP BY MONTH(ReleaseDate), YEAR(ReleaseDate)
ORDER BY YEAR(ReleaseDate) ASC, MONTH(ReleaseDate) ASC