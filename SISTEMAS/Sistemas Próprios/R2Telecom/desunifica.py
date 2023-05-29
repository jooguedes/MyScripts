from shutil import ExecError
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from apps.atendimento import models as amodels
from django.db.models import Q, Max
import csv
metodo = amodels.Metodo.objects.all()[0]
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-exporta_clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
            try:
                id=row[0]
                servico=admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__id=id, servico__tipo=1)
                cobranca_unificada1=fmodels.Cobranca.objects.filter(clientecontrato__servicointernet__id=servico[0].id)
                fmodels.Cobranca.objects.filter(id=cobranca_unificada1[0].id).update(cobranca_unificada=None)
            except Exception as e:
                print(e)