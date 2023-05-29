

--- CLIENTES
select DISTINCT
cliente.codcliente as id,
cliente.nome, 
cliente.cpfcnpj,
cliente.pessoafisica,
cliente.razaosocial,
cliente.datahoracadastro,
cliente.rg,
cliente.datanascimento,
cliente.nomemae,
cliente.nomepai,
cliente.obs,
cliente.datacontrato,
cliente.dataativacao,
cliente.datacabeamento,
cliente.contato,
cliente.centralassinantestatus,
cliente.profissao,
cliente.estadocivil,
cliente.situacao as status, #(0 - ativo  1 - cancelado 2 - Suspenso )
cliente.codusuariocadastro,
cliente.dataentregacontrato,
cliente.rgorgaoemissor,
cliente.inscricaoEstadual_UF,
plano.nome as plano,
plano.precoforcado as preco,
0 as upload,
0 as download,
login.login as login,
'' as senha,       #Não idenficado senha ate o momento
login.loginpai as login_principal,
IFNULL((select  nome from sis_cidades cidade inner join cli_enderecos on (cli_enderecos.sis_cidades_codcidade=cidade.codcidade) where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ), 'SEM_CIDADE') as cidade,
IFNULL((select  nome from sis_estados estado inner join cli_enderecos on (cli_enderecos.sis_cidades_sis_estados_codestado=estado.codestado) where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1) , 'estado') as estado,
IFNULL((select bairro FROM cli_enderecos where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ),'SEM BAIRRO') AS bairro,
IFNULL((select rua FROM cli_enderecos where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ),'SEM  RUA') AS rua,
IFNULL((select cep FROM cli_enderecos where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ),'') AS cep,
IFNULL((select complemento FROM cli_enderecos where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ),'') AS complemento,
IFNULL((select obs FROM cli_enderecos where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ),'') AS ponto_referencia,
IFNULL((select numeroEndereco FROM cli_enderecos where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ),'') AS numero,
IFNULL((select numeroApto FROM cli_enderecos where cli_enderecos.cli_clientes_codcliente=cliente.codcliente ORDER by cli_enderecos.codendereco limit 1 ),'') AS numeroApto,
IFNULL((select portador.codtiposcobranca from fin_tiposcobranca portador where  cobcliente.fin_tiposcobranca_codtiposcobranca=portador.codtiposcobranca), 'SEM PORTADOR') as portador,
IFNULL((select portador.diacobranca from fin_tiposcobranca portador where  cobcliente.fin_tiposcobranca_codtiposcobranca=portador.codtiposcobranca), '10') as vencimento
from cli_clientes cliente 
inner join fin_cobrancascliente cobcliente on (cobcliente.cli_clientes_codcliente= cliente.codcliente)
inner join fin_cobrancasclienteplanos cobclienteplano on (cobcliente.codcobrancascliente = cobclienteplano.fin_cobrancascliente_codcobrancascliente)
inner join plan_planos plano on (cobclienteplano.plan_planos_codplano=plano.codplano)
inner join plan_logins login on (login.fin_cobrancasclienteplanos_codcobrancascliente=cobcliente.codcobrancascliente)
INTO OUTFILE '/tmp/bemtevi-clientes.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

--inner join cli_enderecos endereco on (endereco.cli_clientes_codcliente=cliente.codcliente)

---USUÁRIOS
select 
codusuario,
usuario,
senha,
nome,
email
from sis_usuarios
INTO OUTFILE '/tmp/bemtevi-usuarios.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

---Emails
select
email.email,
email.cli_clientes_codcliente as codigocliente
from cli_emails email
INTO OUTFILE '/tmp/bemtevi-emails.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

---Celulares
select
celular.numero,
celular.cli_clientes_codcliente
from cli_celulares celular
INTO OUTFILE '/tmp/bemtevi-celulares.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



--- TITULOS ----
select
cobranca.codcliente,
cobranca.dataprocessamento,
cobranca.datavencimento,
cobranca.valorcobranca as valor,
cobranca.nossonumero,
cobranca.codcobrancacliente,
cobranca_pagamentos.datapagamento,
cobranca_pagamentos.obs,
cobranca_pagamentos.valor as valor_pago,
cobranca_pagamentos.databaixa,
cobranca.cob_cobrancasgeradas_fin_tiposcobranca_codtiposcobranca as id_portador
from cob_cobrancas cobranca
left join  cob_pagamentos cobranca_pagamentos on (cobranca_pagamentos.codcobranca=cobranca.codcobranca)
INTO OUTFILE '/tmp/bemtevi-titulos.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';





