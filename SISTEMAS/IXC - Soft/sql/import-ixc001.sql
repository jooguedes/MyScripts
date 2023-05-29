
select id,conta,permitir_pag_saldo_negativo from contas
INTO OUTFILE '/tmp/ixc-caixas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select c.id,c.descricao,co.cod_banco,co.agencia,co.agencia_dv,co.numero_conta,co.numero_conta_dv,c.n_convenio,c.carteira,c.c_cedente,c.aceite,c.especie_doc, c.gateway_nome, c.gateway_token, c.gerencia_client_id, c.gerencia_client_secret
from fn_carteira_cobranca c INNER JOIN contas co ON (co.id=c.id_conta)
INTO OUTFILE '/tmp/ixc-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select nome,email,senha from usuarios
INTO OUTFILE '/tmp/ixc-usuarios.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select 
vd.id,
vd.nome,
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
c.id as idcliente,
cc.id as idcontrato,
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
ru.login,
ru.senha,
ru.ip,
ru.mac,
vd.id as plano,
cc.id_carteira_cobranca,
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
c.id as idcliente,
cc.id as idcontrato,
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
ru.login,
ru.senha,
ru.ip,
ru.mac,
vd.id as plano,
cc.id_carteira_cobranca,
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
c.id as idcliente,
cc.id as idcontrato,
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
ru.login,
ru.senha,
ru.ip,
ru.mac,
vd.id as plano,
cc.id_carteira_cobranca,
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


INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id )
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
LEFT JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato=cc.id and cc.status_internet in ('A','CM','CA','FA','D'))
WHERE ru.login is null
ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
INTO OUTFILE '/tmp/ixc-clientes-semlogin.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#and c.filial_id=20

SELECT 
ru.login,
cc.status_internet,
c.ativo

FROM cliente c  
INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id)
INNER JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato =cc.id and cc.status_internet in ('A','CM','CA','FA','D')) 
ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')

INTO OUTFILE '/tmp/ixc-logins-status.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#and c.filial_id=4


select id_cliente, id, id_filial from cliente_contrato
#WHERE id_filial=4
INTO OUTFILE '/tmp/ixc-clientes-filial.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#

SELECT 
c.id as idcliente,
cc.id as idcontrato,
c.filial_id,
cc.id_filial
FROM cliente c  
LEFT JOIN cliente_contrato cc ON (cc.id_cliente=c.id) where cc.id_filial = 12
INTO OUTFILE '/tmp/ixc-clientescontratos-filial.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#WHERE c.filial_id=20


SELECT 
c.id as idcliente,
c.data_cadastro
from cliente c

INTO OUTFILE '/tmp/ixc-clientes-datascad.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#WHERE c.filial_id=4

select id,fabricante_modelo,descricao,ip,porta_ssh,porta_telnet,login,senha from radpop_radio
INTO OUTFILE '/tmp/ixc-olts.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select p.id,p.id_pop_radio,s.numero_slot,p.numero_pon, p.interface,p.vlan_pppoe
from radpop_radio_porta p 
left join radpop_olt_slot s ON (s.id = p.id_slot)
INTO OUTFILE '/tmp/ixc-pons.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id, descricao,codigo_estilo_caixa,latitude,longitude,endereco,numero,bairro,cep,capacidade,obs_caixa_ftth 
from rad_caixa_ftth
INTO OUTFILE '/tmp/ixc-ctos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id, id_transmissor, id_caixa_ftth, slotno, ponno, onu_numero, mac, serial_number, onu_tipo, vlan, nome, porta_ftth, id_perfil
from radpop_radio_cliente_fibra
INTO OUTFILE '/tmp/ixc-onus.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id_perfil, mac from radpop_radio_cliente_fibra INTO OUTFILE '/tmp/ixc-onus-perfis.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id, nome, comando 
from radpop_radio_cliente_fibra_perfil 
INTO OUTFILE '/tmp/ixc-onutemplate.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select login, onu_mac from radusuarios where onu_mac != ''
INTO OUTFILE '/tmp/ixc-logins-onus.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select
       r.id_cliente,
       r.id_contrato,
       r.id_conta,
       r.id_carteira_cobranca,
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
       r.id_carteira_cobranca,
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








