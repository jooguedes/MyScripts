from datetime import datetime
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from django.db.models import Q
import csv
import re
import sys

fnum = lambda n: re.sub('[^0-9.]','',n) 
ustrl = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='sgp')
with open('/tmp/synsuit-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=ustrl(row[26])
        id_contrato = int(row[47])

        clientecontrato=None
        if admmodels.ClienteContrato.objects.filter(id=id_contrato).count() > 0:
            clientecontrato = admmodels.ClienteContrato.objects.filter(id=id_contrato)[0]
        else:
            continue

        if clientecontrato != None:
            status =int(row[53].strip())
            #status_bloqueado = row[42]

            if(status):
                status_cc = 1
                status_s = 1
                status_c = 1
                if status == 3:
                    isento = 100

                if status in [7, 6]:
                    status_cc = 4
                    status_s = 4
                    status_c = 4

                if status in [4, 9]:
                    status_cc = 3
                    status_s = 3
                    status_c = 3


            for ic in [6,2,status_cc]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = clientecontrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario
                    new_status.data_cadastro = datetime.now()
                    new_status.save()

                    new_status.data_cadastro = datetime.now()
                    new_status.save()


from apps.admcore import models 
import copy

#Caso deseje fazer em um contrato apenas, 
#Substitua -> for c in models.ClienteContrato.objects.all(): na linha 10
#Para      -> for c in models.ClienteContrato.objects.filter(id=IDCONTRATO): 
#E depois descomente a linha 8, informando o id do contrato no lugar de 1
#IDCONTRATO = 1

for c in models.ClienteContrato.objects.all():
    servicos = []
    for s in c.servicointernet_set.all():
        servicos.append(s)
    for s in c.servicotv_set.all():
        servicos.append(s)
    for s in c.servicomultimidia_set.all():
        servicos.append(s)
	for s in c.servicotelefonia_set.all():
		servicos.append(s)
    if len(servicos) > 1:
        for s in servicos[1:]:
            try:
                print s
                new_endereco = copy.copy(c.cobranca.endereco)
                new_endereco.id = None 
                new_endereco.save()
                new_cobranca = copy.copy(c.cobranca)
                new_cobranca.id = None
                new_cobranca.endereco = new_endereco
                new_cobranca.save() 
                new_contrato = copy.copy(c)
                status = new_contrato.status.status
                usuario = new_contrato.status.usuario
                data_cadastro = new_contrato.status.data_cadastro
                new_contrato.id = None
                new_contrato.status = None 
                new_contrato.cobranca = new_cobranca
                new_contrato.save()
                for ic in [6,2,status]:
                    new_status = models.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario 
                    new_status.data_cadastro = data_cadastro 
                    new_status.save()             
                    new_status.data_cadastro = data_cadastro 
                    new_status.save() 
                s.clientecontrato=new_contrato
                s.save()
                print s
            except Exception as e:
                print (e)