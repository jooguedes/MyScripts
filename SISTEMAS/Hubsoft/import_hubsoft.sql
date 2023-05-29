
CREATE FUNCTION increment_cliente_id (subtotal int) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 8000;
END;
$$ LANGUAGE plpgsql;



CREATE FUNCTION increment_servico_id (subtotal int) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 8000;
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION increment_portador_id (subtotal int) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 8000;
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION increment_ocorrencia_id (subtotal int) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 8000;
END;
$$ LANGUAGE plpgsql;


CREATE FUNCTION increment_notafiscal_id (subtotal int) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 8000;
END;    
$$ LANGUAGE plpgsql;



--- CLIENTES
COPY (select
DISTINCT
(SELECT increment_cliente_id(c.id_cliente)),
c.nome_razaosocial as nome,
c.nome_fantasia, 
c.telefone_primario as celular,
c.telefone_secundario as telefone,
c.cpf_cnpj,
c.rg,
c.tipo_pessoa,
c.email_principal,
c.email_secundario,
c.data_cadastro,
c.ativo as status_cliente,
c.nome_pai,
c.nome_mae,
c.profissao,
aut.login||'@hubsoftware',
aut.password,
(SELECT increment_servico_id((select s.id_servico  from servico s where s.id_servico=cs.id_servico))) as id_plano,
(select s.descricao  from servico s where s.id_servico=cs.id_servico)||'@hubsoftware' as plano,
(select s.valor  from servico s where s.id_servico=cs.id_servico) as valor,
(select sn.download from servico_navegacao sn where sn.id_servico=(select s.id_servico from servico s  where s.id_servico=cs.id_servico )) as download,
(select sn.upload from servico_navegacao sn where sn.id_servico=(select s.id_servico from servico s  where s.id_servico=cs.id_servico )) as upload,
(select v.dia_vencimento from vencimento v where cs.id_vencimento=v.id_vencimento) as vencimento,
cs.id_forma_cobranca as ID_portador,
cs.data_cadastro,
(select endn.numero from endereco_numero endn where  cend.id_endereco_numero=endn.id_endereco_numero) as numero,
(select endn.complemento from endereco_numero endn where  cend.id_endereco_numero=endn.id_endereco_numero) as complemento,
(select endn.bairro from endereco_numero endn where  cend.id_endereco_numero=endn.id_endereco_numero) as bairro,
(select endn.endereco from endereco_numero endn where  cend.id_endereco_numero=endn.id_endereco_numero) as logradouro,
(select endn.cep from endereco_numero endn where  cend.id_endereco_numero=endn.id_endereco_numero) as cep,
(select endn.coordenadas from endereco_numero endn where  cend.id_endereco_numero=endn.id_endereco_numero) as coordenadas,
(select c.nome as cidade from cidade c where (select endn.id_cidade from endereco_numero endn where (cend.id_endereco_numero=endn.id_endereco_numero))=c.id_cidade),
c.data_nascimento,
(SELECT increment_cliente_id(cs.id_cliente_servico)) as contrato
from cliente  c
inner join cliente_servico cs on (c.id_cliente=cs.id_cliente)
inner join cliente_servico_autenticacao aut on (aut.id_cliente_servico=cs.id_cliente_servico)
inner join cliente_endereco_numero cend on (cend.id_cliente=c.id_cliente) ) TO '/tmp/hubsoft-clientes.csv' WITH DELIMITER '|' CSV;


---Titulos
COPY(
select 
t.id_fatura,
(SELECT increment_portador_id(t.id_forma_cobranca)) as portador,
t.nosso_numero,
t.numero_documento,
t.valor,
t.valor_pago,
t.data_vencimento,
t.data_pagamento,
t.data_cadastro as emicao,
(SELECT increment_servico_id(t.id_cliente_servico)) as id_servico,
t.numero_controle,
t.linha_digitavel,
t.codigo_barras,
t.nosso_numero_dv as nosso_numero_digito,
t.link,
t.parcela
from fatura t) TO '/tmp/hubsoft-titulos.csv' WITH DELIMITER '|' CSV;



---OCORRENCIAS
COPY(
select
(SELECT increment_ocorrencia_id(oc.id_atendimento)),
oc.protocolo,
(SELECT increment_ocorrencia_id(oc.id_cliente_servico)),
oc.id_tipo_atendimento,
oc.descricao_abertura,
oc.descricao_fechamento,
oc.data_cadastro,
oc.data_fechamento
from atendimento oc) TO '/tmp/hubsoft-ocorrencia.csv' WITH DELIMITER '|' CSV;


---NOTA FISCAL
COPY(
select 
(SELECT increment_notafiscal_id(nf.id_nota_fiscal)),
nf.numero_nota,
nf.serie_nota,
nf.cfop,
nf.data_emissao,
nf.data_cancelamento,
nf.valor,
nf.valor_icms,
(SELECT increment_cliente_id(nf.id_cliente)),
nf.emitente_documento as cpf_cnpj,
nf.emitente_razao_social,
nf.destinatario_documento as cpf_cnpj_destinatario,
nf.destinatario_razao_social,
nf.destinatario_endereco,
nf.destinatario_numero,
nf.destinatario_complemento,
nf.destinatario_bairro,
nf.destinatario_cidade,
nf.destinatario_uf,
nf.destinatario_cep,
nf.destinatario_ibge,
nf.destinatario_telefone,
nfcob.descricao,
(select f.nosso_numero from fatura f where  f.id_fatura=cob.id_fatura) as nosso_numero
from nota_fiscal nf
left  join nota_fiscal_cobranca nfcob on (nfcob.id_nota_fiscal=nf.id_nota_fiscal)
inner join cobranca cob on (cob.id_cobranca = nfcob.id_cobranca)) TO '/tmp/hubsoft-notafiscal.csv' WITH DELIMITER '|' CSV;



---FORNECEDORES
select
f.id_fornecedor,
f.nome_razaosocial,
f.nome_fantasia,
f.telefone_primario,
f.telefone_secundario,
f.email_primario,
f.cpf_cnpj,
f.tipo_pessoa
FROM fornecedor f;


---PORTADORES
COPY ( 
select (SELECT increment_portador_id(id_forma_cobranca)) AS ID_portador,
id_forma_cobranca,
descricao,
id_banco as codigo
from forma_cobranca) TO '/tmp/hubsoft-portadores.csv' WITH DELIMITER '|' CSV;