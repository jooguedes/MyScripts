-- EMPRESAS
copy (
select distinct 
	cp.id                   ,
	cp.code                 ,
	cp.active               ,
	cp.description          ,
	cp.name_2               ,
	cp.tx_id                ,
	cp.postal_code          ,
	cp.street               ,
	cp."number"             ,
	cp.address_complement   ,
	cp.neighborhood         ,
	cp.city                 ,
	cp.state                ,
	cp.city_code            ,
	cp.phone                ,
	cp.beginning_activities ,
	cp.created              ,
	cp.modified
from companies_places cp 
where cp.deleted = 'f'
) TO '/tmp/synsuit-empresas.csv' DELIMITER '|' csv;

-- PORTADORES
copy (
select distinct 
	ba.id                  ,
	b."name"               ,
	b.code                 ,
	b.central_bank_code    ,
	ba.active              ,
	ba.description         ,
	ba.agency              ,
	ba.agency_check_digit  ,
	ba.account             ,
	ba.account_check_digit
from bank_accounts ba 
inner join banks b on (ba.bank_id = b.id)
where ba.deleted = 'f'
) TO '/tmp/synsuit-portadores.csv' DELIMITER '|' csv;


-- CLIENTES ATIVADOS
copy (
select distinct 
	p.id                           ,
	p.situation                    ,
	p.type_tx_id                   ,
	p.tx_id                        ,
	p."name"                       ,
	p.name_2                       ,
	-- Endereço do cliente
	p.postal_code                  ,
	p.street                       ,
	p.street_type                  ,
	p."number"                     ,
	p.address_complement           ,
	p.neighborhood                 ,
	p.city                         ,
	p.code_city_id                 ,
	p.state                        ,
	p.lat                          ,
	p.lng                          ,
	p.address_reference            ,
	p.status                       ,
	p.client                       ,
	-- Endereco de cobranca 
	p.financier_postal_code        ,
	p.financier_street             ,
	p.financier_number             ,
	p.financier_address_complement ,
	p.financier_neighborhood       ,
	p.financier_city               ,
	p.financier_code_city_id       ,
	p.financier_state              ,
	p.financier_address_reference  ,
	fn.title                       ,
	p.email                        ,
	p."email_NFE"                  ,
	pg.title                       ,
	pg.description                 ,
	p."identity" as rgie           ,
	p.birth_date as dt_nascimento  ,
	p.parents_name as mae          ,
	p.administrative_observation   ,
	p.created as dt_cadastro       ,
	p.modified                     ,
	p.phone                        ,
	p.commercial_phone             ,
	p.fax_phone                    ,
	p.cell_phone_1                 ,
	p.cell_phone_2                 ,
	p.observ                       ,
	p.observ2                      ,
	c.id as id_contrato            ,
	c.company_place_id             ,
	c.description                  ,
	c."date"                       ,
	c.observation                  ,
	c.collection_day as vencimento ,
	c.status                       ,
	c.cancellation_date            ,
	c.cancellation_motive          ,
	c.end_date                     ,
	fn2.description                ,
	ci.total_amount as valor_plano ,
	sp.title                       ,
	sp.description                 ,
	sp.upload_max_limit            ,
	sp.download_max_limit          ,
	ac."user"  as login            ,
	ac."password"  as senha        ,
	ac.port_olt                    ,
	ac.slot_olt                    ,
	ac.equipment_serial_number     ,
	-- Endereco de servico
	ac.postal_code                 ,
	ac.street_number               ,
	ac.neighborhood                ,
	ac.street                      ,
	ac.city                        ,
	ac.state                       ,
	ac.address_complement          ,
	ac.reference                   ,
	ac.lat                         ,
	ac.lng                         ,
	ac.complement as obs_service   ,
	ac.authentication_ip           ,
	ac.mac
from people p
left join financers_natures fn on (fn.id = p.financier_nature_id)
left join people_groups pg on (pg.id = p.people_group_id)
inner join contracts c on (c.client_id = p.id)
left join financers_natures fn2 on (fn2.id = c.financer_nature_id)
inner join contract_items ci on (ci.contract_id = c.id)
inner join service_products sp on (ci.service_product_id = sp.id)
inner join authentication_contracts ac on (ac.contract_item_id = ci.id)
where p.deleted = 'f' and c.deleted = 'f'
) TO '/tmp/synsuit-clientes-ativos.csv' DELIMITER '|' csv;

