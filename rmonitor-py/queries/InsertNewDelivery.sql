INSERT INTO Delivery(SalesOrder, SalesInvoice, ARD, POS, CustomerID, ReleaseDate, DueDate, AccountManager, Status, ExtensionID, Comments, Frequency) 
VALUES (%(so)s,%(si)s,%(ard)s,%(pos)s,
%(clientid)s,%(releasedate)s,%(duedate)s,%(am)s,%(status)s,%(extension)s,NULL,%(frequency)s);
