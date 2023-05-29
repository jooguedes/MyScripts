from apps.admcore import models as models
from django.db.models import Q
from apps.cauth.models import User
from django.db import transaction
import csv
import re
sgpuser = User.objects.get(username='sgp')
with open('/tmp/Conv-CLIENTE_BLOQUEADOS.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[2]
        contratos=models.ClienteContrato.objects.filter(servicointernet__login=login)

        with transaction.atomic():    
            for cc in contratos:
                print (cc)
                
                status = models.ClienteContratoStatus.objects.create(cliente_contrato=cc, status=4, usuario=sgpuser, modo=models.CONTRATO_STATUS_MODO_MANUAL, observacao="Cancelado para correção da importação mediante protocolo: 230207124302")
                cc.status = status
                cc.save()
                    
                for s in cc.servicointernet_set.all():
                    s.status = models.SERVICO_CANCELADO
                    s.save()


#ISENTA
from apps.admcore import models as models
from django.db.models import Q
from apps.cauth.models import User
from apps.financeiro import models as fmodels
from django.db import transaction
import csv

with open('/tmp/Conv-CLIENTE_-_CANCELADOS.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[2]
        contratos=fmodels.Cobranca.objects.filter(cleinte__clientecontrato__servicointernet__login=login).update(isento=100)


#ALTERAÇÃO STATUS
from apps.admcore import models as models
from django.db.models import Q
from apps.cauth.models import User
from django.db import transaction
import csv
import re
sgpuser = User.objects.get(username='sgp')
with open('/tmp/Conv-CLIENTE_BLOQUEADOS.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[2]
        models.ClienteContratoStatus.objects.filter(clientecontrato__servicointernet__login=login).update(status=4)