-- CLIENTES DESATIVADOS
copy (
select distinct 
	p.id                           ,
	p.situation                    ,
	p.type_tx_id                   ,
	p.tx_id                        ,
	p."name"                       ,
	p.name_2                       ,
	-- Endereço do cliente
	p.postal_code                  ,
	p.street                       ,
	p.street_type                  ,
	p."number"                     ,
	p.address_complement           ,
	p.neighborhood                 ,
	p.city                         ,
	p.code_city_id                 ,
	p.state                        ,
	p.lat                          ,
	p.lng                          ,
	p.address_reference            ,
	p.status                       ,
	p.client                       ,
	-- Endereco de cobranca 
	p.financier_postal_code        ,
	p.financier_street             ,
	p.financier_number             ,
	p.financier_address_complement ,
	p.financier_neighborhood       ,
	p.financier_city               ,
	p.financier_code_city_id       ,
	p.financier_state              ,
	p.financier_address_reference  ,
	fn.title                       ,
	p.email                        ,
	p."email_NFE"                  ,
	pg.title                       ,
	pg.description                 ,
	p."identity" as rgie           ,
	p.birth_date as dt_nascimento  ,
	p.parents_name as mae          ,
	p.administrative_observation   ,
	p.created as dt_cadastro       ,
	p.modified                     ,
	p.phone                        ,
	p.commercial_phone             ,
	p.fax_phone                    ,
	p.cell_phone_1                 ,
	p.cell_phone_2                 ,
	p.observ                       ,
	p.observ2                      ,
	c.id as id_contrato            ,
	c.company_place_id             ,
	c.description                  ,
	c."date"                       ,
	c.observation                  ,
	c.collection_day as vencimento ,
	c.status                       ,
	c.cancellation_date            ,
	c.cancellation_motive          ,
	c.end_date                     ,
	fn2.description                ,
	ci.total_amount as valor_plano ,
	sp.title                       ,
	sp.description                 ,
	sp.upload_max_limit            ,
	sp.download_max_limit          ,
	ac."user"  as login            ,
	ac."password"  as senha        ,
	ac.port_olt                    ,
	ac.slot_olt                    ,
	ac.equipment_serial_number     ,
	-- Endereco de servico
	ac.postal_code                 ,
	ac.street_number               ,
	ac.neighborhood                ,
	ac.street                      ,
	ac.city                        ,
	ac.state                       ,
	ac.address_complement          ,
	ac.reference                   ,
	ac.lat                         ,
	ac.lng                         ,
	ac.complement as obs_service   ,
	ac.authentication_ip           ,
	ac.mac
from people p
left join financers_natures fn on (fn.id = p.financier_nature_id)
left join people_groups pg on (pg.id = p.people_group_id)
inner join contracts c on (c.client_id = p.id)
left join financers_natures fn2 on (fn2.id = c.financer_nature_id)
inner join contract_items ci on (ci.contract_id = c.id)
inner join service_products sp on (ci.service_product_id = sp.id)
left join authentication_contracts ac on (ac.contract_item_id = ci.id)
where p.deleted = 'f' and c.deleted = 'f' and c.status in ('9', '4')
) TO '/tmp/synsuit-clientes-desativados.csv' DELIMITER '|' csv;


