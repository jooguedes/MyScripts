SELECT 
DISTINCT 
c.id as idcliente,
cc.id as idcontrato,
cc.id_carteira_cobranca
FROM cliente c  

INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id)
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
INNER JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato=cc.id and cc.status_internet in ('A','CM','CA','FA','D'))
WHERE c.ativo='S'

ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
INTO OUTFILE '/tmp/ixc-clientes-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';





SELECT 
c.id as idcliente,
cc.id as idcontrato,
cc.id_carteira_cobranca
FROM cliente c  

INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id)
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
INNER JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato=cc.id and cc.status_internet in ('A','CM','CA','FA','D'))
WHERE c.ativo='N'
ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
INTO OUTFILE '/tmp/ixc-clientes-desativados-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



SELECT 
DISTINCT
c.id as idcliente,
cc.id as idcontrato,
cc.id_carteira_cobranca


FROM cliente c  


INNER JOIN cliente_contrato cc ON (cc.id_cliente=c.id and cc.status_internet in ('A','CM','CA','FA','D'))
INNER JOIN cliente_contrato_tipo cct ON (cct.id=cc.id_tipo_contrato)
INNER JOIN condicoes_pagamento cp ON (cp.id=cct.id_condicoes_pagamento)
INNER JOIN vd_contratos vd ON (vd.id = cc.id_vd_contrato)
INNER JOIN vd_contratos_produtos vdp ON (vdp.id_vd_contrato=vd.id)
LEFT JOIN radusuarios ru  ON (ru.id_cliente=c.id and ru.id_contrato=cc.id and cc.status_internet in ('A','CM','CA','FA','D'))
WHERE ru.login is null
ORDER BY c.id, cc.id, cc.status_internet in ('A','CM','CA','FA','D')
INTO OUTFILE '/tmp/ixc-clientes-semlogin-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
#and c.filial_id=20