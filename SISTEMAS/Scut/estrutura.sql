CREATE TABLE acesso (
	USU_CODIGO int(11) NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	MEN_CODIGO int(11) NOT NULL ,
	ACE_INCLUIR varchar(1),
	ACE_EXCLUIR varchar(1),
	ACE_ALTERAR varchar(1),
	ACE_DEGRAU varchar(1) default '0',
	PRIMARY KEY (USU_CODIGO,EMP_DOMINIO,MEN_CODIGO)
);



CREATE TABLE apagar (
	PAG_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	PAG_DATA date default '0000-00-00' NOT NULL ,
	PAG_FAVORECIDO varchar(100),
	PAG_REFERENTE varchar(100),
	PAG_NUMERO varchar(10) NOT NULL ,
	PAG_VALOR decimal(10,2) default '0.00' NOT NULL ,
	USU_LOGIN varchar(25),
	PAG_BAIXA date,
	PAG_PARCELA int(11) default '1' NOT NULL ,
	PAG_CUSTO_FIXO char(1) default 'N' NOT NULL ,
	PAG_BANCO varchar(25) NOT NULL ,
	PRIMARY KEY (PAG_CODIGO),
   KEY PAG_DATA (PAG_DATA,EMP_DOMINIO)
);

CREATE TABLE avaliacao (
	AVA_CODIGO int(11) NOT NULL auto_increment,
	CLI_LOGIN varchar(25) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	QUE_TIPO int(11) default '0' NOT NULL ,
	SUP_CODIGO int(11),
	AVA_USUARIO varchar(50),
	AVA_DATA date,
	AVA_HORA time,
	AVA_ENTREVISTADO varchar(80) NOT NULL ,
	AVA_DATA_PREVISTA date,
	AVA_CONTADOR int(11) default '1' NOT NULL ,
	AVA_STATUS char(1),
	PRIMARY KEY (AVA_CODIGO,CLI_LOGIN,EMP_DOMINIO,QUE_TIPO)
);

CREATE TABLE aviso (
	AVI_SEQ int(11) NOT NULL auto_increment,
	AVI_DATA date default '0000-00-00' NOT NULL ,
	AVI_HORA time default '00:00:00' NOT NULL ,
	AVI_IP varchar(15) NOT NULL ,
	PRIMARY KEY (AVI_SEQ)
);




CREATE TABLE baixa (
	bnid int(11) default '2' NOT NULL ,
	cod_baixa int(11) default '1' NOT NULL ,
	`desc` text NOT NULL ,
	flag varchar(1) default ' ' NOT NULL ,
	PRIMARY KEY (bnid,cod_baixa)
);




CREATE TABLE bancobranca (
	BAN_CODIGO int(11) NOT NULL auto_increment,
	BNID int(11) default '0' NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	AGENCIA varchar(10),
	FONE varchar(20),
	NR_CONTA varchar(20),
	BAN_CONVENIO varchar(20),
	CEDENTE varchar(30),
	LOCALPGTO varchar(120),
	NR_CARTEIRA varchar(20),
	INSTRUCAO1 varchar(100),
	INSTRUCAO2 varchar(100),
	INSTRUCAO3 varchar(100),
	INSTRUCAO4 varchar(80),
	BAN_LAYOUT int(11),
	INSTRUCAO_SCM varchar(120),
	ESTAB1 varchar(80),
	ESTAB3 varchar(120),
	ESTAB4 varchar(120),
	ESTAB5 varchar(120),
	ESTAB6 varchar(120),
	ESTAB7 varchar(80),
	BOLETO varchar(80),
	NR_REMESSA int(11),
	NR_REMESSA_DIA int(11),
	BAN_BOLETO int(11),
	BAN_NOME_FISICA varchar(30),
	BAN_CPF varchar(15),
	BAN_TOKEN varchar(140),
	EMP_DOMINIO_FILIAL varchar(80),
	BAN_DIAS_BAIXA int(11),
	BAN_PROTESTAR varchar(1),
	BAN_DIAS int(11),
	HOJE date,
	clientId varchar(150),
	clientSecret varchar(150),
	PRIMARY KEY (BAN_CODIGO,EMP_DOMINIO)
);

CREATE TABLE bancos (
	bnid int(10) unsigned NOT NULL auto_increment,
	layout varchar(40) NOT NULL ,
	nome varchar(30) NOT NULL ,
	codigo int(10) unsigned default '0' NOT NULL ,
	uso_do_banco varchar(50) NOT NULL ,
	ban_baixa varchar(50),
	dominio varchar(80),
   KEY bnid (bnid)
);




CREATE TABLE banda (
	BAN_CODIGO int(11) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	BAN_BANDA varchar(50),
	BAN_DESCRICAO varchar(80),
	BAN_BANDA2 varchar(50),
	BAN_DESCRICAO2 varchar(50),
	BAN_BURST_LIMIT varchar(30),
	BAN_BURST_THRESHOLD varchar(30),
	BAN_BURST_TIME varchar(30),
	BAN_PROMOCAO int(11) default '0' NOT NULL ,
	PRIMARY KEY (BAN_CODIGO,EMP_DOMINIO)
);

CREATE TABLE boletos (
	bid int(10) unsigned NOT NULL ,
	bnid int(10) unsigned default '0' NOT NULL ,
	banco varchar(3) NOT NULL ,
	cid int(10) unsigned default '0' NOT NULL ,
	titulo int(11),
	agencia varchar(10) NOT NULL ,
	cedente varchar(255) NOT NULL ,
	conta_cedente varchar(20) NOT NULL ,
	especie_documento varchar(10) NOT NULL ,
	codigo varchar(40) NOT NULL ,
	sacado varchar(120) NOT NULL ,
	cpf varchar(20) NOT NULL ,
	local_pagamento varchar(255),
	sacador varchar(50) NOT NULL ,
	carteira varchar(30) NOT NULL ,
	instrucoes_linha1 varchar(100) NOT NULL ,
	instrucoes_linha2 varchar(100) NOT NULL ,
	instrucoes_linha3 varchar(100) NOT NULL ,
	instrucoes_linha4 varchar(100) NOT NULL ,
	instrucoes_linha5 varchar(100),
	login varchar(80),
	dominio varchar(50) NOT NULL ,
	dt_emissao date,
	dt_pgto date,
	dt_venc date,
	val_titulo decimal(10,2) default '0.00' NOT NULL ,
	descontos decimal(10,2) default '0.00' NOT NULL ,
	desconto_vencimento decimal(10,2),
	juros decimal(10,2) default '0.00' NOT NULL ,
	val_total decimal(10,2) default '0.00' NOT NULL ,
	val_pago decimal(10,2) default '0.00' NOT NULL ,
	val_diferenca decimal(10,2) default '0.00' NOT NULL ,
	status int(11) default '0' NOT NULL ,
	nosso_numero varchar(20),
	situacao int(11) default '9' NOT NULL ,
	nota_emitida date,
	CLI_DIATARI int(11),
	CAI_CODIGO int(11),
	emitido int(11) default '7' NOT NULL ,
	capa char(1) default 'N' NOT NULL ,
	flag char(1) NOT NULL ,
	ano_mes_sequencia varchar(14),
	chave_digital varchar(40),
	parcela int(11) default '1' NOT NULL ,
	baixa_manual varchar(1) default ' ' NOT NULL ,
	barra varchar(255) NOT NULL ,
	barra2 varchar(255) NOT NULL ,
	link varchar(250) NOT NULL ,
	id_gerencianet int(11),
	forma_pgto varchar(30),
	PRIMARY KEY (bid,dominio),
   KEY cid (cid),
   KEY login (login),
   KEY dominio (dominio),
   KEY nosso_numero (nosso_numero),
   KEY titulo (titulo),
   KEY id_gerencianet (id_gerencianet)
);

