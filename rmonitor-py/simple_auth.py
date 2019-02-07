# userlist.txt should have this format
# (username), (password), (role)
# (username), (password), (role)
# ...

import datetime
import base64
import hashlib
import os
import mysql.connector
from controller_functions import make_query

def authenticate(user_cred):
    userlist = []
    for line in open('userlist.txt'):
        fline = [x.strip() for x in line.split(',')]
        userlist.append(fline)

    for user in userlist:
        if (user_cred[0] == user[0] and user_cred[1] == user[1]):
            return "{}\n{}".format(user[2], make_time_key())

    return ""

# Check if the inputs provided by the user match the credentials stored
# in the database
def authenticate_new(user_cred):
    dbconfig = {
                "database": "PCRental",
                "user": "logindb",
                "password": "correctstaplehorsebattery",
                "host": "127.0.0.1"
                }
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()

    # returns only the data of corresponding username
    cursor.execute(make_query("ViewLogin.sql"), {'username': user_cred[0]})
    for (Username, Password, Salt, Role) in cursor:
        # password hash matched
        if (isPassword(user_cred[1], Salt, Password)):
            # user not already logged in
            if not check_if_logged(Username, cnx):
                ChangeQuery({'username': Username}, "SetLoginStatusTrue")
                result = Role		

                cursor.close()
                cnx.close()
                #found a match
                return "{}\n{}".format(result, make_time_key())
            else:
                break

    cursor.close()
    cnx.close()
    
    # didn't find any
    return ""

# Checks if the user is already logged in to the system
# This function is only called by authenticate_new
def check_if_logged(username, sqlconn):
    # make local cursor different from parent function
    cursor = sqlconn.cursor()
    
    # checks if username is already in the table
    cursor.execute(make_query("CheckIfLogin.sql"), {'username': username})
    for (Username, foo) in cursor:
        # user is already logged in
        if Username == username:
            cursor.close()
            #found a match
            return True

    cursor.close()
    #didn't find it
    return False

def retrieveHash(user_cred):
    dbconfig = {
                "database": "PCRental",
                "user": "logindb",
                "password": "correctstaplehorsebattery",
                "host": "127.0.0.1"
                }
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()

    # returns only the data of corresponding username  
    cursor.execute(make_query("ViewLogin.sql"), {'username': user_cred[0]})
    for (Username, Password, Salt, Role) in cursor:
        return Salt, Password

    return ""

def ChangeQuery(user_option_data, query):
    dbconfig = {
                "database": "PCRental",
                "user": "logindb",
                "password": "correctstaplehorsebattery",
                "host": "127.0.0.1"
                }
    cnx = mysql.connector.connect(**dbconfig)
    cursor = cnx.cursor()

    try:
        cursor.execute(make_query(query+'.sql'), user_option_data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return "Successfully completed the operation!"
    except mysql.connector.Error as err:
        print(err)
        cursor.close()
        cnx.close()
        return ("Failed to complete the operation. {}").format(err)
 
def make_time_key():
    return datetime.datetime.now().strftime("%Y%m%d%I%M%S")

def getDigest(password, salt=None):
    if not salt:
        salt = base64.b64encode(os.urandom(32))
        digest = hashlib.sha512(salt + password).hexdigest()
        return salt, digest
    else:
        digest = hashlib.sha512(salt + password).hexdigest()
        return salt, digest

def isPassword(password, salt, digest):
    return getDigest(password, salt)[1] == digest  
