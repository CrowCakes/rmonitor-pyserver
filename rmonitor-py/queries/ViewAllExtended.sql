SELECT D.DeliveryID, C.Name, D.SalesOrder, 
D.SalesInvoice, D.ARD, D.POS, 
D.ReleaseDate, D.DueDate, D.AccountManager, 
D.Status, D.ExtensionID, D.Frequency
FROM Delivery D INNER JOIN Client C
ON D.CustomerID = C.ClientID
WHERE D.ExtensionID <> 0
ORDER BY D.DeliveryID ASC