#!/bin/bash
#versao:2.0
#autor: João Guedes
BCK=$1

sudo chmod 777 * 

iconv -f ISO-8859-1 -t UTF-8 $BCK > Bbackup.sql

mysql -uroot  -e "drop database if exists scut"
mysql -uroot  -e "create database scut"

mysql -uroot -f scut < Bbackup.sql --ignore-column=instrucoes_linha1 --ignore-column=instrucoes_linha5