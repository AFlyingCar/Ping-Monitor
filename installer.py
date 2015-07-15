import os,sys,getpass,urllib2

try:
	import MySQLdb
except ImportError:
	print "Installing MySQLdb"
	if sys.platform.startswith("linux"):
		system("sudo apt-get instal python-MySQLdb")
	import MySQLdb

host="localhost"
usr=raw_input("User: ")
pass=getpass.getpass("Password: ")
name="pingmonitor"


print "Creating Database."
DB_CREATE_COMMAND = "CREATE DATABASE %s;"%(name)

db=MySQLdb.connect(username=usr,passwd=pass)
cur = db.cursor()

cur.execute(DB_CREATE_COMMAND)


print "Creating IP_LIST."
IPLIST_CREATE_COMMAND = "CREATE TABLE IF NOT EXISTS IP_LIST(idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx), CompanyID INT, IP VARCHAR(16)) ENGINE=InnoDB;"

cur.execute(IPLIST_CREATE_COMMAND")


print "Creating CompanyList."
COMPANYLIST_CREATE_COMMAND = "CREATE TABLE IF NOT EXISTS CompanyList (idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx), CompanyName VARCHAR(255)) ENGINE=InnoDB;"

cur.execute(COMPANYLIST_CREATE_COMMAND")


print "Creating dataTable."
DATATABLE_CREATE_COMMAND = "CREATE TABLE IF NOT EXISTS dataTable (idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx), IP VARCHAR(16), pingTimes VARCHAR(16), datetime TIMESTAMP) ENGINE=InnoDB;

cur.execute(DATATABLE_CREATE_COMMAND)



print "Downloading application."
url="https://raw.githubusercontent.com/AFlyingCar/Ping-Monitor/master/"

fileList=["Config.py","pingMonitor.py","argParser.py"]

for f in fileList:
	print "Downloading %s."%(f)
	data = urllib2.urlopen(url+f)
	open(f,'wb').write(data.read())

