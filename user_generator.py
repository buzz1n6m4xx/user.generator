#!/usr/bin/env python

"""
This program generates user names based on famous inventors, innovators, scientists etc.
 (https://github.com/docker/docker-ce/blob/523cf7e71252013fbb6a590be67a54b4a88c1dae/components/engine/pkg/namesgenerator/names-generator.go)
 and common first names over the last 100 years. Generated users can be exported to a CSV file for further usage.
"""

__author__ = "buzz1n6m4xx"
__status__ = "Production"
__version__ = "0.1"


# =============================================================================
#  MODULES
# =============================================================================

import configparser
import csv
from os import getcwd
import os
import platform
import random
import secrets
import string
from sys import exit
from ldap3 import Server, Connection, ALL
# https://ldap3.readthedocs.io/en/latest/tutorial_intro.html

sysos = platform.system()

if sysos == "Windows":
    import win32api
    import win32net
    import win32netcon
    localhost = win32api.GetComputerName()


# =============================================================================
#  VARIABLES
# =============================================================================

# IMPORT CONFIG FILE
config = configparser.ConfigParser()
config.read("ug_config.ini")

# SYSTEM INFO
sysinfo = platform.uname()
directory = getcwd()

# TEXT OPTIONS
txtcolreset = "\x1b[0;0m"
txtcolgr = "\x1b[1;32m"
txtcolbd = "\x1b[1m"

# CSV FILE SETTINGS
csvfilename = config["CSV Options"]["csv filename"]
csvfilelocal = config["CSV Options"]["csv filename for local users"]
csvfilead = config["CSV Options"]["csv filename for ad users"]
csvfileldap = config["CSV Options"]["csv filename for ldap users"]
csvhead = ["FirstName", "LastName", "FullName"]
csvlocalhead = ["FullName", "Name", "Password"]
csvadhead = ["displayName", "givenName", "sn", "sAMAccountName",
             "userPrincipalName", "password"]
csvldaphead = ["displayName", "givenname", "surname", "uid", "password"]

# USER OPTIONS
maxusers = int(config["User Options"]["max users"])

