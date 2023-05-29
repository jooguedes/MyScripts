select
       r.id_cliente,
       r.id_contrato,
       r.id_conta,
       r.id_carteira_cobranca,
       r.id as nosso_numero,
       r.documento,
       r.valor,
       m.credito as valor_pago,
       m.vdesconto as desconto,
       r.pagamento_valor,
       m.data as data_pagamento

from fn_areceber r 
INNER JOIN cliente c ON (c.id=r.id_cliente)
INNER JOIN fn_carteira_cobranca carteira ON (carteira.id=r.id_carteira_cobranca)
LEFT OUTER JOIN fn_movim_finan m on (m.id_receber=r.id and m.credito > 0.00)
WHERE liberado='S' and (tipo_renegociacao IS NULL OR tipo_renegociacao != 'R') and r.pagamento_valor IS NOT NULL and r.pagamento_valor <> r.valor and m.credito

INTO OUTFILE '/tmp/ixc-titulos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';