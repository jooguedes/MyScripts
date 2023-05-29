import csv
import sys
if sys.version_info < (3,0): 
	reload(sys)
	sys.setdefaultencoding('utf-8')
from apps.admcore import models 
with open('/opt/clientes-obs.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter=';', quotechar='"')
    for row in conteudo:
        cliente = models.Cliente.objects.filter(pk=row[0])
        if cliente:
            cli = cliente[0]
            cli.observacao=row[1]
            cli.save()
            print cliente[0],row[1]