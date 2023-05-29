import csv
import re 
from apps.financeiro import models as fmodels
from django.db.models import Q, Max

with open('/tmp/Conv-CSV_IMPORTACAO SGP_BLUENET.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[21]
        if row[19]=='ISENTO':
            fmodels.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__login__iexact=login).update(isento=100)
            