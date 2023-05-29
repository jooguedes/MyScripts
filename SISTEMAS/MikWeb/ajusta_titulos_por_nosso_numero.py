from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from django.db.models import Q
import csv
import re
import sys
from unicodedata import normalize
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=1)
fnum = lambda n: re.sub('[^0-9.]','',n) 
with open('/tmp/Cobrancas-Total-Mikiweb.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            nosso_numero=row[0]
            nome=normalize('NFKD', unicode(row[1].strip().lower())).encode('ASCII', 'ignore').decode('ascii')
            cliente=admmodels.Cliente.objects.filter(pessoa__nome__unaccent__lower__iexact=nome)
            fmodels.Titulo.objects.filter(nosso_numero=nosso_numero).update(cliente=cliente[0].id)
        except Exception as e:
            print(e)