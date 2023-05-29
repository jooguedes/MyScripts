SELECT c.id,
       IFNULL(l.user,concat('c',c.id)) as usuario,
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
       IFNULL(l.groupname,'SEM PLANO') as plano,
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
