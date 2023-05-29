import copy
from hashlib import new
from pyexpat import model
from apps.admcore import models
from apps.financeiro import models as fmodels
import csv
from django.db import DatabaseError, transaction

with open('/tmp/Conv-Clientes-2022-ativos.csv', 'rb') as csvfile:
    conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
    for row in conteudo:


        adicionais= row[8].split('-')
        try:
            if adicionais[1]:
                for ad in adicionais:
                    login_principal=row[6]

                    if models.ServicoInternet.objects.filter(login=ad).count()==0:
                        servico=models.ServicoInternet.objects.get(login=login_principal)
                        contrato=models.ClienteContrato.objects.get(servicointernet__id=servico.id)
                        endereco=models.Endereco.objects.get(cliente__clientecontrato__servicointernet__id=servico.id)
                        cobranca= fmodels.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__id=servico.id)[0]
                        clientecontratostatus=models.ClienteContratoStatus.objects.filter(cliente_contrato__id=contrato.id)[0]
                        print("Servico de internet Original: ", servico)
                        print("Contrato original: ", contrato)
                        print("Endereco original: ", endereco)
                            
                        try:
                            with transaction.atomic():
                                
                            
                                ###ENDERECO COBRANCA####
                                new_endereco_cobranca=copy.copy(endereco)
                                new_endereco_cobranca.id=None
                                new_endereco_cobranca.save()

                                ##ENDERECO SERVICO####
                                new_endereco_servico=copy.copy(endereco)
                                new_endereco_servico.id=None
                                
                                new_endereco_servico.save()

                            
                            
                                ###COPIA DA COBRANCA####
                                new_cobranca=copy.copy(cobranca)
                                new_cobranca.id=None
                                new_cobranca.endereco=new_endereco_cobranca
                                new_cobranca.save()

                                ######COPIA DO CONTRATO#####
                                new_contrato=copy.copy(contrato)
                                new_contrato.cobranca=new_cobranca
                                new_contrato.id=None
                                new_contrato.status=None
                                new_contrato.save()


                                ######COPIA DO SERVICO#####
                                new_servico=copy.copy(servico)
                                new_servico.login=ad
                                new_servico.endereco=new_endereco_servico
                                new_servico.clientecontrato=new_contrato
                                new_servico.id=None
                                new_servico.mac_dhcp=None
                                new_servico.servico=None
                                new_servico.mac=None
                                new_servico.ip=None
                                new_servico.save()

                                new_clientecontratostatus=copy.copy(clientecontratostatus)
                                new_clientecontratostatus.id=None
                                new_clientecontratostatus.cliente_contrato=new_contrato
                                new_clientecontratostatus.save()

                        except DatabaseError as e:
                        
                            print('Essa é minha Exception: ', e)


                        print(ad)
        except Exception as e:
            print(e)