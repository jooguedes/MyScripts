import csv
import re
from django.db.models import Q, Max
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]','',n)
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-planos_para_aplicar_desconto.csv', 'rU') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            plano=admmodels.Plano.objects.filter(descricacao__iexact=row[1])[0]
            for p in plano:
                admmodels.Plano.objects.filter(id=p.id).update(desconto_venc=10)
        except Exception as e:
            print(e)