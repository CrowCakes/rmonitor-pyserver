#!/bin/sh

mysqldump -u root -pP@ss12345 --all-databases --routines | gzip > /home/logadmin/rmonitor-data/MySQLDB_`date +'%m-%d-%Y'`.sql.gz
