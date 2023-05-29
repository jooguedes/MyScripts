from apps.financeiro import models

DATA_VENCIMENTO_INICIAL='01-12-2023'
DATA_VENCIMENTO_FINAL='06-12-2023'
for t in models.Titulo.objects.filter(portador_id__in=[3,4], data_vencimento__date__gte=DATA_VENCIMENTO_INICIAL, data_vencimento__date__lte=DATA_VENCIMENTO_FINAL):
    try:
        t.updateDadosFormatados()
        print t
    except Exception as e:
        print(e)