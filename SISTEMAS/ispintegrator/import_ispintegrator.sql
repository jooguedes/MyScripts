
--PORTADORES
SELECT DISTINCT 
	fc.codcob       ,
	fc.descri_cob   ,
	fc.nro_arq      ,
	fc.nosso_nro    ,
	fc.pix          ,
	b.nome_ban      ,
	b.razao_social  ,
	b.nro_agencia   ,
	b.nro_conta     ,
	b.nro_banco     ,
	b.obs 
FROM forma_cobrancas fc 
LEFT JOIN bancos b ON (fc.codban = b.codban)
INTO OUTFILE '/tmp/ispintegrator-portadores.csv' FIELDS 
TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



-- CLIENTES COM LOGIN
SELECT DISTINCT 
    c.codcli                            ,
    c.codgcli                           ,
    c.nome_cli                          ,
    c.nome_fan                          ,
    c.rg                                ,
    c.cpf                               ,
    c.cnpj                              ,
    c.ativo  as  status                 ,
    -- endereco cadastro
    c.endereco                          ,
    c.referencia                        ,
    c.apto                              ,
    c.sala                              ,
    c.bairro                            ,
    c.cidade                            ,
    c.cep                               ,
    CONCAT(c.ddd, c.fone)               ,
    c.fax                               ,
    c.celular                           ,
    c.e_mail                            ,
    c.contato                           ,
    c.aniversario                       ,
    c.data_nac                          ,
    c.tipo_cliente                      ,
    -- endereco cobranca
    c.endereco_cob                      ,
    c.bairro_cob                        ,
    c.cidade_cob                        ,
    c.cep_cob                           ,
    CONCAT(c.longitude, ',', c.latitude) ,
    c.data_cad                          ,
    c.nunca_suspender                   ,
    c.obs                               ,
    lr.login                            ,
    lr.senha                            ,
    (SELECT s.descri_ser from servicos s where s.codser=sc.codser),
    (SELECT s.formula from servicos s where s.codser=sc.codser),
    (SELECT siv.upload from servicos_ivr siv where siv.codser=sc.codser),
    (SELECT siv.download from servicos_ivr siv where siv.codser=sc.codser),
    sc.data_can as data_cancelamento_servico,
    sc.codsercli as id_contrato,
    sc.codcob as PORTADOR
    from clientes c
    inner join servicos_cli sc on (sc.codcli=c.codcli)
	INNER JOIN login_radius lr on (lr.codsercli=sc.codsercli)
	WHERE lr.login is not null ORDER BY  sc.data_con DESC;
	INTO OUTFILE '/tmp/ispintegrator-clientes.csv' FIELDS 
	TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-- CLIENTES SEM LOGIN
SELECT DISTINCT 
    c.codcli                            ,
    c.codgcli                           ,
    c.nome_cli                          ,
    c.nome_fan                          ,
    c.rg                                ,
    c.cpf                               ,
    c.cnpj                              ,
    c.ativo                             ,
    -- endereco cadastro
    c.endereco                          ,
    c.referencia                        ,
    c.apto                              ,
    c.sala                              ,
    c.bairro                            ,
    c.cidade                            ,
    c.cep                               ,
    CONCAT(c.ddd, c.fone)               ,
    c.fax                               ,
    c.celular                           ,
    c.e_mail                            ,
    c.contato                           ,
    c.aniversario                       ,
    c.data_nac                          ,
    c.tipo_cliente                      ,
    -- endereco cobranca
    c.endereco_cob                      ,
    c.bairro_cob                        ,
    c.cidade_cob                        ,
    c.cep_cob                           ,
    CONCAT(c.longitude, ',', c.latitude) ,
    c.data_cad                          ,
    c.nunca_suspender                   ,
    c.obs                               ,
    lr.login                            ,
    lr.senha                            ,
    (SELECT s.descri_ser from servicos s where s.codser=sc.codser),
    (SELECT s.formula from servicos s where s.codser=sc.codser),
    (SELECT siv.upload from servicos_ivr siv where siv.codser=sc.codser),
    (SELECT siv.download from servicos_ivr siv where siv.codser=sc.codser),
    sc.data_can as data_cancelamento_servico,
    sc.codsercli as id_contrato,
    sc.codcob as PORTADOR
    from clientes c
    inner join servicos_cli sc on (sc.codcli=c.codcli)
	LEFT JOIN  login_radius lr on (lr.codsercli=sc.codsercli) WHERE lr.login is null ORDER BY  sc.data_con DESC;



---OBS CLIENTES 
SELECT DISTINCT 
	o.codobs          ,
	o.codcli          ,
	o.codtobs         ,
	o.codusu          ,
	o.data_hora       ,
	o.mostra_ao_abrir ,
	o.obs 
FROM observacoes o 
INTO OUTFILE '/tmp/ispintegrator-observacoes-clientes.csv' FIELDS 
TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



----HISTORICO CLIENTES
SELECT DISTINCT 
	hc.codcli as id_cliente    ,
	hc.tabela                  ,
	hc.`data`                  ,
	hc.usuario                 ,
	hc.ip                      ,
	hc.texto 
FROM historico_cliente hc 
INTO OUTFILE '/tmp/ispintegrator-historicos-clientes.csv' FIELDS 
TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


-----TITULOS
SELECT DISTINCT 
	f.codfat             ,
	f.codcli    as codigo cliente        ,
	f.codcob    as PORTADOR         ,
	f.codnf              ,
	f.n_boleto           ,
	f.nro_doc            ,
	f.status             ,
	f.data_lan           ,
	f.data_ven           ,
	f.data_bai           ,
	f.valor_lan          ,
	f.histo_fat          ,
	fp.status_pix        ,
	fp.location          ,
	fp.data_criacao      ,
	fp.data_expiracao    ,
	fp.data_pg_banco     ,
	fp.tix               ,
	fp.textoImagemQRcode ,
	fp.valor_pix         ,
	fp.juros_pix         ,
	fp.desconto_pix 
FROM faturas f  
LEFT JOIN faturas_pix fp ON (fp.codfat = f.codfat)
INTO OUTFILE '/tmp/ispintegrator-titulos.csv' FIELDS 
TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
































##para analise
SELECT count(r.login)  FROM  ispintegrator.login_radius r inner join ispintegrator.servicos_cli s on(r.codsercli=s.codsercli);

SELECT  login from ispintegrator.clientes c ;