CREATE TABLE boletos_log (
	id int(11) NOT NULL auto_increment,
	bid int(10) unsigned NOT NULL ,
	bnid int(10) unsigned default '0' NOT NULL ,
	cid int(10) unsigned default '0' NOT NULL ,
	titulo varchar(30),
	agencia varchar(10) NOT NULL ,
	cedente varchar(255) NOT NULL ,
	conta_cedente varchar(20) NOT NULL ,
	especie_documento varchar(10) NOT NULL ,
	codigo varchar(40) NOT NULL ,
	sacado varchar(120) NOT NULL ,
	cpf varchar(20) NOT NULL ,
	local_pagamento varchar(255) NOT NULL ,
	sacador varchar(50) NOT NULL ,
	carteira varchar(30) NOT NULL ,
	instrucoes_linha1 varchar(100) NOT NULL ,
	instrucoes_linha2 varchar(100) NOT NULL ,
	instrucoes_linha3 varchar(100) NOT NULL ,
	instrucoes_linha4 varchar(100) NOT NULL ,
	instrucoes_linha5 varchar(100),
	login varchar(80) NOT NULL ,
	dominio varchar(50) NOT NULL ,
	dt_emissao date,
	dt_pgto date,
	dt_venc date,
	val_titulo decimal(10,2) default '0.00' NOT NULL ,
	descontos decimal(10,2) default '0.00' NOT NULL ,
	juros decimal(10,2) default '0.00' NOT NULL ,
	val_total decimal(10,2) default '0.00' NOT NULL ,
	val_pago decimal(10,2) default '0.00' NOT NULL ,
	status int(11) default '0' NOT NULL ,
	nosso_numero int(11),
	situacao int(11) default '9' NOT NULL ,
	nota_emitida date,
	CLI_DIATARI int(11),
	CAI_CODIGO int(11),
	emitido int(11) default '7' NOT NULL ,
	capa char(1) default 'N' NOT NULL ,
	flag char(1) NOT NULL ,
	ano_mes_sequencia varchar(14),
	chave_digital varchar(40),
	usuario varchar(50) NOT NULL ,
	data date NOT NULL ,
	hora time NOT NULL ,
	barra varchar(250) NOT NULL ,
	barra2 varchar(250) NOT NULL ,
	ip varchar(20),
	ip2 varchar(20),
	PRIMARY KEY (id,bid,login,dominio),
   KEY cid (cid),
   KEY login (login),
   KEY dominio (dominio)
);




CREATE TABLE caixa (
	CAI_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	USU_CODIGO int(11) default '0' NOT NULL ,
	CAI_DATA date,
	CAI_HORA time,
	CAI_TIPO char(1),
	CAI_SALDO_ANT decimal(10,2),
	CAI_VALOR decimal(10,2),
	CAI_SALDO decimal(10,2),
	CAI_DC char(1),
	CAI_DESCRICAO varchar(80),
	USU_LOGIN varchar(20),
	bid int(11),
	CAI_ANTECIPADO int(11) default '0' NOT NULL ,
	EMP_DOMINIO_FILIAL varchar(80) NOT NULL ,
	PRIMARY KEY (CAI_CODIGO,EMP_DOMINIO,USU_CODIGO),
   KEY USU_LOGIN (USU_LOGIN),
   KEY USU_LOGIN_2 (USU_LOGIN),
   KEY USU_LOGIN_3 (USU_LOGIN),
   KEY bid (bid)
);

CREATE TABLE cancelamento (
	CAN_CODIGO int(11) default '0' NOT NULL ,
	CAN_ID int(11) NOT NULL auto_increment,
	CLI_LOGIN varchar(15) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	USU_LOGIN varchar(80),
	CAN_DATA date,
	CAN_HORA time NOT NULL ,
	CAN_MOTIVO text,
	MOT_DESCRICAO varchar(80) NOT NULL ,
	PRIMARY KEY (CAN_ID),
   KEY CAN_CODIGO (CAN_CODIGO,CLI_LOGIN,EMP_DOMINIO)
);


CREATE TABLE cep_scut (
	cidade varchar(50),
	estado varchar(2) NOT NULL ,
	logradouro varchar(70),
	bairro varchar(72),
	cep varchar(9) NOT NULL ,
	tp_logradouro varchar(20),
	IBGE int(11) NOT NULL ,
	PRIMARY KEY (cep),
   KEY cidade (cidade)
);




CREATE TABLE cep_unico (
	Seq bigint(20) default '0' NOT NULL ,
	Nome varchar(50) NOT NULL ,
	NomeSemAcento varchar(50),
	Cep varchar(9),
	UF char(2) NOT NULL ,
	PRIMARY KEY (Seq),
   KEY idx_cep_loc (Cep)
);




CREATE TABLE cepbr_bairro (
	id_bairro int(11) NOT NULL ,
	bairro varchar(100),
	id_cidade int(11),
	PRIMARY KEY (id_bairro),
   KEY id_cidade (id_cidade)
);




CREATE TABLE cepbr_cidade (
	id_cidade int(11) NOT NULL ,
	cidade varchar(100),
	uf varchar(2),
	cep varchar(16),
	cod_ibge varchar(10) default '0' NOT NULL ,
	area float default '0',
	id_municipio_subordinado int(11),
	PRIMARY KEY (id_cidade),
   KEY uf (uf)
);




CREATE TABLE cepbr_endereco (
	cep varchar(10) NOT NULL ,
	logradouro varchar(200),
	tipo_logradouro varchar(80),
	complemento varchar(100),
	local varchar(120),
	id_cidade int(11),
	id_bairro int(11),
	PRIMARY KEY (cep),
   KEY id_cidade (id_cidade),
   KEY id_bairro (id_bairro)
);




CREATE TABLE cepbr_estado (
	uf varchar(2) NOT NULL ,
	estado varchar(100),
	cod_ibge varchar(10) default '0' NOT NULL ,
	PRIMARY KEY (uf)
);




CREATE TABLE cfop (
	CFOP_ID int(11) NOT NULL ,
	CFOP_DESCRICAO varchar(255) NOT NULL ,
	CFOP_FLAG varchar(4),
	PRIMARY KEY (CFOP_ID)
);




CREATE TABLE changelog (
	CHANGELOG_CODIGO int(10) unsigned NOT NULL auto_increment,
	CHANGELOG_DESC varchar(80) NOT NULL ,
	CHANGELOG_DATA date default '0000-00-00' NOT NULL ,
	CHANGELOG_VERSAO varchar(10) NOT NULL ,
	CHANGELOG_FLAG varchar(7) NOT NULL ,
	PRIMARY KEY (CHANGELOG_CODIGO)
);




CREATE TABLE changelog_flag (
	CHANGELOG_FLAG_CODIGO int(10) unsigned NOT NULL auto_increment,
	CHANGELOG_FLAG varchar(7) NOT NULL ,
	CHANGELOG_FLAG_NAME varchar(15) NOT NULL ,
	CHANGELOG_FLAG_DESC varchar(80) NOT NULL ,
	PRIMARY KEY (CHANGELOG_FLAG_CODIGO)
);




CREATE TABLE cheque (
	CHE_CODIGO int(11) NOT NULL auto_increment,
	CAI_CODIGO int(11) default '0' NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	CHE_NUMERO varchar(15),
	CHE_NOME varchar(80),
	CHE_BANCO decimal(5,0),
	CHE_AGENCIA varchar(5),
	CHE_CONTA varchar(20),
	CHE_VALOR decimal(10,2),
	CHE_DC char(1),
	CHE_DATA_EMISSAO date,
	CHE_DATA_DEPOSITO date,
	USU_NOME varchar(80),
	PRIMARY KEY (CHE_CODIGO,CAI_CODIGO,EMP_DOMINIO),
   KEY IDX_cheque1 (EMP_DOMINIO)
);




CREATE TABLE cheque_temp (
	CHE_CODIGO int(11) NOT NULL auto_increment,
	NUMERO int(11) default '0' NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	CHE_NUMERO varchar(15),
	CHE_NOME varchar(80),
	CHE_BANCO decimal(5,0),
	CHE_AGENCIA varchar(5),
	CHE_CONTA varchar(20),
	CHE_VALOR decimal(10,2),
	CHE_DC char(1),
	CHE_DATA_EMISSAO date,
	CHE_DATA_DEPOSITO date,
	USU_NOME varchar(80),
	PRIMARY KEY (CHE_CODIGO,NUMERO),
   KEY IDX_cheque1 (EMP_DOMINIO)
);




CREATE TABLE cidades (
	CID_CODIGO int(11) NOT NULL auto_increment,
	CID_ESTADO char(2) default 'SP' NOT NULL ,
	CID_NOME varchar(50) NOT NULL ,
	PRIMARY KEY (CID_CODIGO)
);




CREATE TABLE classe (
	CLA_CODIGO int(11) NOT NULL auto_increment,
	CLA_DESCRICAO varchar(50),
	PRIMARY KEY (CLA_CODIGO)
);




CREATE TABLE cliente_mk (
	EMP_DOMINIO varchar(80) NOT NULL ,
	CLI_LOGIN varchar(50) NOT NULL ,
	CMK_DHCP varchar(1),
	CMK_IP_MK varchar(50),
	INT_DESCRICAO varchar(80),
	CMK_HOTSPOT_PROFILE varchar(50),
	COM_TIPO varchar(20),
	CMK_GUPO varchar(20) default ' ' NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,CLI_LOGIN)
);

