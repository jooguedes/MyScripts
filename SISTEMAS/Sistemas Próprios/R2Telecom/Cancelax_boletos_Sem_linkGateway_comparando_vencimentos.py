from apps.financeiro import models as fmodels
from apps.admcore import models


clientes= models.ClienteContrato.objects.all()

for c in clientes:
    print('Cliente', c)
    titulos_sem_link=fmodels.Titulo.objects.filter(cliente__clientecontrato__id=c.id, usuario_g__username='sgp', status=fmodels.MOVIMENTACAO_GERADA, titulogateway__isnull=True)
    titulos_com_link=fmodels.Titulo.objects.filter(cliente__clientecontrato__id=c.id, usuario_b__username='sgp', status=fmodels.MOVIMENTACAO_GERADA, titulogateway__isnull=False)
    for t in titulos_com_link:
        for tf in titulos_sem_link:
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