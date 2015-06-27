import subprocess
import sys,datetime

import Config

FAIL_MESSAGE = "request timed out"

CFG_DEFAULT="""
@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@ Ping Monitor Config file @
@@@@@@@@@@@@@@@@@@@@@@@@@@@@

@ File path to iplist
IP_LIST="~/Desktop/iplist.txt"

@ Amount of times to ping a server
PING_AMT=16

@ Host of database
DB_HOST="stratait.com"

@ Username to use when interfacing with the database
DB_USER="default"

@ Password to use when interfacing with the database
DB_PASS="hunter2"

@ Name of the database
DB_NAME="pingMonitorDB"

@ Whether to write every ping
WRITE_PINGS=true

@ Whether to write the average of all pings
WRITE_AVG=true
"""

def resetCFGFile():
	open('pingMonitor.cfg').write(CFG_DEFAULT)

def formatOutput(pOutput):
	fOut=[]
	for line in pOutput.splitlines()[1:-4]:
		if "=" not in line:
			fOut.append("0,0")
		else:
			fOut.append('1,' + int([line.rpartition('=')[-1]]))
	return '\n'.join(fOut)

def formatWebName(name):
	fname=name
	if name.startswith('http') or name.startswith('ssh') or name.startswith('ftp'):
		fname=name[name.find("://"):]
	fname=fname.replace(".","-")
	fname=fname[:fname.find("/")]
	return fname

def createDBTable(cursor,name):
	#TODO: Finish SQL_CREATE_COMMAND
	SQL_CREATE_COMMAND = """CREATE TABLE IF NOT EXISTS %s(
		index INT(0) AUTO_INCREMENT PRIMARY KEY,
		time VARCHAR(16),
		date VARCHAR(12)
		) ENGINE=InnoDB"""%(name)
	cursor.execute(SQL_CREATE_COMMAND)

def writeToDB(cursor,data,date,name):
	SQL_WRITE_COMMAND = """
		INSERT INTO %s (time,date)
		VALUES(%s,%s);"""%(name,date,data)
	cursor.execute(SQL_WRITE_COMMAND)

def formateDateTime():
	now = datetime.now()
	fdate = ""
	fdate += ("0" if now.month < 10 else "") + now.month + "-"
	fdate += ("0" if now.day < 10 else "") + now.day + "-"
	fdate += str(now.year)[2:] + "-"
	fdate += ("0" if now.hour < 10 else "") + now.hour + ":"
	fdate += ("0" if now.minute < 10 else "") + now.minute + ":"
	fdate += ("0" if now.second < 10 else "") + now.second + ":"
	return fdate

def getAverage(out):
	out = out.split('\n')[1:-5]
	times=[]
	avg=0
	for line in out:
		#if FAIL_MESSAGE not in line.lower():
		if '=' not in line.lower():
			times.append(line.split('=')[-1].split('ms')[0])
	for t in times:
		avg += float(t)
	return (avg/len(times))

def processArgs():
	url="google.com"
	times=5
	for arg in sys.argv:
		if arg.startswith('url='):
			url=arg.split('=')[1]
		if arg.startswith('times='):
			times=arg.split('=')[1]
	return [url,str(times)]

def getPingOutput(url,time):
	CMD=['ping',url,'-c ' + time]
	result = subprocess.check_output(CMD)
	return result

def pingIP(url,amt):
	out = getPingOutput(url,amt)
	times=[]
	for line in out:
		if '=' not in line.lower():
			times.append(line.split('=')[-1].split('ms')[0])
		else:
			times.append(0)
	return times

def main():
	try:
		cfg = Config.Config("pingMonitor.cfg")
	except OSError:
		resetCFGFile()
		cfg = Config.Config('pingMonitor.cfg')
	host = cfg.getOption("DB_HOST")
	user = cfg.getOption("DB_USER")
	pswd = cfg.getOption("DB_PASS")
	name = cfg.getOption("DB_NAME")
	ips = open(cfg.getOption("IP_LIST")).read().split("\n")
	pings = cfg.getOption("PING_AMT")
	writePings = cfg.getOption("WRITE_PINGS")
	writeAvg = cfg.getOption("WRITE_AVG")
	db = MySQLdb.connect(host=host,user=user,passwd=pswd,db=name)
	cur = db.cursor()
	for ip in ips:
		fname = formatWebName(ip)
		createDBTable(cur,fname)
		times = pingIP(ip)
		dt = formatDateTime()
		if writePings:
			for t in times:
				writeToDB(cur,t,dt)
		if writeAvg:
			avg = getAverage(times)
			writeToDB(cur,avg,dt)

if __name__ == '__main__':
	try:
		import MySQLdb
	except ImportError:
		from os import system
		if sys.platform.startswith("linux"):
			system("sudo apt-get install python-MySQLdb")
		import MySQLdb
	main()
