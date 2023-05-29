#!/bin/bash
#autor:gileno cordeiro duarte
#07/04/2023
#$1 - backup $2 - script para extrair os dados
DB=$(cat $1 | grep Database:  | awk -F: '{print$3}')

echo "Criando Database..."
sudo mysql -uroot  -e "drop database $DB"
sudo mysql -uroot  -e "create database $DB"
echo "Restaurando banco de dados.."
sudo mysql -uroot -f  $DB  < $1
sudo rm /tmp/bemtevi-*
sudo  mysql -uroot $DB < $2
sudo mkdir arquivos_importacao
cp /tmp/bemtevi-* arquivos_importacao/
sed -i "s/\\\N//g" arquivos_importacao/*.csv 