select
       r.id_cliente,
       r.id_contrato,
       r.id_conta,
       r.id_carteira_cobranca,
       r.id as nosso_numero,
       r.documento,
       r.nparcela,
       r.valor,
       r.obs,
       r.pagamento_valor as valor_pago,
       r.pagamento_data as data_pagamento,
       r.data_emissao,
       r.data_vencimento,
       r.data_cancelamento,
       r.status,
       r.id_carteira_cobranca,
       r.nn_boleto,
       r.gateway_link,
       r.valor - r.pagamento_valor as desconto

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
WHERE liberado='S' and (tipo_renegociacao IS NULL OR tipo_renegociacao != 'R')
and r.pagamento_data is not null and r.pagamento_valor is not null

INTO OUTFILE '/tmp/ixc-titulos-pagos7.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#AND c.filial_id=20




select
       DISTINCT
       r.id_cliente,
       r.id_contrato,
       r.id_conta,
       r.id_carteira_cobranca,
       r.id as nosso_numero,
       r.documento,
       c.cnpj_cpf

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id)
WHERE liberado='S' and tipo_renegociacao = 'R'
INTO OUTFILE '/tmp/ixc-titulos-renegociados.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#AND c.filial_id=20







select
       r.id_cliente,
       r.id_contrato,
       r.id as nosso_numero,
       r.documento,
       r.nparcela
from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id)
INTO OUTFILE '/tmp/ixc-titulos-emitidos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id,nasname,shortname,description,secret, login,senha from nas
INTO OUTFILE '/tmp/ixc-nas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id, 
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



select distinct pa.id,
       pa.planejamento_analitico
from fn_apagar p 
inner join planejamento_analitico pa on (pa.id=p.id_conta)
inner join planejamento pj on (pj.id=id_planejamento)

order by pa.id
INTO OUTFILE '/tmp/ixc-planocontas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#where p.filial_id=20

select distinct 
       p.id,
       p.id_fornecedor,
       p.obs,
       p.valor,
       p.tipo_pagamento,
       pa.id,
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
f.id,
f.cnpj,
c.id,
c.cnpj_cpf,
v.id_contrato,
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
#AND c.filial_id=20

select
filial_id,
id_cliente,
id_contrato,
indFinal,
indPres,
tpemis_nfe,
tpimp_nfe,
finalidade_nfe,
data_emissao,
data_saida,
data_cancelamento,
mot_cancelamento,
valor_total,
id_cfop,
serie,
serie_nf,
numero_nf,
modelo_nf,
modalidade_frete,
infCpl,
nfe_chave,
gera_estoque
from vd_saida
where modelo_nf not in ('21','22')
order by numero_nf
INTO OUTFILE '/tmp/ixc-nfall.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id,setor from empresa_setor
INTO OUTFILE '/tmp/ixc-setor.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id,assunto from su_oss_assunto
INTO OUTFILE '/tmp/ixc-ocorrenciatipo.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select
id,
id_cliente,
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
cm.id_chamado,
cm.mensagem,
cm.data_inicio,
cm.data_final,
e.descricao
from su_oss_chamado_mensagem cm
inner join su_oss_evento e on (e.id=cm.id_evento)
INTO OUTFILE '/tmp/ixc-chamados-mensagem.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id, id_oss_chamado,descricao,local_arquivo,data_envio
from su_oss_chamado_arquivos
INTO OUTFILE '/tmp/ixc-chamados-arquivos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select 
radacctid            ,
acctsessionid        ,
acctuniqueid         ,
username             ,
realm                ,
nasipaddress         ,
nasportid            ,
nasporttype          ,
acctstarttime        ,
AcctUpdateTime       ,
acctstoptime         ,
acctsessiontime      ,
acctauthentic        ,
connectinfo_start    ,
connectinfo_stop     ,
acctinputoctets      ,
acctoutputoctets     ,
calledstationid      ,
callingstationid     ,
acctterminatecause   ,
servicetype          ,
framedprotocol       ,
framedipaddress      ,
framedipv6prefix     ,
delegatedipv6prefix  
from radacct
INTO OUTFILE '/tmp/ixc-radacct.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id_contrato,historico,data from cliente_contrato_historico
INTO OUTFILE '/tmp/ixc-historico.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id_cliente,descricao,local_arquivo,data_envio,id_contrato from cliente_arquivos 
INTO OUTFILE '/tmp/ixc-clientes-arquivos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#EXTRAIR ALERTAS IXC
select id, obs, alerta from cliente INTO  OUTFILE '/tmp/ixc-alertas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"'  LINES TERMINATED BY '\n';

