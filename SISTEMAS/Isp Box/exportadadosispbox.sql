select 
    c.id,
    c.nome,
    c.tipo_pessoa,
    c.cpf,
    c.rg,
    c.data_nascimento as nascimento,
    c.cnpj,
    c.cep,
    c.sexo,
    c.endereco as rua,
    c.endereco_numero as numero,
    c.endereco_complemento as complemento,
    c.endereco_bairro as bairro,
    c.endereco_referencia as referencia,
    c.cidade,
    c.uf,
    c.telefone,
    c.celular,
    c.email,
    c.nome_pai,
    c.nome_mae,
    c.data_cadastro as cadastro,
    ci.tipo_conexao as conexao,
    ci.radio_mac as mac,
    ci.pppoe_login as logincliente,
    ci.pppoe_senha as senha,
    it.nome as nome_plano,
    it.velocidade_down as down,
    it.velocidade_up as up,
    it.valor_scm as valor,
    cb.valor_pago as pago,
    cb.data_vencimento as vencimento,
    cb.datagerado as emisao,
    cb.data_cancelado as cancelado,
    cb.data_pagamento as pagamento,
    from clientes c
    INNER JOIN clientes_has_internetplanos ci on (c.id=ci.clientes_id)
    INNER JOIN internetplanos it on (it.id=ci.internetplanos_id)
    INNER JOIN cobrancas cb on(cb.clientes_id=c.id)
    ORDER BY c.id
    INTO OUTFILE '/tmp/ispbox-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
    


select 
    p.id,
    p.nome,
    p.coordenadas,
    p.endereco as rua,
    p.endereco_numero as numero,
    p.endereco_complemento as complemento,
    p.endereco_bairro as bairro,
    p.cidade as cidade
    from pops p
    INTO OUTFILE '/tmp/ispbox-pops.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';
    

select 
    rn.id,
    rn.vendor,
    rn.nasname as ip,
    rn.secret as senha,
    rn.description as descricao
    from radius_nas rn
    INTO OUTFILE '/tmp/ispbox-nas.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';






