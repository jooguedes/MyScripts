from apps.admcore import models
from apps.financeiro import models as fmodels
from decimal import Decimal

ID_PORTADOR=6




clientes= models.ClienteContrato.objects.filter(cliente__cobranca__portador=ID_PORTADOR, clientecontratostatus__status__in=[2,3])


for c in clientes:
    print c
    try:
        plano=fmodels.Cobranca.objects.filter(cliente__clientecontrato__id=c.id).update(desconto_venc=0.00)
    except Exception as e:
        print(e)
        
    print(plano)