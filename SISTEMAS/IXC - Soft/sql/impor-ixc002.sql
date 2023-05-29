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
SET @CLIENTECONTRATOID=20000;
SET @PREFIXO='@IXCNOVO';
SET @PLANOID=500;
SET @PORTADORID=30;
SET @CAIXAID=30;
SET @OLTID=20;
SET @PONID=300;
SET @CTOID=2000;
SET @ONUID=20000;
SET @ONUTEMPLATEID=20;
---SET @LOGINONUID=200;
SET @NASID=100;
SET @PLANOCONTASID=350;
SET @PAGARID= 300;
SET @NF2121ID=60000;
SET @CHAMADOID=200000;
SET @FORNECEDORID=200;


SELECT 
c.id + @CLIENTECONTRATOID as idcliente,
c.razao
FROM cliente c  
RIGHT JOIN cliente_contrato cc ON (cc.id_cliente=c.id) 
INTO OUTFILE '/tmp/ixc-clientes-filial-12-com-nomes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id + @CAIXAID, conta,permitir_pag_saldo_negativo from contas
INTO OUTFILE '/tmp/ixc-caixas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select c.id + @PORTADORID,c.descricao,co.cod_banco,co.agencia,co.agencia_dv,co.numero_conta,co.numero_conta_dv,c.n_convenio,c.carteira,c.c_cedente,c.aceite,c.especie_doc, c.gateway_nome, c.gateway_token, c.gerencia_client_id, c.gerencia_client_secret
from fn_carteira_cobranca c INNER JOIN contas co ON (co.id=c.id_conta)
INTO OUTFILE '/tmp/ixc-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select nome,email,senha from usuarios
INTO OUTFILE '/tmp/ixc-usuarios.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select 
vd.id + @PLANOID,
CONCAT(vd.nome,@PREFIXO),
IFNULL(radg.download,'0') as download,
IFNULL(radg.upload,'0') as upload,
vdp.valor_unit as valor
from vd_contratos vd 
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
LEFT JOIN radgrupos radg ON (radg.id=vdp.id_plano)
INTO OUTFILE '/tmp/ixc-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#--WHERE id_filial=20

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
(select nome from cidade where id=c.cidade) as cidade,
(select sigla from uf where id=c.uf) as uf,
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
cc.id_carteira_cobranca  + @PORTADORID,
cp.dia_fixo as vencimento,
c.responsavel,
c.im,
cc.data,
cc.data_ativacao,
ru.id as idservico,
cc.endereco,
cc.numero,
cc.complemento,
cc.bairro,
(select nome from cidade where id=cc.cidade) as cidade,
(select sigla from uf where id=(select uf from cidade where id=cc.cidade)) as uf,
cc.cep,
cc.referencia, 
ru.endereco,
ru.numero,
ru.complemento,
ru.bairro,
(select nome from cidade where id=ru.cidade) as cidade,
(select sigla from uf where id=(select uf from cidade where id=ru.cidade)) as uf,
ru.cep,
ru.referencia

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

#--and c.filial_id=20

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
(select nome from cidade where id=c.cidade) as cidade,
(select sigla from uf where id=c.uf) as uf,
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
cc.id_carteira_cobranca  + @PORTADORID,
cp.dia_fixo as vencimento,
c.responsavel,
c.im,
cc.data,
cc.data_ativacao,
ru.id as idservico,
cc.endereco,
cc.numero,
cc.complemento,
cc.bairro,
(select nome from cidade where id=cc.cidade) as cidade,
(select sigla from uf where id=(select uf from cidade where id=cc.cidade)) as uf,
cc.cep,
cc.referencia, 
ru.endereco,
ru.numero,
ru.complemento,
ru.bairro,
(select nome from cidade where id=ru.cidade) as cidade,
(select sigla from uf where id=(select uf from cidade where id=ru.cidade)) as uf,
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
#and c.filial_id=20


