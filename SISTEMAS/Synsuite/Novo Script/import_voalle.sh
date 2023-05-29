#!/bin/bash
#versao:1.0
#autor: João guedes
SQL=$1
cp $SQL dump.sql

export PGPASSWORD="postgres"

psql -U postgres -h localhost -c "drop database if exists synsuit"
psql -U postgres -h localhost -c "create database synsuit"
cat dump.sql  |  grep "^COPY"  | sed "s/COPY erp./CREATE TABLE /g" | sed "s/,/ text,/g" | sed "s/) FROM stdin/ text)/g" | psql -U postgres -h localhost -d synsuit
cat | sed "s/COPY erp./COPY /g" | sed "s/\\\N//g" | psql -U postgres -h localhost -d synsuit -f dump.sql
rm dump.sql