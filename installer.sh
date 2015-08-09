#!/bin/bash

function installDependency {
    sudo apt-get install "$1" || { exit 1; }
}

function execMySQL {
    mysql -u root -p "$1" -e "$2" "$3"
}

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

echo 'Creating pingmonitor database'
mysql -u root 0p $pass 'CREATE DATABASE pingmonitor;'

echo 'Creating IP_LIST'
execMySQL $pass 'CREATE TABLE IF NOT EXISTS IP_LIST(idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx), CompanyID INT, IP VARCHAR(16)) ENGINE=InnoDB;' pingmonitor

echo 'Creating CompanyList'
execMySQL $pass 'CREATE TABLE IF NOT EXISTS CompanyList(idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx),CompanyName VARCHAR(255)) ENGINE=InnoDB;' pingmonitor

echo 'Creating dataTable'
execMySQL $pass 'CREATE TABLE IF NOT EXISTS dataTable(idx INT NOT NULL AUTO_INCREMENT, PRIMARY KEY(idx),IP VARCHAR(16),pingTimes VARCHAR(16) datetime TIMESTAMP) ENGINE=InnoDB;' pingmonitor

