
# clientes
SELECT DISTINCT
	t.userid                      ,
	t.company                     ,
	t.vat                         ,
	t.phonenumber                 ,
	t.city                        ,
	t.zip                         ,
	t.state                       ,
	t.address                     ,
	t.website                     ,
	t.datecreated                 ,
	t.active                      ,
	t.billing_street              ,
	t.billing_city                ,
	t.billing_state               ,
	t.billing_zip                 ,
	t.shipping_street             ,
	t.shipping_city               ,
	t.shipping_state              ,
	t.shipping_zip                ,
	t.longitude                   ,
	t.latitude                    ,
	t.show_primary_contact        ,
	t.registration_confirmed      ,
	t.addedfrom                   ,
  tc.id as id_contrato          ,
  tc.dateadded as data_cadastro ,
  tct.name as tipo_contrato     ,
	tbc.content
FROM tblclients t
LEFT JOIN tblcontracts tc ON (t.userid=tc.client)
LEFT JOIN tblcontracts_types tct ON (tc.contract_type=tct.id)
LEFT JOIN tblcontract_comments tbc ON (tbc.contract_id = tc.id)
ORDER BY t.userid INTO OUTFILE '/tmp/perfex-clientes.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


# Contatos
SELECT DISTINCT
	t.id            ,
	t.userid        ,
	t.firstname     ,
	t.lastname      ,
	t.email         ,
	t.phonenumber   ,
	t.title
FROM tblcontacts t ORDER BY t.id INTO OUTFILE '/tmp/perfex-contatos.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


# Notas de Crédito
SELECT DISTINCT
	t.id                            ,
	t.clientid                      ,
	t.`number`                      ,
	t.prefix                        ,
	t.number_format                 ,
	t.datecreated                   ,
	t.`date`                        ,
	t2.symbol                       ,
	t2.name                         ,
	t.subtotal                      ,
	t.total                         ,
	t.billing_street                ,
	t.billing_city                  ,
	t.billing_state                 ,
	t.billing_zip                   ,
	t.show_shipping_on_credit_note  ,
	t.reference_no
FROM tblcreditnotes t
LEFT JOIN tblcurrencies t2 ON (t.currency=t2.id)
ORDER BY t.id INTO OUTFILE '/tmp/perfex-notas-credito.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


# Cobranças
SELECT DISTINCT
	t.id                    ,
	t.sent                  ,
	t.clientid              ,
	t.`number`              ,
	t.prefix                ,
	t.number_format         ,
	t.datecreated           ,
	t.`date`                ,
	t2.symbol               ,
	t2.name                 ,
	t.subtotal              ,
	t.total                 ,
	t.clientnote            ,
	t.discount_total        ,
	t.terms                 ,
	t.billing_street        ,
	t.billing_city          ,
	t.billing_state         ,
	t.billing_zip           ,
	t3.amount as valorpago  ,
	t3.paymentmethod        ,
	t3.`date`               ,
	t3.daterecorded         ,
	t.status
FROM tblinvoices t
LEFT JOIN tblcurrencies t2 ON (t.currency = t2.id)
LEFT JOIN tblinvoicepaymentrecords t3 ON (t.id = t3.invoiceid)
ORDER BY t.id INTO OUTFILE '/tmp/perfex-titulos.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


# Chamados Internos
SELECT DISTINCT
	t.id            ,
	t.name          ,
	t.description   ,
	tp.name         ,
	t.dateadded     ,
	t.startdate     ,
	t.datefinished
FROM tbltasks t
INNER JOIN tbltickets_priorities tp ON (t.priority=tp.priorityid)
INTO OUTFILE '/tmp/perfex-chamadso-internos.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

# Mensagens Chamados Internos
SELECT DISTINCT
	tc.id           ,
	tc.content      ,
	tc.taskid       ,
	tc.contact_id   ,
	tc.dateadded
FROM tbltask_comments tc
INTO OUTFILE '/tmp/perfex-chamadso-internos-msg.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

# Chamados Externos
SELECT DISTINCT
	t.ticketid      ,
	t.userid        ,
	t2.email        ,
	t2.phonenumber  ,
	t3.name         ,
	tp.name         ,
	ts.name         ,
	t4.name         ,
	t.subject       ,
	t.message       ,
	t.`date`        ,
	t.lastreply
FROM tbltickets t
LEFT JOIN tblcontacts t2 ON (t2.id=t.contactid)
LEFT JOIN tbldepartments t3 ON (t3.departmentid=t.department)
INNER JOIN tbltickets_priorities tp ON (tp.priorityid=t.priority)
INNER JOIN tbltickets_status ts ON (ts.ticketstatusid=t.status)
INNER JOIN tblservices t4 ON (t4.serviceid=t.service)
INTO OUTFILE '/tmp/perfex-chamadso-externos.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

# Histórico de Emails
SELECT DISTINCT
	tm.id           ,
	tm.rel_type     ,
	tm.`date`       ,
	tm.email        ,
	tm.opened       ,
	tm.date_opened  ,
	tm.subject
FROM tbltracked_mails tm
INTO OUTFILE '/tmp/perfex-historico-emails.csv'
CHARACTER SET utf8 FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


# Só foi identificado modo de pagamento como Bradesco, porém segundo o S. Fernando também geram cobranças locais.