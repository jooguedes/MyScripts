from apps.admcore import models
from django.db.models import F
import csv
with open('/tmp/topsapp-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        idCliente=row[0]
        idServico=row[58]
        if not idServico or idServico=='':
            idServico=int(idCliente)+20000
        
        status=row[42]
        if status=='bloqueado':
            models.ClienteContratoStatus.objects.filter(clientecontrato__cliente__id=idCliente, clientecontrato=idServico).update(status=4)