SELECT 
DISTINCT
c.id + @CLIENTECONTRATOID as idcliente ,
cc.id  + @CLIENTECONTRATOID as idcontrato,
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
(select nome from cidade where id=c.cidade) as cidade,
(select sigla from uf where id=c.uf) as uf,
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
CONCAT(@PREFIXO, ru.login) ,
ru.senha,
ru.ip,
ru.mac,
vd.id + @PLANOID as plano,
cc.id_carteira_cobranca + @PORTADORID,
cp.dia_fixo as vencimento,
c.responsavel,
c.im,
cc.data,
cc.data_ativacao,
ru.id as idservico,
cc.endereco,
cc.numero,
cc.complemento,
cc.bairro,
(select nome from cidade where id=cc.cidade) as cidade,
(select sigla from uf where id=(select uf from cidade where id=cc.cidade)) as uf,
cc.cep,
cc.referencia, 
ru.endereco,
ru.numero,
ru.complemento,
ru.bairro,
(select nome from cidade where id=ru.cidade) as cidade,
(select sigla from uf where id=(select uf from cidade where id=ru.cidade)) as uf,
ru.cep,
ru.referencia

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
#and c.filial_id=20


select id + @OLTID, fabricante_modelo,descricao,ip,porta_ssh,porta_telnet,login,senha from radpop_radio
INTO OUTFILE '/tmp/ixc-olts.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select p.id + @PONID,p.id_pop_radio + @OLTID,s.numero_slot,p.numero_pon, p.interface,p.vlan_pppoe
from radpop_radio_porta p 
left join radpop_olt_slot s ON (s.id = p.id_slot)
INTO OUTFILE '/tmp/ixc-pons.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id + @CTOID, descricao,codigo_estilo_caixa,latitude,longitude,endereco,numero,bairro,cep,capacidade,obs_caixa_ftth 
from rad_caixa_ftth
INTO OUTFILE '/tmp/ixc-ctos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id + @ONUID, id_transmissor + @OLTID, id_caixa_ftth + @CTOID, slotno, ponno, onu_numero, mac, serial_number, onu_tipo, vlan, nome, porta_ftth, id_perfil
from radpop_radio_cliente_fibra
INTO OUTFILE '/tmp/ixc-onus.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id + @ONUTEMPLATEID, nome, comando 
from radpop_radio_cliente_fibra_perfil 
INTO OUTFILE '/tmp/ixc-onutemplate.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select CONCAT(@PREFIXO ,login), onu_mac from radusuarios where onu_mac != ''
INTO OUTFILE '/tmp/ixc-logins-onus.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


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
#AND  c.filial_id=4




select id + @NASID,nasname,shortname,description,secret, login,senha from nas
INTO OUTFILE '/tmp/ixc-nas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id + @FORNECEDORID, 
       razao,
       fantasia,
       telefone,
       '',
       representante,
       tipo,
       ie_identidade,
       cpf_cnpj,
       endereco,
       bairro,
       cep,
       nomecidade,
       siglauf,
       referencia,
       email,
       obs 
from fornecedor 
INTO OUTFILE '/tmp/ixc-fornecedores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



select distinct pa.id + @PLANOCONTASID,
       pa.planejamento_analitico
from fn_apagar p 
inner join planejamento_analitico pa on (pa.id=p.id_conta)
inner join planejamento pj on (pj.id=id_planejamento)

order by pa.id
INTO OUTFILE '/tmp/ixc-planocontas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#where p.filial_id=20

select distinct 
       p.id + @PAGARID,
       p.id_fornecedor + @FORNECEDORID,
       p.obs,
       p.valor,
       p.tipo_pagamento,
       pa.id + @PLANOCONTASID,
       p.data_emissao,
       p.data_vencimento,
       p.valor_pago
from fn_apagar p 
inner join planejamento_analitico pa on (pa.id=p.id_conta)
inner join planejamento pj on (pj.id=id_planejamento)
where p.status <> "C"
order by pa.id
INTO OUTFILE '/tmp/ixc-pagar.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#WHERE p.filial_id=20



select
f.id + @NF2121ID,
f.cnpj,
c.id + @CLIENTECONTRATOID,
c.cnpj_cpf,
v.id_contrato + @CLIENTECONTRATOID,
v.data_emissao,
v.data_saida,
v.data_cancelamento,
v.mot_cancelamento,
v.valor_total,
v.id_cfop,
v.serie,
v.serie_nf,
v.numero_nf,
v.modelo_nf,
v.infCpl,
v.nfe_chave,
r.id,
r.documento
from vd_saida v
inner join cliente c on (v.id_cliente=c.id)
inner join filial f on (f.id=v.filial_id)
left join fn_areceber r on (v.id=r.id_saida)
where v.modelo_nf in ('21','22')

