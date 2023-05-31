-- EMPRESAS
SELECT DISTINCT 
	e.EMP_CODIGO       ,
	e.EMP_DOMINIO      ,
	e.EMP_RAZAO        ,
	e.EMP_FANTAZIA     ,
	e.EMP_ENDERECO     ,
	e.EMP_NUMERO       ,
	e.EMP_COMPLEMENTO  ,
	e.EMP_CIDADE       ,
	e.EMP_ESTADO       ,
	e.EMP_BAIRRO       ,
	e.EMP_LAT          ,
	e.EMP_LONG         ,
	e.EMP_CEP          ,
	e.EMP_CGC          ,
	e.EMP_INSCRICAO    ,
	e.EMP_FONE         ,
	e.EMP_FAX          ,
	e.EMP_ADMIN        ,
	e.EMP_DATA 
FROM empresa e 
INTO OUTFILE '/tmp/scut-empresas.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

-- POPS
SELECT DISTINCT 
	t.TOR_CODIGO      ,
	t.EMP_DOMINIO     ,
	t.TOR_DESCRICAO   ,
	e.EMP_ESTADO 
FROM torres t 
LEFT JOIN empresa e ON (e.EMP_DOMINIO = t.EMP_DOMINIO)
INTO OUTFILE '/tmp/scut-pops.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- PORTADORES
SELECT DISTINCT 
	b.BAN_CODIGO          ,
	b.BNID                ,
	b.EMP_DOMINIO         ,
	b2.nome               ,
	b2.codigo             ,
	b.AGENCIA             ,
	b.NR_CONTA            ,
	b.BAN_CONVENIO        ,
	b.CEDENTE             ,
	b.LOCALPGTO           ,
	b.NR_CARTEIRA         ,
	b.INSTRUCAO1          ,
	b.INSTRUCAO2          ,
	b.INSTRUCAO3          ,
	b.INSTRUCAO4          ,
	b.INSTRUCAO_SCM 
FROM bancobranca b 
LEFT JOIN bancos b2 ON (b2.bnid = b.BNID)
INTO OUTFILE '/tmp/scut-portadores.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

-- PLANOS
SELECT DISTINCT 
	b.BAN_CODIGO        ,
	b.BAN_BANDA         ,
	b.BAN_DESCRICAO     ,
	b.BAN_DESCRICAO2    ,
	m.MEN_DESCRICAO     ,
	m.MEN_VALOR         ,
	m.MEN_MENSAGEM      ,
	m.MEN_VAL_ADICIONAL ,
	m.MEN_DESCONTOS     ,
	m.MEN_STATUS 
FROM banda b 
LEFT JOIN mensalidade m ON (m.BAN_CODIGO = b.BAN_CODIGO)
INTO OUTFILE '/tmp/scut-planos.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

-- CLIENTES
SELECT DISTINCT 
	c.CLI_LOGIN                   ,
	c.EMP_DOMINIO                 ,
	c.CLI_SENHA                   ,
	c.CLI_CGC                     ,
	c.CLI_CPF                     ,
	c.CLI_TIPO                    ,
	c.CLI_NOME                    ,
	c.CLI_ENDERECO                ,
	c.CLI_REFERENCIA              ,
	c.CLI_CIDADE                  ,
	c.CLI_ESTADO                  ,
	c.CLI_BAIRRO                  ,
	c.CLI_CEP                     ,
	c.CLI_COMPLEMENTO             ,
	c.CLI_LAT                     ,
	c.CLI_LONG                    ,
	c.CLI_DIATARI                 ,
	c.CLI_FONE                    ,
	c.CLI_FAX                     ,
	c.CLI_CELULAR                 ,
	c.CLI_NOTAFIS                 ,
	c.CLI_DESCONTOS               ,
	c.CLI_DTNASCIMENTO            ,
	c.CLI_DTCADASTRO              ,
	c.CLI_INICIO                  ,
	c.CLI_ATIVACAO                ,
	c.CLI_BLOQUEADO               ,
	c.CLI_SUSPENSO                ,
	c.CLI_OBS                     ,
	c.CLI_MAC                     ,
	c.CLI_IP                      ,
	c.CLI_OBS_CONTRATO            ,
	c.CLI_CHAVE_CENTRAL           ,
	c.BAN_CODIGO as CODIGO_PLANO  ,
	c.CLI_MEIO                    ,
	c.TIPO_CLIENTE                ,
	mm.MOV_DESC                   ,
	mm.MOV_DATA                   ,
	c.TOR_CODIGO
