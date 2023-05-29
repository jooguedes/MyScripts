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
with open('/tmp/Conv-exporta_chamados.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            contrato=admmodels.ClienteContrato.objects.get(id=row[1])
            codigo_chamado=row[2]
            amodels.Ocorrencia.objects.filter(numero=codigo_chamado).update(clientecontrato=contrato.id)
        except Exception as e:
            print(e)