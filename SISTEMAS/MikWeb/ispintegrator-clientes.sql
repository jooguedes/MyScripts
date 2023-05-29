```sql
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
    lr.senha
    (SELECT )
    from clientes c
    inner join servicos_cli sc on (sc.codcli=c.codcli)
	INNER JOIN login_radius lr on (lr.codsercli=sc.codsercli) 
	
	WHERE lr.login is not null;
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
    lr.senha
    from clientes c
    inner join servicos_cli sc on (sc.codcli=c.codcli)
	LEFT JOIN  login_radius lr on (lr.codsercli=sc.codsercli) WHERE lr.login is null;


##para analise
SELECT count(r.login)  FROM  ispintegrator.login_radius r inner join ispintegrator.servicos_cli s on(r.codsercli=s.codsercli);

SELECT  login from ispintegrator.clientes c ;
```