SET @SERVICOID=100;
SET @PREFIXO='@CONADMIN';
SET @PORTADORID=10;
SET @CLIENTCONTRATOID=200;
SET @OCORRENCIAID=200;





select s.IdServico+ @SERVICOID,
       CONCAT(@PREFIXO,s.DescricaoServico),
       sv.valor,
       '1024k/2048k' as velocidade,
       s.DiasLimiteBloqueio,
       s.DiasAvisoAposVencimentoEmail
FROM Servico s
INNER JOIN ServicoValor sv ON (sv.idservico=s.idservico)
LEFT JOIN ServicoParametro sp ON (sp.idservico=s.idservico and sp.Descricaoparametroservico='Grupo de Acesso')
INTO OUTFILE '/tmp/conadmin-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select lc.IdLocalCobranca + @PORTADORID, 
CONCAT(@PREFIXO, lc.DescricaoLocalCobranca),
lcp1.ValorLocalCobrancaParametro as agencia,
lcp2.ValorLocalCobrancaParametro as conta,
lcp3.ValorLocalCobrancaParametro as contadv,
lcp4.ValorLocalCobrancaParametro as carteira,
lcp5.ValorLocalCobrancaParametro as inicionossonumero, 
lcp6.ValorLocalCobrancaParametro as localpagamento,
lcp7.ValorLocalCobrancaParametro as Instrucoes1,
lcp8.ValorLocalCobrancaParametro as Instrucoes2,
lcp9.ValorLocalCobrancaParametro as Instrucoes3,
lcp10.ValorLocalCobrancaParametro as Instrucoes4,
lcp11.ValorLocalCobrancaParametro as Instrucoes5,
lcg.PercentualMulta as multa,
(lcg.PercentualJurosDiarios * 30) as juros

from LocalCobranca lc
INNER JOIN Loja l on (l.IdLoja=lc.IdLoja)
INNER JOIN LocalCobrancaGeracao lcg ON (lcg.IdLocalCobranca=lc.IdLocalCobranca)
#LEFT JOIN LocalCobrancaParametro lcp1 on (lcp1.IdLocalCobranca=lc.IdLocalCobranca and lcp1.IdLocalCobrancaParametro='Agencia')
#LEFT JOIN LocalCobrancaParametro lcp2 on (lcp2.IdLocalCobranca=lc.IdLocalCobranca and lcp2.IdLocalCobrancaParametro='Conta')
#LEFT JOIN LocalCobrancaParametro lcp3 on (lcp3.IdLocalCobranca=lc.IdLocalCobranca and lcp3.IdLocalCobrancaParametro='ContaDigito')
#LEFT JOIN LocalCobrancaParametro lcp4 on (lcp4.IdLocalCobranca=lc.IdLocalCobranca and lcp4.IdLocalCobrancaParametro='Carteira')
#LEFT JOIN LocalCobrancaParametro lcp5 on (lcp5.IdLocalCobranca=lc.IdLocalCobranca and lcp5.IdLocalCobrancaParametro='InicioNossoNumero')
#LEFT JOIN LocalCobrancaParametro lcp6 on (lcp6.IdLocalCobranca=lc.IdLocalCobranca and lcp6.IdLocalCobrancaParametro='LocalPagamento')
#LEFT JOIN LocalCobrancaParametro lcp7 on (lcp7.IdLocalCobranca=lc.IdLocalCobranca and lcp7.IdLocalCobrancaParametro='Instrucoes1')
#LEFT JOIN LocalCobrancaParametro lcp8 on (lcp8.IdLocalCobranca=lc.IdLocalCobranca and lcp8.IdLocalCobrancaParametro='Instrucoes2')
#LEFT JOIN LocalCobrancaParametro lcp9 on (lcp9.IdLocalCobranca=lc.IdLocalCobranca and lcp9.IdLocalCobrancaParametro='Instrucoes3')
#LEFT JOIN LocalCobrancaParametro lcp10 on (lcp10.IdLocalCobranca=lc.IdLocalCobranca and lcp10.IdLocalCobrancaParametro='Instrucoes4')
#LEFT JOIN LocalCobrancaParametro lcp11 on (lcp11.IdLocalCobranca=lc.IdLocalCobranca and lcp11.IdLocalCobrancaParametro='Instrucoes5')
INTO OUTFILE '/tmp/conadmin-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

#PORTADORES SEM DADOS
select lc.IdLocalCobranca + @PORTADORID, 
CONCAT(@PREFIXO ,lc.DescricaoLocalCobranca),
'0' as  agencia,
'0' as conta,
'0' as contadv,
'0' as carteira,
'0' as inicionossonumero, 
'0' as localpagamento,
'0' as Instrucoes1,
'0' as Instrucoes2,
'0' as Instrucoes3,
'0 ' as Instrucoes4,
'0' as Instrucoes5,
'0' as multa,
'0' as juros
from LocalCobranca lc
INTO OUTFILE '/tmp/conadmin-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select 
p.IdPessoa + @CLIENTCONTRATOID,
c.IdContrato + @CLIENTCONTRATOID,
p.Nome                      ,  
p.RazaoSocial               ,
p.NomeRepresentante         ,  
p.TipoPessoa                ,    
p.DataNascimento            ,  
p.Sexo                      ,  
p.RG_IE                     ,  
p.OrgaoExpedidor            ,  
p.CPF_CNPJ                  ,  
p.EstadoCivil               ,  
p.InscricaoMunicipal        ,  
p.Cob_FormaCorreio          ,  
p.Cob_FormaEmail            ,  
p.NomePai                   ,  
p.NomeMae                   ,

