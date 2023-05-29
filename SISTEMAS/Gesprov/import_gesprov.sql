select c.id,
       c.nome,
       999,
       c.agencia,
       c.digito_verificador_agencia,
       c.conta,
       c.digito_verificador_conta,
       c.convenio,
       c.carteira_boletos,
       c.nome,
       c.aceite,
       c.especie,
       b.nome,
       c.token_privado,
       c.client_id,
       c.client_secret,
       c.cnab
from contas_bancarias c
INNER JOIN bancos b on (b.id=c.id_banco)
INTO OUTFILE '/tmp/gesprov-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id,
       nome,
       download,
       upload,
       valor
from planos
INTO OUTFILE '/tmp/gesprov-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


SELECT c.id,
       a.usuario,
       c.tipo,
       c.nome_razao_social,
       cc.id,
       c.cpf_cnpj,
       10,
       15,
       c.rg_ie,
        '' as profissao,
       '' as sexo,
       c.dt_nascimento,
       c.nome_fantasia,
       c.referencia, 
       ec.rua, c.numero, c.complemento,
       ec.bairro,ec.cep, est.sigla as uf, cid.nome as cidade,
       c.telefone1, 
       c.telefone2,
       c.email,
       c.observacoes,
       c.dt_cadastro,
       c.dt_cadastro,
       '' as servidor,
       p.id,
       p.nome,
       c.tipo,
       a.ipv4, 
       a.ipv4, 
       a.mac,
       s.vencimento,
       s.desconto_servico as desconto, 
       s.acrescimo_servico as acrescimento,
       '' as transmissor,
       '' as receptor,
       s.fidelidade as comodato,
       CASE WHEN s.valor_servico = s.desconto_servico then true else false end as isento,
       cc.status,
       s.situacao,
       a.senha,
       p.download,
       p.upload,
       p.valor,
       s.id_conta_bancaria_servico as conta, 
       c.telefone3,
       a.usuario,
       es.rua, 
       s.numero, 
       es.bairro,
       cids.nome as cidade,
       es.cep,
       ests.sigla as uf,
       s.complemento,
       c.pai,
       c.mae,
       s.referencia,
       cid.codigo_ibge,
       cids.codigo_ibge,
       c.login_central,
       c.senha_central,
       s.id,
       a.latitude,
       a.longitude


FROM 
clientes c
INNER JOIN enderecos ec ON (ec.id=c.id_endereco)
INNER JOIN cidades cid ON (cid.id=ec.id_cidade)
INNER JOIN estados est ON (est.id=cid.id_estado)
INNER JOIN contratos cc ON (cc.id_cliente=c.id)
INNER JOIN servicos s ON (s.id_contrato=cc.id)
INNER JOIN planos p ON (p.id=s.id_plano)
INNER JOIN enderecos es ON (es.id=s.id_endereco)
INNER JOIN cidades cids ON (cids.id=es.id_cidade)
INNER JOIN estados ests ON (ests.id=cids.id_estado)
INNER JOIN acessos a ON (a.id_servico=s.id) 
INTO OUTFILE '/tmp/gesprov-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



select cc.id,
       c.id_conta_bancaria,
       c.id,
       IF(c.nosso_numero is null,c.id_boleto, c.nosso_numero),
       c.parcela,
       cli.cpf_cnpj,
       a.usuario,
       c.descricao,
       c.valor,
       c.valor_pagamento,
       c.data_processamento,
       c.vencimento,
       c.data_pagamento,
       c.data_pagamento,
       case when c.situacao = 0 then now() else c.data_cancelamento end as data_cancelamento,
       c.motivo_cancelado,
       c.linha_digitavel,
       c.barcode_number,
       c.situacao, 
       c.vencimento_original,
       IF(c.id_boleto is null,c.nosso_numero, c.id_boleto),
       c.boleto_url
from contas_receber c 
inner join servicos s on (s.id=c.id_servico)
inner join acessos a on (a.id_servico=s.id)
inner join contratos cc on (cc.id=s.id_contrato)
inner join clientes cli on (cli.id=cc.id_cliente) 
INTO OUTFILE '/tmp/gesprov-titulos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

 


#########################################QUANDO ID CHANGE FOR NULL ############################################
select cc.id,
       c.id_conta_bancaria,
       c.id,
       c.nosso_numero,
       c.parcela,
       cli.cpf_cnpj,
       a.usuario,
       c.descricao,
       c.valor,
       c.valor_pagamento,
       c.data_processamento,
       c.vencimento,
       c.data_pagamento,
       c.data_pagamento,
       case when c.situacao = 0 then now() else c.data_cancelamento end as data_cancelamento,
       c.motivo_cancelado,
       c.linha_digitavel,
       c.barcode_number,
       c.situacao, 
       c.vencimento_original,
       c.nosso_numero,
       c.id_boleto, 
       c.nosso_numero
from contas_receber c 
inner join servicos s on (s.id=c.id_servico)
inner join acessos a on (a.id_servico=s.id)
inner join contratos cc on (cc.id=s.id_contrato)
inner join clientes cli on (cli.id=cc.id_cliente) where c.id_conta_bancaria in (9,8)
INTO OUTFILE '/tmp/gesprov-titulos-portador-9-8.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';