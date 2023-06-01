-- EMPRESAS
SELECT DISTINCT 
	ce.ID_EMPRESA         ,
	ce.ATIVO              ,
	ce.RAZAO_SOCIAL       ,
	ce.NOME_FANTASIA      ,
	ce.REGIME_TRIBUTARIO  ,
	ce.CNPJ               ,
	ce.IE                 ,
	ce.IM                 ,
	ce.DOMINIO            ,
	ce.LOGRADOURO         ,
	ce.NUMERO             ,
	ce.COMPLEMENTO        ,
	ce.BAIRRO             ,
	ce.CEP                ,
	ce.CIDADE             ,
	ce.UF                 ,
	ce.TELEFONE           ,
	ce.TELEFONE_0800      ,
	ce.WEBSITE            ,
	ce.EMAIL_FINANCEIRO   ,
	ce.EMAIL_SUPORTE      ,
	ce.EMAIL_FISCAL       ,
	ce.EMAIL_GESTOR 
FROM CNF_EMPRESA ce 
INTO OUTFILE '/tmp/ispfy-empresas.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

-- PLANOS
SELECT DISTINCT 
	cs.ID_SUBPLANO       ,
	cs.FK_ID_EMPRESA     ,
	cs.DESCRICAO         ,
	cs.DETALHES          ,
	cs.VALOR             ,
	cs.ATIVO             ,
	cs.KBPS              ,
	cs.BANDA             ,
	cp.DESCRICAO         ,
	cp.DETALHES          ,
	cp.ATIVO 
FROM CAD_SUBPLANO cs 
LEFT JOIN CAD_PLANO cp ON (cp.ID_PLANO = cs.FK_ID_PLANO)
INTO OUTFILE '/tmp/ispfy-planos.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- PORTADORES
SELECT DISTINCT 
	 fb.ID_BANCO        ,
	 fb.FK_ID_EMPRESA   ,
	 fb.NOME            ,
	 fb.BANCO           ,
	 fb.ATIVO           ,
	 fb.AGENCIA         ,
	 fb.AGENCIA_DV      ,
	 fb.CONTA           ,
	 fb.CONTA_DV
FROM FIN_BANCO fb 
INTO OUTFILE '/tmp/ispfy-portadores.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



-- CLIENTE
SELECT DISTINCT 
	cp.ID_PESSOA               ,
	cp.FK_ID_EMPRESA           ,
	cp.RAZAO_SOCIAL            ,
	cp.NOME_FANTASIA           ,
	cp.CPF_CNPJ                ,
	cp.TIPO                    ,
	cp.GENERO                  ,
	cp.RG_IE                   ,
	cp.DATA_CADASTRO           ,
	cp.ATIVO                   ,
	cp.NASCIMENTO              ,
	cp.SENHA_CENTRAL           ,
	cp.OBSERVACOES             ,
	-- endereco de cadastro
	ce.LOGRADOURO              ,
	ce.NUMERO                  ,
	ce.COMPLEMENTO             ,
	ce.BAIRRO                  ,
	ce.CEP                     ,
	ce.CIDADE                  ,
	ce.UF                      ,
	-- dados de cadastro
	cc.ID_CONTRATO             ,
	cc.FK_ID_EMPRESA           ,
	cc.FK_ID_PLANO             ,
	cc.FK_ID_SUBPLANO          ,
	ci.DESCRICAO               ,
	fb.ID_BANCO                ,
	fb.NOME                    ,
	cc.SITUACAO_CONTRATO       ,
	cc.SITUACAO_INSTALACAO     ,
	cc.MODALIDADE              ,
	cc.APELIDO                 ,
	cc.OBSERVACOES             ,
	cc.DATA_CADASTRO           ,
	cc.DATA_ATIVACAO           ,
	cc.DATA_INICIO             ,
	cc.DATA_TERMINO            ,
	cc.VALOR_MENSAL            ,
	cc.DIA_VENCIMENTO          ,
	-- endereco de cobranca
	ce2.LOGRADOURO              ,
	ce2.NUMERO                  ,
	ce2.COMPLEMENTO             ,
	ce2.BAIRRO                  ,
	ce2.CEP                     ,
	ce2.CIDADE                  ,
	ce2.UF                      ,
	-- endereco de instalacao
	ce3.LOGRADOURO              ,
	ce3.NUMERO                  ,
	ce3.COMPLEMENTO             ,
	ce3.BAIRRO                  ,
	ce3.CEP                     ,
	ce3.CIDADE                  ,
	ce3.UF                      ,
	cc.FORMA_PAGAMENTO          ,
	cc.CORTESIA                 ,
	cc.ASSINADO                 ,
	cc.DESCRICAO_SERVICO        ,
	ii.USUARIO                  ,
	ii.SENHA                    ,
	ii.IP                       ,
	ii.MAC                      ,
	ii.VELOCIDADE               ,
	ii.NUMERO_SERIE_ONU 
