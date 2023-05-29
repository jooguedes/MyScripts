from unicodedata import normalize
import argparse
import csv
import re
import sys
import os
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
from django.conf import settings
from django.db.models import Q, Max

from apps.admcore import models as admmodels
####################INFORMACOES NECESSARIAS NO ARQUIVO##################################
#  versao:1.0              logins                                                      #
#                          ids dos contratos                                           #
#                          senhas                                                      #
#                                                                                      #
#  Obs: só foi possivel atualizar em massa todos os logins de todos os contratos       #
#       devido ao contratos inseridos no sgp terem sido inseridos com mesmo ID         #
#       dos contratos do RadiusNet                                                     #
#                                                                                      #
########################################################################################
logins=[]
duplicado=False
with open('/tmp/Conv-relatorio-correcao-clickinternet.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj= row[2]
        contrato= row[3]
        login= row[6]
        senha=row[7]
        clientes = admmodels.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=cpfcnpj))[:1]
        if clientes > 0:
            try:
                print("######################################################################################")
                print('Atualizando clienet', clientes, 'com login', login)
                print("#######################################################################################")
                admmodels.ServicoInternet.objects.filter(clientecontrato__id=contrato).update(login=login, login_password=senha, login_password_plain=senha)
            except:
                pass