CREATE TABLE clientes (
	CLI_LOGIN varchar(50) NOT NULL ,
	EMP_DOMINIO varchar(50) default '@scut.com.br' NOT NULL ,
	CLI_SENHA varchar(80),
	CLI_CGC varchar(18),
	CLI_CPF varchar(14),
	CLI_INSCRICAO varchar(20),
	CLI_TIPO int(11) default '1' NOT NULL ,
	CLI_NOME varchar(80),
	CLI_ENDERECO varchar(80),
	CLI_REFERENCIA varchar(120) NOT NULL ,
	CLI_CIDADE varchar(30),
	CLI_ESTADO char(2),
	CLI_BAIRRO varchar(30),
	CLI_CEP varchar(9),
	CLI_COMPLEMENTO varchar(80),
	CLI_DIATARI int(11),
	CLI_TIPOTAR int(11),
	CLI_FONE varchar(14),
	CLI_FAX varchar(20),
	CLI_CELULAR varchar(20),
	CLI_OPERADORA varchar(30) default '0' NOT NULL ,
	CLI_NOTAFIS char(1),
	CLI_DESCONTOS decimal(10,2),
	CLI_DTNASCIMENTO date,
	CLI_DTCADASTRO date,
	CLI_DTCONTRATO int(11),
	CLI_MESES int(11),
	CLI_INICIO date,
	CLI_ATIVACAO date,
	CLI_BLOQUEADO date,
	CLI_SUSPENSO date,
	CLI_DTCANCELAMENTO date,
	CLI_BOLETO char(1),
	CLI_OBS text,
	MEN_CODIGO int(11) NOT NULL ,
	CLI_TIPOPLANO int(11) default '1' NOT NULL ,
	CLI_EMAIL varchar(80),
	CLI_MAC varchar(80),
	DEB_BANCO varchar(30),
	DEB_AGENCIA varchar(10),
	DEB_CONTA varchar(10),
	CLI_NR_CONTRATO int(11) default '0',
	CLI_FLAG char(1) default 'N',
	SSID_NUMERO varchar(80),
	CLI_CORTAR int(11) default '0' NOT NULL ,
	CLI_OBS_POSVENDA text,
	CLA_CODIGO int(11) default '6' NOT NULL ,
	CLI_TV_CABO varchar(1) default '0' NOT NULL ,
	BNID int(11),
	TOR_CODIGO int(11) default '0',
	COR_CODIGO int(11) default '0',
	CLI_WIRELESS varchar(1) default '0',
	CLI_PORTA_GRAFICO varchar(20),
	CLI_OBS_CONTRATO varchar(120),
	PAR_CODIGO int(11) default '0' NOT NULL ,
	CLI_LIBERADO date,
	EMP_DOMINIO_FILIAL varchar(80) NOT NULL ,
	CLI_CHAVE_CENTRAL varchar(20) NOT NULL ,
	CLI_VISADA varchar(1) default ' ',
	BAN_CODIGO int(11) default '0' NOT NULL ,
	CFOP varchar(4),
	SET_CODIGO int(11) default '0' NOT NULL ,
	CLI_MAC_OLD varchar(50),
	CLI_IBGE varchar(7),
	CLI_DIAS_BLOQUEIO int(11) default '0',
	CLI_LAT float(10,6) default '0.000000',
	CLI_LONG float(10,6) default '0.000000',
	CLI_MK varchar(80),
	CLI_NOME_MK varchar(100),
	CLI_IP varchar(20),
	CLI_PROTESTAR varchar(1) default 'N' NOT NULL ,
	CLI_AVISO varchar(1) NOT NULL ,
	TEC_DICI varchar(50) NOT NULL ,
	CLI_MEIO varchar(50) NOT NULL ,
	DICI_PRODUTO varchar(50) NOT NULL ,
	TIPO_CLIENTE varchar(20) NOT NULL ,
	PRIMARY KEY (CLI_LOGIN,EMP_DOMINIO)
);


CREATE TABLE clientes2 (
	CLI_LOGIN varchar(50) NOT NULL ,
	EMP_DOMINIO varchar(50) default '@scut.com.br' NOT NULL ,
	CLI_SENHA varchar(80),
	CLI_CGC varchar(18),
	CLI_CPF varchar(14),
	CLI_INSCRICAO varchar(20),
	CLI_TIPO int(11) default '1' NOT NULL ,
	CLI_NOME varchar(80),
	CLI_ENDERECO varchar(80),
	CLI_REFERENCIA varchar(120) NOT NULL ,
	CLI_CIDADE varchar(30),
	CLI_ESTADO char(2),
	CLI_BAIRRO varchar(30),
	CLI_CEP varchar(9),
	CLI_COMPLEMENTO varchar(80),
	CLI_DIATARI int(11),
	CLI_TIPOTAR int(11),
	CLI_FONE varchar(14),
	CLI_FAX varchar(20),
	CLI_CELULAR varchar(20),
	CLI_OPERADORA varchar(30) default '0' NOT NULL ,
	CLI_NOTAFIS char(1),
	CLI_DESCONTOS decimal(10,2),
	CLI_DTNASCIMENTO date,
	CLI_DTCADASTRO date,
	CLI_DTCONTRATO int(11),
	CLI_MESES int(11),
	CLI_INICIO date,
	CLI_ATIVACAO date,
	CLI_BLOQUEADO date,
	CLI_SUSPENSO date,
	CLI_DTCANCELAMENTO date,
	CLI_BOLETO char(1),
	CLI_OBS text,
	MEN_CODIGO int(11) NOT NULL ,
	CLI_TIPOPLANO int(11) default '1' NOT NULL ,
	CLI_EMAIL varchar(80),
	CLI_MAC varchar(80),
	DEB_BANCO varchar(30),
	DEB_AGENCIA varchar(10),
	DEB_CONTA varchar(10),
	CLI_NR_CONTRATO int(11) default '0',
	CLI_FLAG char(1) default 'N',
	SSID_NUMERO varchar(80),
	CLI_CORTAR int(11) default '0' NOT NULL ,
	CLI_OBS_POSVENDA text,
	CLA_CODIGO int(11) default '6' NOT NULL ,
	CLI_TV_CABO varchar(1) default '0' NOT NULL ,
	BNID int(11),
	TOR_CODIGO int(11) default '0',
	COR_CODIGO int(11) default '0',
	CLI_WIRELESS varchar(1) default '0',
	CLI_PORTA_GRAFICO varchar(20),
	CLI_OBS_CONTRATO varchar(120),
	PAR_CODIGO int(11) default '0' NOT NULL ,
	CLI_LIBERADO date,
	EMP_DOMINIO_FILIAL varchar(80) NOT NULL ,
	CLI_CHAVE_CENTRAL varchar(20) NOT NULL ,
	CLI_VISADA varchar(1) default ' ',
	BAN_CODIGO int(11) default '0' NOT NULL ,
	CFOP varchar(4),
	SET_CODIGO int(11) default '0' NOT NULL ,
	CLI_MAC_OLD varchar(50),
	CLI_IBGE varchar(7),
	CLI_DIAS_BLOQUEIO int(11) default '0',
	CLI_LAT float(10,6) default '0.000000',
	CLI_LONG float(10,6) default '0.000000',
	CLI_MK varchar(80),
	CLI_NOME_MK varchar(100),
	CLI_IP varchar(20),
	CLI_PROTESTAR varchar(1) default 'N' NOT NULL ,
	CLI_AVISO varchar(1) NOT NULL ,
	TEC_DICI varchar(50) NOT NULL ,
	CLI_MEIO varchar(50) NOT NULL ,
	DICI_PRODUTO varchar(50) NOT NULL ,
	TIPO_CLIENTE varchar(20) NOT NULL ,
	PRIMARY KEY (CLI_LOGIN,EMP_DOMINIO)
);




CREATE TABLE clientes_mensalidade (
	CLI_LOGIN varchar(50) NOT NULL ,
	EMP_DOMINIO varchar(80) default '@scut.com.br' NOT NULL ,
	MEN_CODIGO int(11) default '0' NOT NULL ,
	QTDADE int(11) default '1' NOT NULL ,
	PRIMARY KEY (CLI_LOGIN,MEN_CODIGO,EMP_DOMINIO)
);

CREATE TABLE cobranca (
	CLI_LOGIN varchar(50) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	COB_CIDADE varchar(30),
	COB_ENDERECO varchar(80),
	COB_ESTADO char(2),
	COB_CEP varchar(9),
	COB_BAIRRO varchar(30),
	COB_COMPLEMENTO varchar(50),
	PRIMARY KEY (CLI_LOGIN,EMP_DOMINIO)
);




