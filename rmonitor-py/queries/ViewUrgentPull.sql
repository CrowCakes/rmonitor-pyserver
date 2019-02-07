SELECT D.DeliveryID, C.Name, D.SalesOrder, 
D.SalesInvoice, D.ARD, D.POS, 
D.ReleaseDate, D.DueDate, D.AccountManager, 
D.Status, D.ExtensionID, D.Frequency
FROM Delivery D, Client C
WHERE D.CustomerID = C.ClientID AND D.Status = "Active" 
AND TO_DAYS(D.DueDate) - TO_DAYS(NOW()) <= 7
ORDER BY D.DeliveryID ASC;