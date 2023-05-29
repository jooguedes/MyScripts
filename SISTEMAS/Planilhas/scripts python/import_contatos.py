import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/Conv-CSV_IMPORTACAO SGP_BLUENET.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj= row[2]
        cliente= admmodels.Cliente.objects.filter(pessoa_cpfcnpj__numfilter=cpfcnpj)
        print(cliente)

        try: 
            celular01=row[8]
        except Exception as e:
            print(e)
            continue

        if(celular01!=''):
            new_contato_celular= admmodels.Contato()
            new_contato_celular.tipo = 'CELULAR_PESSOAL'
            new_contato_celular.contato = re.sub('[^0-9]','',celular01)
            new_contato_celular.save()
            new_ccontato_celular = admmodels.ClienteContato()
            new_ccontato_celular.cliente = cliente[0]
            new_ccontato_celular.contato = new_contato_celular
            new_ccontato_celular.save()
            print(new_ccontato_celular)
