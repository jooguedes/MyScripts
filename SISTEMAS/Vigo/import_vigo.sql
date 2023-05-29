select c.id,
       IFNULL(l.username,'c'||c.id||'_semlogin') as login,
       c.tipo,
       c.nome,
       1,
       c.cpfcgc,
       10,
       15,
       c.rgie,
       '' as profissao,
       c.sexo,
       c.dt_nascimento,
       '' as fantasia, 
       '' as contato, 
       c.cob_endereco,
       '' as cob_numero,
       c.cob_referencia,
       c.cob_bairro,
       c.cob_cep,
       c.cob_uf,
       c.cob_cidade,
       c.telefone,
       c.cob_telefone,
       c.cob_celular,
       c.email,
       IFNULL(l.obs,'') as conn_obs,
       c.dt_cadastro as cadastro,
       c.dt_cadastro  as entrada,
       '' as servidor,
       concat(IFNULL(P.descricao,'PLANO_DESATIVADO'),' ',c.grupo) as plano,
       IFNULL(P.valor,'0') as valor_plano,
       'ppp' as tipoconexao,
       IFNULL(RLIP.value,'') as ip,
       '' as iphotspot,
       IFNULL(RCMAC.value,'') as mac,
       c.vencimento,
       c.vlr_desconto,
       '' as vacrescimo,
       '' as transmissor,
       '' as receptor,
       '' as reccomodato,
       '' as isento,
       c.situacao,
       IFNULL(l.value,'123') as senha,
       pai,
       mae,
       REPLACE(anotacoes, '"', '') as anotacoes,
       latitude,
       longitude,
       dt_situacao,
       c.grupo,
       IFNULL((select r2.value from mikrotik_5739.radcheck r2 where r2.attribute='ClearText-Password' and r2.username=l.username limit 1),'SEM SENHA TXT') as senha_text,
       cad_por as cadastrado_por,
       ug.groupname as velocidade

from cadastro_clientes c
     LEFT OUTER JOIN mikrotik_5739.radcheck l ON (l.id_cliente=c.id and l.attribute='MD5-Password')
     LEFT OUTER JOIN mikrotik_5739.usergroup ug ON (ug.username=l.username)
     LEFT OUTER JOIN mikrotik_5739.radcheck RCMAC ON (l.username=RCMAC.username and RCMAC.attribute='Calling-Station-Id')
     LEFT OUTER JOIN mikrotik_5739.radreply RLIP ON (l.username=RLIP.username and RLIP.attribute='Framed-IP-Address')
     LEFT OUTER JOIN financeiro_planos_clientes PC ON (PC.idcliente = c.id)
     LEFT OUTER JOIN financeiro_planos P ON (P.id = PC.id)
where c.situacao in ('L','B','X') 
INTO OUTFILE '/tmp/vigo-clientes.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select username,groupname from mikrotik_5739.usergroup 
INTO OUTFILE '/tmp/vigo-usergroup.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select c.id,
       c.nome,
       c.cpfcgc,
       c.telefone,
       c.cob_telefone,
       c.cob_celular
from cadastro_clientes c
where c.situacao in ('L','B','X')
INTO OUTFILE '/tmp/vigo-clientes-telefones.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id,nome,login,senha from sistema_operadores
INTO OUTFILE '/tmp/vigo-operadores.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from cadastro_fornecedores 
INTO OUTFILE '/tmp/vigo-fornecedores.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from financeiro_pcontas_classes
INTO OUTFILE '/tmp/vigo-pcontas.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from financeiro_documentos where tipo='PAGAR'
INTO OUTFILE '/tmp/vigo-documentos.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from financeiro_documentos where tipo='RECEBER'
INTO OUTFILE '/tmp/vigo-receber.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id_caixa,data,debito,credito,descricao from financeiro_fluxo 
where data >= '2016-09-23'
INTO OUTFILE '/tmp/vigo-fluxo-0923.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id_caixa,data,debito,credito,descricao from financeiro_fluxo 
INTO OUTFILE '/tmp/vigo-fluxo-all.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id_caixa,data,debito,credito,descricao from financeiro_fluxo 
where descricao not like 'Documento a PAGAR: %' 
and descricao not like 'Boleto: %RECEBIDO%RETORNO%' 
and descricao not like 'Boleto: %LIQUIDADO%DATA%' 
and descricao not like 'Boleto: %LIQUIDADO%com%' 
and descricao not like 'Boleto: %liquidado%com%' 
and descricao not like 'Boleto: %ESTORNADO%' 
and descricao not like 'Documento a RECEBER: %'
and descricao not like 'boleto %liquidado%manu%'
INTO OUTFILE '/tmp/vigo-fluxo.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select id_caixa,data,debito,credito,descricao from financeiro_fluxo 
where descricao not like 'Documento %' 
INTO OUTFILE '/tmp/vigo-fluxo-avulsos.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id_caixa,data,debito,credito,descricao from financeiro_fluxo 
where descricao not like 'Documento a PAGAR: %' 
and descricao not like 'Documento a RECEBER: %' order by data desc;