# USER ATTRIBUTES
userData = {}
givenname = ["Aaron","Abigail","Adam","Alan","Albert","Alexander","Alexis","Alice","Amanda","Amber","Amy","Andrea","Andrew","Angela","Ann","Anna","Anthony","Arthur","Ashley","Austin","Barbara","Benjamin","Betty","Beverly","Billy","Bobby","Bradley","Brandon","Brenda","Brian","Brittany","Bruce","Bryan","Carl","Carol","Carolyn","Catherine","Charles","Charlotte","Cheryl","Christian","Christina","Christine","Christopher","Cynthia","Daniel","Danielle","David","Deborah","Debra","Denise","Dennis","Diana","Diane","Donald","Donna","Doris","Dorothy","Douglas","Dylan","Edward","Elizabeth","Emily","Emma","Eric","Ethan","Eugene","Evelyn","Frances","Frank","Gabriel","Gary","George","Gerald","Gloria","Grace","Gregory","Hannah","Harold","Heather","Helen","Henry","Isabella","Jack","Jacob","Jacqueline","James","Janet","Janice","Jason","Jean","Jeffrey","Jennifer","Jeremy","Jerry","Jesse","Jessica","Joan","Joe","John","Johnny","Jonathan","Jordan","Jose","Joseph","Joshua","Joyce","Juan","Judith","Judy","Julia","Julie","Justin","Karen","Katherine","Kathleen","Kathryn","Kayla","Keith","Kelly","Kenneth","Kevin","Kimberly","Kyle","Larry","Laura","Lauren","Lawrence","Linda","Lisa","Logan","Louis","Madison","Margaret","Maria","Marie","Marilyn","Mark","Martha","Mary","Matthew","Megan","Melissa","Michael","Michelle","Nancy","Natalie","Nathan","Nicholas","Nicole","Noah","Olivia","Pamela","Patricia","Patrick","Paul","Peter","Philip","Rachel","Ralph","Randy","Raymond","Rebecca","Richard","Robert","Roger","Ronald","Rose","Roy","Russell","Ruth","Ryan","Samantha","Samuel","Sandra","Sara","Sarah","Scott","Sean","Sharon","Shirley","Sophia","Stephanie","Stephen","Steven","Susan","Teresa","Terry","Theresa","Thomas","Timothy","Tyler","Victoria","Vincent","Virginia","Walter","Wayne","William","Willie","Zachary"]
surname = ["Albattani","Agnesi","Allen","Almeida","Antonelli","Archimedes","Ardinghelli","Aryabhata","Austin","Babbage","Banach","Banzai","Bardeen","Bartik","Bassi","Beaver","Bell","Benz","Bhabha","Bhaskara","Black","Blackburn","Blackwell","Bohr","Booth","Borg","Bose","Bouman","Boyd","Brahmagupta","Brattain","Brown","Buck","Burnell","Cannon","Carson","Cartwright","Carver","Cerf","Chandrasekhar","Chaplygin","Chatelet","Chatterjee","Chaum","Chebyshev","Clarke","Cohen","Colden","Cori","Cray","Curie","Curran","Darwin","Davinci","Dewdney","Dhawan","Diffie","Dijkstra","Dirac","Driscoll","Dubinsky","Easley","Edison","Einstein","Elbakyan","Elgamal","Elion","Ellis","Engelbart","Euclid","Euler","Faraday","Feistel","Fermat","Fermi","Feynman","Franklin","Gagarin","Galileo","Galois","Ganguly","Gates","Gauss","Germain","Goldberg","Goldstine","Goldwasser","Golick","Goodall","Gould","Greider","Grothendieck","Haibt","Hamilton","Haslett","Hawking","Heisenberg","Hellman","Hermann","Herschel","Hertz","Heyrovsky","Hodgkin","Hofstadter","Hoover","Hopper","Hugle","Hypatia","Ishizaka","Jackson","Jang","Jemison","Jennings","Jepsen","Johnson","Joliot","Jones","Kalam","Kapitsa","Kare","Keldysh","Keller","Kepler","Khayyam","Khorana","Kilby","Kirch","Knuth","Kowalevski","Lalande","Lamarr","Lamport","Leakey","Leavitt","Lederberg","Lehmann","Lewin","Lichterman","Liskov","Lovelace","Lumiere","Mahavira","Mandela","Margulis","Matsumoto","Maxwell","Mayer","Mccarthy","Mcclintock","Mclaren","Mclean","Mcnulty","Meitner","Mendel","Mendeleev","Meninsky","Merkle","Mestorf","Mirzakhani","Montalcini","Moore","Morse","Moser","Murdock","Napier","Nash","Neumann","Newton","Nightingale","Nobel","Noether","Northcutt","Noyce","Panini","Pare","Pascal","Pasteur","Payne","Perlman","Pike","Poincare","Poitras","Proskuriakova","Ptolemy","Raman","Ramanujan","Rhodes","Ride","Ritchie","Robinson","Roentgen","Rosalind","Rubin","Saha","Sammet","Sanderson","Satoshi","Shamir","Shannon","Shaw","Shirley","Shockley","Shtern","Sinoussi","Snowden","Snyder","Solomon","Spence","Stonebraker","Sutherland","Swanson","Swartz","Swirles","Taussig","Tereshkova","Tesla","Tharp","Thompson","Thunberg","Torvalds","Tu","Turing","Varahamihira","Vaughan","Villani","Visvesvaraya","Volhard","Wescoff","Wilbur","Wiles","Williams","Williamson","Wilson","Wing","Wozniak","Wright","Wu","Yalow","Yonath","Zhukovsky"]

# PASSWORD SETTINGS
passwdchar = string.ascii_letters + string.digits
passwdlen = int(config["Password Options"]["password lenght"])

# AD CONNECTION SETTINGS
ADDomain = config["Active Directory Connection"]["ad domain name"]
ADServer = config["Active Directory Connection"]["ad domain controller"]
ADUser = config["Active Directory Connection"]["ad bind user"]
ADPwd = config["Active Directory Connection"]["ad bind password"]
ADBase = config["Active Directory Connection"]["ad base dn"]

# LDAP CONNECTION SETTINGS
LDAPServer = config["LDAP Connection"]["ldap server"]
LDAPUser = config["LDAP Connection"]["ldap bind user"]
LDAPPwd = config["LDAP Connection"]["ldap bind password"]
LDAPBase = config["LDAP Connection"]["ldap base dn"]


# =============================================================================
#  FUNCTIONS
# =============================================================================

