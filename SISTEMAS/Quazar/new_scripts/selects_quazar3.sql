

SELECT 
	c.id,
	c.nome,
	c.ip,
	c.usuario,
	c.senha,
	c.fabricante 
FROM concentrador c
INTO OUTFILE '/tmp/quazar-nas.csv' CHARACTER SET utf8 
FIELDS TERMINATED BY '|'  OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select
	fc.id,
	fc.razaosocial,
	fc.fantasia,
	fc.cnpj,
	fc.responsavel,
	fc.bank_conv,
	fc.bank_conv_dv,
	fc.agency,
	fc.agencydigit,
	fc.account,
	fc.accountdigit,
  fc.carteira,
	fc.gatewayAmbient,
	fc.gatewayClientToken,
	fc.gatewayClientId,
	fc.gatewayClientSecret,
	fc.description
from financeiroCarteira fc
INTO OUTFILE '/tmp/quazar-portadores.csv' CHARACTER SET utf8 
FIELDS TERMINATED BY '|'  OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select distinct c.id,
  c.tipoPessoa as pessoa,
  c.nome,
  1,
  c.cpfcnpj,
  10,
  15,
  c.rg,
  '' as profissao,
  c.sexo as sexo,
  c.datanasc as nascimento,
  '' as fantasia, 
  '' as contato, 
  c.endereco,
  c.numero,
  c.complemento,
  c.bairro,
  c.cep,
  c.uf as estado,
  COALESCE(ci.nome,'TRACUNHAÉM') as cidade,
  c.telefonecel as celular,
  c.telSms as celular2,
  c.email,
  c.obs,
  c.pai,
  c.mae,
  cl.user as login,
  cl.pass as senha,
  cl.ip,
  cl.mac,
  g.name as plano,
  ct.valorUnitario as valor,
  ct.vencimento,
  ct.dataContrato,
  ct.dataAtivacao,
  ct.id as contratoId,
  ct.idEstado as status
from clientes  c 
INNER JOIN contratoLogin cl on (c.id= cl.idCliente) 
INNER JOIN contrato ct on(c.id= ct.idCliente)
INNER JOIN groups g on(g.id=cl.idGroup) 
LEFT JOIN cidade ci on(ci.id=c.cidade) 
INTO OUTFILE '/tmp/quazar-clientes.csv' CHARACTER SET utf8 
FIELDS TERMINATED BY '|'  OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select (select cl.user from contratoLogin cl where(f.idContrato=cl.idContrato)) as login,
  f.id,
  f.numero,
  f.nossoNumero,
  f.descricao,
  f.criacao as data_criacao,
  f.cliente_id as cliente,
  f.reg_valor,
  fg.codigoBarra,
  fg.linhaDigitavel,
  f.idRemessa,
  f.bx_pagamento as data_pagamento,
  f.bx_valor_pago,
  fg.vencimento,
  fg.link,
  fg.idGateway,
  f.carne,
  f.reg_deleted,
  f.alteracao,
  fg.linkPagamento,
  f.idCarteira
from financeiro f
INNER JOIN clientes c on (f.cliente_id=c.id)
INNER JOIN financeiroGateway fg on(fg.idFinanceiro=f.id)
INTO OUTFILE '/tmp/quazar-titulos.csv' CHARACTER SET utf8 
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


--portadores convencionais
select (select cl.user from contratoLogin cl where(f.idContrato=cl.idContrato)) as login,
  f.id,
  f.numero,
  f.nossoNumero,
  f.descricao,
  f.criacao as data_criacao,
  f.cliente_id as cliente,
  f.reg_valor,
  f.codigoBarras,
  f.linhaDigitavel,
  f.idRemessa,
  f.bx_pagamento as data_pagamento,
  f.bx_valor_pago,
  f.reg_vencimento,
  '',
  '',
  f.carne,
  f.reg_deleted,
  f.alteracao,
  '',
  f.idCarteira
  
from financeiro f
INNER JOIN clientes c on (f.cliente_id=c.id) where f.idCarteira=6
INTO OUTFILE '/tmp/quazar-titulos-banco-convencional-id-06-sem-duplicidade.csv' CHARACTER SET utf8 
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

SELECT 
	oc.id,
	oc.tipo,
	oc.descricao
FROM osCategoria oc
INTO OUTFILE '/tmp/quazar-chamadoassuntos.csv' CHARACTER SET utf8 
FIELDS TERMINATED BY '|'  OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

SELECT 
	oo.id,
	oo.idCliente,
	oo.idContrato,
	oo.idCategoria,
	oo.protocolo,
	oo.fechamento,
	oo.criacao,
	oo.dataPrevista,
	oo.problema,
	oo.observacoes 
FROM osOrdem oo
INTO OUTFILE '/tmp/quazar-chamados.csv' CHARACTER SET utf8 
FIELDS TERMINATED BY '|'  OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';





---Puxar titulos sem duplicidade

