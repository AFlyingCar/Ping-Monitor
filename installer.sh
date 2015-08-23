#!/bin/bash

# Install the specified dependency, and exit upon failure
function installDependency {
    sudo apt-get install "$1" || { exit 1; }
}

# Install the specified file in /var/www/, and exit upon failure
function installFile{
    sudo wget -t 10 -P /var/www/ http://raw.githubusercontent.com/AFlyingCar/Ping-Monitor/master/"$1" || { exit 1; }
}

# Assume that all extra parameters are -u or --upgrade
# It doesn't matter, because the same operations take place
if [[ $# -eq 0 ]]; then
   read -p 'Enter the new password for the mysql database: ' pass
else
   read -p 'Enter the password for the mysql database: ' pass
fi

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

