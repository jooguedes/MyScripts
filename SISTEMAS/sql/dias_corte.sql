select c.login, c.dias_corte from sis_cliente c INTO OUTFILE '/tmp/mkauth-clientes-atvados-dias_cortes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
;