select 1,login,cpf_cnpj,formapag,tipo,descricao,processamento,datavenc,
        datapag,titulo,nossonum,valor,valorpag,valorger,geranfe,codigo_carne,linhadig,'',status,calculado, numconta
from vtab_titulos where deltitulo=0 and numconta={portador}  order by codigo_carne,titulo INTO OUTFILE '/tmp/mkauth-titulos-{portador}.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select 1,login,cpf_cnpj,formapag,tipo,descricao,processamento,datavenc,
        datapag,titulo,nossonum,valor,valorpag,valorger,geranfe,codigo_carne,linhadig,'',status,calculado, numconta
from vtab_titulos where deltitulo=1 and numconta={portador} order by codigo_carne,titulo INTO OUTFILE '/tmp/mkauth-titulos-removidos-{portador}.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select * from sis_boleto \G;
select * from sis_provedor \G;




"""select 1,login,cpf_cnpj,formapag,tipo,descricao,processamento,datavenc,
        datapag,titulo,nossonum,valor,valorpag,valorger,geranfe,codigo_carne,linhadig,'',status,calculado, numconta
from vtab_titulos where deltitulo=0 and numconta=2 and date(processamento) > '2022-08-01' order by codigo_carne,titulo INTO OUTFILE '/tmp/mkauth-titulos-2-a-partir-do-mes-8.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



select 1,login,cpf_cnpj,formapag,tipo,descricao,processamento,datavenc,
        datapag,titulo,nossonum,valor,valorpag,valorger,geranfe,codigo_carne,linhadig,'',status,calculado, numconta
from vtab_titulos where deltitulo=0 and numconta=1  and  valorpag is not null and datapag is not null  order by codigo_carne,titulo INTO OUTFILE '/tmp/mkauth-titulos-1-ajuste.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
"""