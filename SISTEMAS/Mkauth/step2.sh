#!/bin/bash
#versao:3.2
#autor: Gileno Cordeiro Duarte
SQLMKAUTH=$1
DIRETORIOMIGRACAO=$2
SERVIDORCLIENTE=$3

#cria o datbase, exporta o sql do mkauth pega os ids dos portadores 
mysql -uroot  -e "drop database mkauth"
mysql -uroot  -e "create database mkauth"

#elimina o problema do compression 
sed -i "s/\`compression\`='tokudb_zlib'//g"  $SQLMKAUTH
mysql -uroot -f  mkauth  < $SQLMKAUTH
mysql -uroot  mkauth   < sql/Id_Portador.sql
mysql -uroot  mkauth -e "select id from sis_boleto" > ./ids

#remove  a palavra id do arquivos de ID
sed -i "s/id//g" ids 


# parte responsavel por pegar os IDs e chamar no sql exportaPortadores 
IDS=$(cat ids)

#cria o arquivo de backup do sql que exporta os portadores
cat sql/exportaportadores.sql > sql/exportaportadores.backup

for id in $IDS
do
   sed -i "s/{portador}/$id/g" sql/exportaportadores.sql
   mysql -u root mkauth < sql/exportaportadores.sql >> mkauth-portadores.csv
   cat sql/exportaportadores.backup > sql/exportaportadores.sql
done;
rm ./ids 

#MOVENDO ARQUIVOS PARA O DIRETORIO DA MIGRACAO DO MKAUTH
mv /tmp/mkauth-* ./$DIRETORIOMIGRACAO
mv mkauth-portadores.csv ./$DIRETORIOMIGRACAO

#ELIMINANDO AS QUEBRAS DE LINHAS E CONVERTENDO EM UTF-8
sed -i "s/\\\N//g" ./$DIRETORIOMIGRACAO/*.csv 
for i in $(ls $DIRETORIOMIGRACAO/*.csv); do iconv -f iso8859-1 -t utf-8 $i > $i.utf8; rm $i; done


#enviando para a máquina do cliente 
scp -P 13770 $DIRETORIOMIGRACAO/mkauth-*.csv.utf8 suporte@$SERVIDORCLIENTE:/tmp/