p.Senha as senhacentral     ,
p.LoginCriacao as cadastradopor,
pei.Endereco as endereco_inst,
pei.Numero   as numero_inst,
pei.complemento as complemento_inst,
pei.CEP as cep_inst,
pei.bairro  as bairro_inst,
pei.latitude as lat_inst,
pei.longitude as lon_inst,
(select ci.nomecidade from Cidade ci where ci.idcidade=pei.idcidade and ci.idestado=pei.idestado limit 1) as cidade_inst,
(select ei.siglaestado from Estado ei where ei.idestado=pei.idestado limit 1) as uf_inst,

pec.Endereco as endereco_cob,
pec.Numero   as numero_cob,
pec.complemento as complemento_cob,
pec.CEP as cep_cob,
pec.bairro  as bairro_cob,
pec.latitude as lat_cob,
pec.longitude as lon_cob,
(select cc.nomecidade from Cidade cc where cc.idcidade=pec.idcidade and cc.idestado=pec.idestado limit 1) as cidade_cob,
(select ec.siglaestado from Estado ec where ec.idestado=pec.idestado limit 1) as uf_cob,

c.DiaCobranca,
c.IdLocalCobranca  + @PORTADORID as idportador,
c.DataInicio as data_cadastro,

c.idstatus as status,
CONCAT(@PREFIXO ,(select login.valor from ContratoParametro login where login.idcontrato=c.idcontrato and login.IdParametroServico=1 limit 1)) as login,
(select senha.valor from ContratoParametro senha where senha.idcontrato=c.idcontrato and senha.IdParametroServico=2 limit 1) as senha,
(select mac.valor from ContratoParametro mac where mac.idcontrato=c.idcontrato and mac.IdParametroServico=4 limit 1) as mac,
(select ip.valor from ContratoParametro ip where ip.idcontrato=c.idcontrato and ip.IdParametroServico=5 limit 1) as ip,
(select modoaq.valor from ContratoParametro modoaq where modoaq.idcontrato=c.idcontrato and modoaq.IdParametroServico=7 limit 1) as modoaquisicao,
(select tipo_equip.valor from ContratoParametro tipo_equip where tipo_equip.idcontrato=c.idcontrato and tipo_equip.IdParametroServico=8 limit 1) as tipo_equipamento,
s.idservico + @SERVICOID as planoid,
REPLACE(p.Obs, '"', '') as obs,
REPLACE(c.obs,'"','') as contrato_obs

FROM Pessoa p
INNER JOIN Contrato c on (c.idpessoa=p.idpessoa)
INNER JOIN PessoaEndereco pei on (pei.idpessoa=p.idpessoa and pei.IdPessoaEndereco=c.idpessoaendereco)
INNER JOIN PessoaEndereco pec on (pec.idpessoa=p.idpessoa and pec.IdPessoaEndereco=c.idpessoaenderecoCobranca)
INNER JOIN Servico s on (s.idservico=c.idservico)
ORDER BY c.idcontrato desc
INTO OUTFILE '/tmp/conadmin-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select 
c.idstatus as status,
CONCAT(@PREFIXO, (select login.valor from ContratoParametro login where login.idcontrato=c.idcontrato and login.IdParametroServico=1 limit 1)) as login
FROM Pessoa p
INNER JOIN Contrato c on (c.idpessoa=p.idpessoa)
INNER JOIN PessoaEndereco pei on (pei.idpessoa=p.idpessoa and pei.IdPessoaEndereco=c.idpessoaendereco)
INNER JOIN PessoaEndereco pec on (pec.idpessoa=p.idpessoa and pec.IdPessoaEndereco=c.idpessoaenderecoCobranca)
INNER JOIN Servico s on (s.idservico=c.idservico)
INTO OUTFILE '/tmp/conadmin-login-status.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

MariaDB [cnt]> select distinct idstatus,count(IdContrato)from Contrato group by idstatus
    -> ;
+----------+-------------------+
| idstatus | count(IdContrato) |
+----------+-------------------+
|        1 |               686 |
|      101 |               139 |
|      102 |               470 |
|      200 |              1242 |
|      201 |                42 |
|      202 |                 9 |
|      203 |               144 |
|      204 |                 1 |
|      301 |                 2 |
|      303 |                58 |
|      305 |                 3 |
|      307 |                 2 |
+----------+-------------------+

