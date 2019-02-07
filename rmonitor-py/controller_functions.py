import mysql.connector
import os
import socket
from datetime import date

#---------------------------------------------------------
# Prepare the list of queries that only need exactly one
# additional user input
#---------------------------------------------------------
def fetchQueries():
  fetch_queries = ["FetchParts",
                   "ViewOriginalSpecs",
                   "ViewRentalUnitHistory",
                   "ViewClientHistory",
                   "ViewComputerRentalNumber",
                   "ViewComputerParentDelivery",
                   "Projection",
                   "FilterSmallAccessories",
                   "FilterParts",
                   "FilterAccessories",
                   "FilterDeliveries",
                   "FilterDeliveriesName",
                   "FilterClients",
                   "FetchPulledComputers",
                   "FetchPulledDeliveryAccessories",
                   "FetchPendingDeliveryAccessories",
                   "FetchPendingComputers",
                   "FetchComputers",
                   "FetchCompleteComputers",
                   "FetchDeliveryAccessories",
                   "FetchActiveCompleteComputers",
                   "FetchActiveDeliveryAccessories",
                   "FindListIDs",
                   "FindClientContactPerson",
                   "FindClient",
                   "FindDelivery",
                   "FilterAvailableParts",
                   "DeleteSmallAccessory",
                   "DeleteComputer",
                   "DeleteClient",
                   "DeleteParts",
                   "DeleteAccessory",
                   "ReturnAccessory",
                   "SetRentalPending",
                   "SetRentalUnavailable",
                   "FetchPullOut",
                   "CompleteDelivery",
                   "TraceComputer",
			"FetchDeliveryPeripherals"]
  return fetch_queries

def ManagementQueries():
  queries = ["ViewAllLogin",
             "ViewLogin",
             "ChangeRole",
             "ChangePassword",
             "ChangeUserPassword",
             "ViewPersonalLogin",
             "Suspend",
             "Activate",
             "Create"]
  return queries

#---------------------------------------------------------
# Prepare and print the pretty list of query names
#---------------------------------------------------------
def display_options(itemlist):
  available_display = "Available Options: "
  for stritem in itemlist:
    available_display += (stritem + "\r\n")
  print available_display

#---------------------------------------------------------
# Construct a query from a multiline sql file in queries
# subdirectory
#---------------------------------------------------------
def make_query(filename):
  query = ""
  query_dir = os.path.dirname(__file__)
  rel_path = os.path.join("queries", filename)
  abs_path = os.path.join(query_dir, rel_path)
  for line in open(abs_path):
    query += line
  return query

#---------------------------------------------------------
# Check if the input is bad
#---------------------------------------------------------
def validate_string(string):
  bad_chars = (";", "\\", "/*", "*/", "=", "@@")
  if any(bad in string for bad in bad_chars):
    print "Yikes, bad char detected"
    return False
  else:
    return True

def only_good_char(string):
  if not validate_string(string):
    return False
  else:
    for char in string:
      try:
        foo = int(char)
        print "Yikes, that wasn't a letter"
        return False
      except ValueError as err:
        continue

def validate_int(integer):
  try:
    test = int(integer)
    return True
  except ValueError as err:
    print "Yikes, that wasn't an integer"
    return False

def validate_date(date):
  if (validate_int(date[0:4]) and
      validate_int(date[5:7]) and
      validate_int(date[8:10]) and
      len(date) == 10 and
      date[4] == "-" and
      date[7] == "-"):
    return True
  else:
    return False
  

#---------------------------------------------------------
# Listen for and construct user client input
#---------------------------------------------------------
def get_client_input(socket_connection):
  data = ""
  #print "Waiting for input from user client"
  while True:
      stream_data = socket_connection.recv(1)
      if stream_data == '\n':
        break
      elif stream_data == '\r':
        pass
      else:
        data += stream_data
  #print "Received data:", data
  return data



#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewParts query
#---------------------------------------------------------
def ViewParts(sqlcursor, conn):
  for (PartID, Name, PartType, Status, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(PartID, Name, PartType, Status, Price)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(PartID, Name, PartType, Status, Price))
	
