import csv
import re 
from apps.admcore import models
from django.db.models import Q, Max
from apps.cauth.models import User
sgpuser = User.objects.get(username='sgp')
with open('/tmp/Conv-clientes-beesweb-novaimportacao-20-07.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if row[28]=='Desativado':
            try:
                contratos = models.ClienteContrato.objects.filter(pop=15, status__status=models.CONTRATO_ATIVO, servicointernet__login=row[24])[0]
            except Exception as e:
                print(e)
                continue
            status = models.ClienteContratoStatus.objects.create(cliente_contrato=contratos,
                        status=models.CONTRATO_CANCELADO,
                        usuario=sgpuser,
                        modo=models.CONTRATO_STATUS_MODO_MANUAL,
                        observacao="canceladosem lote para correção de impportação")
                        
            contratos.status = status
            contratos.save()
                    
            for s in contratos.servicointernet_set.all():
                s.status = models.SERVICO_CANCELADO
                s.save()
        else:
            print('cliente já está ativo')

    
