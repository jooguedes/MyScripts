----DECLARACAO DE VARIAVEIS---
---- CONFIRME OS MAX ID DE TODOS ESSAS VARIAVEIS NO SISTEMA DO CLIENTE ANTES DE INSERIR ---


--- select max(id) from admcore_cliente; ok
--- select max(id) from admcore_clientecontrato; ok
--- select max(id) from admcore_plano; ok 
--- select max(id) from financeiro_portador; ok
--- select  max(id) from financeiro_pontorecebimento; ok
---select  max(id) from financeiro_pontorecebimento; ok
--- select max(id) from netcore_oltpon; ok
----select max(id) from netcore_ONUTemplate; ok
--- select max(id) from netcore_olt; ok
--- select max(id) from netcore_splitter; ok
--- select max(id) from netcore_onu; ok
--- select max(id) from netcore_nas; ok
--- select max(id) from financeiro_centrodecusto; ok
--- select max(id) from fiscal_notafiscal; ok
--- select max(id) from financeiro_pagar; ok
--- select max(id) from atendimento_ocorrencia; ok
--- select max(id) from financeiro_fornecedor;

SET @CLIENTECONTRATOID=150000;
SET @PREFIXO='@IXC';
SET @PLANOID=1100;
SET @PORTADORID=255;
SET @CAIXAID=300;
SET @OLTID=10;
SET @PONID=20;
SET @CTOID=200;
SET @ONUID=200;
SET @ONUTEMPLATEID=20;
---SET @LOGINONUID=200;
SET @NASID=300;
SET @PLANOCONTASID=200;
SET @PAGARID= 30;
SET @NF2121ID=10000;
SET @CHAMADOID=600;
SET @FORNECEDORID=50;


select 
vd.id  + @PLANOID,
CONCAT(vd.nome,@PREFIXO),
IFNULL(radg.download,'0') as download,
IFNULL(radg.upload,'0') as upload,
vdp.valor_unit as valor
from vd_contratos vd 
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
LEFT JOIN radgrupos radg ON (radg.id=vdp.id_plano)
INTO OUTFILE '/tmp/ixc-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select c.id + @PORTADORID,
c.descricao,
0,
0,
0,
0,
0,
c.n_convenio,c.carteira,
c.c_cedente,
c.aceite,
c.especie_doc, 
c.gateway_nome, 
c.gateway_token, 
c.gerencia_client_id, 
c.gerencia_client_secret
from fn_carteira_cobranca c 
INTO OUTFILE '/tmp/ixc-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


SELECT 
DISTINCT 
c.id + @CLIENTECONTRATOID as idcliente,
cc.id + @CLIENTECONTRATOID as idcontrato,
c.razao,
c.fantasia,
c.ie_identidade,
c.tipo_pessoa,
c.Sexo,
c.data_nascimento,
c.nacionalidade,
c.estado_civil,
c.profissao,
c.cnpj_cpf,
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.uf as uf,
c.cep,
c.referencia,
c.telefone_celular,
c.telefone_comercial,
c.email,
c.nome_pai,
c.nome_mae,
c.obs,
c.ativo,
cc.status_internet,
CONCAT(@PREFIXO ,ru.login),
ru.senha,
ru.ip,
ru.mac,
vd.id + @PLANOID as plano,
255, --cc.id_carteira_cobranca  + @PORTADORID,
cp.dia_fixo as vencimento,
c.responsavel,
c.im,
cc.data,
cc.data_ativacao,
ru.id as idservico,
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.cidade as uf,
c.cep,
c.referencia, 
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade cidade,
c.cidade as uf,
c.cep,
c.referencia

FROM cliente c  

INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id)
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
INNER JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato=cc.id and cc.status_internet in ('A','CM','CA','FA','D'))
WHERE c.ativo='S'

ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
INTO OUTFILE '/tmp/ixc-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



SELECT 
c.id + @CLIENTECONTRATOID as idcliente,
cc.id + @CLIENTECONTRATOID as idcontrato,
c.razao,
c.fantasia,
c.ie_identidade,
c.tipo_pessoa,
c.Sexo,
c.data_nascimento,
c.nacionalidade,
c.estado_civil,
c.profissao,
c.cnpj_cpf,
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.uf as uf,
c.cep,
c.referencia,
c.telefone_celular,
c.telefone_comercial,
c.email,
c.nome_pai,
c.nome_mae,
c.obs,
c.ativo,
cc.status_internet,
CONCAT(@PREFIXO ,ru.login),
ru.senha,
ru.ip,
ru.mac,
vd.id + @PLANOID as plano,
255, --cc.id_carteira_cobranca  + @PORTADORID,
cp.dia_fixo as vencimento,
c.responsavel,
c.im,
cc.data,
cc.data_ativacao,
ru.id as idservico,
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.uf as uf,
cc.cep,
cc.referencia, 
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.uf  as uf,
ru.cep,
ru.referencia

FROM cliente c  

INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id)
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
INNER JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato=cc.id and cc.status_internet in ('A','CM','CA','FA','D'))
WHERE c.ativo='N'
ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
INTO OUTFILE '/tmp/ixc-clientes-desativados.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


SELECT 
DISTINCT
c.id + @CLIENTECONTRATOID as idcliente,
cc.id + @CLIENTECONTRATOID as idcontrato,
c.razao,
c.fantasia,
c.ie_identidade,
c.tipo_pessoa,
c.Sexo,
c.data_nascimento,
c.nacionalidade,
c.estado_civil,
c.profissao,
c.cnpj_cpf,
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.uf as uf,
c.cep,
c.referencia,
c.telefone_celular,
c.telefone_comercial,
c.email,
c.nome_pai,
c.nome_mae,
c.obs,
c.ativo,
cc.status_internet,
CONCAT(@PREFIXO ,ru.login),
ru.senha,
ru.ip,
ru.mac,
vd.id + @PLANOID as plano,
255, --cc.id_carteira_cobranca  + @PORTADORID,
cp.dia_fixo as vencimento,
c.responsavel,
c.im,
cc.data,
cc.data_ativacao,
ru.id as idservico,
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.uf as uf,
c.cep,
c.referencia, 
c.endereco,
c.numero,
c.complemento,
c.bairro,
c.cidade as cidade,
c.uf as uf,
c.cep,
c.referencia

FROM cliente c  


INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id and cc.status_internet in ('A','CM','CA','FA','D'))
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
LEFT JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato=cc.id and cc.status_internet in ('A','CM','CA','FA','D'))
WHERE ru.login is null
ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
INTO OUTFILE '/tmp/ixc-clientes-semlogin.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select
       r.id_cliente + @CLIENTECONTRATOID,
       r.id_contrato + @CLIENTECONTRATOID,
       r.id_conta,
       r.id_carteira_cobranca + @PORTADORID,
       r.id as nosso_numero,
       r.documento,
       r.nparcela,
       r.valor,
       r.obs,
       m.credito as valor_pago,
       m.data as data_pagamento,
       r.data_emissao,
       r.data_vencimento,
       r.data_cancelamento,
       r.status,
       r.id_carteira_cobranca + @PORTADORID,
       r.nn_boleto,
       r.gateway_link,
       m.vdesconto as desconto

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id and m.credito > 0.00)
WHERE liberado='S' and (tipo_renegociacao IS NULL OR tipo_renegociacao != 'R')

INTO OUTFILE '/tmp/ixc-titulos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';