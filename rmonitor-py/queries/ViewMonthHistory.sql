SELECT D.DeliveryID, C.Name, D.SalesOrder, 
D.SalesInvoice, D.ARD, D.POS, 
D.ReleaseDate, D.DueDate, D.AccountManager, 
D.Status, D.ExtensionID, D.Frequency
FROM Delivery D INNER JOIN Client C
ON D.CustomerID = C.ClientID
WHERE MONTH(D.ReleaseDate) = %(month)s AND YEAR(D.ReleaseDate) = %(year)s
ORDER BY YEAR(D.ReleaseDate) ASC, MONTH(D.ReleaseDate) ASC