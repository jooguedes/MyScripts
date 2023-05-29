import csv
from apps.admcore import models as admmodels
with open('/tmp/mkauth-clientes-desativados.csv.utf8', 'rU') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=str(row[1]).lower().strip()

        bairro=row[52]

        print('Atualizando o logradouro: ', logradouro,   ' do login: ', login)
        try:
            admmodels.Endereco.objects.filter(cobranca__cliente__clientecontrato__servicointernet__login=login).update(bairro=bairro)
        
            admmodels.Endereco.objects.filter(servicointernet__login=login).update(bairro=bairro)

            admmodels.Endereco.objects.filter(cliente__clientecontrato__servicointernet__login=login).update(bairro=bairro)
        except Exception as e:
            print(e)


###################################### BEESWEB #################################################################
from apps.admcore import models as admmodels
import csv

with open('/tmp/beesweb-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=str(row[24]).lower().strip()

        map_ll=row[20]
        print(login, map_ll)

        print('Atualizando o Coordenadas: ', map_ll,   ' do login: ', login)
        try:
            admmodels.Endereco.objects.filter(cobranca__cliente__clientecontrato__servicointernet__login=login).update(map_ll=map_ll)
        
            admmodels.Endereco.objects.filter(servicointernet__login=login).update(map_ll=map_ll)

            admmodels.Endereco.objects.filter(cliente__clientecontrato__servicointernet__login=login).update(map_ll=map_ll)
        except Exception as e:
            print(e)