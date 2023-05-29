import csv
from apps.admcore import models


with open('/tmp/Conv-Clientes-POP-Corrente_CSV.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    indice = 0
    for row in conteudo:
      cpfcnpj=row[2]
      models.ClienteContrato.objects.filter(pop=12, cliente__pessoa__cpfcnpj__numfilter=cpfcnpj).update(pop=14)








#### ATUALIZA NAS##########

import csv
from apps.admcore import models


with open('/tmp/Conv-Clientes-POP-Riacho-Frio.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    indice = 0
    for row in conteudo:
      cpfcnpj=row[2]
      models.ServicoInternet.objects.filter(clientecontrato__pop=2, clientecontrato__cliente__pessoa__cpfcnpj__numfilter=cpfcnpj).update(nas=2)
