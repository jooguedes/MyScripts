#!/bin/bash
#versao:1.0
#autor: João Guedes de Moura Junior
sudo chmod 777 ./*

# Passar a senha do postgres
export PGPASSWORD="12345678"

# Remover o arquivo create caso este exista
sudo rm create.sql 

# Criar o create.sql contendo o script de criação do banco de dados
for arquivos in $(ls *.csv)
do 
  NOME=$(echo $arquivos | cut -d "." -f 2);
  echo "" >> create.sql
  echo "create table $NOME(" >> create.sql;   
  head -n 1 $arquivos | sed "s/;/ text,/g" >> create.sql;
  echo "text);" >> create.sql;
done;

# remover os arquivos no tmp
sudo rm /tmp/*.*.csv

# Copiar arquivos para o diretório TMP
for i in *.*.csv; do cp $i /tmp/; done 

# Criar banco de dados
psql -U postgres -h localhost -c "select pg_terminate_backend(pid) from pg_stat_activity where pid <> pg_backend_pid() and datname = 'dbcontrollr';";
psql -U postgres -h localhost -c "drop database dbcontrollr";
psql -U postgres -h localhost -c "create database dbcontrollr";
psql -U postgres -d dbcontrollr -h localhost -c "SET client_encoding = 'UTF8'"
psql -U postgres -d dbcontrollr -h localhost -f create.sql

# Copiar dados das tabelas csv no tmp para o banco de dados
for arquivos in $(ls *.csv)
do 
  sed -i '1d' /tmp/$arquivos;
  NOME=$(echo $arquivos | cut -d "." -f 2);
  psql -U postgres -h localhost -d dbcontrollr -c "COPY $NOME FROM '/tmp/$arquivos' DELIMITER ';' CSV"
done;

# Extrair dados e envia-los para o /tmp/
psql -U postgres -d dbcontrollr -h localhost -f exporDados.sql

# Remover essa pasta coso ela exista Controllr_Import
rm -r ./Controllr_Import

# Criar a pasta Controllr_Import
mkdir ./Controllr_Import

# Mover arquivos do tmp para a pasta Controllr_Import
mv /tmp/controllr-* ./Controllr_Import/

# Remover \N das células em branco
sed -i "s/\\\N//g" ./Controllr_Import/*.csv

echo "Script finalizado! Arquivos extraídos econtram-se no diretorio ./Controllr_Import"