select * from financeiro_caixas
INTO OUTFILE '/tmp/vigo-caixas.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from sistema_auditoria_cliente
INTO OUTFILE '/tmp/vigo-auditoria-cliente.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select id,id_cliente, 
        id_funcionario,
        id_tatendimento,
        numero_os,
        dt_fechamento,h_fechamento,
        dt_agendamento,h_agendamento,
        dt_abertura,h_abertura,
        aberto_por,
        fechado_por,
        descricao,anotacao_tecnica,historico from cadastro_atendimentos INTO OUTFILE '/tmp/vigo-atendimentos.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select * from sistema_tipoatendimentos
INTO OUTFILE '/tmp/vigo-tipoatendimentos.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



select c.id,
       c.cpfcgc,
       c.telefone,
       c.cob_telefone,
       c.cob_celular,
       c.email
from cadastro_clientes c
INTO OUTFILE '/tmp/vigo-telefones.csv'
FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select distinct id_banco from financeiro_boletos;
+----------+
| id_banco |
+----------+
|        1 |
|        2 |
|        3 |
|        4 |
|        5 |
|        6 |
+----------+


select 1,
       b.id_cliente,
       c.cpfcgc,
       '',
       'boleto',
       b.referencia,
       b.emissao,
       b.vencimento,
       b.pago_data,
       b.seunumero,
       b.nossonumero,
       b.valor,
       b.pago_valor,
       b.valor,
       b.nf_numero,
       '',
       b.linhadigitavel,
       b.codigobarras,
       b.ativo,
       b.plano_conta,
       b.pago_tarifa,
       b.pago_local,
       b.pago_agencia

from financeiro_boletos b
inner join cadastro_clientes c ON (c.id=b.id_cliente)
where b.ativo='S' and id_banco=6 order by b.vencimento desc 
INTO OUTFILE '/tmp/vigo-titulos-6.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


###AJUDAR NO DEBUG#####
#select ativo,id_banco,nome from financeiro_boletos where id_banco = 1 and ativo='S';
#select distinct(id_banco) from financeiro_boletos;
#select id, nomebanco from financeiro_bancos;


SELECT DISTINCT
	b.id                ,
	b.nomebanco         ,
	b.agencia           ,
	b.conta             ,
	b.convenio          ,
	b.complemento       ,
	b.codigoescritural  ,
	b.codigotransmissao ,
	b.tipo              ,
	b.cedente           ,
	se.rsocial          ,
	se.fantasia         ,
	se.cnpj             ,
	b.clientid          ,
	b.clientsecret      ,
	b.chavepix 
FROM financeiro_bancos b 
LEFT JOIN sistema_empresas se ON (b.idempresa = se.id)
INTO OUTFILE '/tmp/vigo-portadores.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



select * from sistema_cidades_ibge INTO OUTFILE '/tmp/vigo-cidades_ibge.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';




documentos

                id: 32
          id_caixa: 1
        id_empresa: 1
     id_fornecedor: 8
   nome_fornecedor: NEILTON
  id_tipodocumento: 4
nome_tipodocumento: NOTA SIMPLES
     id_planoconta: 1.11.1106
   nome_planoconta: 
         historico: CH. 850117 - VIDRA?ARIA-NEILTON
           emissao: 2010-02-03
        vencimento: 2010-02-03
             valor: 450
              pago: 1
         pago_data: 2010-02-03
        pago_valor: 450
        pago_autor: adm
              tipo: PAGAR


