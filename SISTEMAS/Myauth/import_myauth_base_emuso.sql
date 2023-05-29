
----DECLARACAO DE VARIAVEIS---
---- CONFIRME OS MAX ID DE TODOS ESSAS VARIAVEIS NO SISTEMA DO CLIENTE ANTES DE INSERIR ---


--- select max(id) from admcore_cliente; ok --> 11648
--- select max(id) from admcore_clientecontrato; ok --> 14358
--- select max(id) from admcore_plano;  ok --> 410
--- select max(id) from financeiro_portador; ok --> 6
--- select  max(id) from financeiro_pontorecebimento; ok -->  21
---select  max(id) from financeiro_pontorecebimento; ok -->  21
--- select max(id) from netcore_oltpon; ok --> 120 
----select max(id) from netcore_ONUTemplate; ok --> 5
--- select max(id) from netcore_olt; ok --> 5
--- select max(id) from netcore_splitter;  ok --> 1361 (CTO)
--- select max(id) from netcore_onu;  OK --> 8269 
--- select max(id) from netcore_nas; OK --> 83
--- select max(id) from financeiro_centrodecusto; ok --> 234
--- select max(id) from fiscal_notafiscal; ok --> 49624
--- select max(id) from financeiro_pagar; ok --> 207
--- select max(id) from atendimento_ocorrencia;  ok --> 108615
--- select max(id) from financeiro_fornecedor; 0k --> 140
SET @CLIENTECONTRATOID=500;
SET @PREFIXO='@MYAUTH';
----SET @PLANOID=500;
---- SET @PORTADORID=30;
---- SET @CAIXAID=30;
---- SET @OLTID=20;
---- SET @PONID=300;
---- SET @CTOID=2000;
---- SET @ONUID=20000;
---- SET @ONUTEMPLATEID=20;
---SET @LOGINONUID=200;
----SET @NASID=100;
--- SET @PLANOCONTASID=350;
--- SET @PAGARID= 300;
--- SET @NF2121ID=60000;
--- SET @CHAMADOID=200000;
--- SET @FORNECEDORID=200;



SELECT c.id + @CLIENTECONTRATOID,
       CONCAT(IFNULL(l.user,CONCAT('c',c.id)),@PREFIXO) as usuario,
       c.tipo as tipop,
       c.nome,
       1,
       c.cpfcnpj,
       10,
       15,
       c.rg,'' as profissao,
       c.sexo,
       c.datanasc,
       c.fantasia,'' as contato,
       c.endereco,
       c.numero,
       c.complemento,
       c.bairro,
       c.cep,
       c.uf,
       c.cidade,
       c.telefoneres,
       c.telefonecom,
       c.telefonecel,
       c.email,
       c.observacao,
       c.datacad,
       c.dataalt,'' as servidor, 
       CONCAT(IFNULL(l.groupname,'SEM PLANO'), @PREFIXO) as plano,
       '0' as valor,
       'pppoe' as tipo,
       l.ip,
       l.ip,
       l.mac,
       c.vencimento,
       '0' as desconto,
       '0' as acrescimo,
       '' as transmissor,
       '' as receptor,
       '0' as comodato,
       '0' as isento,
       '1' as ativo,
       IFNULL(l.pass,'SEM SENHA') as senha,
       c.pai,
       c.mae,
       c.referencia,
       c.corp_id,
       c.ie,
       c.im,
       c.status,
       c.valor_mensalidade
       
FROM clientes c
LEFT JOIN login l on (l.cliente_id=c.id)
INTO OUTFILE '/tmp/myauth-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

SELECT c.cpfcnpj,
       l.user
FROM clientes c
INNER JOIN login l on (l.cliente_id=c.id)
INTO OUTFILE '/tmp/myauth-logins-cpfcnpj.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


SELECT c.id + @CLIENTECONTRATOID,
       CONCAT(l.user,@PREFIXO),
       c.cpfcnpj,
       f.descricao,
       f.id as numero_documento,
       f.nosso_numero,
       f.reg_lancamento as emissao,
       f.reg_vencimento as vencimento,
       f.reg_valor_total as valortotal,
       f.bx_valor_pago as valorpago,
       f.bx_pagamento as datapagamento,
       c.corp_id

FROM clientes c INNER JOIN login l on (l.cliente_id=c.id)
INNER JOIN financeiro f on (f.cliente_id=c.id) 
WHERE f.reg_deleted=0
ORDER BY f.id
INTO OUTFILE '/tmp/myauth-titulos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

SELECT c.id,
       l.user,
       c.cpfcnpj,
       f.descricao,
       f.id as numero_documento,
       f.nosso_numero,
       f.reg_lancamento as emissao,
       f.reg_vencimento as vencimento,
       f.reg_valor_total as valortotal,
       f.bx_valor_pago as valorpago,
       f.bx_pagamento as datapagamento,
       c.corp_id

FROM clientes c INNER JOIN login l on (l.cliente_id=c.id)
INNER JOIN financeiro f on (f.cliente_id=c.id) 
WHERE f.reg_deleted=1
ORDER BY f.id
INTO OUTFILE '/tmp/myauth-titulos-removidos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
