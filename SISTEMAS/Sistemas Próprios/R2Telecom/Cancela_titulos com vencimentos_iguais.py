from apps.financeiro import models as fmodels
from apps.admcore import models


clientes= models.ClienteContrato.objects.all()

for c in clientes:
    print('Cliente', c)
    titulos_abertos=fmodels.Titulo.objects.filter(cliente__clientecontrato__id=c.id, usuario_g__username='sgp', status=fmodels.MOVIMENTACAO_GERADA)
    titulos_pagos=fmodels.Titulo.objects.filter(cliente__clientecontrato__id=c.id, usuario_b__username='sgp', status=fmodels.MOVIMENTACAO_PAGA)
    for t in titulos_abertos:
        for tf in titulos_pagos:
            if (str(t.data_vencimento).split('-')[0]==str(tf.data_vencimento).split('-')[0] and str(t.data_vencimento).split('-')[1]==str(tf.data_vencimento).split('-')[1]):
                print('#################################################')
                print('###')
                print('###', ' Esse é meu titulo pago', tf, 'esse é o id do titulo:',tf.id, tf.numero_documento, ' ####')
                print('###', ' Esse é meu titulo aberto', t, t.id, t.numero_documento, ' ####')
                print('###')
                print('#################################################')
                print('esse é o id do titulo: ',tf.id)
                print('esse é o vencimento: ', str(tf.data_vencimento))
                data=tf.data_vencimento
                fmodels.Titulo.objects.filter(id=tf.id).update(status=fmodels.MOVIMENTACAO_CANCELADA, data_cancela=data)
            else:
                #print('esse titulo não bateu', tf)
                pass

from apps.financeiro import models
titulo=models.Titulo.objects.filter(numero_documento=54540, cliente__clientecontrato__id=1744, status=models.MOVIMENTACAO_CANCELADA)
for t in titulo:
    print(t, t.status)
    datapagamento=t.data_vencimento
    valor=t.valor
    models.Titulo.objects.filter(id=t.id).update(status=models.MOVIMENTACAO_PAGA, data_pagamento=datapagamento, valorpago=valor)