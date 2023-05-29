import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/Conv-contatos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj= row[3]
        cliente= admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
        print(cliente)
        
        try: 
            celular01=row[1].split('#-#')[1]
        except Exception as e:
            print(e)
            continue
        if(celular01!=''):
            try:
                new_contato_celular= admmodels.Contato()
                new_contato_celular.tipo = 'CELULAR_PESSOAL'
                new_contato_celular.contato = re.sub('[^0-9]','',celular01)
                new_contato_celular.save()
                new_ccontato_celular = admmodels.ClienteContato()
                new_ccontato_celular.cliente = cliente[0]
                new_ccontato_celular.contato = new_contato_celular
                new_ccontato_celular.save()
                print(new_contato_celular)
            except Exception as e:
                print(e, 'Erro ao cadastrar celular01')
 
        try: 
            celular02=row[1].split('#-#')[2]
        except Exception as e:
            print(e)
            continue


        if(celular02!=''):
            try:
                new_contato_celular= admmodels.Contato()
                new_contato_celular.tipo = 'CELULAR_PESSOAL'
                new_contato_celular.contato = re.sub('[^0-9]','',celular02)
                new_contato_celular.save()
                new_ccontato_celular = admmodels.ClienteContato()
                new_ccontato_celular.cliente = cliente[0]
                new_ccontato_celular.contato = new_contato_celular
                new_ccontato_celular.save()
                print(new_contato_celular)
            except Exception as e:
                print(e,'Erro ao cadastrar celular 02')

       
        try:
            celular03=row[1].split('#-#')[3]
        except Exception as e:
            print(e)
            continue

        if(celular03!=''):
            try:
                new_contato_celular= admmodels.Contato()
                new_contato_celular.tipo = 'CELULAR_PESSOAL'
                new_contato_celular.contato = re.sub('[^0-9]','',celular03)
                new_contato_celular.save()
                new_ccontato_celular = admmodels.ClienteContato()
                new_ccontato_celular.cliente = cliente[0]
                new_ccontato_celular.contato = new_contato_celular
                new_ccontato_celular.save()
                print(new_contato_celular)
            except Exception as e:
                print(e,'Erro ao cadastrar celular 03')

















##########EMAIL##############

import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/Conv-contatos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj= row[3]
        cliente= admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
        print(cliente)

        try:
            email=row[2].split('#-#')[1]
        except Exception as e:
            print(e)
            continue

        if row[2]!='':
            try:
                new_contato_email= admmodels.Contato()
                new_contato_email.tipo = 'EMAIL'
                new_contato_email.contato = email
                new_contato_email.save()
                new_ccontato_email = admmodels.ClienteContato()
                new_ccontato_email.cliente = cliente[0]
                new_ccontato_email.contato = new_contato_email
                new_ccontato_email.save()
                print(new_contato_email)
            except Exception as e:
                print(e, 'Erro ao cadastrar email')