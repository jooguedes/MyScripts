
----DECLARACAO DE VARIAVEIS---
---- CONFIRME OS MAX ID DE TODOS ESSAS VARIAVEIS NO SISTEMA DO CLIENTE ANTES DE INSERIR ---

--- select max(id) from netcore_nas; ok
--- select max(id) from admcore_plano; ok 
--- select max(id) from financeiro_portador; ok
--- select max(id) from admcore_cliente; ok
--- select max(id) from admcore_clientecontrato; ok


CREATE FUNCTION increment_nas_id (subtotal char) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 40;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION increment_plano_id (subtotal char) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 1500;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION increment_portador_id (subtotal char) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 50;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION increment_cliente_id (subtotal char) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 8000;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION increment_contrato_id (subtotal char) RETURNS int AS $$
BEGIN
    RETURN CAST (subtotal as int) + 8000;
END;
$$ LANGUAGE plpgsql;

CREATE FUNCTION add_string_login (string_login char) RETURNS char AS $$
BEGIN
    RETURN CONCAT(string_login,'_importcontrol02');
END;
$$ LANGUAGE plpgsql;



-- CONCENTRADORES
COPY (
select distinct
(SELECT increment_nas_id(an.nas_pk)),
an.nas_name          ,
an.nas_enabled       ,
an.nas_identifier    ,
an.nas_addr          , --nasname
an.nas_radius_secret , --secret
an.nas_access_user   , -- xuser
an.nas_access_pass   , -- xpassword
an.nas_access_port    -- xport
from aaa_nas an ) TO '/tmp/controllr-nas.csv' WITH DELIMITER '|' CSV;

-- PLANOS
COPY (
select distinct
(SELECT increment_plano_id(ap.plan_pk)),
ap.plan_name       ,
ap.plan_amount     , --valor do plano
ap.plan_rx_nominal , --velocidade de upload
ap.plan_tx_nominal , --velocidade de download
ap.plan_rx_speed   ,
ap.plan_tx_speed
from aaa_plan ap ) TO '/tmp/controllr-planos.csv' WITH DELIMITER '|' CSV;

-- PORTADORES
COPY (
select distinct
(SELECT increment_portador_id(ba.bank_account_pk)),
ba.bank_account_code             ,
ba.bank_account_identification   ,
ba.bank_account_transferor       ,
ba.bank_account_localpayment     ,
ba.bank_account_gateway_username ,
ba.bank_account_gateway_password ,
ba.bank_account_gateway_token    ,
ba.bank_account_agency           , --agencia
ba.bank_account_agency_dv        , --digito da agencia
ba.bank_account_account          , --conta
ba.bank_account_account_dv       , --dígito da conta
ba.bank_account_wallet_variation , --carteira
ba.bank_account_num_convenio     , --convênio 
ba.bank_account_num_convenio_dv
from bank_account ba ) TO '/tmp/controllr-portadores.csv' WITH DELIMITER '|' CSV;