def exportCsv(exportfilename):
    """ Prepare Export File """

    if os.access(exportfilename, os.F_OK):
        exfile = input(txtcolreset + "The file \"" + exportfilename + "\" already exists." + txtcolgr + "\nDo you want to overwrite the existing file? (y/n): ")
        while exfile not in {"y", "Y", "n", "N"}:
            exfile = input(txtcolreset + "Please enter a valid option." + txtcolgr + "\nDo you want to overwrite the existing file? (y/n): ")
        if exfile in ("y", "Y"):
            try:
                csvfile = open(exportfilename, "w", newline="")
                csvwriter = csv.writer(csvfile)
                return csvwriter
            except PermissionError:
                print ("\nPermission denied: File \"" + exportfilename + "\" is inaccessible.")
                print ("Close the file or ensure you have appropriate permissions at \"" + directory + "\"")
                exit()
        if exfile in ("n", "N"):
            print ("\nPlease rename the file \"" + exportfilename + "\" and restart the program.")
            exit()
    else:
        try:
            csvfile = open(exportfilename, "w", newline="")
            csvwriter = csv.writer(csvfile)
            return csvwriter
        except PermissionError:
            print ("\nPermission denied to access file \"" + exportfilename + "\"")
            print ("\nClose the file or ensure you have write permissions in " + directory)
            exit()

def userCount():
    """ User Count Validation """

    try:
        count = int(input(txtcolgr + "How many users should be generated? "))
    except ValueError:
        print(txtcolreset + "\nInvalid Input. \nPlease enter a number between 0 and " + str(maxusers) + ".")
        return userCount()
    if (count < 0) or (count > maxusers):
        print(txtcolreset + "\nUser creation is limited to max. " + str(maxusers) + " accounts.\nPlease enter a number between 0 and " + str(maxusers) + ".")
        return userCount()              # return is important otherwise the return statement below return count returns None
    if (count >= 0) and (count <= maxusers):
        return count

def restartMenu(restart):
    """ Restart Program Function """

    while restart not in {"y", "Y", "n", "N"}:                       # allow only valid options
        restart = input("Please enter a valid option. Return to Menu? (y/n): ")

    if restart in ("y", "Y"):
        init()

    if restart in ("n", "N"):
        print(txtcolreset + "\nBye")
        exit()

def generateUser():
    """ Generate Users """

    cgn = random.choice(givenname)
    csn = random.choice(surname)
    ccn = csn + " " + cgn
    countgn = cgn[:1]
    countsn = csn[:7]
    csam = countsn + countgn
    return cgn, csn, ccn, csam

def generatePasswd():
    """ Generate Passwords """

    passwd = "".join(secrets.choice(passwdchar) for i in range(passwdlen))
    return passwd

