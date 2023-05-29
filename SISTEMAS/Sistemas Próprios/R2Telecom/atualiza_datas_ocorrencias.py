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
            data_abertura=row[3]
            ocorrencia=amodels.Ocorrencia.objects.filter(numero=row[2])
            print('atualizando ocorrência ', ocorrencia)
            amodels.Ocorrencia.objects.filter(numero=row[2]).update(data_cadastro=data_abertura)
        except Exception as e:
            print(e)