FROM CAD_PESSOA cp 
LEFT JOIN CAD_ENDERECO ce ON (ce.FK_ID_PESSOA = cp.ID_PESSOA and ce.TIPO = 'P')
INNER JOIN CAD_CONTRATO cc ON (cc.FK_ID_CLIENTE = cp.ID_PESSOA)
LEFT JOIN CAD_INSTALACAO ci ON (ci.ID_BENEFICIO = cc.FK_ID_INSTALACAO)
LEFT JOIN FIN_CARTEIRA_COBRANCA fcc ON (cc.FK_ID_CARTEIRA = fcc.ID_CARTEIRA_COBRANCA)
LEFT JOIN FIN_BANCO fb ON (fcc.FK_ID_BANCO = fb.ID_BANCO)
LEFT JOIN CAD_ENDERECO ce2 ON (ce2.FK_ID_CONTRATO = cc.ID_CONTRATO and ce2.TIPO = 'P')
LEFT JOIN CAD_ENDERECO ce3 ON (ce3.FK_ID_CONTRATO = cc.ID_CONTRATO and ce3.TIPO = 'I')
LEFT JOIN IP_IP ii ON (ii.FK_ID_CONTRATO = cc.ID_CONTRATO)
WHERE cp.CLIENTE = 'S'
INTO OUTFILE '/tmp/ispfy-cliente.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- CONTATOS
SELECT DISTINCT 
	cc.ID_CONTATO      ,
	cc.FK_ID_PESSOA    ,
	cc.TIPO            ,
	cc.CONTATO         ,
	cc.TELEFONE        ,
	cc.EMAIL 
FROM CAD_CONTATO cc 
INTO OUTFILE '/tmp/ispfy-contatos.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- FORNECEDORES
SELECT DISTINCT 
	cp.ID_PESSOA        ,
	cp.FK_ID_EMPRESA    ,
	cp.RAZAO_SOCIAL     ,
	cp.NOME_FANTASIA    ,
	cp.CPF_CNPJ         ,
	cp.TIPO             ,
	cp.GENERO           ,
	cp.RG_IE            ,
	cp.DATA_CADASTRO    ,
	cp.ATIVO
FROM CAD_PESSOA cp 
WHERE cp.FORNECEDOR = S''
INTO OUTFILE '/tmp/ispfy-fornecedores.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- TITULOS
SELECT DISTINCT 
	fb.ID_BOLETO                    ,
	fb.FK_ID_EMPRESA                ,
	fb.FK_ID_CLIENTE                ,
	fb.FK_ID_CONTRATO               ,
	fb.FK_ID_CARTEIRA_COBRANCA      ,
	fb.SITUACAO                     ,
	fb.DATA_EMISSAO                 ,
	fb.DATA_VENCIMENTO              ,
	fb.DATA_PAGAMENTO               ,
	fb.DATA_COMPENSACAO             ,
	fb.DATA_CANCELAMENTO            ,
	fb.VALOR                        ,
	fb.DESCONTOS                    ,
	fb.VALOR_PAGO                   ,
	fb.BAIXADO_BANCO                ,
	fb.GERENCIANET_ID               ,
	fb.GERENCIANET_LINK_INDIVIDUAL  ,
	fb.GERENCIANET_LINK_CARNE       ,
	fb.GERENCIANET_CARNE_ID         ,
	fb.GERENCIANET_CARNE_PARCELA    ,
	fb.GERENCIANET_TOKEN            ,
	fb.GALAXPAY_ID                  ,
	fb.GALAXPAY_URL                 ,
	fb.PIX                          ,
	fb.CODIGOBARRA                  ,
	fb.BB_CLIENT_ID                 ,
	fb.LINHADIGITAVEL 
FROM FIN_BOLETO fb 
INTO OUTFILE '/tmp/ispfy-titulos.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- OCORRENCIAS
SELECT DISTINCT 
	os.ID_SUPORTE             ,
	os.FK_ID_EMPRESA          ,
	oc.ID_CATEGORIA           ,
	oc.DESCRICAO              ,
	os2.ID_SUBCATEGORIA       ,
	os2.DESCRICAO             ,
	os.DATA_ABERTURA          ,
	os.DATA_FECHAMENTO        ,
	os.DATA_AGENDADA          ,
	os.PROBLEMA               ,
	os.SOLUCAO                ,
	os.SITUACAO               ,
	os.OBSERVACOES
FROM OS_SUPORTE os 
LEFT JOIN OS_CATEGORIA oc ON (oc.ID_CATEGORIA = os.FK_ID_CATEGORIA)
LEFT JOIN OS_SUBCATEGORIA os2 ON (os2.ID_SUBCATEGORIA = os.FK_ID_SUBCATEGORIA)
INTO OUTFILE '/tmp/ispfy-ocorrencias.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


