def callOption(option):
    """ Main Function """

    while option not in {"1", "2", "3", "4", "5"}: # allow only valid options
        option = input(txtcolgr + "\nPlease enter a valid option: 1, 2, 3, 4 or 5: ")

    if option == "1":

        # Get user count
        count = userCount()
        print("\n")

        # Create file and write header
        csvwriter = exportCsv(csvfilename)
        csvwriter.writerow(csvhead)

        for x in range(count):

            # Prepare attributes
            cgn, csn, ccn, csam = generateUser()

            # Write user to file
            csvrows = [cgn, csn, ccn]
            csvwriter.writerow(csvrows)

        print(txtcolreset + "\n" + str(count) + " Users have been generated and exported to: \n" + txtcolgr + "\"" + directory + "\\" + csvfilename + "\"")
        restart = input(txtcolgr + "\nReturn to Menu? (y/n): ")
        restartMenu(restart)

    if option == "2":

        if sysos == "Windows":

            # Get user count
            count = userCount()
            print("\n")

            # Create file and write header
            csvwriter = exportCsv(csvfilelocal)
            csvwriter.writerow(csvlocalhead)

            for x in range(count):

                # Prepare attributes
                cgn, csn, ccn, csam = generateUser()
                passwd = generatePasswd()

                # Create local Windows user
                userData["name"] = csam
                userData["full_name"] = ccn
                userData["password"] = passwd
                userData["flags"] = win32netcon.UF_NORMAL_ACCOUNT | win32netcon.UF_SCRIPT  # specifies the type of account to create, UF_SCRIPT is necessary
                userData["priv"] = win32netcon.USER_PRIV_USER  # controls the privileges of the new user, a normal user
                win32net.NetUserAdd(localhost, 2, userData)  # Create user corresponding to PyGROUP_INFO_2

                # Join user to group
                groupData = [{"domainandname": localhost+"\\"+csam}]
                win32net.NetLocalGroupAddMembers(localhost, "Users", 3, groupData)  # Adds user to a local group
                print(txtcolreset + "User " + txtcolgr + csam + txtcolreset + " has been created on " + txtcolgr + localhost)

                # Write user to file
                csvrows = [ccn, csam, passwd]
                csvwriter.writerow(csvrows)

            print("\n" + txtcolreset + str(count) + " Users have been generated and exported to " + txtcolgr + "\"" + directory + "\\" + csvfilename + "\"")
            restart = input(txtcolgr + "\nReturn to Menu? (y/n): ")
            restartMenu(restart)

        else:
            # If Linux or Mac is used, this option 2 is not possible
            print(txtcolreset + "\nYour current system platform doesn't meet the requirements.\nYour system must be Windows-based to create local Windows users.\n")
            print("Current System Platform: " + txtcolgr + sysos + txtcolreset)
            print("\nHostname: " + sysinfo.node)
            print("System  : " + sysinfo.system)
            print("Release : " + sysinfo.release)
            print("Version : " + sysinfo.version)

            restart = input("\nReturn to Menu? (y/n): ")
            restartMenu(restart)

    if option == "3":

        # Get user count
        count = userCount()
        print("\n")

        # Create file and write header
        csvwriter = exportCsv(csvfilead)
        csvwriter.writerow(csvadhead)

        # AD connection
        server = Server(ADServer, use_ssl = True, get_info=ALL) # SSL and Port 636 are needed to set AD passwords
        conn = Connection(server, ADUser, ADPwd, auto_bind=True)
        conn.start_tls() # needed to set AD passwords

        for x in range(count):

            # Prepare attributes
            cgn, csn, ccn, csam = generateUser()
            passwd = generatePasswd()

            # Create AD user
            cupn = cgn + "." + csn + "@" + ADDomain
            userdn = "CN="+csam+","+ADBase
            conn.add("cn=" + csam + "," + ADBase, "User", {"givenName": cgn, "sn": csn, "displayName": ccn, "sAMAccountName": csam, "userPrincipalName": cupn})
            print(txtcolreset + "User " + txtcolgr + csam + txtcolreset + " has been created in " + txtcolgr + ADBase)
            
            # Set password (differently as there is no AD attribute to store the password)
            conn.extend.microsoft.modify_password(userdn, passwd)
            print(txtcolreset + "Password for User " + txtcolgr + csam + txtcolreset + " has been set")

            # Write user to file
            csvrows = [ccn, cgn, csn, csam, cupn, passwd]
            csvwriter.writerow(csvrows)

        # Disconnect
        conn.unbind()

        print("\n" + txtcolreset + str(count) + " Users have been generated and exported to " + txtcolgr + "\"" + directory + "\\" + csvfilename + "\"")
        restart = input(txtcolgr + "\nReturn to Menu? (y/n): ")
        restartMenu(restart)

    if option == "4":

        count = userCount()
        print("\n")

        # Get user count
        csvwriter = exportCsv(csvfileldap)
        csvwriter.writerow(csvldaphead)

        # LDAP connection
        server = Server(LDAPServer, get_info=ALL)
        conn = Connection(server, LDAPUser, LDAPPwd, auto_bind=True)

        for x in range(count):

            # Prepare attributes
            cgn, csn, ccn, csam = generateUser()
            passwd = generatePasswd()

            # Create LDAP user
            conn.add("cn=" + csam + "," + LDAPBase, "inetOrgPerson", {"givenName": cgn, "sn": csn, "displayName": ccn, "uid": csam, "userPassword": passwd})
            print(txtcolreset + "User " + txtcolgr + csam + txtcolreset + " has been created in " + txtcolgr + LDAPBase)

            # Write user to file
            csvrows = [ccn, cgn, csn, csam, passwd]
            csvwriter.writerow(csvrows)

        # Disconnect
        conn.unbind()

        print("\n" + txtcolreset + str(count) + " Users have been generated and exported to " + txtcolgr + "\"" + directory + "\\" + csvfilename + "\"")
        restart = input(txtcolgr + "\nReturn to Menu? (y/n): ")
        restartMenu(restart)

    if option == "5":
        exit()

def init():
    """ Init/Start Function """

    print(txtcolreset)
    print(txtcolbd + "\nUser Generator / Creator")
    print("************************")
    print(txtcolreset + "\nThis program generates users based on famous inventors, innovators, scientists etc.\nFirst names are based on the most common first names over the last 100 years.")
    print("\nYou can generate users, create them in Active Directory, in a LDAP-based directory or locally.\nAll user details will be exported to a CSV file.")
    print(txtcolgr + "\nSelect an option to continue: " + txtcolreset)
    print("\n (1) Generate & Export Users to CSV File")
    print(" (2) Generate & Create Local Users (Windows)")
    print(" (3) Generate & Create Active Directory Users")
    print(" (4) Generate & Create LDAP Users")
    print(" (5) Quit Program")

    option = input(txtcolgr + "\n (1-5) : ")
    callOption(option)


# =============================================================================
#  PROGRAM START
# =============================================================================

init()
