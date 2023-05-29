import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/Conv-CSV_IMPORTACAO SGP_BLUENET.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj=row[2]
        valor=row[19].replace('R$', '').replace(',','.')
        admmodels.Plano.objects.filter(descricao__iexact=row[18]).update(preco=valor)