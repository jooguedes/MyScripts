import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/mkauth-clientes-ativados3.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        admmodels.Endereco.objects.filter(servicointernet__login=row[1]).update(pontoreferencia=row[60])
        admmodels.Endereco.objects.filter(cobranca__cliente__clientecontrato__servicointernet__login=row[1]).update(pontoreferencia=row[60])
        admmodels.Endereco.objects.filter(cliente__clientecontrato__servicointernet__login=row[1]).update(pontoreferencia=row[60])