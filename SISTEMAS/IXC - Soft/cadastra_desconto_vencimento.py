from apps.financeiro import models as fmodels
from apps.admcore import models as admodels
import csv


from apps.admcore import models as admmodels
from django.db.models import Q, Max
with open('/tmp/Conv-Clientes-com-desconto-vencimento.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        idcontrato=row[2]
        try:

            print(fmodels.Cobranca.objects.filter(cliente__clientecontrato__cobranca=idcontrato, cliente__clientecontrato__clientecontratostatus__status=1).update(desconto_venc=15.00))
        except Exception as e:
            print(e)