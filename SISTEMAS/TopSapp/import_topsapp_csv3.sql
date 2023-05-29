echo "" > create
echo "create table clientes(" >> create
head -n 1 clientes.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table servicos(" >> create
head -n 1 servicos.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table servicos_clientes(" >> create
head -n 1 servicos_clientes.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table servicos_clientes_acesso(" >> create; 
head -n 1 servicos_clientes_acesso.csv | sed "s/,/ text,/g" >> create 
echo "text);" >> create
echo "" >> create
echo "create table planos(" >> create
head -n 1 planos.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table cidades(" >> create
head -n 1 cidades.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table vencimentos(" >> create
head -n 1 vencimentos.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table receber(" >> create
head -n 1 receber.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table receber_f2b(" >> create
head -n 1 receber_f2b.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create
echo "create table portadores(" >> create
head -n 1 portadores.csv | sed "s/,/ text,/g" >> create
echo "text);" >> create
echo "" >> create

for i in clientes.csv servicos.csv servicos_clientes.csv servicos_clientes_acesso.csv planos.csv cidades.csv vencimentos.csv receber.csv portadores.csv; do cp $i /tmp; done 


COPY clientes FROM '/tmp/clientes.csv' DELIMITER ',' CSV;
COPY servicos FROM '/tmp/servicos.csv' DELIMITER ',' CSV;
COPY servicos_clientes FROM '/tmp/servicos_clientes.csv' DELIMITER ',' CSV;
COPY servicos_clientes_acesso FROM '/tmp/Servicos_clientes_acesso.csv' DELIMITER ',' CSV;
COPY planos FROM '/tmp/Planos.csv' DELIMITER ',' CSV;
COPY cidades FROM '/tmp/Cidades.csv' DELIMITER ',' CSV;
COPY vencimentos FROM '/tmp/Vencimentos.csv' DELIMITER ',' CSV;
COPY receber FROM '/tmp/Receber.csv' DELIMITER ',' CSV;
COPY portadores FROM '/tmp/Portadores.csv' DELIMITER ',' CSV;

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
tsc.observacoes,
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
tc.observacoes,
tc.senhacentral,
tc.observacoes_tecnica,
tsc.id as id_servico,
null,
null
FROM clientes tc 
INNER JOIN cidades cid on (cid.id=tc.cidade)
INNER JOIN servicos_clientes tsc ON (tsc.cliente_id=tc.id) 
INNER JOIN servicos_clientes_acesso tsca ON (tsca.servico_cliente_id=tsc.id) 
INNER JOIN servicos ts on (ts.id=tsc.servico_id)
INNER JOIN planos tp ON (tp.id_servico=ts.id)
) TO '/tmp/topsapp-clientes.csv' DELIMITER '|' CSV;


COPY (
SELECT 
1,
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
'' as gfiscal,
'' as codigo_carne,
'' as linhadig,
'' as codigobarras,
case when r.datapagto is null then 'aberto' else 'pago' end as status,
r.valor,
'0.00'
--r.desconto_vencimento
--'0.00' as desconto_venc
FROM receber r
INNER JOIN clientes tc ON (tc.id=r.id_cliente)
INNER JOIN cidades cid on (cid.id=tc.cidade)
INNER JOIN servicos_clientes tsc ON (tsc.cliente_id=tc.id) 
INNER JOIN servicos_clientes_acesso tsca ON (tsca.servico_cliente_id=tsc.id) 
WHERE r.id_portador='4'
ORDER BY r.id ) TO '/tmp/topsapp-titulos-PAGAMENTO_CLICKNET_GERAR_CARNE.csv' DELIMITER '|' CSV;

COPY (
SELECT 
1,
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
'' as gfiscal,
'' as codigo_carne,
'' as linhadig,
'' as codigobarras,
case when r.datapagto is null then 'aberto' else 'pago' end as status,
r.valor,
g.url,
---g.lote or
'' ,
g.chave_gnt
FROM receber r
INNER JOIN clientes tc ON (tc.id=r.id_cliente)
INNER JOIN servicos_clientes tsc ON (tsc.cliente_id=tc.id) 
INNER JOIN servicos_clientes_acesso tsca ON (tsca.servico_cliente_id=tsc.id) 
INNER JOIN receber_f2b g ON (g.id_receber=r.id)
--WHERE r.id_portador='23'
ORDER BY r.id ) TO '/tmp/titulos.csv' DELIMITER '|' CSV;


COPY (
SELECT 
1,
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
r.gfiscal,
'' as codigo_carne,
'' as linhadig,
'' as codigobarras,
case when r.datapagto is null then 'aberto' else 'pago' end as status,
r.valor
FROM topsapp.receber r
INNER JOIN topsapp.clientes tc ON (tc.id=r.id_cliente)
INNER JOIN topsapp.servicos_clientes tsc ON (tsc.cliente_id=tc.id) 
INNER JOIN topsapp.servicos_clientes_acesso tsca ON (tsca.servico_cliente_id=tsc.id) 
WHERE r.id_portador=1
AND r.id not in (select g.id_receber from topsapp.receber_f2b g)
ORDER BY r.id ) TO '/tmp/titulos-1.csv' DELIMITER '|' CSV;






