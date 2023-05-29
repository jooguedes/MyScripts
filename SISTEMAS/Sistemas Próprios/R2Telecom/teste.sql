select fc.id as id_cobranca, fc.cobranca_unificada_id as id_cobranca_unificada,
ac.id as id_cliente,
acc.id as id_contrato,
a_s.id as id_servicointernet
from financeiro_cobranca fc 
inner join admcore_cliente ac on (fc.cliente_id=ac.id)
inner join admcore_clientecontrato acc on (acc.cliente_id=ac.id)
inner join admcore_servicointernet a_s on (a_s.clientecontrato_id=acc.id)
where ac.id=2837;


select fc.id as id_cobranca, fc.cobranca_unificada_id as id_cobranca_unificada,
ac.id as id_cliente,
acc.id as id_contrato,
a_s.id as id_servicointernet
from financeiro_cobranca fc 
inner join admcore_cliente ac on (fc.cliente_id=ac.id)
inner join admcore_clientecontrato acc on (acc.cliente_id=ac.id)
inner join admcore_servicointernet a_s on (a_s.clientecontrato_id=acc.id)
where fc.id=23861;