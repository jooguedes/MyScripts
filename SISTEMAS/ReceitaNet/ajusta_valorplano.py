import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/Conv-mensalidades.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        admmodels.Plano.objects.filter(descricao__iexact=row[1]).update(preco=row[3])