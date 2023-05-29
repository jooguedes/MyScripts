import csv
import re


#python import_gnet.py --settings=sgp.gnet.settings --portador=1 --arquivo=Conv-Gnet-Cobrancas.csv

from django.conf import settings
from django.db.models import Q, Max
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')



with open('/tmp/Conv-18972-GERENCIAMENTO-DE-CLIENTES-2022-11-01.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj=row[8]
        email=row[6]
        if row[6]!='':
            admmodels.Contato.objects.filter(clientecontato__cliente__pessoa__cpfcnpj__numfilter=cpfcnpj, tipo='EMAIL').update(contato=email)
