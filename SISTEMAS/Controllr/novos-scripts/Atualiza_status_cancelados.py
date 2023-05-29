from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import sys

with open('/tmp/Conv-Autenticacao-Lista-desativados.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[2]
        admmodels.ClienteContratoStatus.objects.filter(clientecontrato__servicointernet__login=login).update(status=3)