CREATE TABLE comandos_mk (
	COM_CODIGO int(11) NOT NULL auto_increment,
	COM_VERSAO varchar(2) NOT NULL ,
	COM_NRVERSAO int(11) NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	COM_COMANDO text NOT NULL ,
	COM_TIPO varchar(20),
	COM_FLAG varchar(5) default '0' NOT NULL ,
	OBS text,
	COM_SEM_MAC int(11) NOT NULL ,
	COM_GRUPO varchar(1) NOT NULL ,
	COM_NEWTERMINAL text NOT NULL ,
	PRIMARY KEY (COM_CODIGO,COM_VERSAO)
);




CREATE TABLE comodato (
	CLI_LOGIN varchar(50) NOT NULL ,
	COM_SEQ int(11) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	MAT_CODIGO int(11) default '0' NOT NULL ,
	COM_QTDADE decimal(10,2),
	COM_DATA date,
	SUP_CODIGO int(11),
	PRIMARY KEY (CLI_LOGIN,EMP_DOMINIO,MAT_CODIGO,COM_SEQ)
);



CREATE TABLE complemento (
	COM_CODIGO int(11) NOT NULL auto_increment,
	SUP_CODIGO int(11) default '0' NOT NULL ,
	COM_TRANS varchar(30),
	COM_KMSAIDA varchar(10),
	COM_KMCHEGADA varchar(10),
	COM_HCHEGADA time,
	COM_HSAIDA time,
	COM_HENTREGA time,
	COM_MAC varchar(30),
	COM_IP varchar(30),
	COM_ISSID varchar(30),
	COM_OBS varchar(50),
	PRIMARY KEY (COM_CODIGO),
   KEY SUP_CODIGO (SUP_CODIGO)
);




CREATE TABLE conexao (
	EMP_DOMINIO varchar(80) NOT NULL ,
	MK_IP varchar(50) NOT NULL ,
	COM_TIPO varchar(50) NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,MK_IP,COM_TIPO)
);


CREATE TABLE conta (
	CON_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	CON_AGENCIA varchar(6) NOT NULL ,
	CON_NUMERO varchar(12),
	CON_BANCO varchar(30),
	CON_TITULAR varchar(80),
	CON_FLAG char(1),
	PRIMARY KEY (CON_CODIGO,EMP_DOMINIO)
);

CREATE TABLE contador (
	id int(11) NOT NULL auto_increment,
	visitas int(11),
	PRIMARY KEY (id)
);




CREATE TABLE corujao (
	COR_CODIGO int(11) NOT NULL auto_increment,
	COR_DESCRICAO varchar(50),
	COR_TIME varchar(20) NOT NULL ,
	COR_DIAS varchar(80),
	PRIMARY KEY (COR_CODIGO)
);




CREATE TABLE descontos (
	DES_CODIGO int(11) default '0' NOT NULL ,
	CLI_LOGIN varchar(15) NOT NULL ,
	EMP_DOMINIO varchar(50),
	EMP_CODIGO int(11) default '0' NOT NULL ,
	DESC_DESCRICAO varchar(80),
	DESC_VALOR decimal(10,2),
	PRIMARY KEY (DES_CODIGO)
);




CREATE TABLE dici (
	ID int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(50) NOT NULL ,
	ANO int(4) NOT NULL ,
	MES int(2) NOT NULL ,
	CNPJ varchar(14) NOT NULL ,
	COD_IBGE varchar(7) NOT NULL ,
	TIPO_CLIENTE varchar(2) NOT NULL ,
	TIPO_ATENDIMENTO varchar(20) NOT NULL ,
	TIPO_MEIO varchar(20) NOT NULL ,
	TIPO_PRODUTO varchar(20) NOT NULL ,
	TIPO_TECNOLOGIA varchar(20) NOT NULL ,
	VELOCIDADE varchar(10) NOT NULL ,
	QT_ACESSOS int(10) NOT NULL ,
	PRIMARY KEY (ID)
);

CREATE TABLE diciproduto (
	DICI_ID int(11) NOT NULL auto_increment,
	DICI_PRODUTO varchar(50) NOT NULL ,
	DICI_DEDECAO varchar(50) NOT NULL ,
	PRIMARY KEY (DICI_ID)
);




CREATE TABLE dominio (
	DOM_CODIGO int(11) NOT NULL auto_increment,
	CLI_LOGIN varchar(15),
	EMP_DOMINIO varchar(50),
	DOM_NOME varchar(80),
	PRIMARY KEY (DOM_CODIGO)
);




CREATE TABLE empresa (
	EMP_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(50) NOT NULL ,
	EMP_RAZAO varchar(80),
	EMP_FANTAZIA varchar(80),
	EMP_ENDERECO varchar(100),
	EMP_NUMERO varchar(10) NOT NULL ,
	EMP_COMPLEMENTO varchar(30) NOT NULL ,
	EMP_CIDADE varchar(30),
	EMP_ESTADO char(2),
	EMP_BAIRRO varchar(30),
	EMP_CEP varchar(9),
	EMP_CGC varchar(19),
	EMP_INSCRICAO varchar(20),
	EMP_FONE varchar(60),
	EMP_0800 varchar(50) NOT NULL ,
	EMP_DDD varchar(4),
	EMP_FAX varchar(20),
	EMP_DIAS smallint(6) default '0' NOT NULL ,
	EMP_DIAS_TOLERANCIA int(11) NOT NULL ,
	EMP_DIAS_AVISO int(11) default '2' NOT NULL ,
	EMP_ADMIN varchar(80),
	EMP_PADMIN varchar(15),
	EMP_MENS varchar(255),
	EMP_DATA date,
	EMP_REDUCAO decimal(10,2) default '0.00' NOT NULL ,
	EMP_ALIQUOTA decimal(10,2) default '0.00' NOT NULL ,
	EMP_OBS text,
	EMP_HOST varchar(30),
	EMP_USER varchar(30),
	EMP_SENHA varchar(30),
	EMP_MIKROTIK varchar(30),
	EMP_MKNOME varchar(80),
	EMP_MIKROTIK_V varchar(10),
	EMP_MIKROTIK2 varchar(30),
	EMP_MKNOME2 varchar(80),
	EMP_MIKROTIK2_V varchar(10),
	EMP_MIKROTIK3 varchar(30),
	EMP_MKNOME3 varchar(80),
	EMP_MIKROTIK3_V varchar(10),
	EMP_MIKROTIK4 varchar(30),
	EMP_MKNOME4 varchar(80),
	EMP_MIKROTIK4_V varchar(10),
	EMP_PAGAMENTO date,
	EMP_WWW varchar(80) NOT NULL ,
	EMP_PPPOE varchar(1),
	EMP_HOTSPOT varchar(1),
	EMP_IPMAC varchar(1),
	EMP_VER_MK varchar(10),
	EMP_DHCP varchar(1),
	EMP_MULTA decimal(10,2),
	EMP_MULTA_PER decimal(10,2),
	EMP_JUROS decimal(10,2),
	EMP_JUROS_PER decimal(10,5),
	EMP_OCULTA_MALA_DIRETA char(1) NOT NULL ,
	EMP_RESPONSAVEL varchar(28) NOT NULL ,
	EMP_ATIVA varchar(1) NOT NULL ,
	EMP_SEPARA_OS varchar(1) NOT NULL ,
	EMP_ITEM varchar(1) NOT NULL ,
	EMP_EMITE_BLOQUEADOS varchar(1) NOT NULL ,
	EMP_CAIXA int(11) NOT NULL ,
	EMP_SMS_GATEWAY varchar(2) NOT NULL ,
	EMP_SMS_EMPRESA varchar(50) NOT NULL ,
	EMP_SMS varchar(250) NOT NULL ,
	EMP_SMS_USER varchar(50) NOT NULL ,
	EMP_SMS_SENHA varchar(50) NOT NULL ,
	EMP_TOLERANCIA int(11) NOT NULL ,
	EMP_SMTP varchar(150) NOT NULL ,
	EMP_EMAIL_SMTP varchar(150) NOT NULL ,
	EMP_SENHA_SMTP varchar(50) NOT NULL ,
	EMP_INSTALACAO int(11) NOT NULL ,
	EMP_MANUTENCAO int(11) NOT NULL ,
	EMP_SUSPENSA varchar(1) NOT NULL ,
	EMP_CIDADE2 varchar(80) NOT NULL ,
	EMP_ESTADO2 varchar(2) NOT NULL ,
	EMP_CEP2 varchar(10) NOT NULL ,
	EMP_CPF_CLIENTE varchar(1) default 'N' NOT NULL ,
	EMP_ENVIA_MAIL varchar(1) NOT NULL ,
	EMP_ENVIA_EMAIL_DIAS int(11) default '0' NOT NULL ,
	EMP_BAIXAR varchar(1) default 'S' NOT NULL ,
	EMP_LAT float(10,6) NOT NULL ,
	EMP_LONG float(10,6) NOT NULL ,
	EMP_LIBERA varchar(1) default 'N' NOT NULL ,
	EMP_CANCELADA date,
	EMP_TOKEN varchar(80) NOT NULL ,
	EMP_MEN1 varchar(100) NOT NULL ,
	EMP_MEN2 varchar(100) NOT NULL ,
	EMP_ULTIMO_BOLETO int(11) NOT NULL ,
	EMP_PIX varchar(1),
	PRIMARY KEY (EMP_CODIGO,EMP_DOMINIO)
);