#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewPartsAndQty query
#---------------------------------------------------------
def ViewPartsAndQty(sqlcursor, conn):
  for (Name, PartType, Count) in sqlcursor:
    #print("{}, {}, {}").format(Name, PartType, Count)
    conn.sendall(("{}, {}, {}\n").format(Name, PartType, Count))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewOriginalSpecs query
#---------------------------------------------------------
def ViewOriginalSpecs(sqlcursor, conn):
  for (PartID, Name, PartType, Status, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(PartID, Name, PartType, Status, Price)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(PartID, Name, PartType, Status, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewMonthDeliveryCount query
#---------------------------------------------------------
def ViewMonthDeliveryCount(sqlcursor, conn):
  for (Month, Year, Count) in sqlcursor:
    #print("{}, {}, {}").format(Month, Year, Count)
    conn.sendall(("{}, {}, {}\n").format(Month, Year, Count))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewDeliverySpecs query
#---------------------------------------------------------
def ViewDeliverySpecs(sqlcursor, conn):
  previous = ""
  previous2 = ""
  for (DeliveryID, RentalNumber, CPU, PCType, OS, Name, PartType) in sqlcursor:
    if previous != DeliveryID:
      #print("{}").format(DeliveryID)
      conn.sendall(("{}\n").format(DeliveryID))
      previous = DeliveryID
    if previous2 != RentalNumber:
      #print("{}, {}, {}, {}").format(RentalNumber, CPU, PCType, OS)
      conn.sendall(("{}, {}, {}, {}\n").format(RentalNumber, CPU, PCType, OS))
      previous2 = RentalNumber
    #print("{}, {}").format(Name, PartType)
    conn.sendall(("{}, {}\n").format(Name, PartType))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewDeliveries query
#---------------------------------------------------------
def ViewDeliveries(sqlcursor, conn):
  for (DeliveryID, Name, SO, SI, ARD, POS, Release, Due, AM, Status, ExtensionID, Freq) in sqlcursor:
    #print("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}").format(DeliveryID, Name, SO, SI, ARD, POS, Release, Due, AM, Status, ExtensionID, Freq)
    conn.sendall(("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n").format(DeliveryID, Name, SO, SI, ARD, POS, Release, Due, AM, Status, ExtensionID, Freq))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewComputersStatus query
#---------------------------------------------------------
def ViewComputersStatus(sqlcursor, conn):
  for (RentalNumber, Status) in sqlcursor:
    #print("{}, {}").format(RentalNumber, Status)
    conn.sendall("{}, {}\n").format(RentalNumber, Status)

#---------------------------------------------------------
# Display the pretty(?) results of the ViewComputers
# AND ViewComputerRentalNumber query
#---------------------------------------------------------
def ViewComputers(sqlcursor, conn):
  previous = ""
  for (RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, CPrice, PID, Name, PartType, PPrice) in sqlcursor:
    if previous != RentalNumber:
      #print("{}, {}, {}, {}, {}, {}, {}, {}, {}").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, CPrice)
      conn.sendall(("{}, {}, {}, {}, {}, {}, {}, {}, {}\n").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, CPrice))
      previous = RentalNumber
    #print("{}, {}, {}, {}").format(PID, Name, PartType, PPrice)
    conn.sendall(("{}, {}, {}, {}\n").format(PID, Name, PartType, PPrice))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewAllExtended query
#---------------------------------------------------------
def ViewAllExtended(sqlcursor, conn):
  for (DeliveryID, Name, SO, SI, ARD, POS, Release, Due, AM, Status, ExtensionID) in sqlcursor:
    #print("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}").format(DeliveryID, Name, SO, SI, ARD, POS, Release, Due, AM, Status, ExtensionID)
    conn.sendall(("{}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\n").format(DeliveryID, Name, SO, SI, ARD, POS, Release, Due, AM, Status, ExtensionID))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewAccessoryRentalNumbersByTypes AND FilterAccessories
# query
#---------------------------------------------------------
def ViewAccessoryRentalNumbersByTypes(sqlcursor, conn):
  for (Name, AccessoryType, RentalNumber, Status, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(Name, AccessoryType, RentalNumber, Status, Price)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(Name, AccessoryType, RentalNumber, Status, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewAccessoriesAndQty query
#---------------------------------------------------------
def ViewAccessoriesAndQty(sqlcursor, conn):
  for (Name, AccessoryType, Count) in sqlcursor:
    #print("{}, {}, {}").format(Name, AccessoryType, Count)
    conn.sendall(("{}, {}, {}\n").format(Name, AccessoryType, Count))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FindOnHandParts query
#---------------------------------------------------------
def FindOnHandParts(sqlcursor, conn):
  for (PartID, Name, AccessoryType, Status, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(PartID, Name, AccessoryType, Status, Price)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(PartID, Name, AccessoryType, Status, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FindOnHandComputers query
#---------------------------------------------------------
def FindOnHandComputers(sqlcursor, conn):
  for (RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}, {}, {}, {}, {}").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price)
    conn.sendall(("{}, {}, {}, {}, {}, {}, {}, {}, {}\n").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FindOnHandAccessories query
#---------------------------------------------------------
def FindOnHandAccessories(sqlcursor, conn):
  for (RentalNumber, Status, Name, AccessoryType, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(Name, AccessoryType, RentalNumber, Status, Price)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(Name, AccessoryType, RentalNumber, Status, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FindListIDs query
#---------------------------------------------------------
def FindListIDs(sqlcursor, conn):
  for (ListID, foo) in sqlcursor:
    #print("{}").format(ListID)
    conn.sendall(("{}\n").format(ListID))


#---------------------------------------------------------
# Display the pretty(?) results of the
# FindAvailablei7 query
#---------------------------------------------------------
def FindAvailablei7(sqlcursor, conn):
  for (RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}, {}, {}, {}, {}").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price)
    conn.sendall(("{}, {}, {}, {}, {}, {}, {}, {}, {}\n").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FetchParts, FilterParts, AND FilterAvailableParts query
#---------------------------------------------------------
def FetchParts(sqlcursor, conn):
  for (PartID, Name, PartType, Status, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(PartID, Name, PartType, Status, Price)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(PartID, Name, PartType, Status, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FetchComputers query
#---------------------------------------------------------
def FetchComputers(sqlcursor, conn):
  for (RentalNumber, foo) in sqlcursor:
    #print("{}, {}").format(str(RentalNumber),foo)
    conn.sendall(("{}\n").format(str(RentalNumber)))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FetchXCompleteComputers and ViewPullOutListUnits query
#---------------------------------------------------------
def FetchCompleteComputers(sqlcursor, conn):
  previous = ""
  for (RentalNumber, PID, Price) in sqlcursor:
    if previous != RentalNumber:
      #print("{}, {}").format(RentalNumber, Price)
      conn.sendall(("{}, {}\n").format(RentalNumber, Price))
      previous = RentalNumber
    #print("{}").format(PID)
    conn.sendall(("{}\n").format(PID))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewLatestDeliveryVersion query
#---------------------------------------------------------
def ViewLatestDeliveryVersion(sqlcursor, conn):
  for (DeliveryID, Extension) in sqlcursor:
    #print("{}, {}").format(DeliveryID, Extension)
    conn.sendall(("{}, {}\n").format(DeliveryID, Extension))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewClients query
#---------------------------------------------------------
def ViewClients(sqlcursor, conn):
  for (ClientID, Name, Address, ContactPerson, ContactNumber) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(ClientID, Name, Address, ContactPerson, ContactNumber)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(ClientID, Name, Address, ContactPerson, ContactNumber))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FindClient query
#---------------------------------------------------------
def FindClient(sqlcursor, conn):
  for (ID, foo) in sqlcursor:
    #print("{}").format(str(ID))
    conn.sendall(("{}\n".format(str(ID))))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FindClientContactPerson query
#---------------------------------------------------------
def FindClientContactPerson(sqlcursor, conn):
  for (contact, foo) in sqlcursor:
    #print("{}").format(contact)
    conn.sendall(("{}\n".format(contact)))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FetchDeliveryAccessories query
#---------------------------------------------------------
def FetchDeliveryAccessories(sqlcursor, conn):
  for (RentalNumber, Status, Name, AccessoryType, Price) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(Name, AccessoryType, RentalNumber, Status, Price)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(Name, AccessoryType, RentalNumber, Status, Price))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewPullOuts and FetchPullOut query
#---------------------------------------------------------
def ViewPullOuts(sqlcursor, conn):
  for (DeliveryID, FormNumber, DateCreated, Status) in sqlcursor:
    #print("{}, {}, {}, {}").format(DeliveryID, FormNumber, DateCreated, Status)
    conn.sendall(("{}, {}, {}, {}\n").format(DeliveryID, FormNumber, DateCreated, Status))

#---------------------------------------------------------
# Display the pretty(?) results of the
# GetPullOutList query
#---------------------------------------------------------
def GetPullOutList(sqlcursor, conn):
  for (DeliveryID, FormNumber, RentalNumber) in sqlcursor:
    #print("{}, {}, {}").format(DeliveryID, FormNumber, RentalNumber)
    conn.sendall(("{}\n").format(RentalNumber))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewAllLogin query
#---------------------------------------------------------
def ViewAllLogin(sqlcursor, conn):
  for (Username, Role) in sqlcursor:
    #print("{}, {}").format(Username, Role)
    conn.sendall(("{}, {}\n").format(Username, Role))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewLogin query
#---------------------------------------------------------
def ViewLogin(sqlcursor, conn):
  for (Username, Password, Salt, Role) in sqlcursor:
    #print("{}, {}, {}, {}\n").format(Username, Password, Salt, Role)
    conn.sendall(("{}, {}, {}, {}\n").format(Username, Password, Salt, Role))

#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewCPUQty query
#---------------------------------------------------------
def ViewCPUQty(sqlcursor, conn):
  for (CPU, Count) in sqlcursor:
    #print("{}, {}").format(CPU, Count)
    conn.sendall(("{}: {}\n").format(CPU, Count))

#---------------------------------------------------------
# Display the pretty(?) results of the
# TraceComputer query
#---------------------------------------------------------
def TraceComputer(sqlcursor, conn):
  for (RentalNumber, foo) in sqlcursor:
    #print("{}").format(RentalNumber)
    if RentalNumber:
      conn.sendall(("{}\n").format(RentalNumber))
    else:
      conn.sendall("\n");
    
#---------------------------------------------------------
# Display the pretty(?) results of the
# ViewSmallAccessories and FilterSmallAccessories queries
#---------------------------------------------------------
def ViewSmallAccessories(sqlcursor, conn):
  for (Name, AccessoryType, Price, Quantity, Minus) in sqlcursor:
    #print("{}, {}, {}, {}, {}").format(Name, AccessoryType, Price, Quantity, Minus)
    conn.sendall(("{}, {}, {}, {}, {}\n").format(Name, AccessoryType, Price, Quantity, Minus))

#---------------------------------------------------------
# Display the pretty(?) results of the
# FetchDeliveryPeripherals query
#---------------------------------------------------------
def FetchDeliveryPeripherals(sqlcursor, conn):
  for (Name, Quantity) in sqlcursor:
    #print("{}, {}").format(Name, Quantity)
    conn.sendall(("{}, {}\n").format(Name, Quantity))

#---------------------------------------------------------
# Generates CSV files that contain the data from
# each of the following tables found in the database
# Returns the path to the created CSV file
#---------------------------------------------------------
def ReportComputers(sqlcursor, conn):
  query_dir = os.path.dirname(__file__)
  rel_path = os.path.join("reports", ("InventoryOfComputers-{}.csv").format(date.today().strftime("%m-%d-%y")))
  abs_path = os.path.join(query_dir, rel_path)
  
  with open(abs_path, 'w') as outf:
    outf.write("Rental#, Status, CPU, PC Type, OS, Purchase Date, Is Upgraded, Description, Total Price, Part 1, Name, Type, Part 2, Name, Type, Part 3, Name, Type, Part 4, Name, Type, Part 5, Name, Type, Part 6, Name, Type, Part 7, Name, Type, Part 8, Name, Type, Part 9, Name, Type")
    #conn.sendall("Rental#, Status, CPU, PC Type, OS, Purchase Date, Is Upgraded, Description, Total Price, Part 1, Name, Type, Part 2, Name, Type, Part 3, Name, Type, Part 4, Name, Type, Part 5, Name, Type, Part 6, Name, Type, Part 7, Name, Type, Part 8, Name, Type, Part 9, Name, Type")
    previous = ""
    for (RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, CPrice, PID, Name, PartType, PPrice) in sqlcursor:
      if previous != RentalNumber:
        #print("{}, {}, {}, {}, {}, {}, {}, {}, {}").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description, CPrice)
        outf.write(("\n{}, {}, {}, {}, {}, {}, {}, {}").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description))
        #conn.sendall(("\n{}, {}, {}, {}, {}, {}, {}, {}").format(RentalNumber, Status, CPU, PCType, OS, PurchaseDate, IsUpgraded, Description))
        previous = RentalNumber
      #print("{}, {}, {}, {}").format(PID, Name, PartType, PPrice)
      outf.write((", {}, {}, {}").format(PID, Name, PartType))
      #conn.sendall((", {}, {}, {}").format(PID, Name, PartType))

  conn.sendall(("{}").format(abs_path))

def ReportParts(sqlcursor, conn):
  query_dir = os.path.dirname(__file__)
  rel_path = os.path.join("reports", ("InventoryOfParts-{}.csv").format(date.today().strftime("%m-%d-%y")))
  abs_path = os.path.join(query_dir, rel_path)
  
  with open(abs_path, 'w') as outf:
    outf.write("Part ID, Name, Part Type, Status\n")
    #conn.sendall("Part ID, Name, Part Type, Status\n")
    for (PartID, Name, PartType, Status, Price) in sqlcursor:
      #print("{}, {}, {}, {}, {}").format(PartID, Name, PartType, Status, Price)
      outf.write(("{}, {}, {}, {}\n").format(PartID, Name, PartType, Status))
      #conn.sendall(("{}, {}, {}, {}\n").format(PartID, Name, PartType, Status))

  conn.sendall(("{}").format(abs_path))

def ReportAccessories(sqlcursor, conn):
  query_dir = os.path.dirname(__file__)
  rel_path = os.path.join("reports", ("InventoryOfAccessories-{}.csv").format(date.today().strftime("%m-%d-%y")))
  abs_path = os.path.join(query_dir, rel_path)
  
  with open(abs_path, 'w') as outf:
    outf.write("Rental#, Name, Type, Status\n")
    #conn.sendall("Rental#, Name, Type, Status\n")
    for (Name, AccessoryType, RentalNumber, Status, Price) in sqlcursor:
      #print("{}, {}, {}, {}, {}").format(Name, AccessoryType, RentalNumber, Status, Price)
      outf.write(("{}, {}, {}, {}\n").format(RentalNumber, Name, AccessoryType, Status))
      #conn.sendall(("{}, {}, {}, {}\n").format(RentalNumber, Name, AccessoryType, Status))

  conn.sendall(("{}").format(abs_path))

def ReportSmallAccessories(sqlcursor, conn):
  query_dir = os.path.dirname(__file__)
  rel_path = os.path.join("reports", ("InventoryOfSmallAccessories-{}.csv").format(date.today().strftime("%m-%d-%y")))
  abs_path = os.path.join(query_dir, rel_path)
  #print "ReportSmallAccessories: " + str(abs_path)
  
  with open(abs_path, 'w') as outf:
    outf.write("Name, Type, Total Qty, Qty in Use, Qty Remaining\n")
    #conn.sendall("Name, Type, Total Qty, Qty in Use, Qty Remaining\n")
    for (Name, AccessoryType, Price, Quantity, Minus) in sqlcursor:
      #print("{}, {}, {}, {}, {}").format(Name, AccessoryType, Price, Quantity, Minus)
      outf.write(("{}, {}, {}, {}, {}\n").format(Name, AccessoryType, Quantity, Minus, int(Quantity) - int(Minus)))
      #conn.sendall(("{}, {}, {}, {}, {}\n").format(Name, AccessoryType, Quantity, Minus, int(Quantity) - int(Minus)))

  conn.sendall(("{}").format(abs_path))
  #print "ReportSmallAccessories: Done!"

#---------------------------------------------------------
# Handles the multiline query processing of
# the insert query and sends the result to the
# user client
#---------------------------------------------------------
def InsertSQL(multi_result, conn):
  for cur in multi_result:
    #print(("cursor: {}").format(cur))
    if cur.with_rows:
      cur.fetchall()
      #print(("result: {}").format(cur.fetchall()))
  #conn.sendall("Succcessfully completed the operation!")