-- TITULOS
copy (
select distinct 
	ft.id                             ,
	ft.company_place_id               ,
	ft.client_id                      ,
	ft.situation                      ,
	ft.title                          ,
	ft.parcel                         ,
	ft.bank_title_number              ,
	ft.company_place_business_unit_id ,
	ft.document_amount                ,
	ft.title_amount                   ,
	ft.issue_date                     ,
	ft.entry_date                     ,
	ft.expiration_date                ,
	ft.original_expiration_date       ,
	fo.code                           ,
	fo.title                          ,
	fn.code                           ,
	fn.title                          ,
	ft.bank_account_id                ,
	fc.title                          ,
	fc.bank_account_id                ,
	pc.title                          ,
	ft.complement                     ,
	ft.contract_id                    ,
	ft.competence                     ,
	ft.typeful_line                   ,
	ft.barcode                        ,
	ft.created                        ,
	ft.modified                       ,
	fr.receipt_date as data_bx        ,
	fr.client_paid_date as data_pg    ,
	fr.total_amount                   ,
	fr.complement 
from financial_receivable_titles ft
left join financial_operations fo on (fo.id = ft.financial_operation_id)
left join financers_natures fn on (fn.id = ft.financer_nature_id)
left join financial_collection_types fc on (fc.id = ft.financial_collection_type_id) 
left join payment_conditions pc on (pc.id = ft.payment_condition_id)
left join financial_receipt_titles fr on (fr.financial_receivable_title_id = ft.id) 
where ft.deleted = 'f' and ft.bank_account_id != ''
) TO '/tmp/synsuit-titulos-areceber.csv' DELIMITER '|' csv;


copy (
select distinct 
	ft.id                             ,
	ft.company_place_id               ,
	ft.client_id                      ,
	ft.situation                      ,
	ft.title                          ,
	ft.parcel                         ,
	ft.bank_title_number              ,
	ft.company_place_business_unit_id ,
	ft.document_amount                ,
	ft.title_amount                   ,
	ft.issue_date                     ,
	ft.entry_date                     ,
	ft.expiration_date                ,
	ft.original_expiration_date       ,
	fo.code                           ,
	fo.title                          ,
	fn.code                           ,
	fn.title                          ,
	ft.bank_account_id                ,
	fc.title                          ,
	fc.bank_account_id                ,
	pc.title                          ,
	ft.complement                     ,
	ft.contract_id                    ,
	ft.competence                     ,
	ft.typeful_line                   ,
	ft.barcode                        ,
	ft.created                        ,
	ft.modified                       ,
	fr.receipt_date as data_bx        ,
	fr.client_paid_date as data_pg    ,
	fr.total_amount                   ,
	fr.complement 
from financial_receivable_titles ft
left join financial_operations fo on (fo.id = ft.financial_operation_id)
left join financers_natures fn on (fn.id = ft.financer_nature_id)
left join financial_collection_types fc on (fc.id = ft.financial_collection_type_id) 
left join payment_conditions pc on (pc.id = ft.payment_condition_id)
left join financial_receipt_titles fr on (fr.financial_receivable_title_id = ft.id) 
where ft.deleted = 'f' and ft.bank_account_id = ''
) TO '/tmp/synsuit-titulos-areceber-sembanco.csv' DELIMITER '|' csv;

-- FORNECEDORES
copy (
select distinct 
	p.id                           ,
	p.type_tx_id                   ,
	p.tx_id                        ,
	p."name"                       ,
	p.name_2                       ,
	p.postal_code                  ,
	p.street                       ,
	p.street_type                  ,
	p."number"                     ,
	p.address_complement           ,
	p.neighborhood                 ,
	p.city                         ,
	p.code_city_id                 ,
	p.state                        ,
	p.lat                          ,
	p.lng                          ,
	p.address_reference            ,
	p.email                        ,
	p."email_NFE"                  ,
	p.administrative_observation   ,
	p.created as dt_cadastro       ,
	p.modified                     ,
	p.phone                        ,
	p.commercial_phone             ,
	p.fax_phone                    ,
	p.cell_phone_1                 ,
	p.cell_phone_2                 ,
	p.observ                       ,
	p.observ2
from people p
where p.deleted = 'f' and (p.supplier = 't' or p.supplier = '1')
) TO '/tmp/synsuit-fornecedores.csv' DELIMITER '|' csv;