CREATE TABLE erros (
	bnid int(11) NOT NULL ,
	cod_erro varchar(11) NOT NULL ,
	erro text NOT NULL ,
	PRIMARY KEY (bnid,cod_erro)
);




CREATE TABLE erros2 (
	bnid int(11) NOT NULL ,
	cod_erro varchar(11) NOT NULL ,
	erro text NOT NULL ,
	flag varchar(1) NOT NULL ,
	PRIMARY KEY (bnid,cod_erro)
);




CREATE TABLE extrato (
	data datetime default '0000-00-00 00:00:00' NOT NULL ,
	login varchar(30) NOT NULL ,
	fone varchar(10),
	ip varchar(15) NOT NULL ,
	seg int(11) default '0' NOT NULL ,
	inicio datetime default '0000-00-00 00:00:00' NOT NULL ,
	tempo time,
	ras varchar(5) NOT NULL ,
	PRIMARY KEY (login,data)
);




CREATE TABLE feriados (
	FER_ID int(11) NOT NULL auto_increment,
	FER_DATA date NOT NULL ,
	FER_SEMANA varchar(25) NOT NULL ,
	PRIMARY KEY (FER_ID)
);




CREATE TABLE fornecedores (
	FOR_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	FOR_NOME varchar(80) NOT NULL ,
	FOR_ENDERECO varchar(100) NOT NULL ,
	FOR_CIDADE varchar(50) NOT NULL ,
	FOR_ESTADO varchar(2) NOT NULL ,
	FOR_FONE varchar(30) NOT NULL ,
	FOR_CONTATO varchar(80) NOT NULL ,
	FOR_CNPJ varchar(20) NOT NULL ,
	FOR_INSCRICAO varchar(20) NOT NULL ,
	FOR_EMAIL varchar(80) NOT NULL ,
	FOR_CEP varchar(10) NOT NULL ,
	FOR_BAIRRO varchar(30) NOT NULL ,
	PRIMARY KEY (FOR_CODIGO,EMP_DOMINIO)
);




CREATE TABLE futuro (
	fut_codigo int(11) NOT NULL auto_increment,
	cli_login varchar(50) NOT NULL ,
	emp_dominio varchar(80) default '0' NOT NULL ,
	fut_data date,
	fut_somar decimal(10,2),
	fut_diminuir decimal(10,2),
	fut_qtdade decimal(10,2) default '1.00' NOT NULL ,
	fut_descricao varchar(80) NOT NULL ,
	MAT_CODIGO int(11),
	PRIMARY KEY (fut_codigo,emp_dominio),
   KEY emp_dominio (emp_dominio)
);




CREATE TABLE horario (
	EMP_DOMINIO varchar(80) NOT NULL ,
	HOR_CODIGO int(11) NOT NULL auto_increment,
	HOR_DESCRICAO varchar(80) NOT NULL ,
	PRIMARY KEY (HOR_CODIGO),
   KEY EMP_DOMINIO (EMP_DOMINIO)
);




CREATE TABLE ibge (
	CODIGO int(11) NOT NULL ,
	CIDADE varchar(80) NOT NULL ,
	PRIMARY KEY (CODIGO)
);




CREATE TABLE info (
	id int(11) NOT NULL auto_increment,
	info_titulo varchar(80) NOT NULL ,
	info_desc text NOT NULL ,
	info_desc1 text,
	info_link varchar(120),
	PRIMARY KEY (id)
);




CREATE TABLE interface (
	INT_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	EMP_MKNOME varchar(30) NOT NULL ,
	INT_DESCRICAO varchar(80),
	INT_MAC varchar(30),
	INT_ARP varchar(1),
	TIN_CODIGO int(11) default '0' NOT NULL ,
	MK_IP varchar(50),
	INT_DHCP varchar(30),
	PRIMARY KEY (INT_CODIGO,EMP_DOMINIO,EMP_MKNOME)
);

CREATE TABLE ips (
	IPS_STATUS int(11) default '0' NOT NULL ,
	IPS_SEQUENCIA int(11) NOT NULL auto_increment,
	IPS_NUMERO varchar(15) NOT NULL ,
	IPS_GW varchar(20) NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	MK_IP varchar(50),
	IPS_BARRAMENTO varchar(3) default '/30' NOT NULL ,
	INT_DESCRICAO varchar(80) default 'Clientes' NOT NULL ,
	IPS_PRIMEIRO int(11) default '0' NOT NULL ,
	IPS_SELECIONADO varchar(1) NOT NULL ,
	USU_CODIGO int(11) NOT NULL ,
	IPS_AVULSO varchar(1) NOT NULL ,
	PRIMARY KEY (IPS_SEQUENCIA),
   KEY IPS_NUMERO (IPS_NUMERO)
);

CREATE TABLE item_nota (
	ITE_CODIGO int(11) NOT NULL auto_increment,
	BID int(11) default '0' NOT NULL ,
	EMP_DOMINIO varchar(50) default '@commtat.com.br' NOT NULL ,
	ITE_DESCRICAO varchar(80),
	ITE_VALOR decimal(10,2),
	ITE_QTDADE decimal(10,2),
	ITE_VALOR_UNI decimal(10,2),
	ITE_OPERACAO char(1) default 'C' NOT NULL ,
	MEN_CODIGO int(11) default '0' NOT NULL ,
	NR int(11) default '0' NOT NULL ,
	ITE_BASE decimal(10,2),
	ITE_REDUCAO decimal(10,2),
	ITE_ALIQUOTA decimal(10,2),
	ITE_ICMS decimal(10,2),
	MEN_DICI int(10) default '0' NOT NULL ,
	MEN_ICMS varchar(1) NOT NULL ,
	PRIMARY KEY (ITE_CODIGO,BID,EMP_DOMINIO),
   KEY BID (BID),
   KEY EMP_DOMINIO (EMP_DOMINIO)
);

CREATE TABLE item_nota_log (
	ITE_CODIGO int(11) NOT NULL auto_increment,
	BID int(11) default '0' NOT NULL ,
	EMP_DOMINIO varchar(50) default '@commtat.com.br' NOT NULL ,
	ITE_DESCRICAO varchar(80),
	ITE_VALOR decimal(10,2),
	ITE_QTDADE decimal(10,2) default '1.00' NOT NULL ,
	ITE_VALOR_UNI decimal(10,2),
	ITE_OPERACAO char(1) default 'C' NOT NULL ,
	PRIMARY KEY (ITE_CODIGO,BID,EMP_DOMINIO)
);

CREATE TABLE log_cliente (
	LOG_CLI_SEQ int(11) NOT NULL auto_increment,
	LOG_CLI_DATA date,
	LOG_CLI_HORA time,
	LOG_CLI_USUARIO varchar(80),
	LOG_CLI_DESCRICAO text,
	LOG_CLI_LOGIN varchar(50) NOT NULL ,
	LOG_CLI_DOMINIO varchar(80) NOT NULL ,
	PRIMARY KEY (LOG_CLI_SEQ,LOG_CLI_LOGIN,LOG_CLI_DOMINIO),
   KEY LOG_CLI_LOGIN (LOG_CLI_LOGIN),
   KEY LOG_CLI_DATA (LOG_CLI_DATA)
);

CREATE TABLE log_comandos (
	id int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(120) NOT NULL ,
	COMANDO text NOT NULL ,
	DATA date NOT NULL ,
	HORA time NOT NULL ,
	USUARIO varchar(50) NOT NULL ,
	LOGIN varchar(50) NOT NULL ,
	PRIMARY KEY (id)
);