FROM clientes2 c 
LEFT JOIN movimento_material mm ON (mm.CLI_LOGIN = c.CLI_LOGIN)
INTO OUTFILE '/tmp/scut-clientes.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- BOLETOS
SELECT DISTINCT 
	b.bid                 ,
	b.bnid                ,
	b.banco               ,
	b.titulo              ,
	b.conta_cedente       ,
	b.codigo              ,
	b.sacado              ,
	b.cpf                 ,
	b.instrucoes_linha1   ,
	b.instrucoes_linha2   ,
	b.instrucoes_linha3   ,
	b.instrucoes_linha4   ,
	b.instrucoes_linha5   ,
	b.login               ,
	b.dt_emissao          ,
	b.dt_pgto             ,
	b.dt_venc             ,
	b.val_titulo          ,
	b.descontos           ,
	b.desconto_vencimento ,
	b.juros               ,
	b.val_total           ,
	b.val_pago            ,
	b.status              ,
	b.situacao            ,
	b.CLI_DIATARI         ,
	b.parcela 
FROM boletos2 b 
INTO OUTFILE '/tmp/scut-titulos.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- CONTAS A PAGAR
SELECT DISTINCT 
	a.PAG_CODIGO          ,
	a.PAG_DATA            ,
	a.PAG_FAVORECIDO      ,
	a.PAG_REFERENTE       ,
	a.PAG_NUMERO          ,
	a.PAG_VALOR           ,
	a.USU_LOGIN           ,
	a.PAG_BAIXA           ,
	a.PAG_BANCO
FROM apagar a 
INTO OUTFILE '/tmp/scut-contas-apagar.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- SUPORTES
SELECT DISTINCT 
	s.SUP_CODIGO       ,
	u.USU_NOME         ,
	s.CLI_LOGIN        ,
	s.EMP_DOMINIO      ,
	s.SUP_DATA         ,
	s.SUP_HORA         ,
	s.SUP_DESCRICAO    ,
	s.SUP_HPREVISAO    ,
	s.SUP_DTPREVISAO   ,
	s.SUP_PRIORIDADE   ,
	s.SUP_TIPO         ,
	s.SUP_TECNICO      ,
	s.SUP_STATUS       ,
	s2.SOL_DESCRICAO   ,
	s2.SOL_DATA        ,
	s2.SOL_HORA        ,
	s2.SOL_STATUS 
FROM suporte s  
LEFT JOIN usuarios u ON (u.USU_CODIGO = s.USU_CODIGO)
LEFT JOIN solucao s2 ON (s2.SUP_CODIGO = s.SUP_CODIGO)
INTO OUTFILE '/tmp/scut-suportes.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- NOTAS FISCAIS 1
SELECT DISTINCT 
	in2.ITE_CODIGO       ,
	in2.ITE_DESCRICAO    ,
	in2.ITE_VALOR        ,
	in2.ITE_QTDADE       ,
	in2.ITE_VALOR_UNI    ,
	in2.ITE_OPERACAO     ,
	in2.ITE_BASE         ,
	in2.ITE_ALIQUOTA     ,
	in2.ITE_ICMS
FROM item_nota in2 
INTO OUTFILE '/tmp/scut-notas-fiscais-1.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- NOTAS FISCAIS 2
SELECT DISTINCT 
	in2.ITE_CODIGO       ,
	in2.ITE_DESCRICAO    ,
	in2.ITE_VALOR        ,
	in2.ITE_QTDADE       ,
	in2.ITE_VALOR_UNI    ,
	in2.ITE_OPERACAO     ,
	in2.ITE_BASE         ,
	in2.ITE_ALIQUOTA     ,
	in2.ITE_ICMS
FROM item_nota2 in2 
INTO OUTFILE '/tmp/scut-notas-fiscais-2.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- USUARIOS
SELECT DISTINCT 
	u.EMP_DOMINIO         ,
	u.USU_CODIGO          ,
	u.USU_LOGIN           ,
	u.USU_NOME            ,
	u.USU_SENHA           ,
	u.USU_NIVEL           ,
	u.USU_HORARIO_INICIO  ,
	u.USU_HORARIO_FIM     ,
	u.USU_STATUS 
FROM usuarios u 
INTO OUTFILE '/tmp/scut-usuarios.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- HISTÓRICO CLIENTE
SELECT DISTINCT 
	lc.LOG_CLI_SEQ                             ,
	CONCAT(lc.LOG_CLI_DATA, ' ', LOG_CLI_HORA) ,
	lc.LOG_CLI_USUARIO                         ,
	lc.LOG_CLI_DESCRICAO                       ,
	lc.LOG_CLI_LOGIN                           ,
	lc.LOG_CLI_DOMINIO 
FROM log_cliente lc  
INTO OUTFILE '/tmp/scut-historico-clientes.csv' CHARACTER SET utf8
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';















