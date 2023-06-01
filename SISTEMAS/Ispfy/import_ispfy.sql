select id,nome from sis_caixas
INTO OUTFILE '/tmp/ispfy-caixas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select
id,
carteira_nome,
codigo_banco,
codigo_agencia,
'',
codigo_conta,
'',
codigo_convenio,
codigo_carteira,
'EMPRESA X',
'A',
'',
'',
client_token,
client_id,
client_secret
from sis_carteira
INTO OUTFILE '/tmp/ispfy-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select 
id,
descricao,
SUBSTRING_INDEX(maxLimit,'/',-1) as download,
SUBSTRING_INDEX(maxLimit,'/',1) as upload,
valor as valor
from sis_plano
INTO OUTFILE '/tmp/ispfy-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


SELECT 
DISTINCT 
c.id as idcliente,
cc.id as idcontrato,
c.nome,
c.fantasia,
'' as ie,
'' as tipo,
'' as sexo,
c.nascimento,
'' as nacionalidade,
'' as estadocivil,
'' as profissao,
c.cgc,
c.endereco_cob,
c.numero_cob,
c.complemento_cob,
c.bairro_cob,
(select nome from sis_cidades where id=c.cidade_cob) as cidade,
(select uf from sis_cidades where id=c.cidade_cob) as uf,
c.cep_cob,
'' as referencia,
(select contato from sis_cliente_contato where tipo='c' and idcliente=c.id limit 1) as celular,
(select contato from sis_cliente_contato where tipo='t' and idcliente=c.id limit 1) as telefonecomercial,
(select contato from sis_cliente_contato where tipo='e' and idcliente=c.id limit 1) as email,
'' as nomepai,
'' as nomemae,
'' as cli_obs,
cc.ativo,
cc.acesso,
ponto.usuario,
ponto.senha,
ponto.v4_wan_addr,
ponto.mac,
plano.id,
cc.carteira_id,
cc.datarecorrencia as vencimento,
'' as responsavel,
'' as im,
cc.datapedido,
cc.dataadesao,
ponto.id as idservico,
c.endereco_cob,
c.numero_cob,
c.complemento_cob,
c.bairro_cob,
(select nome from sis_cidades where id=c.cidade_cob) as cidade,
(select uf from sis_cidades where id=c.cidade_cob) as uf,
c.cep_cob,
'' as referencia_cob,
ponto.endereco,
ponto.numero,
ponto.complemento,
ponto.bairro,
(select nome from sis_cidades where id=ponto.cidade) as cidade,
(select uf from sis_cidades where id=ponto.cidade) as uf,
ponto.cep,
'' as referencia_install,
ponto.ativo
FROM sis_cliente c  
INNER JOIN sis_clientes_contrato cc ON (cc.idcliente=c.id)
INNER JOIN sis_clientes_pontos ponto ON (ponto.idcontrato=cc.id)
INNER JOIN sis_clientes_pontos_planos pp ON (pp.id_ponto = ponto.id)
INNER JOIN sis_plano plano on (plano.id=pp.id_plano)
INTO OUTFILE '/tmp/ispfy-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select
       c.id,
       cc.id,
       '',
       r.carteira_id,
       r.nossoNumGerado as nosso_numero,
       r.id,
       r.parcela,
       r.valor,
       r.obs,
       r.valorpag,
       r.datapag,
       r.datalanc,
       r.datavenc,
       r.data_exclusao,
       r.status,
       r.carteira_id,
       r.gw_code,
       r.gw_linkbol,
       r.gw_extra,
       r.gw_codbar

from sis_titulos r
INNER JOIN sis_clientes_contrato cc on (cc.id=r.idcontrato) 
INNER JOIN sis_cliente c ON (c.id=cc.idcliente)
INNER JOIN sis_carteira carteira on (carteira.id=r.carteira_id)
INTO OUTFILE '/tmp/ispfy-titulos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



sed -i "s/\\\N//g" *.csv
for i in $(ls *.csv); do iconv -f iso8859-1 -t utf-8 $i > $i.utf8; rm $i; done 
for i in $(ls *.csv); do iconv -f iso8859-1 -t utf-8 $i > $i.utf8; done 







#EXTRAIR CLIENTES DE BANCO DE DADOS COM CAMPOS ALTERADOS
SELECT 
DISTINCT 
c.id as idcliente,
cc.id as idcontrato,
c.nome,
c.fantasia,
'' as ie,
'' as tipo,
'' as sexo,
c.nascimento,
'' as nacionalidade,
'' as estadocivil,
'' as profissao,
c.cgc,
c.endereco_cob,
c.numero_cob,
c.complemento_cob,
c.bairro_cob,
(select nome from sis_cidades where id=c.cidade_cob) as cidade,
(select uf from sis_cidades where id=c.cidade_cob) as uf,
c.cep_cob,
'' as referencia,
(select contato from sis_cliente_contato where tipo='c' and idcliente=c.id limit 1) as celular,
(select contato from sis_cliente_contato where tipo='t' and idcliente=c.id limit 1) as telefonecomercial,
(select contato from sis_cliente_contato where tipo='e' and idcliente=c.id limit 1) as email,
'' as nomepai,
'' as nomemae,
'' as cli_obs,
cc.ativo,
cc.acesso,
ponto.usuario,
ponto.senha,
ponto.v4_wan_addr,
ponto.mac,
plano.id as plano,
cc.carteira_id,
cc.datarecorrencia as vencimento,
'' as responsavel,
'' as im,
cc.datapedido,
cc.dataadesao,
ponto.id as idservico,
c.endereco_cob,
c.numero_cob,
c.complemento_cob,
c.bairro_cob,
(select nome from sis_cidades where id=c.cidade_cob) as cidade,
(select uf from sis_cidades where id=c.cidade_cob) as uf,
c.cep_cob,
'' as referencia_cob,
ponto.endereco,
ponto.numero,
ponto.complemento,
ponto.bairro,
(select nome from sis_cidades where id=ponto.cidade) as cidade,
(select uf from sis_cidades where id=ponto.cidade) as uf,
ponto.cep,
'' as referencia_install,
ponto.ativo
FROM sis_cliente c  
INNER JOIN sis_clientes_contrato cc ON (cc.idcliente=c.id)
INNER JOIN sis_clientes_pontos ponto ON (ponto.idcontrato=cc.id)
INNER JOIN sis_clientes_pontos_planos pontos_planos ON (pontos_planos.id_ponto=ponto.id)
INNER JOIN sis_plano plano on (plano.id=pontos_planos.id_plano)
INTO OUTFILE '/tmp/ispfy-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';





select 
id,
nome,
SUBSTRING_INDEX(maxLimit,'/',-1) as download,
SUBSTRING_INDEX(maxLimit,'/',1) as upload,
valor as valor
from sis_plano
INTO OUTFILE '/tmp/ispfy-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';