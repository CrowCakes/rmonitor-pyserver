SELECT D.DeliveryID, C.Name, D.SalesOrder, 
D.SalesInvoice, D.ARD, D.POS, 
D.ReleaseDate, D.DueDate, D.AccountManager, 
D.Status, D.ExtensionID, D.Frequency
FROM Delivery D, Client C
WHERE D.CustomerID = C.ClientID
AND D.DeliveryID LIKE %(deliveryid)s
ORDER BY D.DeliveryID