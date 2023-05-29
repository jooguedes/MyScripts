import csv
import re

from django.conf import settings
from django.db.models import Q, Max
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')


with open('/tmp/Ajusta_planos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
       try:
            planointernet=admmodels.PlanoInternet.objects.filter(plano__descricao__lower__iexact=row[7].lower())
            print(planointernet)
            admmodels.ServicoInternet.objects.filter(login=row[3]).update(planointernet=planointernet[0])
       except Exception as e:
            print(e)
            continue
            