+--------------------+--------------+------+-----+-----------+----------------+
| Field              | Type         | Null | Key | Default   | Extra          |
+--------------------+--------------+------+-----+-----------+----------------+
| id                 | int(11)      | NO   | PRI | NULL      | auto_increment |
| id_caixa           | int(10)      | NO   |     | 0         |                |
| id_empresa         | int(10)      | NO   |     | 0         |                |
| id_fornecedor      | int(10)      | NO   |     | 0         |                |
| nome_fornecedor    | varchar(250) | NO   |     |           |                |
| id_tipodocumento   | int(10)      | NO   |     | 0         |                |
| nome_tipodocumento | varchar(250) | NO   |     |           |                |
| id_planoconta      | varchar(250) | NO   |     | 0.00.0000 |                |
| nome_planoconta    | varchar(250) | NO   |     |           |                |
| historico          | varchar(250) | NO   |     |           |                |
| emissao            | date         | YES  |     | NULL      |                |
| vencimento         | date         | YES  |     | NULL      |                |
| valor              | double       | NO   |     | 0         |                |
| pago               | char(1)      | NO   |     | 0         |                |
| pago_data          | date         | YES  |     | NULL      |                |
| pago_valor         | double       | NO   |     | 0         |                |
| pago_autor         | varchar(250) | NO   |     | adm       |                |
| tipo               | varchar(7)   | NO   |     | PAGAR     |                |
+--------------------+--------------+------+-----+-----------+----------------+

mysql> select * from financeiro_tiposdocumentos;
+----+--------------------+-----------+
| id | descricao          | idempresa |
+----+--------------------+-----------+
|  1 | FOLHA DE PAGAMENTO |      9999 |
|  2 | TELEFONE           |      9999 |
|  3 | NOTA FISCAL        |      9999 |
|  4 | NOTA SIMPLES       |      9999 |
|  5 | DUPLICATA          |      9999 |
|  6 | RECIBO             |      9999 |
|  7 | BOLETO BANCARIO    |      9999 |
|  8 | CHEQUE             |      9999 |
|  9 | CART?O DE CREDITO  |      9999 |
| 10 | CART?O BNDES       |      9999 |
+----+--------------------+-----------+




mestre
+------------------+-------------+------+-----+---------+----------------+
| Field            | Type        | Null | Key | Default | Extra          |
+------------------+-------------+------+-----+---------+----------------+
| id               | int(10)     | NO   | PRI | NULL    | auto_increment |
| nome_arquivo     | varchar(32) | NO   | MUL |         |                |
| cnpjcpf          | varchar(14) | NO   |     |         |                |
| ie               | varchar(14) | NO   |     |         |                |
| rsocial          | varchar(35) | NO   |     |         |                |
| uf               | varchar(2)  | NO   |     |         |                |
| classe           | varchar(1)  | NO   |     |         |                |
| fase             | varchar(1)  | NO   |     |         |                |
| grupo            | varchar(2)  | NO   |     |         |                |
| codigo           | varchar(12) | NO   |     |         |                |
| emissao          | varchar(8)  | NO   |     |         |                |
| modelo           | varchar(2)  | NO   |     |         |                |
| serie            | varchar(3)  | NO   |     |         |                |
| numero           | varchar(9)  | NO   |     |         |                |
| cad_md5          | varchar(32) | NO   |     |         |                |
| valor_total      | varchar(12) | NO   |     |         |                |
| icms             | varchar(12) | NO   |     |         |                |
| op_isentas       | varchar(12) | NO   |     |         |                |
| outros           | varchar(12) | NO   |     |         |                |
| situacao         | varchar(1)  | NO   |     |         |                |
| bc_icms          | varchar(12) | NO   |     |         |                |
| ano_mes          | varchar(4)  | NO   |     |         |                |
| referencia       | varchar(9)  | NO   |     |         |                |
| numero_terminal  | varchar(12) | NO   |     |         |                |
| brancos          | varchar(5)  | NO   |     |         |                |
| cad_md5_registro | varchar(32) | NO   |     |         |                |
| boleto_nnumero   | varchar(30) | NO   | MUL |         |                |
| boleto_idbanco   | int(10)     | NO   |     | 0       |                |
+------------------+-------------+------+-----+---------+----------------+


