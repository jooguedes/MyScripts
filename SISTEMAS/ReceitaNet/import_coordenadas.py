import csv
from apps.admcore import models as admmodels

with open('/tmp/Conv-clientes-coordenadas-livnet.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        coordenadas=str(row[27])+',' + str(row[28])

        print(row)
        print(admmodels.Endereco.objects.filter(servicointernet__login__iexact=row[0], servicointernet__clientecontrato__pop=113).update(map_ll=coordenadas))
        print(admmodels.Endereco.objects.filter(cobranca__clientecontrato__servicointernet__login__iexact=row[0], servicointernet__clientecontrato__pop=113).update(map_ll=coordenadas))
