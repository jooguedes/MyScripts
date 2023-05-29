select CODIGO,
    NOME,
    VLRPP,
    VLR_DESC,
    VLRANT,
    GRUPO,
    sici,
    codlan_1,
    velocidade_down,
    velocidade_up,
    ATIVO
from tva1000 
INTO OUTFILE '/tmp/gerenet-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select 
c.CONTRA,
c.NOME,
c.NOME_FANTASIA,
c.RGINS,
c.CPFCGC,
c.DATNAS,
c.NOME_PAI,
c.NOME_MAE,
c.CODRUA,
c.NENDE,
c.ANDAR,
c.BLOCO,
c.COMPLE,
c.QUADRA,
c.LOTE,
c.CASA,
c.BAIRRO,
c.CODAREA,
c.CIDADE,
c.UF,
c.CEP,
c.PAIS,
CONCAT(c.TEL_DDD1,c.TEL_NUM1) as telefone1,
c.TEL_CON1 as telefone1_obs,
CONCAT(c.TEL_DDD2,c.TEL_NUM2) as telefone2,
c.TEL_CON2 as telefone2_obs,
CONCAT(c.TEL_DDD3,c.TEL_NUM3) as telefone3,
c.TEL_CON3 as telefone3_obs,
CONCAT(c.TEL_DDD4,c.TEL_NUM4) as telefone4,
c.TEL_CON4 as telefone4_obs,
CONCAT(c.TEL_DDD5,c.TEL_NUM5) as telefone5,
c.TEL_CON5 as telefone5_obs,
CONCAT(c.TEL_DDD6,c.TEL_NUM6) as telefone6,
c.TEL_CON6 as telefone6_obs,
c.EMAIL,
c.EMAIL_FIN,
c.ENDEC,
c.COMPLEC,
c.BAIRROC,
c.CIDC,
c.UFC,
c.CEPC,
c.DATCAD,
c.site,
c.TIPOCNT,
c.PLAVEN,
c.vl_ativacao,
c.VENDED,
c.DATVEN,
c.DIAVENC,
c.CART_COB,
c.BCODEB,
c.corte_automatico,
c.recebe_aviso_cobranca,
c.recebe_email_cobranca,
c.cobrar_inadimplente,
c.aviso_inadimplente,
c.email_inadimplente,
c.email_enviar,
c.atualizado,
c.qualificador,
c.usuariocad,
cc.registro as data_ponto,
cc.COMODATO,
cc.DECODER,
p.NOME as PLANO,
cc.PROGRA,
st.NOME,
cc.PONTOS,
r.name,
r.password,
r.caller_id,
c.tva0900_sexo,
c.tva0900_civil,
c.orgao_exp_rg,
r.codigo,
cc.OBS

from tva0900 c
inner join tva1600 cc on (cc.CODIGO=c.CONTRA)
inner join tva1500 st on (st.CODIGO=cc.SITUAC)
inner join tva1000 p on (p.CODIGO=cc.PROGRA)
inner join rede_acesso r on (r.cliente=c.CONTRA and r.ponto=cc.PONTOS)                                                                                                                                                                                                 
INTO OUTFILE '/tmp/gerenet-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select 
r.name,
cc.OBS
from tva0900 c
inner join tva1600 cc on (cc.CODIGO=c.CONTRA)
inner join tva1500 st on (st.CODIGO=cc.SITUAC)
inner join tva1000 p on (p.CODIGO=cc.PROGRA)
inner join rede_acesso r on (r.cliente=c.CONTRA and r.ponto=cc.PONTOS)                                              
INTO OUTFILE '/tmp/gerenet-login-obs.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select 
b.codigo,
b.cliente,
b.emissao,
b.vecto,
b.valor,
b.boleto as nosso_numero,
b.codigo as numero_documento,
'' as data_pagamento,
'' as data_baixa,
'' as valorpago,
'1' as status,
'' as idtransacao,
'' as link,
'' as codigo_barras,
'' as carne_id,
'' as carne_link,
'' as v,
'0000-00-00 00:00:00' as data_cancela,
b.pix_txid,
b.pix_url,
b.pix_ged_qrcode
from tva2410 t 
inner join boleto b on (b.codigo=t.boleto_ultimo)
inner join tva2420 l on (l.DNRTIT=t.DNRTIT)
WHERE t.CART_COB=29
INTO OUTFILE '/tmp/gerenet-areceber-29.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

