from apps.financeiro import models
titulo=models.Titulo.objects.filter(status=models.MOVIMENTACAO_CANCELADA)

for t in titulo:
    try:
        obeservacao=t.observacao.split(':')[1]
    except Exception as e:
        print(e)
        continue
    if obeservacao=='221111152901':
        try:
            print(t, t.observacao)
            models.Titulo.objects.filter(id=t.id).update(status=models.MOVIMENTACAO_GERADA, data_cancela=None, usuario_c=None)
        
        except Exception as e:
            print(e)