-- CONTAS A PAGAR
copy (
select distinct 
	ft.id                       ,
	ft.company_place_id         ,
	ft.supplier_id              ,
	ft.title                    ,
	ft.parcel                   ,
	ft.title_amount             ,
	ft.issue_date               ,
	ft.entry_date               ,
	ft.expiration_date          ,
	ft.original_expiration_date ,
	fo.code                     ,
	fo.title                    ,
	fn.code                     ,
	fn.title                    ,
	ft.complement               ,
	ft.observation              ,
	ft.competence               ,
	ft.bar_code                 ,
	ft.typeful_line             ,
	ft.created                  ,
	ft.modified                 ,
	fp.payment_date             ,
	fp.total_amount 
from financial_payable_titles ft 
left join financial_operations fo on (fo.id = ft.financial_operation_id)
left join financers_natures fn on (fn.id = ft.financer_nature_id)
left join financial_paid_titles fp on (fp.financial_payable_title_id = ft.id) 
where ft.deleted = 'f'
) TO '/tmp/synsuit-contas-a-pagar.csv' DELIMITER '|' csv;


-- OCORRENCIAS
copy (
select distinct 
	a.id                   ,
	ao.description         ,
	ic.code                ,
	ic.title               ,
	ic.description         ,
	ai.client_id           ,
	ai.person_id           ,
	ai.protocol            ,
	ai.date_to_start       ,
	ao.description         ,
	a.title                ,
	a.description          ,
	a.priority             ,
	a.beginning_date       ,
	a.final_date           ,
	a.conclusion_date      ,
	a.status               ,
	a.internal_observation ,
	a.created              ,
	a.modified
from assignments a 
inner join assignment_incidents ai on (ai.assignment_id = a.id)
left join assignment_origins ao on (ao.id = ai.assignment_incident_origin)
left join incident_status ic on (ic.id = ai.incident_status_id)
left join incident_types it on (it.id = ai.incident_type_id)
where a.deleted = 'f'
) TO '/tmp/synsuit-ocorrencias.csv' DELIMITER '|' csv;


-- NOTAS FISCAIS
copy (
select distinct 
	in2.id                        ,
	in2.company_place_id          ,
	in2.company_place_name        ,
	in2.company_place_description ,
	is2.code                      ,
	is2.initials                  ,
	is2.title                     ,
	in2.document_number           ,
	in2.contract_id               ,
	fo.code                       ,
	fo.title                      ,
	in2.dir                       ,
	in2.movement_type             ,
	fct.title                     ,
	in2.movement_date             ,
	pc.title                      ,
	in2.bank_account_id           ,
	in2.client_id                 ,
	in2.client_name               ,
	in2.client_name_2             ,
	in2.client_tx_id              ,
	in2.discounts                 ,
	in2.additions                 ,
	in2.total_amount_liquid       ,
	ini.description
from invoice_notes in2
left join invoice_series is2 on (is2.id = in2.invoice_serie_id)
left join financial_operations fo on (fo.id = in2.financial_operation_id)
left join financial_collection_types fct on (fct.id = in2.financial_collection_type_id)
left join payment_conditions pc on (pc.id = in2.payment_condition_id)
left join invoice_note_items ini on (ini.invoice_note_id = in2.id)
) TO '/tmp/synsuit-notasfiscais.csv' DELIMITER '|' csv;


-- cp /tmp/synsuit-* .
-- sed -i "s/\\\N//g" *.csv
-- for i in $(ls *.csv); do iconv -f iso8859-1 -t utf-8 $i > $i.utf8;  done 