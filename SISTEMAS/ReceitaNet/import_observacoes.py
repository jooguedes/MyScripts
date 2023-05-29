import csv
import re 
from apps.admcore import models as admmodels

with open('/tmp/Conv-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=row[0]).update(observacao=row[33])