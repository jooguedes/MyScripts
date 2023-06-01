echo "" > create
echo "create table clientes(" >> create
head -n 1 clientes.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table servicos(" >> create
head -n 1 servicos.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table servicos_clientes(" >> create
head -n 1 servicos_clientes.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table servicos_clientes_acesso(" >> create; 
head -n 1 servicos_clientes_acesso.csv.utf8 | sed "s/,/ text,/g" >> create 
echo "text);" >> create
echo "" >> create
echo "create table planos(" >> create
head -n 1 planos.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table cidades(" >> create
head -n 1 cidades.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table vencimentos(" >> create
head -n 1 vencimentos.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table receber(" >> create
head -n 1 receber.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table receber_f2b(" >> create
head -n 1 receber_f2b.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table portadores(" >> create
head -n 1 portadores.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table fornecedores(" >> create
head -n 1 fornecedores.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table cfop(" >> create
head -n 1 cfop.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table nf21(" >> create
head -n 1 nf21.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table nf21_itens(" >> create
head -n 1 nf21_itens.csv.utf8 | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create




for i in clientes.csv.utf8 fornecedores.csv.utf8 servicos.csv.utf8 servicos_clientes.csv.utf8 servicos_clientes_acesso.csv.utf8 planos.csv.utf8 cidades.csv.utf8 vencimentos.csv.utf8 receber.csv.utf8 portadores.csv.utf8 fornecedores.csv.utf8 cfop.csv.utf8 nf21.csv.utf8 nf21_itens.csv.utf8; do cp $i /tmp; done 

COPY clientes FROM '/tmp/clientes.csv.utf8' DELIMITER ',' CSV;
COPY servicos FROM '/tmp/servicos.csv.utf8' DELIMITER ',' CSV;
COPY servicos_clientes FROM '/tmp/servicos_clientes.csv.utf8' DELIMITER ',' CSV;
COPY servicos_clientes_acesso FROM '/tmp/servicos_clientes_acesso.csv.utf8' DELIMITER ',' CSV;
COPY planos FROM '/tmp/planos.csv.utf8' DELIMITER ',' CSV;
COPY cidades FROM '/tmp/cidades.csv.utf8' DELIMITER ',' CSV;
COPY vencimentos FROM '/tmp/vencimentos.csv.utf8' DELIMITER ',' CSV;
COPY receber FROM '/tmp/receber.csv.utf8' DELIMITER ',' CSV;
COPY portadores FROM '/tmp/portadores.csv.utf8' DELIMITER ',' CSV;
COPY fornecedores FROM '/tmp/fornecedores.csv.utf8' DELIMITER ',' CSV;
COPY cfop FROM '/tmp/cfop.csv.utf8' DELIMITER ',' CSV;
COPY nf21 FROM '/tmp/nf21.csv.utf8' DELIMITER ',' CSV;
COPY nf21_itens FROM '/tmp/nf21_itens.csv.utf8' DELIMITER ',' CSV;


COPY (
SELECT 
tc.id,
tsca.usuario,
tc.pessoa,
tc.nome,
1,
tc.cpf,
15,
15,
tc.rg,
'' as profissao,
tc.sexo,
tc.data_nascimento,
tc.fantasia,
'' as contato,
tc.endereco,
tc.numero,
tc.complemento,
tc.bairro,
tc.cep,
tc.uf,
cid.cidade,
tc.celular,
tc.telefone,
tc.email,
'',
 tc.data_cadastro,
 tc.data_cadastro,
 '' as grupo,
 '' as nas,
ts.descricao as plano, 
ts.valor as plano_valor, 
'' as conntipo,
tsca.ip,
tsca.ip,
tsca.mac,
10,
tsc.desconto,
tsc.acrescimo,
'' as transmissor,
'' as receptor,
'nao' as comodato,
case when tsc.gerar_fatura = 'f' then  'sim' else 'nao' end as isento,
tsc.status,
tsca.senha,
tp.download,
tp.upload,
tsc.data as servicodata,
tsc.data_bloqueio,
tsc.data_desativacao,
tc.pai,
tc.mae,
tc.natural_cidade,
tc.natural_estado,
tc.insc_estadual,
tc.insc_municipal,
'',
tc.senhacentral,
'',
tsc.id as id_servico,
null,
null
FROM clientes tc 
INNER JOIN cidades cid on (cid.id=tc.cidade)
LEFT JOIN servicos_clientes tsc ON (tsc.cliente_id=tc.id) 
LEFT JOIN servicos_clientes_acesso tsca ON (tsca.servico_cliente_id=tsc.id) 
LEFT JOIN servicos ts on (ts.id=tsc.servico_id)
LEFT JOIN planos tp ON (tp.id_servico=ts.id)
) TO '/tmp/topsapp-clientes.csv' DELIMITER '|' CSV;


COPY (
SELECT 
tc.id,
tsca.usuario,
tc.cpf,
'' as formapag,
'mensalidade' as tipo,
r.historico,
r.data,
r.vencimento,
r.datapagto,
r.id as numero,
r.id as nossonumero,
r.valor,
r.valorpago,
r.valor,
'',
'' as codigo_carne,
'' as linhadig,
'' as codigobarras,
case when r.datapagto is null then 'aberto' else 'pago' end as status,
r.valor,
r.id_portador
FROM receber r
INNER JOIN clientes tc ON (tc.id=r.id_cliente)
INNER JOIN servicos_clientes tsc ON (tsc.cliente_id=tc.id) 
INNER JOIN servicos_clientes_acesso tsca ON (tsca.servico_cliente_id=tsc.id) 
ORDER BY r.id ) TO '/tmp/topsapp-titulos-all.csv' DELIMITER '|' CSV;



COPY (
SELECT 
f.id,
f.fornecedor,
f.fantasia,
f.telefone,
f.celular,
f.fax,
f.insc_est,
f.cnpj,
f.endereco,
f.bairro,
f.cep,
cd.cidade,
f.uf,
f.numero,
f.email
FROM fornecedores f
LEFT JOIN cidades cd ON (cd.id=f.cidade)
ORDER BY f.id ) TO '/tmp/topsapp-fornecedores.csv' DELIMITER '|' CSV;



COPY (
SELECT DISTINCT ON(nf.codnota)
  nf.codnota,
  (select cfop from cfop cf where ni.id_cfop=cf.id) as cfop,
  (select descricao from cfop cf where ni.id_cfop=cf.id) as descricao,
  nf.id_cliente,
  nf.cpf,
  nf.data,
  nf.modelo,
  nf.serie,
  ni.valor_total,
  nf.icms,
  nf.valor_cofins,
  nf.id_receber,
  nf.status
FROM nf21_itens ni
INNER JOIN nf21 nf ON (ni.idnota=nf.id)
ORDER BY nf.codnota ) TO '/tmp/topsapp-nf2122.csv' DELIMITER '|' CSV;





