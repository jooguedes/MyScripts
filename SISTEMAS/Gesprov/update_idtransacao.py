
from apps.financeiro import models
import csv
with open('/tmp/gesprov-titulos-corrigir-portador-03.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            numero_documento=row[0]
            tgway = models.TituloGateway.objects.filter(gateway_id=1, titulo__portador=3, titulo__numero_documento=numero_documento, titulo__usuario_g__username='sgp').update(idtransacao=row[24])
            print tgway