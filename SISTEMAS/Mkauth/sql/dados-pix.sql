SELECT 
	REPLACE (JSON_EXTRACT(sg.dados, '$.data_vencimento'), '\\', '') as data_vencimento       ,
	REPLACE (JSON_EXTRACT(sg.dados, '$.data_documento'), '\\', '') as data_documento         ,
	REPLACE (JSON_EXTRACT(sg.dados, '$.data_processamento'), '\\', '') as data_processamento ,
	JSON_EXTRACT(sg.dados, '$.status') as status                                             ,
	JSON_EXTRACT(sg.dados, '$.valor_boleto') as valor                                        ,
	JSON_EXTRACT(sg.dados, '$.cpf_cnpj') as cpfcnpj                                          ,
	JSON_EXTRACT(sg.dados, '$.numero_documento') as numero_documento                         ,
	REPLACE (JSON_EXTRACT(sg.dados, '$.nosso_numero'), '\\', '') as nosso_numero             ,
	REPLACE (JSON_EXTRACT(sg.dados, '$.qrcode'), '\\', '') as qrcode
FROM sis_gnettits sg 
WHERE JSON_EXTRACT(sg.dados, '$.qrcode') IS NOT NULL 
AND JSON_EXTRACT(sg.dados, '$.qrcode') <> FALSE
INTO OUTFILE '/tmp/mkauth-dados-pix-gerencianet.csv' FIELDS 
TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';