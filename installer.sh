#!/bin/bash

# Install the specified dependency, and exit upon failure
function installDependency {
    sudo apt-get install "$1" || { exit 1; }
}

# Install the specified file in /var/www/, and exit upon failure
function installFile{
    sudo wget -t 10 -P /var/www/ http://raw.githubusercontent.com/AFlyingCar/Ping-Monitor/master/"$1" || { exit 1; }
}

if false; then
function execMySQL {
    mysql -u root -p "$1" -e "$2" "$3"
}
fi

read -p 'Enter the new password for the mysql database: ' pass

echo 'Updating repository list'
sudo apt-get update || { exit 1; }

echo 'Installing Apache'
installDependency apache2

echo 'Installing php5'
installDependency php5

echo 'Installing libapache2-mod-php5'
installDependency libapache2-mod-php5

echo 'Installing mysql'
installDependency "mysql-server --fix-missing"

echo 'Installing mysql-client'
installDependency mysql-client

echo 'Installing php5-mysql'
installDependency php5-mysql

echo 'Installing python-MySQLdb'
installDependency python-MySQLdb

echo 'Setting up mysql Server'
mysql -u root -p $pass < setup.sql

echo 'Installing pingMonitor...'
#Read all filenames from manifest.txt, and install each one
filelist="`wget -qO- http://raw.githubusercontent.com/AFlyingCar/Ping-Monitor/master/MANIFEST`"
while read -r line; do
    echo "Installing $line..."
    installFile "$line"
done <<< "$filelist"





# Skipping all of the old sql stuff, since that has now been moved to install.sql
if false; then
echo 'Creating pingmonitor database'
mysql -u root 0p $pass 'CREATE DATABASE pingmonitor;'

echo 'Creating IP_LIST'
execMySQL $pass 'CREATE TABLE IF NOT EXISTS IP_LIST(idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx), CompanyID INT, IP VARCHAR(16)) ENGINE=InnoDB;' pingmonitor

echo 'Creating CompanyList'
execMySQL $pass 'CREATE TABLE IF NOT EXISTS CompanyList(idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx),CompanyName VARCHAR(255)) ENGINE=InnoDB;' pingmonitor

echo 'Creating dataTable'
execMySQL $pass 'CREATE TABLE IF NOT EXISTS dataTable(idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx),IP VARCHAR(16),pingTimes VARCHAR(16) datetime TIMESTAMP) ENGINE=InnoDB;' pingmonitor

fi