-- CLIENTES
COPY (
select distinct
(SELECT increment_cliente_id(c.client_pk)),
c.client_date_cad             , --data cadastro
c.client_date_birth           , --data nascimento
c.client_complete_name        ,
c.client_observations         ,
c.client_doc1                 ,
c.client_doc2                 ,
c.client_deleted              , --t para cliente cancelado
c.client_date_deleted         , --data de cancelamento
c.client_reason               ,
(select ad.address from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as logradouro_end_cliente,
(select ad.address_number from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as numero_end_cliente,
(select ad.address_neighborhood  from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as bairro_end_cliente,
(select ad.address_province  from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as cidade_end_cliente,
(select ad.address_state from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as estado_end_cliente,
(select ad.address_zipcode from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as cep_end_cliente,
(select ad.address_completation from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as complemento_end_cliente,
(select ad.address_latitude from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as latitude_end_cliente,
(select ad.address_longitude from addresses ad where ad.client_pk=c.client_pk order by ad.address_pk asc limit 1)  as logitude_end_cliente,
(SELECT increment_contrato_id(cc.contract_pk)),
cc.contract_number             ,
cc.contract_pay_day            ,
cc.contract_free               ,
cc.contract_date_cad           ,
cc.contract_status             ,
cc.contract_deleted            ,
cc.contract_observations       ,
o.offices_identification       ,
o.offices_name                 ,
(SELECT increment_portador_id(ba.bank_account_pk)),
ba.bank_account_identification ,
(select a.address from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_number from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_neighborhood from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_province from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_state from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_zipcode from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_completation from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_latitude from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_longitude from addresses a where a.address_pk=cc.address_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
ac.cpe_status                  ,
(SELECT add_string_login(ac.cpe_username)),
ac.cpe_password                ,
ac.cpe_v4_ip_last              ,
ac.cpe_v6_px_last              ,
ac.cpe_mac_last                ,
(SELECT increment_plano_id(ac.plan_pk)),
(select a.address from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_number from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_neighborhood from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_province from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_state from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_zipcode from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_completation from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_latitude from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
(select a.address_longitude from addresses a where ac.contract_pk=cc.contract_pk order by a.address_pk asc limit 1)  as logradouro_end_cliente_cob,
ac.cpe_obs                    ,
(SELECT increment_nas_id(ac.nas_pk))
from client c 
inner join contract cc on (cc.client_pk=c.client_pk)
left join offices o on (cc.offices_pk=o.offices_pk)
left join bank_account ba on (cc.bank_account_pk=ba.bank_account_pk)
left join addresses a on (cc.address_pk=a.address_pk)
inner join aaa_cpe ac on (ac.contract_pk=cc.contract_pk)
left join addresses ei on (ac.address_pk=ei.address_pk) ) TO '/tmp/controllr-clientes.csv' WITH DELIMITER '|' CSV;

-- EMAILS
COPY (
select distinct
ce.client_email_pk             ,
ce.client_email_identification ,
ce.client_email_address        ,
(SELECT increment_cliente_id(ce.client_pk))
from client_email ce ) TO '/tmp/controllr-emails.csv' WITH DELIMITER '|' CSV;


-- TELEFONES
COPY (
select distinct
cp.phone_pk             ,
cp.phone_identification ,
cp.phone_number         ,
cp.phone_operator       ,
(SELECT increment_cliente_id(cp.client_pk))
from client_phone cp ) TO '/tmp/controllr-telefones.csv' WITH DELIMITER '|' CSV;

-- TITULOS
COPY (
select distinct
i.invoice_pk                  ,
i.invoice_document_number     , --numero documento
i.invoice_amount_document     , --valor
i.invoice_amount_paid         , --valorpago
i.invoice_payment_method      , --????
i.invoice_nosso_num           , --nosso numero
i.invoice_date_due            , --data de vencimento
i.invoice_date_document       , --data de documento
i.invoice_date_credit         , --data de pagamento
i.invoice_discount_due_amount , --desconto até o vencimento
(SELECT increment_cliente_id(i.client_pk)),
(SELECT increment_contrato_id(i.contract_pk)),
i.carnet_pk                   ,
i.invoice_deleted             , -- se t cobrança cancelada
i.invoice_gn_key              , --id de transacao
i.invoice_gn_link             , --link de gateway
i.invoice_barcode             , --código de barras
(SELECT increment_portador_id(i.bank_account_pk ))            --id do portador

from invoice i ) TO '/tmp/controllr-titulos.csv' WITH DELIMITER '|' CSV;

-- CHAMADOS
COPY (
select distinct
st.ticket_pk          ,
st.ticket_protocol    ,
st.ticket_title       ,
st.ticket_desc        ,
st.ticket_obs         ,
st.ticket_date_create ,
st.ticket_date_last   ,
st.ticket_date_close  ,
st.ticket_deleted     ,
st.ticket_priority    ,
st.ticket_done        ,
sc.category_pk        , --id categoria
sc.category_name      , --nome categoria
sc.category_desc      , --descricao categoria
(SELECT increment_cliente_id(st.client_pk)),
(SELECT increment_contrato_id(st.contract_pk))
from support_ticket st
left join support_category sc on (st.category_pk=sc.category_pk) ) TO '/tmp/controllr-chamados.csv' WITH DELIMITER '|' CSV HEADER;


-- ANOTACOES
COPY (
select distinct 
ca.annotation_text      ,
ca.annotation_date_cad  ,
ca.user_username        ,
ca.annotation_deleted   ,
ca.client_pk            ,
ca.annotation_obs       ,
ca.contract_pk
from client_annotations ca) TO '/tmp/controllr-anotacoes.csv' WITH DELIMITER '|' CSV;