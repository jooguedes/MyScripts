#!/bin/bash
#versao:1.0
#autor: João guedes
SQL=$1
cp $SQL dump.sql

export PGPASSWORD="postgres"

mysql -uroot  -e "drop database if exists ispcloud"
mysql -uroot  -e "create database ispcloud"

cat dump.sql  |  sed 's/COLLATE=utf8mb4_0900_ai_ci//g' | mysql -uroot -f ispcloud
# cat dump.sql  |  sed -n '/-- Table structure for table/,/-- Dumping data for table/p' | sed 's/COLLATE=utf8mb4_0900_ai_ci//g' | mysql -uroot -f ispcloud

rm dump.sql