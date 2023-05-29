from apps.financeiro import models
from datetime import timedelta
from django.db import transaction

##########################################################
EXECUTAR = False
PLANOS_ID = [1, 2, 5]
VALOR_DESCONTO = 10.00
##########################################################

with transaction.atomic():
    titulos = models.Titulo.objects \
        .filter(status=models.MOVIMENTACAO_GERADA,
                cobranca__clientecontrato__servicointernet__planointernet__id__in=PLANOS_ID)
        
    for t in titulos:
        print(t)
        t.desconto_venc = VALOR_DESCONTO
        if EXECUTAR:
            try:
                t.save()
            except Exception as e:
                pritn(e)



