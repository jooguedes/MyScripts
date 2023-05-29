import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/cpfs_remover.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
       try:
        contrato=admmodels.ClienteContrato.objects.filter(id__gte=50000, pop=17,cliente__pessoa__cpfcnpj__numfilter=row[0]).delete()
        cliente=admmodels.Cliente.objects.filter(id__gte=50000, clientecontrato__pop=17,pessoa__cpfcnpj__numfilter=row[0]).delete()
        pop= admmodels.Pop.objects.filter(clientecontrato__cliente__id=cliente[0].id)
        print(cliente[0], pop[0], contrato[0])
       except Exception as e:
            continue
            
import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max
cliente=cliente=admmodels.Cliente.objects.filter(id__gte=50000, clientecontrato__isnull=True).delete()
for c in cliente:
    print c