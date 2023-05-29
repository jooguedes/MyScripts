select 
id,
nome,
cpf,
rg,
endereco,
numero,
bairro,
cidade,
estado,
cep,
login,
senha,
mac,
celular,
celular2,
telefone,
plano,
complemento,
coordenadas,
nascimento,
cadastro,
vencimento,
ip,
bloqueado,
ativo,
cancelado,
desativado,
observacao,
ativoem 
from CLIENTES INTO OUTFILE '/tmp/meuconsultor-clientes.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';

select 
id, 
pagamento as data_pagamento,
valor,
vencimento,
nossonum,
pago as valor_pago,
observacao,
login as login_cliente,
desconto,
acrescimo as juros,
charge_id as id_transacao,
carnet_id,
pdf as url_notificacao,
processamento as data_emissao
from financeiro INTO OUTFILE '/tmp/meuconsultor-titulos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';



select
id,
nome,
descricao,
valor_total,
upload,
download
from planos INTO OUTFILE '/tmp/meuconsultor-planos.csv' FIELDS TERMINATED BY '|' OPTIONALLY ENCLOSED BY '"' LINES TERMINATED BY '\n';





select fn.id, fn.charge_id from financeiro fn inner join CLIENTES c on (fn.login=c.login);