CREATE TABLE log_obs (
	OBS_CLI_SEQ int(11) NOT NULL auto_increment,
	OBS_CLI_DATA date,
	OBS_CLI_HORA time,
	OBS_CLI_USUARIO varchar(80),
	OBS_CLI_DESCRICAO text,
	OBS_CLI_DESCRICAO_OLD text,
	OBS_CLI_LOGIN varchar(50) NOT NULL ,
	OBS_CLI_DOMINIO varchar(80) NOT NULL ,
	PRIMARY KEY (OBS_CLI_SEQ,OBS_CLI_LOGIN,OBS_CLI_DOMINIO),
   KEY OBS_CLI_LOGIN (OBS_CLI_LOGIN),
   KEY OBS_CLI_DATA (OBS_CLI_DATA)
);




CREATE TABLE log_usuario (
	id int(11) NOT NULL auto_increment,
	dominio varchar(80) NOT NULL ,
	login varchar(50) NOT NULL ,
	ip varchar(20) NOT NULL ,
	data date NOT NULL ,
	hora time NOT NULL ,
	data_hora datetime NOT NULL ,
	chave varchar(20) NOT NULL ,
	PRIMARY KEY (id)
);




CREATE TABLE logados (
	SEQUENCIA int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	RB varchar(50) NOT NULL ,
	C1 varchar(50),
	C2 varchar(50),
	C3 varchar(150),
	C4 varchar(50),
	C5 varchar(50),
	USER varchar(50) NOT NULL ,
	C6 varchar(50) NOT NULL ,
	C7 varchar(50) NOT NULL ,
	C8 varchar(50) NOT NULL ,
	C9 varchar(50) NOT NULL ,
	C10 varchar(50) NOT NULL ,
	C11 varchar(50) NOT NULL ,
	C12 varchar(50) NOT NULL ,
	C13 varchar(50) NOT NULL ,
	C14 varchar(50) NOT NULL ,
	C15 varchar(50) NOT NULL ,
	C16 varchar(50) NOT NULL ,
	C17 varchar(50) NOT NULL ,
	C18 varchar(50) NOT NULL ,
	C19 varchar(50) NOT NULL ,
	C20 varchar(50) NOT NULL ,
	PRIMARY KEY (SEQUENCIA)
);

CREATE TABLE logs (
	EMP_DOMINIO varchar(100) NOT NULL ,
	CLI_LOGIN varchar(50) NOT NULL ,
	LOG_DATA date NOT NULL ,
	LOG_HORA time NOT NULL ,
	LOG_MK varchar(100) NOT NULL ,
	LOG_CONEXAO varchar(20) NOT NULL ,
	LOG_IP varchar(20) NOT NULL ,
	LOG_MAC varchar(20) NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,CLI_LOGIN,LOG_DATA,LOG_HORA)
);




CREATE TABLE logs_temp (
	LOG_ID int(11) NOT NULL auto_increment,
	LOG_DATA varchar(300) NOT NULL ,
	PRIMARY KEY (LOG_ID)
);




CREATE TABLE markers (
	id int(11) NOT NULL auto_increment,
	name varchar(60) NOT NULL ,
	address varchar(80) NOT NULL ,
	lat float(10,6) NOT NULL ,
	lng float(10,6) NOT NULL ,
	type varchar(30) NOT NULL ,
	PRIMARY KEY (id)
);




CREATE TABLE material (
	MAT_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) default '@commtat.com.br' NOT NULL ,
	MAT_DESCRICAO varchar(80),
	MAT_UNIDADE char(3),
	MAT_VALOR decimal(10,2) default '0.00',
	MAT_ESTOQUE decimal(10,2) default '0.00',
	MAT_ESTMIN decimal(10,2) default '0.00',
	MAT_TIPO int(11) default '1' NOT NULL ,
	PRIMARY KEY (MAT_CODIGO,EMP_DOMINIO)
);

CREATE TABLE meio (
	MEI_ID int(11) NOT NULL auto_increment,
	MEI_DESCRICAO varchar(50) NOT NULL ,
	MEI_USUAL varchar(50) NOT NULL ,
	PRIMARY KEY (MEI_ID)
);




CREATE TABLE mensagem (
	MEN_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	MEN_MENSAGEM text,
	MEN_STATUS int(11) default '2' NOT NULL ,
	MEN_SERVIDOR varchar(50),
	MEN_PORTA varchar(10),
	MEN_IP varchar(20),
	PRIMARY KEY (MEN_CODIGO,EMP_DOMINIO,MEN_STATUS)
);




CREATE TABLE mensalidade (
	MEN_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) default '@scut.com.br' NOT NULL ,
	MEN_DESCRICAO varchar(80),
	MEN_VALOR decimal(10,2),
	MEN_NRHORAS int(11) default '0' NOT NULL ,
	MEN_VAL_ADICIONAL decimal(10,2) default '0.00',
	MEN_MENSAGEM varchar(40),
	MEN_DESCONTOS decimal(10,2),
	BAN_CODIGO int(11),
	MEN_INICIO int(11),
	MEN_FIM time,
	MEN_QUOTA varchar(50),
	HOR_CODIGO int(11) NOT NULL ,
	MEN_STATUS varchar(10) NOT NULL ,
	MEN_DICI int(10),
	MEN_ICMS varchar(1) default 'S' NOT NULL ,
	PRIMARY KEY (MEN_CODIGO,EMP_DOMINIO)
);

CREATE TABLE menu (
	MEN_CODIGO int(11) NOT NULL auto_increment,
	MEN_DESC varchar(150) NOT NULL ,
	MEN_NIVEL int(11) NOT NULL ,
	MEN_NIVEL0 int(11) NOT NULL ,
	MEN_NIVEL1 int(11) NOT NULL ,
	MEN_NIVEL2 int(11) NOT NULL ,
	MEN_NIVEL3 int(11) NOT NULL ,
	MEN_LINK varchar(150),
	TAG_INICIO varchar(50) NOT NULL ,
	TAG_FIM varchar(50) NOT NULL ,
	MEN_VISIVEL varchar(1) default 'S' NOT NULL ,
	PRIMARY KEY (MEN_CODIGO)
);




CREATE TABLE menu_new (
	MEN_CODIGO int(11) NOT NULL auto_increment,
	MEN_DESC varchar(150) NOT NULL ,
	MEN_NIVEL int(11) NOT NULL ,
	MEN_NIVEL0 int(11) NOT NULL ,
	MEN_NIVEL1 int(11) NOT NULL ,
	MEN_NIVEL2 int(11) NOT NULL ,
	MEN_NIVEL3 int(11) NOT NULL ,
	MEN_LINK varchar(150),
	TAG_INICIO varchar(50) NOT NULL ,
	TAG_FIM varchar(50) NOT NULL ,
	MEN_VISIVEL varchar(1) default 'S' NOT NULL ,
	PRIMARY KEY (MEN_CODIGO)
);




CREATE TABLE menu_usuario (
	EMP_DOMINIO varchar(80) NOT NULL ,
	USU_CODIGO int(11) NOT NULL ,
	MEN_CODIGO int(11) NOT NULL ,
	MEN_NIVEL int(11) NOT NULL ,
	FLAG varchar(1),
	MEN_NIVELBK int(11),
	MEN_STATUS varchar(1) default '0' NOT NULL ,
	USU_LOGIN varchar(30) NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,USU_CODIGO,MEN_CODIGO)
);

CREATE TABLE mk (
	MK_CODIGO int(11) NOT NULL auto_increment,
	MK_AVISO varchar(1) default 'N',
	EMP_DOMINIO varchar(50) NOT NULL ,
	MK_NOME varchar(80) NOT NULL ,
	MK_IP varchar(50) NOT NULL ,
	MK_SSH varchar(30),
	MK_PORTA_GRAFICO varchar(20),
	MK_VERSAO varchar(10),
	MK_NRVERSAO int(11) NOT NULL ,
	MK_BLOQUEIO int(11) default '2' NOT NULL ,
	MK_NOME_HOTSPOT varchar(80),
	MK_HOTSPOT varchar(10),
	MK_PPPOE varchar(10),
	MK_NR_VERSAO int(11),
	MK_QUEUE varchar(10),
	MK_USER_API varchar(80),
	MK_SENHA_API varchar(80),
	MK_PORTA_API varchar(10),
	IPMAC varchar(15),
	IPMAC_LIST varchar(15),
	IPMAC_BURST varchar(15),
	PPPOE varchar(15),
	IPV6 int(11) NOT NULL ,
	PROFILE varchar(80) NOT NULL ,
	HOTSPOT varchar(15),
	MK_DIRETORIO_GRAFICO varchar(50),
	PRIMARY KEY (MK_CODIGO,EMP_DOMINIO)
);