MariaDB [gerenet_cearanet]> select distinct CART_COB from tva2410;
+----------+
| CART_COB |
+----------+
|       24 |
|       26 |
|       27 |
|       29 |
+----------+

-- identificar carteiras de cobrança
select distinct 
bcd.codigo, 
bcd.nome, 
bcd.cob_carteira, 
bcd.inscr_empresa, 
bcd.convenio_boleto, 
bcd.convenio_boleto, 
bcd.convenio, 
bcd.agencia, 
bcd.dig_agencia, 
bcd.conta,
bcd.dig_conta,
bcd.cedente,
bcd.sequencia,
bcd.inicio_nsonum,
bcd.posto
from boletocad bcd
INTO OUTFILE '/tmp/gerenet-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

-- a receber gerencianet
select 
g.id,
g.contra as cliente,
g.geracao,
g.vencimento,#g.vecto,
g.total,
g.transacao as nosso_numero,
g.transacao as numero_documento,
g.pagamento as data_pagamento,
g.pagamento as data_baixa,
g.total_pago as valorpago,
g.status,      --- 0 = Cancelado 1 = Aberto 2=pago
g.transacao,
g.link,
g.codigobarra,
gc.carnet_id,
gc.link_carne,
g.vencimento,
g.cancela_solicita_registro
from tva0500_pagseguro_id g
left join tva0500_pagseguro_carne gc on (gc.codigo=g.tva0500_pagseguro_carne)
where conta_meio_pagamento=2
INTO OUTFILE '/tmp/gerenet-gerencianet-2.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
    

select 
g.id,
c.CANCELA
from tva0500_pagseguro_id g
inner join tva0500_pagseguro p on (p.tva0500_pagseguro_id=g.id)
inner join tva2400_cancela c on (c.DNRTIT=p.dnrtit)
where g.cancela_solicita_registro='0000-00-00 00:00:00'
INTO OUTFILE '/tmp/gerenet-gerencianet-tva2400.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



-- cancelados 
select * from tva2400_cancela;

-- lancamentos tit. cancelados 
select * from tva2420_cancela;

--titulos a receber: tva2410
--titulos a recebidos: tva2412
--titulos cancelados: tva2400_cancela
--lançamentos: tva2420
--lançamentos de titulos cancelados: tva2420_cancela
--tabela boleto: boleto
--

select CONTRA,AVISO from tva0900_aviso
INTO OUTFILE '/tmp/gerenet-avisos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


estoqproduto
estoqmov
estoqmov_serial
estoqsaldo



#DEBUG
MariaDB [dados]> select DISTINCT(conta_meio_pagamento) from  tva0500_pagseguro_id;
+----------------------+
| conta_meio_pagamento |
+----------------------+
|                    3 |
|                    2 |
|                    4 |
|                    5 |
|                    6 |
|                    7 |
+----------------------+
6 rows in set (0.060 sec)
    

select id, transacao, pagamento as data_pagamento, status, total_pago as valor_pago,  vencimento from tva0500_pagseguro_id where conta_meio_pagamento=2 and id=100643;
+--------+-----------+---------------------+--------+------------+------------+
| id     | transacao | data_pagamento      | status | valor_pago | vencimento |
+--------+-----------+---------------------+--------+------------+------------+
| 100643 | 120785161 | 0000-00-00 00:00:00 |      1 |       0.00 | 2019-03-20 |
+--------+-----------+---------------------+--------+------------+------------+