item
+------------------+-------------+------+-----+---------+----------------+
| Field            | Type        | Null | Key | Default | Extra          |
+------------------+-------------+------+-----+---------+----------------+
| id               | int(10)     | NO   | PRI | NULL    | auto_increment |
| nome_arquivo     | varchar(32) | NO   | MUL |         |                |
| cnpjcpf          | varchar(14) | NO   |     |         |                |
| uf               | varchar(2)  | NO   |     |         |                |
| classe           | varchar(1)  | NO   |     |         |                |
| fase             | varchar(1)  | NO   |     |         |                |
| grupo            | varchar(2)  | NO   |     |         |                |
| emissao          | varchar(8)  | NO   |     |         |                |
| modelo           | varchar(2)  | NO   |     |         |                |
| serie            | varchar(3)  | NO   |     |         |                |
| numero           | varchar(9)  | NO   |     |         |                |
| cfop             | varchar(4)  | NO   |     |         |                |
| item             | varchar(3)  | NO   |     |         |                |
| cod_servico      | varchar(10) | NO   |     |         |                |
| desc_servico     | varchar(40) | NO   |     |         |                |
| cod_classifica   | varchar(4)  | NO   |     |         |                |
| unidade          | varchar(6)  | NO   |     |         |                |
| quant_contratada | varchar(11) | NO   |     |         |                |
| quant_prestada   | varchar(11) | NO   |     |         |                |
| total            | varchar(11) | NO   |     |         |                |
| desconto         | varchar(11) | NO   |     |         |                |
| acrescimos       | varchar(11) | NO   |     |         |                |
| bc_icms          | varchar(11) | NO   |     |         |                |
| icms             | varchar(11) | NO   |     |         |                |
| op_isentas       | varchar(11) | NO   |     |         |                |
| outros           | varchar(11) | NO   |     |         |                |
| aliquota         | varchar(4)  | NO   |     |         |                |
| situacao         | varchar(1)  | NO   |     |         |                |
| ano_mes          | varchar(4)  | NO   |     |         |                |
| brancos          | varchar(5)  | NO   |     |         |                |
| cad_registro     | varchar(32) | NO   |     |         |                |
| boleto_nnumero   | varchar(30) | NO   | MUL |         |                |
| boleto_idbanco   | int(10)     | NO   |     | 0       |                |
+------------------+-------------+------+-----+---------+----------------+

dados
+-----------------+-------------+------+-----+---------+----------------+
| Field           | Type        | Null | Key | Default | Extra          |
+-----------------+-------------+------+-----+---------+----------------+
| id              | int(10)     | NO   | PRI | NULL    | auto_increment |
| nome_arquivo    | varchar(32) | NO   | MUL |         |                |
| cnpjcpf         | varchar(14) | NO   |     |         |                |
| ie              | varchar(14) | NO   |     |         |                |
| rsocial         | varchar(35) | NO   |     |         |                |
| logradouro      | varchar(45) | NO   |     |         |                |
| numero          | varchar(5)  | NO   |     |         |                |
| complemento     | varchar(15) | NO   |     |         |                |
| cep             | varchar(8)  | NO   |     |         |                |
| bairro          | varchar(15) | NO   |     |         |                |
| municipio       | varchar(30) | NO   |     |         |                |
| uf              | varchar(2)  | NO   |     |         |                |
| telefone        | varchar(12) | NO   |     |         |                |
| codigo          | varchar(12) | NO   |     |         |                |
| numero_terminal | varchar(12) | NO   |     |         |                |
| uf_habilitacao  | varchar(2)  | NO   |     |         |                |
| brancos         | varchar(5)  | NO   |     |         |                |
| cad_registro    | varchar(32) | NO   |     |         |                |
| sequencial      | varchar(9)  | NO   |     |         |                |
| boleto_nnumero  | varchar(30) | NO   | MUL |         |                |
| boleto_idbanco  | int(10)     | NO   |     | 0       |                |
+-----------------+-------------+------+-----+---------+----------------+

--------------+---------------------------+-------------+-------+---------+-------------+-----+------+
| id | rsocial                              | fantasia | cnpj               | ie        | im | endereco                                                           | bairro        | cidade  | uf | cep       | telefone       | fax            | email                      | site                      | voip        | skype | cad_por | dt_cadastro | obs | foto |
+----+--------------------------------------+----------+--------------------+-----------+----+--------------------------------------------------------------------+---------------+---------+----+-----------+----------------+----------------+--------------