CREATE TABLE motivo (
	MOT_CODIGO int(11) NOT NULL auto_increment,
	MOT_DESCRICAO varchar(80) NOT NULL ,
	PRIMARY KEY (MOT_CODIGO)
);




CREATE TABLE movimento_material (
	MOV_CODIGO int(11) NOT NULL auto_increment,
	MAT_CODIGO int(11) default '0' NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	MOV_DATA date default '0000-00-00' NOT NULL ,
	MOV_DESC varchar(80),
	MOV_ENTRADA decimal(10,2) default '0.00' NOT NULL ,
	MOV_SAIDA decimal(10,2) default '0.00' NOT NULL ,
	MOV_ESTOQUE decimal(10,2) default '0.00' NOT NULL ,
	MOV_ESTOQUE_ANT decimal(10,2) default '0.00' NOT NULL ,
	USU_LOGIN varchar(25),
	CLI_LOGIN varchar(50),
	PRIMARY KEY (MOV_CODIGO,EMP_DOMINIO)
);

CREATE TABLE noticias (
	codigo int(11) NOT NULL auto_increment,
	datahora datetime default '0000-00-00 00:00:00' NOT NULL ,
	titulo varchar(100) NOT NULL ,
	foto varchar(50),
	noticia text NOT NULL ,
	Destaque char(1),
	PRIMARY KEY (codigo)
);




CREATE TABLE obs_nota (
	EMP_DOMINIO varchar(120) NOT NULL ,
	CLI_LOGIN varchar(80) NOT NULL ,
	OBS text,
	CLI_NOME varchar(120) NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,CLI_LOGIN,CLI_NOME)
);




CREATE TABLE parceiros (
	EMP_DOMINIO varchar(80) NOT NULL ,
	PAR_CODIGO int(11) NOT NULL auto_increment,
	PAR_NOME varchar(80) NOT NULL ,
	PAR_VALOR decimal(10,2) NOT NULL ,
	PAR_TIPO varchar(1) NOT NULL ,
	PAR_VALIDADE date,
	EMP_DOMINIO_FILIAL varchar(80) NOT NULL ,
	PRIMARY KEY (PAR_CODIGO)
);




CREATE TABLE pedido (
	PED_CODIGO int(11) NOT NULL ,
	FOR_CODIGO int(11) NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	MAT_CODIGO int(11) NOT NULL ,
	USU_CODIGO varchar(80) NOT NULL ,
	PED_QTDADE decimal(10,2) NOT NULL ,
	PED_STATUS int(11) NOT NULL ,
	PED_DATA date NOT NULL ,
	PED_HORA time NOT NULL ,
	FLAG1 varchar(1) NOT NULL ,
	FLAG2 varchar(1) NOT NULL ,
	FLAG3 varchar(1) NOT NULL ,
	PRIMARY KEY (PED_CODIGO,FOR_CODIGO,EMP_DOMINIO,MAT_CODIGO)
);




CREATE TABLE posvenda (
	POS_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	MOT_CODIGO int(11) NOT NULL ,
	CLI_LOGIN varchar(80) NOT NULL ,
	POS_TIPO int(11) NOT NULL ,
	POS_DATA datetime NOT NULL ,
	POS_DESCRICAO text NOT NULL ,
	PRIMARY KEY (POS_CODIGO,EMP_DOMINIO,CLI_LOGIN)
);




CREATE TABLE predatado (
	PRE_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	PRE_DATA date default '0000-00-00' NOT NULL ,
	PRE_FAVORECIDO varchar(100),
	PRE_REFERENTE varchar(100),
	CON_CODIGO int(11) default '0' NOT NULL ,
	PRE_CHEQUE varchar(10) NOT NULL ,
	PRE_VALOR decimal(10,2) default '0.00' NOT NULL ,
	USU_LOGIN varchar(25),
	PRE_BAIXA date,
	PRIMARY KEY (PRE_CODIGO)
);




CREATE TABLE produtos (
	EMP_DOMINIO varchar(40) NOT NULL ,
	PRO_CODIGO int(11) NOT NULL auto_increment,
	PRO_DESCRICAO varchar(80),
	PRO_UNIDADE varchar(10),
	PRO_CUSTO decimal(10,2),
	PRO_VENDA decimal(10,2),
	PRO_ESTOQUE decimal(5,2),
	PEO_ESTMIN decimal(5,2) default '0.00' NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,PRO_CODIGO),
   KEY IDX_produto1 (PRO_CODIGO,EMP_DOMINIO)
);




CREATE TABLE profile (
	EMP_DOMINIO varchar(80) NOT NULL ,
	PRO_PROFILE varchar(80) NOT NULL ,
	COM_TIPO varchar(20) NOT NULL ,
	MK_IP varchar(80) NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,PRO_PROFILE,COM_TIPO,MK_IP)
);


CREATE TABLE questoes (
	QUE_TIPO int(11) default '0' NOT NULL ,
	QUE_CODIGO int(11) default '0' NOT NULL ,
	QUE_DESCRICAO text,
	PRIMARY KEY (QUE_TIPO,QUE_CODIGO),
   KEY IDX_questoes1 (QUE_TIPO,QUE_CODIGO)
);




CREATE TABLE queue_type (
	MK_IP varchar(20) NOT NULL ,
	QTY_NAME varchar(30) NOT NULL ,
	QTY_KIND varchar(15) NOT NULL ,
	QTY_RATE varchar(15) NOT NULL ,
	QTY_LIMIT varchar(15) NOT NULL ,
	QTY_TOTAL_LIMIT varchar(15) NOT NULL ,
	QTY_BURST_RETE varchar(15) NOT NULL ,
	QTY_BURST_THRESHOLD varchar(15) NOT NULL ,
	QTY_BURST_TIME varchar(15) NOT NULL ,
	QTY_CLASSIFIER varchar(15) NOT NULL ,
	QTY_DST_ADDRESS_MASK varchar(15) NOT NULL ,
	QTY_SRC_ADDRESS6_MASK varchar(15) NOT NULL ,
	QTY_DST_ADDRESS6_MASK varchar(15) NOT NULL ,
	EMP_DOMINIO varchar(80) NOT NULL ,
	QTY_SRC_ADDRESS_MASK varchar(15) NOT NULL ,
	PRIMARY KEY (MK_IP,QTY_NAME,EMP_DOMINIO)
);




CREATE TABLE quota (
	EMP_DOMINIO varchar(80) NOT NULL ,
	CLI_LOGIN varchar(25) NOT NULL ,
	QUO_ANO int(11) default '0' NOT NULL ,
	QUO_MES int(11) default '0' NOT NULL ,
	QUO_VALOR varchar(20),
	PRIMARY KEY (EMP_DOMINIO,CLI_LOGIN,QUO_ANO,QUO_MES)
);




CREATE TABLE rede (
	IPS_NUMERO varchar(15) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	CLI_LOGIN varchar(50) NOT NULL ,
	MK_IP varchar(50) default '0',
	IPS_NUMERO_ANT varchar(50) NOT NULL ,
	IP_BK varchar(20) NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,CLI_LOGIN),
   KEY IPS_NUMERO (IPS_NUMERO)
);


CREATE TABLE respostas (
	AVA_CODIGO int(11) default '0' NOT NULL ,
	CLI_LOGIN varchar(25) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	QUE_TIPO int(11) default '0' NOT NULL ,
	QUE_CODIGO int(11) default '0' NOT NULL ,
	RES_DESCRICAO text,
	PRIMARY KEY (AVA_CODIGO,CLI_LOGIN,EMP_DOMINIO,QUE_TIPO,QUE_CODIGO),
   KEY IDX_respostas1 (AVA_CODIGO,CLI_LOGIN,EMP_DOMINIO,QUE_TIPO,QUE_CODIGO)
);




CREATE TABLE retonto (
	dominio varchar(120) NOT NULL ,
	bid int(11) NOT NULL ,
	dt_venc date,
	dt_pgto date,
	val_titulo decimal(10,0),
	val_pago decimal(10,0),
	tarifa decimal(10,0),
	ocorrenci varchar(255),
	motivo varchar(255),
	obs varchar(255),
	falg varchar(1),
	PRIMARY KEY (dominio,bid)
);