order by v.numero_nf
INTO OUTFILE '/tmp/ixc-nf2122.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select
id + @CHAMADOID,
id_cliente + @CLIENTECONTRATOID,
id_assunto,
setor,
protocolo,
status,
data_abertura,
data_agenda,
data_fechamento,
mensagem,
mensagem_resposta
from su_oss_chamado 
INTO OUTFILE '/tmp/ixc-chamados.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select
cm.id_chamado + @CHAMADOID,
cm.mensagem,
cm.data_inicio,
cm.data_final,
e.descricao
from su_oss_chamado_mensagem cm
inner join su_oss_evento e on (e.id=cm.id_evento)
INTO OUTFILE '/tmp/ixc-chamados-mensagem.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';




select * from fn_carteira_cobranca \G;



mysql> select * from su_oss_evento;
+----+----------------------+
| id | descricao            |
+----+----------------------+
|  1 | Abertura             |
|  2 | Alteração            |
|  3 | Reabertura           |
|  4 | Alteração de setor   |
|  5 | Agendamento          |
|  6 | Fechamento           |
|  7 | Em Analise           |
|  8 | Assumido             |
|  9 | Em Execução          |
+----+----------------------+

mysql> select distinct status from su_oss_chamado;
+--------+
| status |
+--------+
| F      |
| A      |
| EN     |
| EX     |
| AG     |
+--------+

mysqldump -u consulta -h ostectelecom.com.br --single-transaction -p ixcprovedor  contas fn_carteira_cobranca usuarios vd_contratos vd_contratos_produtos cliente cliente_contrato cliente_contrato_tipo condicoes_pagamento vd_contratos vd_contratos_produtos radusuarios radgrupos radpop_olt_slot cidade uf radpop_radio_porta rad_caixa_ftth radpop_radio_cliente_fibra radpop_radio_cliente_fibra_perfil fn_areceber fn_movim_finan nas fornecedor fn_apagar planejamento_analitico planejamento vd_saida filial vd_saida su_oss_chamado su_oss_chamado_mensagem su_oss_chamado_arquivos cliente_arquivos empresa_setor su_oss_assunto cliente_contrato_historico radacct > ixcprovedor.sql




############################para corrigir o nosso numero##########################
select
       r.id_cliente  + @CLIENTECONTRATOID,
       r.id_contrato + @CLIENTECONTRATOID,
       r.id_conta,
       r.id_carteira_cobranca,
       r.boleto as nosso_numero,
       r.id,
       r.nparcela,
       r.valor,
       r.obs,
       m.credito as valor_pago,
       m.data as data_pagamento,
       r.data_emissao,
       r.data_vencimento,
       r.data_cancelamento,
       r.status,
       r.id_carteira_cobranca,
       r.nn_boleto,
       r.gateway_link,
       m.vdesconto as desconto

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id and m.credito > 0.00)
WHERE liberado='S' and (tipo_renegociacao IS NULL OR tipo_renegociacao != 'R') AND carteira.id=5

INTO OUTFILE '/tmp/ixc-titulos-bb-05.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#AND  c.filial_id=4

#EXTRAIR ALERTAS IXC
select id, obs, alerta from cliente INTO  OUTFILE '/tmp/ixc-alertas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n';


##CORRECAO NOSSO NUMERO BOLETOS
select
       r.id_cliente  + @CLIENTECONTRATOID,
       r.id_contrato + @CLIENTECONTRATOID,
       r.id_conta,
       r.id_carteira_cobranca + @PORTADORID,
       r.boleto as nosso_numero,
       r.id,
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
       m.vdesconto as desconto,
       r.documento

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id and m.credito > 0.00)
WHERE liberado='S' and (tipo_renegociacao IS NULL OR tipo_renegociacao != 'R')

INTO OUTFILE '/tmp/ixc-titulos-corrigidos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';