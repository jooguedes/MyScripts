from apps.financeiro import models as fmodels
from apps.admcore import models as admodels
import csv


from apps.admcore import models as admmodels
from django.db.models import Q, Max
with open('/tmp/CPOP-Presidente-prudente.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            id=int(row[0])+10000
            admodels.ClienteContrato.objects.filter(cliente__id=id, pop=1).update(pop=5)
        except Exception as e:
            print(e)
    





##############TESTE##############
from apps.financeiro import models as fmodels
from apps.admcore import models as admodels
import csv


from apps.admcore import models as admmodels
from django.db.models import Q, Max
with open('/tmp/ixc-clientes-filial-12-com-nomes.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            id=row[0]
            admodels.ClienteContrato.objects.filter(cliente__id=id, pop=11).update(pop=12)
        except Exception as e:
            print(e)
    




### SEPARA POR FILIAL######
from apps.financeiro import models as fmodels
from apps.admcore import models as admodels
import csv


from apps.admcore import models as admmodels
from django.db.models import Q, Max
with open('/tmp/ixc-clientes-filial.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:

            id_contrato=row[1]
            if row[2]=='1':
                admmodels.ClienteContrato.objects.filter(id=id_contrato).update(pop=2)
            elif row[2]=='2':
                admmodels.ClienteContrato.objects.filter(id=id_contrato).update(pop=3)
            elif row[2]=='3':
                admmodels.ClienteContrato.objects.filter(id=id_contrato).update(pop=4)

        except Exception as e:
            print(e)
    