import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))
with open('/tmp/Conv-Clientes.csv ', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            login= row[13]
            cliente= admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login)
            
            
            if(row[18]!=''):
                if ';'in str(row[18]):
                    emails=str(row[18]).split(";")
                    print(emails)
                    if len(emails[1]):
                    
                        try:
                            if emails[0]:
                                new_contato_celular= admmodels.Contato()
                                new_contato_celular.tipo = 'EMAIL'
                                new_contato_celular.contato = emails[0]
                                new_contato_celular.save()
                                new_ccontato_celular = admmodels.ClienteContato()
                                new_ccontato_celular.cliente = cliente[0]
                                new_ccontato_celular.contato = new_contato_celular
                                new_ccontato_celular.save()
                            if emails[1]:
                                new_contato_celular= admmodels.Contato()
                                new_contato_celular.tipo = 'EMAIL'
                                new_contato_celular.contato = emails[1]
                                new_contato_celular.save()
                                new_ccontato_celular = admmodels.ClienteContato()
                                new_ccontato_celular.cliente = cliente[0]
                                new_ccontato_celular.contato = new_contato_celular
                                new_ccontato_celular.save()
                        except Exception as e:
                                print(e)
                                pass

                else:
                    new_contato_celular= admmodels.Contato()
                    new_contato_celular.tipo = 'EMAIL'
                    new_contato_celular.contato = row[18]
                    new_contato_celular.save()
                    new_ccontato_celular = admmodels.ClienteContato()
                    new_ccontato_celular.cliente = cliente[0]
                    new_ccontato_celular.contato = new_contato_celular
                    new_ccontato_celular.save()
        except Exception as e:
            print(e)
            continue    


import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))
with open('/tmp/Conv-Clientes.csv ', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            login= row[13]
            cliente= admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login)

            if(row[19]!=''):
                if '||'in str(row[19]):
                    telefones=str(row[19]).split("||")
                    print(telefones)
                    
                    if len(telefones[1]):
                        if telefones[0]:
                            new_contato_celular= admmodels.Contato()
                            new_contato_celular.tipo = 'CELULAR_PESSOAL'
                            new_contato_celular.contato = telefones[0]
                            new_contato_celular.save()
                            new_ccontato_celular = admmodels.ClienteContato()
                            new_ccontato_celular.cliente = cliente[0]
                            new_ccontato_celular.contato = new_contato_celular
                            new_ccontato_celular.save()
                        if telefones[1]:
                            new_contato_celular= admmodels.Contato()
                            new_contato_celular.tipo = 'CELULAR_PESSOAL'
                            new_contato_celular.contato = telefones[1]
                            new_contato_celular.save()
                            new_ccontato_celular = admmodels.ClienteContato()
                            new_ccontato_celular.cliente = cliente[0]
                            new_ccontato_celular.contato = new_contato_celular
                            new_ccontato_celular.save()
                        if telefones[2]:
                            new_contato_celular= admmodels.Contato()
                            new_contato_celular.tipo = 'CELULAR_PESSOAL'
                            new_contato_celular.contato = telefones[2]
                            new_contato_celular.save()
                            new_ccontato_celular = admmodels.ClienteContato()
                            new_ccontato_celular.cliente = cliente[0]
                            new_ccontato_celular.contato = new_contato_celular
                            new_ccontato_celular.save()
                else:
                    new_contato_celular= admmodels.Contato()
                    new_contato_celular.tipo = 'CELULAR_PESSOAL'
                    new_contato_celular.contato = row[19]
                    new_contato_celular.save()
                    new_ccontato_celular = admmodels.ClienteContato()
                    new_ccontato_celular.cliente = cliente[0]
                    new_ccontato_celular.contato = new_contato_celular
                    new_ccontato_celular.save()
        except Exception as e:
            print(e)
            continue