select * from financeiro_nf_arquivo_mestre
INTO OUTFILE '/tmp/vigo-nf-mestre.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from financeiro_nf_arquivo_dados d
inner join financeiro_nf_arquivo_mestre m on (m.boleto_idbanco=d.boleto_idbanco and m.boleto_nnumero=d.boleto_nnumero)
INTO OUTFILE '/tmp/vigo-nf-dados.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from financeiro_nf_arquivo_item i 
inner join financeiro_nf_arquivo_mestre m on (m.boleto_idbanco=i.boleto_idbanco and m.boleto_nnumero=i.boleto_nnumero)
INTO OUTFILE '/tmp/vigo-nf-item.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select * from sistema_empresas INTO OUTFILE '/tmp/vigo-empresa.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select * from sistema_cidades_ibge INTO OUTFILE '/tmp/vigo-cidades-ibge.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



SELECT 
mestre.boleto_nnumero as dados_boleto,
mestre.boleto_idbanco as dados_banco,
dados.cnpjcpf as dados_cnpjcpf,    
dados.ie as dados_ie,
dados.rsocial as dados_rsocial, 
dados.logradouro as dados_logradouro,
dados.numero as dados_numero,
dados.complemento as dados_complemento,
dados.cep as dados_cep,
dados.bairro as dados_bairro,
dados.municipio as dados_municipio,
dados.uf as dados_uf,
dados.telefone as dados_telefone, 
dados.codigo as dados_codigo,

mestre.classe as mestre_classe,
mestre.emissao as mestre_emissao,
mestre.modelo as mestre_modelo,
mestre.serie as mestre_serie,          
mestre.numero as mestre_numero,
mestre.valor_total as mestre_valortotal,
mestre.icms as mestre_icms,
mestre.op_isentas as mestre_op_isentas,
mestre.outros as mestre_outros,
mestre.situacao as mestre_situacao,
mestre.bc_icms as mestre_bcicms,
mestre.ano_mes as mestre_anomes,
mestre.referencia as mestre_referencia,

item.cfop as item_cfop,
item.desc_servico as item_desc_servico,
item.cod_servico as item_cod_servico,
item.cod_classifica as item_cod_classifica,
item.unidade as item_unidade,
item.quant_contratada as item_quant_contratada,
item.quant_prestada  as item_quant_prestada,
item.total as item_total,
item.desconto as item_desconto,       
item.acrescimos as item_acrescimos,     
item.bc_icms as item_bcicms,        
item.icms as item_icms,           
item.op_isentas as item_opisentas,     
item.outros as item_outros,         
item.aliquota as item_aliquota,
item.item as item_item   

from financeiro_nf_arquivo_dados dados 
INNER JOIN financeiro_nf_arquivo_mestre mestre ON (mestre.boleto_nnumero=dados.boleto_nnumero and mestre.boleto_idbanco=dados.boleto_idbanco and mestre.cnpjcpf=dados.cnpjcpf)
INNER JOIN financeiro_nf_arquivo_item item ON (item.boleto_nnumero=dados.boleto_nnumero and item.boleto_idbanco=dados.boleto_idbanco and item.cnpjcpf=dados.cnpjcpf)
ORDER BY mestre.emissao desc,mestre.numero,item.item 
INTO OUTFILE '/tmp/vigo-notafiscal-all.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select 
radacctid            ,
acctsessionid        ,
acctuniqueid         ,
username             ,
realm                ,
nasipaddress         ,
nasportid            ,
nasporttype          ,
acctstarttime        ,
'' as acctupdatetime       ,
acctstoptime         ,
acctsessiontime      ,
acctauthentic        ,
connectinfo_start    ,
connectinfo_stop     ,
acctinputoctets      ,
acctoutputoctets     ,
calledstationid      ,
callingstationid     ,
acctterminatecause   ,
servicetype          ,
framedprotocol       ,
framedipaddress      ,
'' as framedipv6prefix     ,
'' as delegatedipv6prefix  
from mikrotik_5739.radacct
INTO OUTFILE '/tmp/vigo-radacct.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';






