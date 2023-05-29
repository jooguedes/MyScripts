from datetime import datetime
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from django.db.models import Q
import csv
import re
import sys

fnum = lambda n: re.sub('[^0-9.]','',n) 
ustrl = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='sgp')
with open('/tmp/mkauth-clientes-desativados.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        pop=2
        login=ustrl(row[1])

        clientecontrato=None
        if admmodels.ClienteContrato.objects.filter(servicointernet__login='%s.mkauth' %login, pop=pop).count() >0:
            clientecontrato = admmodels.ClienteContrato.objects.filter(servicointernet__login='%s.mkauth' %login, pop=pop)[0]
            
        elif admmodels.ClienteContrato.objects.filter(servicointernet__login='%s@mkauth' %login, pop=pop).count() >0:
            clientecontrato = admmodels.ClienteContrato.objects.filter(servicointernet__login='%s@mkauth' %login, pop=pop)[0]
        else:
            clientecontrato = admmodels.ClienteContrato.objects.filter(servicointernet__login=login, pop=pop)[0]



        if clientecontrato != None:
            status = ustrl(row[41])
            status_bloqueado = ustrl(row[42])

            if status in  ['Sim','sim','s']:
                status_cc = 1
                status_s = 1
                status_c = 1

                if status_bloqueado in ['Sim','sim']:
                    status_cc = 4
                    status_s = 4
                    status_c = 4

            if status in ['Não','Nao','nao','não','n']:
                status_cc = 3
                status_s = 3
                status_c = 3


            for ic in [6,2,status_cc]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = clientecontrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario
                    new_status.data_cadastro = datetime.now()
                    new_status.save()

                    new_status.data_cadastro = datetime.now()
                    new_status.save()