CREATE TABLE rn_cliente (
	id_cliente int(11) NOT NULL auto_increment,
	id_parceiro int(10) unsigned default '0',
	tipo_cliente varchar(2) NOT NULL ,
	tipo_empresa int(11) NOT NULL ,
	nome varchar(200),
	cpf varchar(13),
	rg varchar(13),
	razao_social varchar(200),
	nome_fantasia varchar(200),
	cnpj varchar(20),
	insc_estadual varchar(20),
	insc_municipal varchar(20),
	email varchar(500),
	telefone varchar(15),
	data_nascimento date,
	observacao text,
	data_cadastro date,
	status varchar(3) NOT NULL ,
	usuario_radius varchar(1) NOT NULL ,
	acompanhar int(10) unsigned NOT NULL ,
	nivel_sinal_os int(10) unsigned default '0' NOT NULL ,
	data_troca_status datetime NOT NULL ,
	senha_central varchar(250),
	DELETED int(11) default '0' NOT NULL ,
	PRIMARY KEY (id_cliente),
   KEY Index_cli (nome,DELETED)
);




CREATE TABLE sacado (
	CODIGO int(11) NOT NULL auto_increment,
	NOME varchar(120) NOT NULL ,
	PRIMARY KEY (CODIGO)
);




CREATE TABLE setor (
	SET_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	SET_DESCRICAO varchar(80) NOT NULL ,
	SET_RESPONSAVEL varchar(80) NOT NULL ,
	PRIMARY KEY (SET_CODIGO)
);

INSERT INTO setor VALUES('134' , '@infocomp.net.br' , '' , '');



CREATE TABLE sms (
	SMS_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	CLI_LOGIN varchar(50) NOT NULL ,
	CLI_CELULAR varchar(20) NOT NULL ,
	CLI_NOME varchar(100),
	SMS_MENSAGEM text NOT NULL ,
	SMS_DATA date NOT NULL ,
	SMS_HORA time NOT NULL ,
	USU_LOGIN varchar(50) NOT NULL ,
	SMS_STATUS int(11) NOT NULL ,
	SMS_ANOMES varchar(7) NOT NULL ,
	PRIMARY KEY (SMS_CODIGO)
);

CREATE TABLE sms_gateway (
	SMS_GW_CODIGO int(10) unsigned NOT NULL auto_increment,
	SMS_GW_EMPRESA varchar(50) NOT NULL ,
	SMS_GW_URL varchar(250) NOT NULL ,
	SMS_GW_URL_SALDO varchar(250) NOT NULL ,
	SMS_GW_STATUS tinyint(1) default '1' NOT NULL ,
	PRIMARY KEY (SMS_GW_CODIGO)
);




CREATE TABLE solucao (
	SOL_CODIGO int(11) NOT NULL auto_increment,
	SUP_CODIGO int(11) default '0' NOT NULL ,
	SOL_DESCRICAO text,
	SOL_DATA date,
	SOL_HORA time default '00:00:00',
	CLI_LOGIN varchar(50),
	EMP_DOMINIO varchar(50) NOT NULL ,
	USU_CODIGO int(11) default '0',
	SOL_STATUS varchar(1) default '0' NOT NULL ,
	PRIMARY KEY (SOL_CODIGO,SUP_CODIGO,EMP_DOMINIO),
   KEY CLI_LOGIN (CLI_LOGIN)
);

CREATE TABLE ssid (
	EMP_DOMINIO varchar(80) NOT NULL ,
	SSID_NUMERO varchar(80) NOT NULL ,
	PRIMARY KEY (EMP_DOMINIO,SSID_NUMERO)
);




CREATE TABLE status (
	STA_CODIGO int(11) NOT NULL auto_increment,
	STA_DESCRICAO char(50),
	PRIMARY KEY (STA_CODIGO)
);




CREATE TABLE suporte (
	SUP_CODIGO int(11) NOT NULL auto_increment,
	USU_CODIGO int(11) default '0' NOT NULL ,
	CLI_LOGIN varchar(50) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	SUP_DATA date,
	SUP_HORA time default '00:00:00',
	SUP_DESCRICAO text,
	SUP_HPREVISAO time,
	SUP_DTPREVISAO date,
	SUP_PRIORIDADE int(11) default '1' NOT NULL ,
	SUP_TIPO int(11) default '1' NOT NULL ,
	USU_LOGIN varchar(25),
	SUP_AVALIACAO char(1) default 'N',
	SUP_TECNICO varchar(60) default '  ' NOT NULL ,
	SUP_STATUS varchar(1) default '0' NOT NULL ,
	SUP_PONTOS int(11) default '0' NOT NULL ,
	PRIMARY KEY (SUP_CODIGO,EMP_DOMINIO),
   KEY EMP_DOMINIO (EMP_DOMINIO),
   KEY CLI_LOGIN (CLI_LOGIN)
);


CREATE TABLE tecnologia (
	TEC_ID int(11) NOT NULL auto_increment,
	TEC_DICI varchar(50) NOT NULL ,
	TEC_NOME varchar(50) NOT NULL ,
	PRIMARY KEY (TEC_ID)
);




CREATE TABLE tipo (
	TIPO int(11) NOT NULL auto_increment,
	TIP_DESCRICAO varchar(80) NOT NULL ,
	PRIMARY KEY (TIPO)
);




CREATE TABLE torres (
	TOR_CODIGO int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) default '@turbonetitajobi.com.br' NOT NULL ,
	TOR_DESCRICAO varchar(80) NOT NULL ,
	TOR_IP varchar(20),
	TOR_ATIVA varchar(1) default 'N' NOT NULL ,
	TOR_COMMUNITY varchar(50),
	TOR_PORTA_GRAFICO varchar(20),
	TOR_OBS varchar(120) NOT NULL ,
	TOR_ENDERECO varchar(150) NOT NULL ,
	TOR_CIDADE varchar(50) NOT NULL ,
	TOR_ESTADO varchar(2) NOT NULL ,
	TOR_BAIRRO varchar(50) NOT NULL ,
	TOR_LAT float(10,6) NOT NULL ,
	TOR_LONG float(10,6) NOT NULL ,
	PRIMARY KEY (TOR_CODIGO)
);


CREATE TABLE transacao (
	tra_codigo int(11) NOT NULL auto_increment,
	tra_status char(1) NOT NULL ,
	EMP_DOMINIO varchar(80),
	USU_LOGIN varchar(25),
	PRIMARY KEY (tra_codigo)
);




CREATE TABLE usuario_filial (
	id int(11) NOT NULL auto_increment,
	EMP_DOMINIO varchar(80) NOT NULL ,
	USU_LOGIN varchar(50) NOT NULL ,
	FILIAL varchar(80) NOT NULL ,
	PRIMARY KEY (id)
);




CREATE TABLE usuarios (
	EMP_DOMINIO varchar(80) default '0' NOT NULL ,
	USU_CODIGO int(11) NOT NULL auto_increment,
	USU_LOGIN varchar(15) NOT NULL ,
	USU_NOME varchar(80) NOT NULL ,
	USU_SENHA varchar(80),
	USU_NIVEL int(11) default '0',
	USU_HORARIO_INICIO time NOT NULL ,
	USU_HORARIO_FIM time NOT NULL ,
	PAR_CODIGO int(11) NOT NULL ,
	EMP_DOMINIO_FILIAL varchar(80) NOT NULL ,
	USU_TECNICO varchar(1) NOT NULL ,
	USU_STATUS varchar(1) NOT NULL ,
	USU_MULTI_FILIAL varchar(1) NOT NULL ,
	PRIMARY KEY (USU_CODIGO)
);


CREATE TABLE usuarios_online (
	id int(11) NOT NULL auto_increment,
	sessao text NOT NULL ,
	tempo timestamp NOT NULL,
	ip varchar(15) NOT NULL ,
	quem varchar(80) NOT NULL ,
	onde varchar(80) NOT NULL ,
	PRIMARY KEY (id)
);




CREATE TABLE vinculados (
	CLI_LOGIN varchar(80) NOT NULL ,
	EMP_DOMINIO varchar(50) NOT NULL ,
	VIN_LOGIN varchar(80) NOT NULL ,
	VIN_SENHA varchar(80),
	VIN_NOME varchar(80),
	VIN_MAC varchar(20),
	BAN_CODIGO varchar(20),
	VIN_BANDA varchar(50) default ' ' NOT NULL ,
	VIN_WIRELESS varchar(10) NOT NULL ,
	VIN_DHCP varchar(1) NOT NULL ,
	VIN_BLOQUEADO date,
	VIN_ENDERECO varchar(120) NOT NULL ,
	VIN_CIDADE varchar(80) NOT NULL ,
	VIN_BAIRRO varchar(80) NOT NULL ,
	VIN_OBS text NOT NULL ,
	PRIMARY KEY (CLI_LOGIN,VIN_LOGIN,EMP_DOMINIO)
);