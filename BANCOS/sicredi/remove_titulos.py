
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

import csv

with open('/tmp/Titulos-sicredi-subir.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        nosso_numero = row[4].split('-')[0].replace('/', '')
        cpfcnpj = row[147]
        fmodels.Titulo.objects.filter(nosso_numero=nosso_numero, portador=1, cliente__pessoa__cpfcnpj__numfilter=cpfcnpj).delete()
        
           