select 
    c.clientes_id,
    IFNULL(e.estacoes_login,c.clientes_id) as login,
    c.clientes_tipo,
    c.clientes_nome,
    1,
    c.clientes_doc,
    2,
    15,
    c.clientes_rg,
    '' as profissao,
    '' as sexo,
    c.clientes_datanascimento,
    '' as fantasia,
    '' as contato,
    c.clientes_endereco,
    c.clientes_numero,
    '' as complemento,
    c.clientes_bairro,
    c.clientes_cep,
    uf.estados_sigla,
    cid.cidades_nome,
    c.clientes_telefonemovel,
    c.clientes_telefonefixo,
    c.clientes_email,
    e.estacoes_obs,
    c.clientes_criadoem,
    c.clientes_criadoem,
    '' as servidor,
    p.planos_nome,
    p.planos_valor,
    '' as tipoconexao,
    e.estacoes_ip,
    e.estacoes_ip,
    e.estacoes_mac,
    c.clientes_vencimento,
    e.estacoes_desconto,
    e.estacoes_acrecimo,
        '' as transmissor,
        '' as receptor,
    '1' as comodato,
    e.estacoes_isento,
    case when e.estacoes_status in (0,1) then 's' else 'n' end as status_ativado,
    case when e.estacoes_status = 0 then 's' else 'n' end as status_bloqueado,
    e.estacoes_senha,
    p.planos_download,
    p.planos_upload,
    p.planos_valor,
    '' as conta,
    '' as fone,
    e.estacoes_login
    from clientes c
    INNER JOIN estacoes e ON (e.estacoes_cliente=c.clientes_id)
    INNER JOIN planos p ON (p.planos_id=e.estacoes_plano)
    INNER JOIN cidades cid on (c.clientes_cidade=cid.cidades_id)
    INNER JOIN estados uf on (uf.estados_id=cid.cidades_estado)
    ORDER BY e.estacoes_id desc
    INTO OUTFILE '/tmp/foxisp-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



    select 
    c.clientes_id,
    IFNULL(e.estacoes_login,c.clientes_id) as login,
    c.clientes_tipo,
    c.clientes_nome,
    1,
    c.clientes_doc,
    2,
    15,
    c.clientes_rg,
    '' as profissao,
    '' as sexo,
    c.clientes_datanascimento,
    '' as fantasia,
    '' as contato,
    c.clientes_endereco,
    c.clientes_numero,
    '' as complemento,
    c.clientes_bairro,
    c.clientes_cep,
    uf.estados_sigla,
    cid.cidades_nome,
    c.clientes_telefonemovel,
    c.clientes_telefonefixo,
    c.clientes_email,
    e.estacoes_obs,
    c.clientes_criadoem,
    c.clientes_criadoem,
    '' as servidor,
    p.planos_nome,
    p.planos_valor,
    '' as tipoconexao,
    e.estacoes_ip,
    e.estacoes_ip,
    e.estacoes_mac,
    c.clientes_vencimento,
    e.estacoes_desconto,
    e.estacoes_acrecimo,
        '' as transmissor,
        '' as receptor,
    '1' as comodato,
    e.estacoes_isento,
    case when e.estacoes_status in (0,1) then 's' else 'n' end as status_ativado,
    case when e.estacoes_status = 0 then 's' else 'n' end as status_bloqueado,
    e.estacoes_senha,
    p.planos_download,
    p.planos_upload,
    p.planos_valor,
    '' as conta,
    '' as fone,
    e.estacoes_login
     from clientes c
    LEFT JOIN estacoes e ON (e.estacoes_cliente=c.clientes_id)
    LEFT JOIN planos p ON (p.planos_id=e.estacoes_plano)
    LEFT JOIN cidades cid on (c.clientes_cidade=cid.cidades_id)
    LEFT JOIN estados uf on (uf.estados_id=cid.cidades_estado)
    WHERE cid.cidades_nome is NULL
    ORDER BY e.estacoes_id desc
    INTO OUTFILE '/tmp/foxisp-clientes-semcidade.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select
    1, 
    IFNULL(e.estacoes_login,f.faturas_cliente) as login,
    '' as cpfcnpj,
    f.faturas_formapagamento,
    '' as tipo,
    '' as descricao,
    f.faturas_dataemissao,
    f.faturas_vencimento,
    f.faturas_datapagamento,
    f.faturas_id,
    f.faturas_id,
    f.faturas_valor,
    f.faturas_valorrecebido,
    f.faturas_valor,
    '' as geranfe,
    f.faturas_lote,
    '' as linhadigitavel,
    '' as codigodebarras,
    f.faturas_status,
    f.faturas_valor,
    f.faturas_pago
    from faturas f
    INNER JOIN estacoes e ON (f.faturas_cliente=e.estacoes_cliente)
    WHERE f.faturas_status in (1,2)
    AND f.faturas_banco=1
    INTO OUTFILE '/tmp/foxisp-titulos-1.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


select
    IFNULL(e.estacoes_login,f.faturas_cliente) as login,
    f.faturas_id,
    f.faturas_chave,
    f.faturas_lote,
    f.faturas_link
    from faturas f
    INNER JOIN estacoes e ON (f.faturas_cliente=e.estacoes_cliente)
    WHERE f.faturas_status in (1,2) and f.faturas_chave is not null and f.faturas_lote='' or f.faturas_lote is null
    INTO OUTFILE '/tmp/foxisp-gnet-titulos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select
    IFNULL(e.estacoes_login,f.faturas_cliente) as login,
    f.faturas_id,
    f.faturas_chave,
    f.faturas_lote,
    f.faturas_link
    from faturas f
    INNER JOIN estacoes e ON (f.faturas_cliente=e.estacoes_cliente)
    WHERE f.faturas_status in (1,2) and f.faturas_chave is not null and f.faturas_lote is not null or f.faturas_lote != ''
    INTO OUTFILE '/tmp/foxisp-gnet-carnesx.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';