select * from fn_carteira_cobranca \G;


NOVO USAR 

alter table radacct2 alter column framedipaddress type text;
alter table radacct2 alter column framedipv6prefix type text;
alter table radacct2 alter column delegatedipv6prefix type text;


COPY radacct2 (radacctid            ,
acctsessionid        ,
acctuniqueid         ,
username             ,
realm                ,
nasipaddress         ,
nasportid            ,
nasporttype          ,
acctstarttime        ,
AcctUpdateTime       ,
acctstoptime         ,
acctsessiontime      ,
acctauthentic        ,
connectinfo_start    ,
connectinfo_stop     ,
acctinputoctets      ,
acctoutputoctets     ,
calledstationid      ,
callingstationid     ,
acctterminatecause   ,
servicetype          ,
framedprotocol       ,
framedipaddress      ,
framedipv6prefix     ,
delegatedipv6prefix  )
FROM '/tmp/ixc-radacct.csv.utf8' DELIMITER '|' CSV;

update radacct2 set framedipaddress=null where framedipaddress='';
update radacct2 set framedipv6prefix=null where framedipv6prefix='';
update radacct2 set delegatedipv6prefix=null where delegatedipv6prefix='';

alter table radacct2 alter column framedipaddress type inet using framedipaddress::inet;
alter table radacct2 alter column framedipv6prefix type inet using framedipv6prefix::inet;
alter table radacct2 alter column delegatedipv6prefix type inet using delegatedipv6prefix::inet;
alter table radacct2 drop column groupname;
alter table radacct2 drop column acctstartdelay;
alter table radacct2 drop column acctstopdelay;
alter table radacct2 drop column xascendsessionsvrkey;



MariaDB [ixcprovedor]> select id,razao,cnpj from filial;



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
       r.id_cliente,
       r.id_contrato,
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
       m.vdesconto as desconto,
       r.documento

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id and m.credito > 0.00)
WHERE liberado='S' and (tipo_renegociacao IS NULL OR tipo_renegociacao != 'R') and r.boleto=175247

INTO OUTFILE '/tmp/ixc-titulos-corrigidos-portador-35-final.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#AND  c.filial_id=4



----- EXTRAIR SENHA DO WIFI  E SSID do IXC ------------
SELECT
id_contrato as contrato_cliente,
ssid_router_wifi,
senha_rede_sem_fio

from radusuarios where ssid_router_wifi is not null and senha_rede_sem_fio is not null and ssid_router_wifi <> '';




-------MAPEAMENTO DOS TEMPLATES CLIENTE ----------
20 -> 33
21 -> 32
22 -> 22
24 -> 34
31 -> 31

---------MAPEAMENTO TEMPLATES ONU---------
SELECT id_contrato as contrato_cliente,
ssid_router_wifi,
senha_rede_sem_fio  
from radusuarios where ssid_router_wifi is not null and senha_rede_sem_fio is not null and ssid_router_wifi <> '' INTO OUTFILE '/tmp/ixc-wifi.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';




###############Ajuste Titulos#############
select
       r.id_cliente,
       r.id_contrato,
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
       m.vdesconto as desconto,
       r.documento

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id and m.credito > 0.00)
WHERE liberado='S' and (tipo_renegociacao IS NULL OR tipo_renegociacao != 'R')

INTO OUTFILE '/tmp/ixc-titulos-corrigidos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#AND  c.filial_id=4