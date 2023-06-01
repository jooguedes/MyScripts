#!/bin/bash
#versao:1.0
#autor: João guedes
SQL=$1
cp $SQL dump.sql

export PGPASSWORD="postgres"

psql -U postgres -h localhost -c "select pg_terminate_backend(pid) from pg_stat_activity where pid <> pg_backend_pid() and datname = 'synsuit';";
psql -U postgres -h localhost -c "drop database if exists synsuit"
psql -U postgres -h localhost -c "create database synsuit"
cat dump.sql  |  grep "^COPY"  | sed "s/COPY erp./CREATE TABLE /g" | sed "s/,/ text,/g" | sed "s/) FROM stdin/ text)/g" | psql -U postgres -h localhost -d synsuit
# cat dump.sql | sed "s/COPY erp./COPY /g" | sed "s/\\\N//g" | psql -U postgres -h localhost -d synsuit
sed -i "s/COPY erp./COPY /g" dump.sql
sed -i "s/\\\N//g" dump.sql
sed -i '/SET/d' dump.sql
sed -i '/SELECT/d' dump.sql
psql -U postgres -h localhost -d synsuit -f dump.sql
rm dump.sql