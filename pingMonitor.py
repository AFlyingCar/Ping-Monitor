# Ping Monitor
# Stores the default configuration file
# Knows how to grab a list of ips from a database, ping each one, and write the data to a table in the same database

import subprocess
import sys,datetime,os

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

# Reset the CFG file with the defaults defined above.
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
        fname=name[name.find("://")+3:]
    fname=fname.replace(".","_")
    return fname

# Creates a database table of 'name' if it doesn't already exist
def createDBTable(cursor,name):
    SQL_CREATE_COMMAND = "CREATE TABLE IF NOT EXISTS %s("%(name)
    SQL_CREATE_COMMAND += """idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx), pingTimes VARCHAR(16), datetime TIMESTAMP) ENGINE=InnoDB;
    """
    cursor.execute(SQL_CREATE_COMMAND)

# Store 'data' in table 'name' by 'ip'
def writeToDB(cursor,data,name,ip):
    SQL_WRITE_COMMAND = """
        INSERT INTO %s (IP,pingTimes)
        VALUES('%s','%s');"""%(name,ip,data)
    cursor.execute(SQL_WRITE_COMMAND)

# Format the current date and time
# DEPRECATED: Use MySQL's DATETIME type instead
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

# Compute the average of a list of times
def getAverage(out):
    avg=0
    for t in out:
        avg += float(t)
    return (avg/len(out))

# Get arguments from the command line.
# DEPRECATED: Use the Config file and IP_LIST table instead
def processArgs():
    url="google.com"
    times=5
    for arg in sys.argv:
        if arg.startswith('url='):
            url=arg.split('=')[1]
        if arg.startswith('times='):
            times=arg.split('=')[1]
    return [url,str(times)]

# Get the output of pinging 'url' 'time' times. Stop trying after 'timeout' time has passed
# If an error occurs, return ""
def getPingOutput(url,time,timeout):
    CMD=['ping',url,'-c ' + str(time),'-W ' + str(timeout)]
    try:
        result = subprocess.check_output(CMD)
    except subprocess.CalledProcessError as e:
        print "Ping to " + url + " failed."
        print e
        result = ""
    return result

# Gets the output of pinging a url and pulls each ping time out of the output
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

# Reads IP_LIST and returns the list of ips to ping
def readIPs(db):
    ips=[]
    db.query("SELECT * FROM IP_LIST")
    res = db.use_result()
    ip=res.fetch_row(1)
    while ip!=():
        ips.append(ip[0][2])
        ip=res.fetch_row(1)
    return ips

def main():
    # Open up the Config file. If it doesn't exist, reset it and exit
    try:
        cfg = Config.Config("pingMonitor.cfg")
    except OSError:
        print "Unable to find pingMonitor.cfg, creating default file."
        resetCFGFile()
        print "Generated config file. Please edit it and place in the correct information."
        return
        cfg = Config.Config('pingMonitor.cfg')

    # Place config values into variables
    host = cfg.getOption("DB_HOST")
    user = cfg.getOption("DB_USER")
    pswd = cfg.getOption("DB_PASS")
    name = cfg.getOption("DB_NAME")
    pings = cfg.getOption("PING_AMT")
    writePings = cfg.getOption("WRITE_PINGS")
    writeAvg = cfg.getOption("WRITE_AVG")
    timeout = cfg.getOption("TIMEOUT")

    if timeout < 1: 
        print "Warning! Timeout values less than 1 can cause the program to hang on unresponsive URLs."
        if raw_input("Use timeout="+str(timeout)+" anyway?(y/n) ") != 'n':
            timeout = 1

    # Open the database and get the list of ips
    db = MySQLdb.connect(host=host,user=user,passwd=pswd,db=name)
    cur = db.cursor()

    os.system("touch ./.pmlock") # Create lock file.

    while(os.path.exists("./.pmlock")):
        ips = readIPs(db);

        # For each ip, ping it and write it to the database
        for ip in ips:
            fname = formatWebName(("http://" if not "://" in str(ip) else "")+str(ip))
            #createDBTable(cur,fname)
            print "Pinging " + ip + "."
            times = pingIP(ip,pings,timeout)
            if writePings:
                print "Writing pings"
                for t in times:
                    writeToDB(cur,t,"dataTable",ip)
            # Only commenting out old functionality in case we want to go back to it
            # We probably don't...
            #       writeToDB(cur,t,fname)
            if writeAvg:
                print "Writing average"
                avg = getAverage(times)
                writeToDB(cur,avg,fname)
            db.commit()
    db.close()

# Run main(), but first check to see if MySQLdb is installed, as it is required for this program to work
if __name__ == '__main__':
    try:
        import MySQLdb
    except ImportError:
        from os import system
        if sys.platform.startswith("linux"):
            system("sudo apt-get install python-MySQLdb")
        import MySQLdb
    main()
