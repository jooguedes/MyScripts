# Descompactar arquivos
for arquivo in $(ls *.gz); do
   gunzip $arquivo
done;

# Juntar todos os arquivos em um dump.sql
cat $(find . -type f -not -name "*.sql") > dump.sql

# Criar estrutura de tabelas
echo "" > estrutura.sql
for arquivo in $(find . -type f -not -name "*.sql"); do
   cat $arquivo | sed -n '/-- Table structure for table/,/-- Dumping data for table/p' >> estrutura.sql
done;

# Recriar banco de dados
mysql -uroot  -e "drop database if exists ispintegrator"
mysql -uroot  -e "create database ispintegrator"

# Restaurar banco de dados
mysql -uroot -f  ispintegrator  < estrutura.sql
mysql -uroot -f  ispintegrator  < dump.sql