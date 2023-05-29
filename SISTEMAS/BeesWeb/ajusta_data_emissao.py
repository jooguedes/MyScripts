from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from django.db.models import Q
import csv
import re
import sys
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=3)
fnum = lambda n: re.sub('[^0-9.]','',n) 
#portador.titulo_set.all().delete()
with open('/tmp/Conv-cobrancas-beesweb.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        numero_documento = row[0]
        d,m,y = row[15].split('/')
        data_documento = '%s-%s-%s' %(y,m,d)
        fmodels.Titulo.objects.filter(numero_documento=numero_documento).update(data_documento=data_documento)