SELECT  DISTINCT  c.id as idcliente, 
cc.id as idcontrato,
 c.razao, c.fantasia
 FROM cliente c    
 INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id)  WHERE c.id=2014 ;




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


LEFT JOIN cliente_contrato cc ON (cc.id_cliente=c.id and cc.status_internet in ('A','CM','CA','FA','D'))
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
LEFT JOIN radusuarios ru  ON (ru.id_cliente=c.id )
WHERE ru.login is null and c.id=2014
ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
