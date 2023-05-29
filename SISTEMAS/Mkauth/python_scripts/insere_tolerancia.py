import csv
from apps.financeiro import models
with open('/tmp/mkauth-clientes-atvados-dias_cortes.csv.utf8', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
                models.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__login=row[0].strip()).update(tolerancia=row[1])