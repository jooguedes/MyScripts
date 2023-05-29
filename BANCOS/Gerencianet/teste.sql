COPY ( select 
DISTINCT cc.id as ID_cliente,
p.nome,
p.cpfcnpj, 
e.logradouro, 
e.bairro, e.numero, 
e.cidade, e.uf, c.contato 
from admcore_cliente cc
inner join admcore_pessoa p on (cc.pessoa_id=p.id) 
inner join admcore_endereco e on (cc.id=e.id) 
inner join admcore_clientecontato clc on (cc.id=clc.cliente_id)
inner join admcore_contato c on (clc.contato_id=c.id)
where cc.id not in (select cliente_id from admcore_clientecontrato) )TO '/tmp/RELATORIO-CLIENTES-SEM-CONTRATO.csv' DELIMITER '|' CSV HEADER;