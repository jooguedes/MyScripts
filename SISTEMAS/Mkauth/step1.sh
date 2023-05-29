#!/bin/bash
#versão 1.0
DIA=$(date +%d-%y)
ARQUIVOMKAUTH=$1
mkdir mkauth$DIA
mv $ARQUIVOMKAUTH mkauth$DIA

cd mkauth$DIA

tar xvf $ARQUIVOMKAUTH

#remove a extensao para fazer o cd do diretório
#NOEXTENSIONNAME=$(echo $ARQUIVOMKAUTH | cut -f 1 -d'.' ) 
#echo $NOEXTENSIONNAME

#cd mk-auth/dados/$NOEXTENSIONNAME/

#cat *.sql > db.sql
#docker run --detach --name some-mariadb --env MARIADB_USER=gileno --env MARIADB_PASSWORD=password --env MARIADB_ROOT_PASSWORD=password  mariadb:latest

#docker exec -i some-mariadb /bin/bash -c 'mysql -uroot -ppassword -e "create database mkauth"'

#docker exec -i some-mariadb /bin/bash -c 'mysql -uroot -ppassword mkauth' < db.sql

#docker exec -i some-mariadb /bin/bash -c 'mysql -uroot -ppassword mkauth ' < /home/gileno/Documents/Trabalho/Scripts_Automacao/first.sql







