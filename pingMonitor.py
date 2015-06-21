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
DB_HOST="localhost"

@ Username to use when interfacing with the database
DB_USER="default"

@ Password to use when interfacing with the database
DB_PASS="hunter2"

@ Name of the database
DB_NAME="myDatabase"

@ Whether to write every ping
WRITE_PINGS=true

@ Whether to write the average of all pings
WRITE_AVG=true

@Time to stop waiting for a response after sending a ping
TIMEOUT=1
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
	print name
	if name.startswith('http') or name.startswith('ssh') or name.startswith('ftp'):
		fname=name[name.find("://")+3:]
	print fname
	fname=fname.replace(".","_")
	return fname

def createDBTable(cursor,name):
	SQL_CREATE_COMMAND = "CREATE TABLE IF NOT EXISTS %s("%(name)
	SQL_CREATE_COMMAND += """idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx), pingTimes VARCHAR(16), datetime TIMESTAMP) ENGINE=InnoDB;
	"""
	print "COM: " + SQL_CREATE_COMMAND
	cursor.execute(SQL_CREATE_COMMAND)

def writeToDB(cursor,data,name):
	SQL_WRITE_COMMAND = """
		INSERT INTO %s (pingTimes)
		VALUES(%s);"""%(name,data)
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
	avg=0
	for t in out:
		avg += float(t)
	return (avg/len(out))

def processArgs():
	url="google.com"
	times=5
	for arg in sys.argv:
		if arg.startswith('url='):
			url=arg.split('=')[1]
		if arg.startswith('times='):
			times=arg.split('=')[1]
	return [url,str(times)]

def getPingOutput(url,time,timeout):
	CMD=['ping',url,'-c ' + str(time),'-W ' + str(timeout)]
	result = subprocess.check_output(CMD)
	return result

def pingIP(url,amt,timeout):
	out = getPingOutput(url,amt,timeout).split("\n")
	times=[]
	out = out[1:-5]
	for line in out:
		if '=' in line.lower():
			#times.append(line.split('=')[-1].split('ms')[0])
			times.append(float(line.split('=')[-1][:-3]))
		else:
			times.append(0)
	return times

def readIPs(db):
	ips=[]
	db.query("SELECT * FROM IP_LIST")
	res = db.use_result()
	ip=res.fetch_row(1)
	while ip!=():
		ips.append(ip[0][1])
		ip=res.fetch_row(1)
	print "IPs:", ips
	return ips

def main():
	try:
		cfg = Config.Config("pingMonitor.cfg")
	except OSError:
		# Really, it doesn't matter if we do this. The default settings don't have the correct information to work with the database
		resetCFGFile()
		cfg = Config.Config('pingMonitor.cfg')
	host = cfg.getOption("DB_HOST")
	user = cfg.getOption("DB_USER")
	pswd = cfg.getOption("DB_PASS")
	name = cfg.getOption("DB_NAME")
	#ips = open(cfg.getOption("IP_LIST")).read().split("\n")
	pings = cfg.getOption("PING_AMT")
	writePings = cfg.getOption("WRITE_PINGS")
	writeAvg = cfg.getOption("WRITE_AVG")
	timeout = cfg.getOption("TIMEOUT")
	db = MySQLdb.connect(host=host,user=user,passwd=pswd,db=name)
	cur = db.cursor()
	ips = readIPs(db);
	for ip in ips:
		fname = formatWebName(("http://" if not "://" in str(ip) else "")+str(ip))
		print "fname:",fname
		createDBTable(cur,fname)
		print "Pinging " + ip + "."
		times = pingIP(ip,pings,timeout)
		if writePings:
			print "Writing pings"
			for t in times:
				writeToDB(cur,t,fname)
		if writeAvg:
			print "Writing average"
			avg = getAverage(times)
			writeToDB(cur,avg,fname)
		db.commit()
	db.close()

if __name__ == '__main__':
	try:
		import MySQLdb
	except ImportError:
		from os import system
		if sys.platform.startswith("linux"):
			system("sudo apt-get install python-MySQLdb")
		import MySQLdb
	main()
