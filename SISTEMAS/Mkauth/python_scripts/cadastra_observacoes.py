import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/mkauth-clientes-ativados.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=row[1]).update(observacao=row[24])