from apps.financeiro import models as fmodels
from apps.admcore import models as admodels
import csv


from apps.admcore import models as admmodels
from django.db.models import Q, Max
with open('/tmp/ixc-clientes-desativados-portadores.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            fmodels.Cobranca.objects.filter(cliente__id=row[0]).update(portador=row[2])
        except Exception as e:
            print(e)