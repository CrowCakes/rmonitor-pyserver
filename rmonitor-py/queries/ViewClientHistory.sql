SELECT D.DeliveryID, C.Name, D.SalesOrder, 
D.SalesInvoice, D.ARD, D.POS, 
D.ReleaseDate, D.DueDate, D.AccountManager, 
D.Status, D.ExtensionID, D.Frequency
FROM Client C INNER JOIN Delivery D
ON C.ClientID = D.CustomerID
WHERE C.Name = %(name)s
ORDER BY D.ReleaseDate ASC