----CHAMADOS----
select
ocorrencia.codsuporte,
ocorrencia.cli_clientes_codcliente as id_cliente,
ocorrencia.problema as descricao,
ocorrencia.datacadastro as data_abertura,
ocorrencia.dataresolvido data_fechamento,
ocorrencia.titulo as titulo_abertura,    
ocorrencia.codsuporte as protocolo,
IFNULL((select status.descricao from  sup_situacoes status where ocorrencia.sup_situacoes_codsituacao=status.codsituacao), 'DEAFAULT') as status
from sup_suportes ocorrencia
INTO OUTFILE '/tmp/bemtevi-chamados.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



----PORTADORES----
select
portador.codtiposcobranca as id_portador,
portador.descricao,
conta.agencia,
conta.numero,
conta.dvnumero,
conta.descricao
from fin_tiposcobranca portador
left join fin_contascorrentes conta on (portador.fin_contascorrentes_codcontacorrente=conta.codcontacorrente)
INTO OUTFILE '/tmp/bemtevi-portadores.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



---- NOTAS FISCAIS
select 
notafiscal.codnotafiscal,
notafiscal.codcobranca,
notafiscal.numero,
notafiscal.dataemissao,
notafiscal.datahorageracao,
notafiscal.codfornecedor,
notafiscal.codcliente,
notafiscal.cpfcnpj,
notafiscal.valor,
notafiscal.valoricms,
notafiscalitem.descricao,
notafiscalitem.qtde,
notafiscalitem.aliquotaicms,
(select tipo.modelo from fin_tiponotasfiscais tipo where tipo.codtiponotafiscal=notafiscal.codtiponotafiscal) as modelo,
notafiscal.cfop as cfop,
notafiscal.telefone,
(select cob.nossonumero from cob_cobrancas cob where notafiscal.codcobranca=cob.codcobranca) as nossonumero,
notafiscalitem.valor
from cob_notasfiscais notafiscal
inner join cob_notasfiscaisitens notafiscalitem on (notafiscalitem.codnotafiscal=notafiscal.codnotafiscal)
INTO OUTFILE '/tmp/bemtevi-notafiscal.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';




---- MAPEAMENTO CLIENTE X SENHAS ------
select DISTINCT 
radius.username,
radius.pass from Bemtevi_Radius.radpostauth radius 
inner join Bemtevi.plan_logins login  on (login.login=radius.username)
where (select CHAR_LENGTH(radius.pass))<=10
and radius.pass <> '' order by radius.id
INTO OUTFILE '/tmp/bemtevi-usuarios-radius.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


---- EXTRATO DE TRAFEGO CLIENTES ----
select 
radius.radacctid,
radius.acctsessionid,
radius.acctuniqueid,
radius.username,
radius.groupname,
radius.realm,
radius.nasipaddress,
radius.nasportid,
radius.nasporttype,
radius.acctstarttime,
radius.acctupdatetime,
radius.acctstoptime,
radius.acctinterval,
radius.acctsessiontime,
radius.acctauthentic,
radius.connectinfo_start,
radius.connectinfo_stop,
radius.acctinputoctets,
radius.acctoutputoctets,
radius.calledstationid,
radius.callingstationid,
radius.acctterminatecause,
radius.servicetype,
radius.framedprotocol,
radius.framedipaddress,
radius.acctstartdelay,
radius.acctstopdelay,
radius.xascendsessionsvrkey,
radius.port_DisconnectRequest
from Bemtevi_Radius.radacct radius
INTO OUTFILE '/tmp/bemtevi-radacct.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';




----TESTE SENHA RADIUS----
select DISTINCT 
radius.username,
radius.pass from Bemtevi_Radius.radpostauth radius 
inner join Bemtevi.plan_logins login  on (login.login=radius.username)
where (select CHAR_LENGTH(radius.pass))<=10 AND radius.username="christianliber"
and radius.pass <> '' order by radius.id;