select IdContrato + @CLIENTCONTRATOID,idstatus from Contrato
INTO OUTFILE '/tmp/conadmin-contrato-status.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select p.idPessoa + @CLIENTCONTRATOID,t.telefone,p.CPF_CNPJ,p.nome from PessoaTelefone t inner join Pessoa p on (p.idPessoa=t.IdPessoa) order by p.idpessoa INTO OUTFILE '/tmp/conadmin-telefones.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select p.idPessoa + @CLIENTCONTRATOID,e.email,p.CPF_CNPJ,p.nome from PessoaEmail e inner join Pessoa p on (p.idPessoa=e.IdPessoa) order by p.idpessoa INTO OUTFILE '/tmp/conadmin-emails.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

SELECT 
os.IdOrdemServico + @OCORRENCIAID,
os.IdServico,
os.IdPessoa + @CLIENTCONTRATOID,
os.DataCriacao as dataabertura,
os.DataConclusao as concluido,
os.IdTipoOrdemServico,
tos.DescricaoTipoOrdemServico,
os.NotaAtendimento,
os.DescricaoOS,
os.DescricaoOutros,
os.Obs
FROM OrdemServico os
INNER JOIN TipoOrdemServico tos on(tos.IdTipoOrdemServico = os.IdTipoOrdemServico)
INTO OUTFILE '/tmp/conadmin-ocorrencias.csv' CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


###TESTE DE INDEX PARA MELHHORIA DA BUSCA###
CREATE INDEX idx_IdLacamentoFinanceiro ON LancamentoFinanceiroContaReceber(IdLacamentoFinanceiro);
CREATE INDEX idx_IdContaReceber ON ContaReceber(IdContaReceber);


select distinct 
	   cr.IdContaReceber ,
	   cr.IdPessoa + @CLIENTCONTRATOID,
	   lf.IdContrato + @CLIENTCONTRATOID,
	   cr.NossoNumero,
	   cr.NumeroDocumento,
	   cr.NumParcela,
	   cr.DataLancamento,
	   cr.DataVencimento,
	   lrr.DataRecebimento,
	   cr.DataCancelamento,	   
	   cr.ValorFinal,
	   lrr.ValorRecebido,
	   lrr.LoginCriacao,
	   lrr.Obs as obs_pag,
	   cr.IdLocalCobranca + @PORTADORID,

	   cr.IdArquivoRemessa

from LancamentoFinanceiroContaReceber lfc 
inner join ContaReceber cr on (lfc.IdContaReceber=cr.IdContaReceber)
inner join LancamentoFinanceiro lf on (lf.IdLancamentoFinanceiro=lfc.IdLancamentoFinanceiro)
inner join LocalCobranca lc on (lc.IdLocalCobranca=cr.IdLocalCobranca) 
left join ContaReceberRecebimento lrr on (lrr.IdContaReceber=cr.IdContaReceber)
#WHERE cr.IdLocalCobranca=5
INTO OUTFILE '/tmp/conadmin-titulos' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select distinct 
	   cr.IdContaReceber,
	   cr.IdPessoa,
	   lf.IdContrato,
	   cr.NossoNumero,
	   cr.NumeroDocumento,
	   cr.NumParcela,
	   cr.DataLancamento,
	   cr.DataVencimento,
	   lrr.DataRecebimento,
	   cr.DataCancelamento,	   
	   cr.ValorFinal,
	   lrr.ValorRecebido,
	   lrr.LoginCriacao,
	   lrr.Obs as obs_pag,
	   cr.IdLocalCobranca,
	   cr.IdArquivoRemessa

from LancamentoFinanceiroContaReceber lfc 
inner join ContaReceber cr on (lfc.IdContaReceber=cr.IdContaReceber)
inner join LancamentoFinanceiro lf on (lf.IdLancamentoFinanceiro=lfc.IdLancamentoFinanceiro)
inner join LocalCobranca lc on (lc.IdLocalCobranca=cr.IdLocalCobranca) 
left join ContaReceberRecebimento lrr on (lrr.IdContaReceber=cr.IdContaReceber)
WHERE cr.IdLocalCobranca=3 and cr.IdArquivoRemessa is not null
INTO OUTFILE '/tmp/conadmin-titulos-2-registrados.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


sed -i "s/\\\N//g" *.csv
for i in $(ls *.csv); do iconv -f iso8859-1 -t utf-8 $i > $i.utf8; rm $i; done 
for i in $(ls *.csv); do iconv -f iso8859-1 -t utf-8 $i > $i.utf8; done 


#AJUDA NO DEBUG

#VER OS GATEWAYS CADASTRADOS
select DescricaoLocalCobranca, IdLocalCobranca from LocalCobranca;
+------------------------------+-----------------+
| DescricaoLocalCobranca       | IdLocalCobranca |
+------------------------------+-----------------+
| Gerencianet Fortunus         |               1 |
| Gerencianet (NOVA API)       |               2 |
| Banco Santander com Registro |               3 |
| GerenciaNet ISP              |               4 |
| Banco Sicredi Registrado     |               5 |
+------------------------------+-----------------+
5 rows in set (0.003 sec)
