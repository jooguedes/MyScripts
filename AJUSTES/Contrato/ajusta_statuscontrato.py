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
with open('/tmp/quazar-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=ustrl(row[26])

        clientecontrato=None
        if admmodels.ClienteContrato.objects.filter(servicointernet__login__lower=login).count() >0:
            clientecontrato = admmodels.ClienteContrato.objects.filter(servicointernet__login__lower=login)[0]
        else:
            continue

        if clientecontrato != None:
            status =int(row[36].strip())
            #status_bloqueado = row[42]

            if(status):
                if(status==1):
                    status_cc = 1
                    status_s = 1
                    status_c = 1

                if (status ==2 or status==3):
                    status_cc = 4
                    status_s = 4
                    status_c = 4

                if (status ==4 or status==5):
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