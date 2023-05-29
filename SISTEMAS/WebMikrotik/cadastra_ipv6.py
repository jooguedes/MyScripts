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
with open('/tmp/Ipv6-relatorio.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[10]
        admmodels.ServicoInternet.objects.filter(login=login).update(ipv6pd=row[13])