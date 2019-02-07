SELECT D.DeliveryID, C.Name, D.SalesOrder, 
D.SalesInvoice, D.ARD, D.POS, 
D.ReleaseDate, D.DueDate, D.AccountManager, 
D.Status, D.ExtensionID, D.Frequency
FROM RentalList R INNER JOIN Delivery D
ON R.DeliveryID = D.DeliveryID
INNER JOIN Client C
ON D.CustomerID = C.ClientID
WHERE R.RentalNumber = %(rentalnumber)s AND D.Status = "Active"
ORDER BY D.ReleaseDate DESC
LIMIT 1