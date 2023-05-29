import csv
from logging import exception
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max

with open('/tmp/Conv-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            id= int(row[0]) + 140
            cliente= admmodels.Cliente.objects.filter(clientecontrato__clieente_id=id)
            
            if(row[14]!=''):
                new_contato_celular= admmodels.Contato()
                new_contato_celular.tipo = 'EMAIL'
                new_contato_celular.contato = row[14]
                new_contato_celular.save()
                new_ccontato_celular = admmodels.ClienteContato()
                new_ccontato_celular.cliente = cliente[0]
                new_ccontato_celular.contato = new_contato_celular
                new_ccontato_celular.save()

            if(row[15]!=''):
                new_contato_celular= admmodels.Contato()
                new_contato_celular.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                new_contato_celular.contato = row[15]
                new_contato_celular.save()
                new_ccontato_celular = admmodels.ClienteContato()
                new_ccontato_celular.cliente = cliente[0]
                new_ccontato_celular.contato = new_contato_celular
                new_ccontato_celular.save()

            if(row[16]!=''):
                new_contato_celular= admmodels.Contato()
                new_contato_celular.tipo = 'CELULAR_PESSOAL'
                new_contato_celular.contato = row[16]
                new_contato_celular.save()
                new_ccontato_celular = admmodels.ClienteContato()
                new_ccontato_celular.cliente = cliente[0]
                new_ccontato_celular.contato = new_contato_celular
                new_ccontato_celular.save()

        except Exception as e:
            print(e)