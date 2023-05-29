from apps.admcore import models as admmodels
import csv
with open('/tmp/Conv-clientes-beesweb-inovamais.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            if row[20]!='':
                try:
                    coordenadas=row[20]
                    print(admmodels.Endereco.objects.filter(servicointernet__login=row[24], servicointernet__clientecontrato__pop=107).update(map_ll=coordenadas))
                    print(admmodels.Endereco.objects.filter(cobranca__clientecontrato__servicointernet__login=row[24], cobranca__clientecontrato__pop=107).update(map_ll=coordenadas))
                except Exception as e:
                    print(e)


