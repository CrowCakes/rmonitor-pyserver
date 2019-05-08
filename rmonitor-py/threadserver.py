import mysql.connector
import os
import sys
import socket
import threading
import datetime
from simple_auth import *
from controller_functions import *
from mysql.connector import errorcode
from mysql.connector import pooling

class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.lock = threading.Lock()

    # the main thread only listens for connections
    def listen(self):
        self.sock.listen(5)
        # the shared dict that stores the deliveryID that a client would want to print
        print_list = {}
        connected_user_list = []
	
        dbconfig = {
                "database": "PCRental",
                "user": "user",
                "password": "sausageinnose",
                "host": "127.0.0.1"
	}
        viewconfig = {
                "database": "PCRental",
                "user": "user",
                "password": "password",
                "host": "127.0.0.1"
	}
        reportconfig = {
                "database": "PCRental",
                "user": "user",
                "password": "password",
                "host": "127.0.0.1"
	}
	
        #---------------------------------------------------------
        # Connect to the database
        #---------------------------------------------------------
        try:
            cnxpool = mysql.connector.connect(pool_name = "admin_pool", pool_size = 5, **dbconfig)
            #cnx = mysql.connector.connect(user='user',
            #                              password='password',
            #                              host='127.0.0.1',
            #                              database='pcrental')
            #cursor = cnx.cursor()
            print "Connected to MySQL database"
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        # Only executes below on successful database login
        else:
            print "Server ready\r\n"
            # Keep listening for clients
            while True:
                #print "{}\nWaiting for client connection\n".format(connected_user_list)
                client, address = self.sock.accept()
                #print "Successfully connected to client from ", address
                #check if connection to mysql closed
		#if not cnx.is_connected():
		#	try:
		#		cnx = mysql.connector.connect(pool_name = "admin_pool", pool_size = 5, **dbconfig)
		#	except mysql.connector.Error as err:
		#		if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		#			print("Something is wrong with your user name or password")
		#		elif err.errno == errorcode.ER_BAD_DB_ERROR:
		#			print("Database does not exist")
		#		else:
		#			print(err)
                pooled_cnx = mysql.connector.connect(pool_name = "admin_pool")
                threading.Thread(target = self.listenToClient,args = (client,address,pooled_cnx,print_list,connected_user_list)).start()

        # Close the database connection
	#cursor.close()
        cnx.close()

    # function of each thread created
    def listenToClient(self, connection, address, cnx, delivery_print, connected_list):
        available_options = []
        for line in open('querylist.txt'):
            fline = line.rstrip()
            available_options.append(fline)

        # These queries require exactly one additional input from user
        fetch_queries = fetchQueries()

        data = get_client_input(connection)
	#print data	

        # Each of the conditional statements except 'else' detect a 'keyword'
        # 'else' detects a query
        if data == "Login":
            #---------------------------------------------------------
            # Receive login credentials from client
            #---------------------------------------------------------
            login_cred = []
            for i in range(2):
              data = get_client_input(connection)
              login_cred.append(data)

            # Authenticate
            # get the lock
            #print "Getting lock"
            with self.lock:
                #print "Got the lock"
                login_reply = authenticate_new(login_cred)

            #duplicate = False
            # Put a user in the connected_user_list
            print(datetime.datetime.now())
            if login_reply != "":
                #print "Getting lock"
                # get lock
                with self.lock:
                    #print "Got the lock"
                    try:
			#remove user from list if he was already logged in before
                        for i in connected_list:
                            if login_cred[0] in i:
                                print "User " + login_cred[0] + " is already logged in!"
                                connected_list.remove(i)
				#duplicate = True
                                break
                        connected_list.remove(login_reply.splitlines()[1] + login_cred[0])
                    except ValueError:
                        connected_list.append(login_reply.splitlines()[1] + login_cred[0])
                    else:
                        connected_list.append(login_reply.splitlines()[1] + login_cred[0])
                # lock released
                print "New login attempt from " + login_cred[0]
		#print login_reply
                print "Current login: " + ", ".join(connected_list)

            else:
                print "Failed login attempt with credentials " + ", ".join(login_cred)
            
            # Access control pending
            connection.sendall(login_reply)
              
            #print "Disconnecting now\r\n"
            print "\r\n"
            connection.close()
		
            try:
                cnx.close()
            except Exception as err:
                pass
            #--------------------end of loop--------------------------#

        elif data == "UserManagement":
            management_queries = ManagementQueries()
            insert_data = []
            
            # get the command
            data = get_client_input(connection)
            user_option = data.strip()

            if user_option not in management_queries:
                print(datetime.datetime.now())
                print user_option + " is not a valid query. Please copy the query name exactly\r\n"
                connection.sendall(
                  "Error: That's not a valid query. Please copy the query name exactly")
                connection.close()

            elif (user_option == "ViewPersonalLogin" or
                  user_option == "Suspend" or
                  user_option == "Activate" or
                  user_option == "ViewLogin"):
                data = get_client_input(connection)
                insert_data.append(data)
                #print insert_data

            elif (user_option == "ChangeRole" or
                  user_option == "ChangeUserPassword"):
                for i in range(2):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            elif (user_option == "ChangePassword" or
                  user_option == "Create"):
                for i in range(3):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            #execute queries
            cursor = cnx.cursor()
            # all the login user pairs
            if (user_option == "ViewAllLogin"):
                cursor.execute(make_query(user_option+'.sql'))
                ViewAllLogin(cursor, connection)

            # produces only one login user pair
            elif (user_option == "ViewPersonalLogin"):
                user_option_data = {'username': insert_data[0]}
                cursor.execute(make_query(user_option+'.sql'), user_option_data)
                ViewAllLogin(cursor, connection)

            elif (user_option == "ViewLogin"):
                user_option_data = {'username': insert_data[0]}
                cursor.execute(make_query(user_option+'.sql'), user_option_data)
                ViewLogin(cursor, connection)

            elif (user_option == "Suspend"):
                user_option_data = {'role': "Suspend",
                                    'username': insert_data[0]}
                connection.sendall(ChangeQuery(user_option_data, "ChangeRole"))

            elif (user_option == "Activate"):
                user_option_data = {'role': "Viewer",
                                    'username': insert_data[0]}
                connection.sendall(ChangeQuery(user_option_data, "ChangeRole"))

            # authenticate the user first
            elif (user_option == "ChangeRole"):
                user_option_data = {'role': insert_data[0],
                                    'username': insert_data[1]}
                connection.sendall(ChangeQuery(user_option_data, "ChangeRole"))

            # generate the hash first before inserting into database
            elif (user_option == "ChangePassword"):
                auth = authenticate_new([insert_data[1], insert_data[2]])
                if auth != "":
                    new_pass = getDigest(insert_data[0])
                    # get the old hash, only works if the credentials are correct
                    auth_pass = retrieveHash([insert_data[1], insert_data[2]])
                    
                    user_option_data = {'password': new_pass[1],
                                        'salt': new_pass[0],
                                        'username': insert_data[1],
                                        'old_password': auth_pass[1]}
                    connection.sendall(ChangeQuery(user_option_data, "ChangePassword"))
                else:
                    connection.sendall("Error: database password and your old password don't match")

            # generate the hash first before inserting into database
            elif (user_option == "ChangeUserPassword"):
                new_pass = getDigest(insert_data[0])
                user_option_data = {'password': new_pass[1],
                                    'salt': new_pass[0],
                                    'username': insert_data[1]}
                connection.sendall(ChangeQuery(user_option_data, "ChangeUserPassword"))

            elif (user_option == "Create"):
                new_pass = getDigest(insert_data[1])
                user_option_data = {'username': insert_data[0],
                                    'password': new_pass[1],
                                    'salt': new_pass[0],
                                    'role': insert_data[2]}
                connection.sendall(ChangeQuery(user_option_data, "InsertNewUser"))

            connection.close()

            try:
                cnx.close()
            except Exception as err:
                pass

        else:
            #---------------------------------------------------------
            # Wait for query choice from user client
            # Make sure the query name matches the filenames exactly
            # Wait for additional user input for certain queries
            #---------------------------------------------------------  
            user_option = data.strip()
            part_id = ""
            insert_data = []

            # catch invalid query names and quit command
            if user_option not in available_options:
                print(datetime.datetime.now())
                print user_option + " is not a valid query. Please copy the query name exactly"
                connection.sendall(
                  "Error: That's not a valid query. Please copy the query name exactly")
                connection.close()
                # the user wants to quit his session
                if user_option[0:4] == "quit":
                    logout_id = user_option[4:]
                    print "Removing user", logout_id, "from connected_user_list"
                    # get lock
                    with self.lock:
                        print "Got the lock"
                        # the user's id does not exist in server memory
                        try:
                            ChangeQuery({'username': user_option[18:]}, "SetLoginStatusFalse")
                            connected_list.remove(logout_id)
                        except Exception as ex:
                            print "The logout_id", logout_id, "does not exist btw"
                    # lock released
                    print "User", logout_id, "at", address, "has logged out"
		   
                    print "Current login: " + ", ".join(connected_list)
                print "\r\n"
                sys.stdout.flush()
                cnx.close()
                return

            elif user_option in fetch_queries:
                #print "Waiting for additional input from user client"
                data = get_client_input(connection)
                #print "Received partID:", data
                part_id = data

            elif (user_option == "InsertDeliverySpecs" or
                  user_option == "ViewMonthHistory" or
                  user_option == "InsertDeliveryAccessories" or
                  user_option == "ReturnUnit" or
                  user_option == "ViewPullOutListUnits" or
                  user_option == "ViewPullOutListAcc" or
                  user_option == "ReturnDelivery" or
                  user_option == "GetPullOutList" or
                  user_option == "DeletePullOut" or
                  user_option == "DeletePullOutList" or
                  user_option == "FetchPendingPeripherals" or
                  user_option == "DeletePullOutPeripherals"):
                for i in range(2):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            elif (user_option == "InsertPullOutListItem" or
                  user_option == "DeletePullOutListItem" or
                  user_option == "InsertDeliveryPeripherals" or
                  user_option == "DeletePullOutPeripheralsItem"):
                for i in range(3):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            elif (user_option == "InsertNewClient" or
                  user_option == "InsertNewRentalAccessory" or
                  user_option == "InsertNewPullOut" or
                  user_option == "SetPeripheralPending"):
                for i in range(4):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data
            
            elif (user_option == "EditClient" or
                  user_option == "EditAccessory" or
                  user_option == "InsertNewSmallAccessory" or
                  user_option == "InsertNewPart"):
                for i in range(5):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            elif (user_option == "EditSmallAccessory" or 
					user_option == "EditPart"):
                for i in range(7):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            elif (user_option == "InsertNewDelivery"):
                for i in range(12):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            elif user_option == "EditDelivery":
                for i in range(13):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data
                
            elif (user_option == "InsertNewRentalComputer"):
                for i in range(17):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data

            elif user_option == "EditComputer":
                for i in range(27):
                    data = get_client_input(connection)
                    insert_data.append(data)
                #print insert_data


            #---------------------------------------------------------
            # Execute the user's query and print its response
            # At this point, no more user input is expected
            #---------------------------------------------------------
            cursor = cnx.cursor(buffered=True)
            results = ""

            #---------------------------------------------------------
            # Insert user's input into query if applicable
            # Validate each input to make sure query is clean
            #---------------------------------------------------------
            try:
                if (user_option == "FetchParts" or
                    user_option == "TraceComputer"):
                    if validate_int(part_id):
                        user_option_data = {'partid': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on PartID"
                        raise Exception("Invalid input on PartID", )

                elif (user_option == "FilterAvailableParts"):
                    if validate_int(part_id):
                        user_option_data = {'partid': ("%{}%").format(part_id)}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on PartID"
                        raise Exception("Invalid input on PartID", )
						
				elif (user_option == "FilterParts" or
						user_option == "FilterSmallAccessories"):
                    if validate_string(part_id):
                        user_option_data = {'partid': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on PartID"
                        raise Exception("Invalid input on PartID", )

                elif (user_option == "ViewComputerRentalNumber" or
						user_option == "FilterAccessories"):
                    if validate_string(part_id):
                        user_option_data = {'rentalnumber': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on RentalNumber"
                        raise Exception("Invalid input on RentalNumber", )

                elif (user_option == "ViewRentalUnitHistory" or
                      user_option == "ViewOriginalSpecs" or
                      user_option == "ViewComputerParentDelivery"):
                    if len(part_id) <= 30:
                        user_option_data = {'rentalnumber': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on RentalNumber"
                        raise Exception("Invalid input on RentalNumber", )

                elif user_option == "FindListIDs":
                    if len(part_id) <= 30:
                        user_option_data = {'rental_number': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on RentalNumber"
                        raise Exception("Invalid input on RentalNumber", )

                elif (user_option == "ViewClientHistory" or
                      user_option == "FindClientContactPerson"):
                    if len(part_id) <= 100:
                        user_option_data = {'name': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on Name"
                        raise Exception("Invalid input on Name", )

                elif (user_option == "FilterDeliveriesName" or
                      user_option == "FindClient"):
                    if validate_string(part_id):
                        user_option_data = {'name': "%{}%".format(part_id)}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on Name"
                        raise Exception("Invalid input on Name", )
						
				elif (user_option == "FilterClients"):
                    if validate_string(part_id):
                        user_option_data = {'name': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on Name"
                        raise Exception("Invalid input on Name", )

                elif (user_option == "FilterDeliveries"):
                    if validate_int(part_id):
                        user_option_data = {'deliveryid': "%{}%".format(part_id)}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on DeliveryID"
                        raise Exception("Invalid input on DeliveryID", )

                elif (user_option == "FetchCompleteComputers" or
                      user_option == "FetchComputers" or
                      user_option == "FetchDeliveryAccessories" or
                      user_option == "FetchActiveCompleteComputers" or
                      user_option == "FetchActiveDeliveryAccessories" or
                      user_option == "FetchPulledComputers" or
                      user_option == "FetchPulledDeliveryAccessories" or
                      user_option == "FetchPendingComputers" or
                      user_option == "FetchPendingDeliveryAccessories" or
                      user_option == "FetchPullOut" or
                      user_option == "FetchDeliveryPeripherals"):
                    if validate_int(part_id):
                        user_option_data = {'deliveryid': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on DeliveryID"
                        raise Exception("Invalid input on DeliveryID", )

                elif user_option == "FindDelivery":
                    if validate_int(part_id):
                        user_option_data = {'deliveryid': int(part_id)}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on DeliveryID"
                        raise Exception("Invalid input on DeliveryID", )

                elif user_option == "ViewMonthHistory":
                    if (validate_int(insert_data[0]) and
						len(insert_data[1]) == 4 and
                        validate_int(insert_data[1])):
                        user_option_data = {
                          'month': insert_data[0],
                          'year': insert_data[1]
                        }
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on date"
                        raise Exception("Invalid input on date", )

                elif user_option == "Projection":
                    if len(part_id) == 10:
                        user_option_data = {'date': part_id}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                    else:
                        print user_option
                        print "Error: invalid input on date"
                        raise Exception("Invalid input on date", )

                elif (user_option == "ViewPullOutListUnits" or
                      user_option == "ViewPullOutListAcc" or
                      user_option == "GetPullOutList" or
                      user_option == "DeletePullOut" or
                      user_option == "DeletePullOutList" or
                      user_option == "FetchPendingPeripherals" or
						user_option == "DeletePullOutPeripherals"):
                    if (validate_int(insert_data[0]) and
                        len(insert_data[1]) <= 20):
                        user_option_data = {'deliveryid': insert_data[0],
                                            'formnumber': insert_data[1]}
                        cursor.execute(make_query(user_option+'.sql'), user_option_data)
                        if (user_option == "DeletePullOut" or
                            user_option == "DeletePullOutList" or
				user_option == "DeletePullOutPeripherals"):
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )
                
                elif (user_option == "InsertNewPullOut"):
                    if (validate_int(insert_data[0]) and
                        len(insert_data[1]) <= 20 and
						len(insert_data[2]) == 10 and
                        len(insert_data[3]) <= 20):
                        user_option_data = {'deliveryid': insert_data[0],
                                            'formnumber': insert_data[1],
                                            'datecreated': insert_data[2],
                                            'status': insert_data[3]}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif (user_option == "InsertPullOutListItem" or
                      user_option == "DeletePullOutListItem"):
                    if (validate_int(insert_data[0]) and
                        len(insert_data[1]) <= 20 and
                        len(insert_data[2]) <= 30):
                        user_option_data = {'deliveryid': insert_data[0],
                                            'formnumber': insert_data[1],
                                            'rentalnumber': insert_data[2]}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                        except mysql.connector.Error as error:
                            print user_option
                            print(error)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif user_option == 'InsertNewClient':
                    if (len(insert_data[0]) <= 100 and
                        len(insert_data[1]) <= 255 and
                        len(insert_data[2]) <= 30 and
                        str.isdigit(insert_data[3])):
                        user_option_data = (insert_data[0],
                                          insert_data[1],
                                          insert_data[2],
                                          insert_data[3])
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif user_option == 'InsertNewPart':
                    if (validate_int(insert_data[0]) and
                        len(insert_data[1]) <= 100 and
                        len(insert_data[2]) <= 20 and
						len(insert_data[3]) <= 100):
                        user_option_data = {'partid': int(insert_data[0]),
                                            'name': insert_data[1],
                                            'type': insert_data[2],
											'remarks': insert_data[3],
                                            'price': insert_data[4]}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )
                    
                elif user_option == 'EditPart':
                    if (validate_int(insert_data[0]) and
                        validate_int(insert_data[1]) and
                        len(insert_data[2]) <= 100 and
                        len(insert_data[3]) <= 20 and
                        len(insert_data[4]) <= 20 and
						len(insert_data[5]) <= 100):
                        user_option_data = {
                            'old_part': insert_data[0],
                            'partid': insert_data[1],
                            'name': insert_data[2],
                            'parttype': insert_data[3],
                            'status': insert_data[4],
							'remarks': insert_data[5],
                            'price': insert_data[6]
                            }
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif user_option == 'EditClient':
                    if (len(insert_data[0]) <= 100 and
                        len(insert_data[1]) <= 100 and
                        len(insert_data[2]) <= 255 and
                        len(insert_data[3]) <= 30 and
                        validate_int(insert_data[4])):
                        user_option_data = {
                            'old_name': insert_data[0],
                            'name': insert_data[1],
                            'address': insert_data[2],
                            'contactp': insert_data[3],
                            'contactn': insert_data[4]
                            }
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif user_option == 'EditAccessory':
                    if (len(insert_data[0]) <= 30 and
                        len(insert_data[1]) <= 30 and
                        len(insert_data[2]) <= 100 and
                        len(insert_data[3]) <= 50):
                        user_option_data = {
                            'old_rental': insert_data[0],
                            'rental_number': insert_data[1],
                            'name': insert_data[2],
                            'acctype': insert_data[3],
                            'price': insert_data[4]
                            }
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                               user_option_data,
                                               multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif user_option == 'InsertNewRentalAccessory':
                    if (len(insert_data[0]) <= 30 and
                        len(insert_data[1]) <= 100 and
                        len(insert_data[2]) <= 50):
                        user_option_data = {
                            'rental_number': insert_data[0],
                            'name': insert_data[1],
                            'acctype': insert_data[2],
                            'price': insert_data[3]
                            }
                        try:
                            rental_number = {'rental_number': insert_data[0]}
                            cursor.execute(make_query('InsertNewRental.sql'), rental_number)
                            cnx.commit()
                        except Exception as err:
                            print user_option + " - InsertNewRental"
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: the RentalNumber already exists")

                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")                        
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif user_option == 'InsertNewSmallAccessory':
                    if (len(insert_data[0]) <= 100 and
						len(insert_data[1]) <= 50 and
						validate_int(insert_data[3]) and
                        validate_int(insert_data[4])
                        ):
                        user_option_data = {
                            'name': insert_data[0],
                            'type': insert_data[1],
                            'price': insert_data[2],
                            'quantity': insert_data[3],
                            'minus': insert_data[4],
                            }
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )


                elif user_option == 'EditSmallAccessory':
                    if (len(insert_data[2]) <= 100 and
						len(insert_data[3]) <= 50 and
						validate_int(insert_data[5]) and
                        validate_int(insert_data[6])
                        ):
                        user_option_data = {
                            'old_name': insert_data[0],
                            'old_type': insert_data[1],
                            'name': insert_data[2],
                            'type': insert_data[3],
                            'price': insert_data[4],
                            'quantity': insert_data[5],
                            'minus': insert_data[6],
                            }
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )


                elif user_option == 'InsertNewDelivery':
                    #print "InsertNewDelivery:"
                    #print insert_data
                    if (validate_int(insert_data[0]) and
						len(insert_data[1]) <= 30 and
						len(insert_data[2]) <= 30 and
						len(insert_data[3]) <= 30 and
						len(insert_data[4]) <= 30 and
                        validate_int(insert_data[5]) and
						len(insert_data[6]) == 10 and
						len(insert_data[7]) == 10 and
						len(insert_data[8]) <= 20 and
						len(insert_data[9]) <= 20 and
                        validate_int(insert_data[10])):
                        ext = insert_data[10]
                        if ext == '0':
                            ext = None	
                        user_option_data = {
                            'deliveryid': insert_data[0],
                            'so': insert_data[1],
                            'si':insert_data[2],
                            'ard': insert_data[3],
                            'pos': insert_data[4],
                            'clientid': insert_data[5],
                            'releasedate': insert_data[6],
                            'duedate': insert_data[7],
                            'am': insert_data[8],
                            'status': insert_data[9],
                            'extension': ext,
                            'frequency': insert_data[11]
                            }
                        try:
                            with self.lock:
                            	cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            	cnx.commit()
								#print "InsertNewDelivery last_insert_id:"
								#print cursor.lastrowid
                            	connection.sendall(str(cursor.lastrowid))
                            	#connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )


                elif user_option == 'EditDelivery':
                    if (validate_int(insert_data[0]) and
                        validate_int(insert_data[1]) and
						len(insert_data[2]) <= 30 and
						len(insert_data[3]) <= 30 and
						len(insert_data[4]) <= 30 and
						len(insert_data[5]) <= 30 and
                        validate_int(insert_data[6]) and
						len(insert_data[7]) == 10 and
						len(insert_data[8]) == 10 and
						len(insert_data[9]) <= 20 and
						len(insert_data[10]) <= 20 and
                        validate_int(insert_data[11])):
                        ext = insert_data[11]
                        if ext == '0':
                            ext = None
                        user_option_data = {
                            'old_delv_id': insert_data[0],
                            'deliveryid': insert_data[1],
                            'so': insert_data[2],
                            'si':insert_data[3],
                            'ard': insert_data[4],
                            'pos': insert_data[5],
                            'clientid': insert_data[6],
                            'releasedate': insert_data[7],
                            'duedate': insert_data[8],
                            'am': insert_data[9],
                            'status': insert_data[10],
                            'extension': ext,
                            'frequency': insert_data[12]
                            }
                        try:
                            with self.lock:
                            	results = cursor.execute(make_query(user_option+'.sql'),
                                              		 user_option_data,
                                              		 multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif (user_option == 'InsertDeliverySpecs' or
                      user_option == 'InsertDeliveryAccessories'):
                    if (validate_int(insert_data[0]) and
                        len(insert_data[1]) <= 30):
                        user_option_data = {
                          'deliveryid': insert_data[0],
                          'rentalnumber': insert_data[1]
                        }
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                               user_option_data,
                                               multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error: invalid input on some input"
                        raise Exception("Invalid input", )

                elif (user_option == "InsertDeliveryPeripherals"):
                    user_option_data = {'delv_id': insert_data[0],
                                        'name': insert_data[1],
                                        'quantity': insert_data[2]}
                    try:
                        results = cursor.execute(make_query(user_option+'.sql'),
                                                 user_option_data,
                                                 multi=True)
                        cnx.commit()
                        connection.sendall("Successfully completed the operation!")
                    except Exception as err:
                        print user_option
                        print(err)
                        cnx.rollback()
                        connection.sendall("Error: please contact administrator")

                elif user_option == 'InsertNewRentalComputer':
                    if (len(insert_data[0]) <= 30 and
                        len(insert_data[1]) <= 10 and
                        len(insert_data[2]) <= 10 and
                        len(insert_data[3]) <= 30 and
                        len(insert_data[4]) == 10 and
                        validate_int(insert_data[8]) and
                        validate_int(insert_data[9]) and
                        validate_int(insert_data[10]) and
                        validate_int(insert_data[11]) and
                        validate_int(insert_data[12]) and
                        validate_int(insert_data[13]) and
                        validate_int(insert_data[14]) and
                        validate_int(insert_data[15]) and
                        validate_int(insert_data[16])):
                        rental_computer_status = ""
                        if insert_data[5] == "True":
                            rental_computer_status = True
                        else:
                            rental_computer_status = False
                        user_option_data = {'rental_number': insert_data[0],
                                          'cpu': insert_data[1],
                                          'pctype': insert_data[2],
                                          'os': insert_data[3],
                                          'purchasedate': insert_data[4],
                                          'status': rental_computer_status,
                                            'price': float(insert_data[6]),
                                            'description': insert_data[7],
                                          'part1': int(insert_data[8]),
                                          'part2': int(insert_data[9]),
                                          'part3': int(insert_data[10]),
                                          'part4': int(insert_data[11]),
                                            'part5': int(insert_data[12]),
                                            'part6': int(insert_data[13]),
                                            'part7': int(insert_data[14]),
                                            'part8': int(insert_data[15]),
                                            'part9': int(insert_data[16])}
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                               user_option_data,
                                               multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error on some input"
                        raise Exception("Invalid input", )

                elif user_option == 'EditComputer':
                    if (len(insert_data[0]) <= 30 and
                        len(insert_data[1]) <= 30 and
                        len(insert_data[2]) <= 10 and
                        len(insert_data[3]) <= 10 and
                        len(insert_data[4]) <= 30 and
                        len(insert_data[5]) == 10 and
                        validate_int(insert_data[9]) and
                        validate_int(insert_data[10]) and
                        validate_int(insert_data[11]) and
                        validate_int(insert_data[12]) and
                        validate_int(insert_data[13]) and
                        validate_int(insert_data[14]) and
                        validate_int(insert_data[15]) and
                        validate_int(insert_data[16])):
                        rental_computer_status = ""
                        if insert_data[6] == "True":
                            rental_computer_status = True
                        else:
                            rental_computer_status = False
                        user_option_data = {'old_rental': insert_data[0],
                                          'rental_number': insert_data[1],
                                          'cpu': insert_data[2],
                                          'pctype': insert_data[3],
                                          'os': insert_data[4],
                                          'purchasedate': insert_data[5],
                                          'up_status': rental_computer_status,
                                            'price': float(insert_data[7]),
                                            'description': insert_data[8],
                                          'part1': int(insert_data[9]),
                                          'part2': int(insert_data[10]),
                                          'part3': int(insert_data[11]),
                                          'part4': int(insert_data[12]),
                                            'part5': int(insert_data[13]),
                                            'part6': int(insert_data[14]),
                                            'part7': int(insert_data[15]),
                                            'part8': int(insert_data[16]),
                                            'part9': int(insert_data[17]),
                                          'listid1': int(insert_data[18]),
                                          'listid2': int(insert_data[19]),
                                          'listid3': int(insert_data[20]),
                                          'listid4': int(insert_data[21]),
                                            'listid5': int(insert_data[22]),
                                            'listid6': int(insert_data[23]),
                                            'listid7': int(insert_data[24]),
                                            'listid8': int(insert_data[25]),
                                            'listid9': int(insert_data[26])}
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                               user_option_data,
                                               multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except Exception as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: please contact administrator")
                    else:
                        print user_option
                        print "Error on some input"
                        raise Exception("Invalid input", )

                elif user_option == "DeleteClient":
                    if validate_int(part_id):
                        user_option_data = {'customerid': part_id}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on input ClientID"
                        raise Exception("Invalid input for ClientID", )

                elif user_option == "DeleteComputer":
                    if validate_string(part_id):
                        user_option_data = {'rental_number': part_id}
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'), user_option_data, multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on input RentalNumber"
                        raise Exception("Invalid input for RentalNumber", )

                elif user_option == "DeleteParts":
                    if validate_int(part_id):
                        user_option_data = {'partid': part_id}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on input PartID"
                        raise Exception("Invalid input for PartID", )

                elif user_option == "DeleteAccessory":
                    if validate_string(part_id):
                        user_option_data = {'rentalnumber': part_id}
                        try:
                            cursor.execute(make_query(user_option+'.sql'),
                                           user_option_data,
                                           multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on input RentalNumber"
                        raise Exception("Invalid input for RentalNumber", )

                elif user_option == "DeleteSmallAccessory":
                    if validate_string(part_id):
                        user_option_data = {'name': part_id}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on input RentalNumber"
                        raise Exception("Invalid input for RentalNumber", )
                    
                elif user_option == "ReturnDelivery":
                    if (validate_int(insert_data[0]) and
                        validate_string(insert_data[1])):
                        user_option_data = {'deliveryid': insert_data[0],
                                            'formnumber': insert_data[1]}
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                                     user_option_data,
                                                     multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on some input"
                        raise Exception("Invalid input", )

                elif user_option == "DeletePullOutPeripheralsItem":
                    if (validate_int(insert_data[0]) and
                        validate_string(insert_data[1])):
                        user_option_data = {'deliveryid': insert_data[0],
                                            'formnumber': insert_data[1],
                                            'name': insert_data[2]}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on some input"
                        raise Exception("Invalid input", )

                elif user_option == "SetPeripheralPending":
                    if (validate_int(insert_data[0]) and
                        validate_string(insert_data[1])):
                        user_option_data = {'deliveryid': insert_data[0],
                                            'formnumber': insert_data[1],
                                            'name': insert_data[2],
                                            'quantity': insert_data[3]}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on some input"
                        raise Exception("Invalid input", )
                
                elif user_option == "CompleteDelivery":
                    if validate_int(part_id):
                        user_option_data = {'deliveryid': part_id}
                        try:
                            cursor.execute(make_query(user_option+'.sql'), user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on some input"
                        raise Exception("Invalid input", )
    
                elif user_option == "ReturnUnit":
                    if (validate_int(insert_data[0]) and validate_string(insert_data[1])):
                        user_option_data = {'deliveryid': insert_data[0],
                                            'rentalnumber': insert_data[1]}
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                                     user_option_data,
                                                     multi=True)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on some input"
                        raise Exception("Invalid input", )

                elif user_option == "ReturnAccessory":
                    if validate_string(part_id):
                        user_option_data = {'rentalnumber': part_id}
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                                     user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on input RentalNumber"
                        raise Exception("Invalid input for RentalNumber", )

                elif (user_option == "SetRentalPending" or
                      user_option == "SetRentalUnavailable"):
                    if validate_string(part_id):
                        user_option_data = {'rentalnumber': part_id}
                        try:
                            results = cursor.execute(make_query(user_option+'.sql'),
                                                     user_option_data)
                            cnx.commit()
                            connection.sendall("Successfully completed the operation!")
                        except mysql.connector.Error as err:
                            print user_option
                            print(err)
                            cnx.rollback()
                            connection.sendall("Error: database could not accept modification")
                    else:
                        print user_option
                        print "Error on input RentalNumber"
                        raise Exception("Invalid input for RentalNumber", )

                #---------------------------------------------------------
                # If no other input was needed to make the query,
                # just execute the query
                #---------------------------------------------------------
                elif (user_option == "ReportComputers"):
                    cursor.execute(make_query("ViewComputers.sql"))

                elif (user_option == "ReportParts"):
                    cursor.execute(make_query("ViewParts.sql"))

                elif (user_option == "ReportAccessories"):
                    cursor.execute(make_query("ViewAccessoryRentalNumbersByTypes.sql"))

                elif (user_option == "ReportSmallAccessories"):
                    cursor.execute(make_query("ViewSmallAccessories.sql"))

                else:
                    cursor.execute(make_query(user_option+'.sql'))

            #---------------------------------------------------------
            # Something went wrong with the SQL operation
            #---------------------------------------------------------
            except mysql.connector.Error as err:
                print(datetime.datetime.now())
                print "Command processed: " + user_option
                if not insert_data:
                    print part_id
                else:
                    print insert_data
                print "Error in SQL operation"
                print(err)
                print "\r\n"

                try:
                    cursor.fetchall()
                    #print "Something got stuck in the cursor"
                except Exception as err:
                    pass
    
                cursor.close()
                sys.stdout.flush()
                #connection.sendall("Database error caused operation to fail")

            #---------------------------------------------------------
            # Validation detected that a part of the input was bad
            #---------------------------------------------------------
            except Exception as message:
                print(datetime.datetime.now())
                print "Command processed: " + user_option
                if not insert_data:
                    print part_id
                else:
                    print insert_data
                print "Error in input"
                print(message)
                print "\r\n"

                try:
                    cursor.fetchall()
                    #print "Something got stuck in the cursor"
                except Exception as err:
                    pass

                cursor.close()
                sys.stdout.flush()
                #connection.sendall("Miscellaneous error caused operation to fail")
                
            #---------------------------------------------------------
            # Query was successful, so send the results to the client
            #---------------------------------------------------------
            else:
                try:
                    if user_option == 'ViewComputers':
                        ViewComputers(cursor, connection)
                    elif user_option == 'ViewComputerRentalNumber':
                        ViewComputers(cursor, connection)
                    elif user_option == 'ViewParts':
                        ViewParts(cursor, connection)
                    elif user_option == 'ViewPartsAndQty':
                        ViewPartsAndQty(cursor, connection)
                    elif user_option == "ViewOriginalSpecs":
                        ViewOriginalSpecs(cursor, connection)
                    elif user_option == 'ViewMonthHistory':
                        ViewDeliveries(cursor, connection)
                    elif user_option == 'ViewMonthDeliveryCount':
                        ViewMonthDeliveryCount(cursor, connection)
                    elif user_option == "ViewDeliverySpecs":
                        ViewDeliverySpecs(cursor, connection)
                    elif user_option == "ViewDeliveries":
                        ViewDeliveries(cursor, connection)
                    elif user_option == "ViewRentalUnitHistory":
                        ViewDeliveries(cursor, connection)
                    elif user_option == "ViewClients" or user_option == "FilterClients":
                        ViewClients(cursor, connection)
                    elif (user_option == "FilterDeliveries" or
                          user_option == "FindDelivery" or
                          user_option == "FilterDeliveriesName"):
                        ViewDeliveries(cursor, connection)
                    elif user_option == 'ViewComputersStatus':
                        ViewComputersStatus(cursor, connection)
                    elif user_option == 'ViewClientHistory':
                        ViewDeliveries(cursor, connection)
                    elif user_option == 'ViewAllExtended':
                        ViewDeliveries(cursor, connection)
                    elif user_option == 'ViewActiveDeliveries':
                        ViewDeliveries(cursor, connection)
                    elif user_option == 'ViewUrgentPull':
                        ViewDeliveries(cursor, connection)
                    elif user_option == 'ViewAccessoryRentalNumbersByTypes':
                        ViewAccessoryRentalNumbersByTypes(cursor, connection)
                    elif user_option == 'ViewAccessoriesAndQty':
                        ViewAccessoriesAndQty(cursor, connection)
                    elif user_option == 'FindOnHandParts':
                        FindOnHandParts(cursor, connection)
                    elif user_option == 'FindOnHandComputers' or user_option == 'Projection':
                        FindOnHandComputers(cursor, connection)
                    elif user_option == 'FindOnHandAccessories':
                        FindOnHandAccessories(cursor, connection)
                    elif user_option == 'FindListIDs':
                        FindListIDs(cursor, connection)
                    elif user_option == 'FindAvailablei7':
                        FindAvailablei7(cursor, connection)
                    elif user_option == 'FetchParts':
                        FetchParts(cursor, connection)
                    elif user_option == 'FetchComputers':
                        FetchComputers(cursor, connection)
                    elif (user_option == 'FetchCompleteComputers' or
                          user_option == 'FetchActiveCompleteComputers' or
                          user_option == 'FetchPulledComputers' or
                          user_option == 'FetchPendingComputers' or
                          user_option == 'ViewPullOutListUnits'):
                        FetchCompleteComputers(cursor, connection)
                    elif (user_option == 'FetchDeliveryAccessories' or
                          user_option == 'FetchActiveDeliveryAccessories' or
                          user_option == 'FetchPulledDeliveryAccessories' or
                          user_option == 'FetchPendingDeliveryAccessories' or
                          user_option == 'ViewPullOutListAcc'):
                        FetchDeliveryAccessories(cursor, connection)
                    elif user_option == 'FilterAccessories':
                        ViewAccessoryRentalNumbersByTypes(cursor, connection)
                    elif user_option == 'FilterParts' or user_option == 'FilterAvailableParts':
                        FetchParts(cursor, connection)
                    elif user_option == 'ViewLatestDeliveryVersion':
                        ViewLatestDeliveryVersion(cursor, connection)
                    elif user_option == 'FindClient':
                        FindClient(cursor, connection)
                    elif user_option == 'FindClientContactPerson':
                        FindClientContactPerson(cursor, connection)
                    elif user_option == 'ViewComputerParentDelivery':
                        ViewDeliveries(cursor, connection)
                    elif (user_option == 'ViewPullOuts' or
                          user_option == 'FetchPullOut'):
                        ViewPullOuts(cursor, connection)
                    elif user_option == 'GetPullOutList':
                        GetPullOutList(cursor, connection)
                    elif user_option == 'ViewCPUQty':
                        ViewCPUQty(cursor, connection)
                    elif user_option == 'TraceComputer':
                        TraceComputer(cursor, connection)
                    elif (user_option == 'ViewSmallAccessories' or
                          user_option == 'FilterSmallAccessories'):
                        ViewSmallAccessories(cursor, connection)
                    elif (user_option == 'FetchDeliveryPeripherals' or
                          user_option == 'FetchPendingPeripherals'):
                        FetchDeliveryPeripherals(cursor, connection)
                    elif user_option == 'ReportComputers':
                        ReportComputers(cursor, connection)
                    elif user_option == 'ReportAccessories':
                        ReportAccessories(cursor, connection)
                    elif user_option == 'ReportParts':
                        ReportParts(cursor, connection)
                    elif user_option == 'ReportSmallAccessories':
                        ReportSmallAccessories(cursor, connection)

                    #---------------------------------------------------------
                    # Process multi-query operations
                    # Commit results to database as all of these functions
                    # change the database contents
                    #---------------------------------------------------------
                    elif (user_option == 'InsertNewRentalComputer' or
                            user_option == 'EditComputer' or
                            user_option == 'InsertDeliverySpecs' or
                            user_option == 'InsertDeliveryAccessories' or
                            user_option == 'EditDelivery' or
                            user_option == 'ReturnDelivery' or
                            user_option == 'DeleteAccessory' or
                            user_option == 'EditAccessory' or
                            user_option == 'ReturnUnit' or
                            user_option == "InsertDeliveryPeripherals"):
                        InsertSQL(results, connection)
                        #print "\r\n"
                        cnx.commit()

                    #---------------------------------------------------------
                    # In case bad query name slipped through
                    #---------------------------------------------------------
                    else:
                        pass
                    
                except Exception as message:
					print(datetime.datetime.now())
					print "Command processed: " + user_option
					print(message)
					if not insert_data:
						print part_id
					else:
						print insert_data
                    connection.sendall("Error: couldn't retrieve database entries properly, please contact administrator")

            #---------------------------------------------------------
            # Disconnect from client to display results
            #---------------------------------------------------------
            #print "Disconnecting now\r\n"
            try:
                cursor.fetchall()
                #print "Something got stuck in the cursor"
            except Exception as err:
                pass 
            try:
                cursor.close()
            except Exception as err:
                print "Couldn't close the cursor"

            try:
                cnx.close()
            except Exception as err:
                pass

            connection.close()
            sys.stdout.flush()
            #--------------------end of loop----------------------------#
        try:
            cnx.close()
        except Exception as err:
            pass
        sys.stdout.flush()
