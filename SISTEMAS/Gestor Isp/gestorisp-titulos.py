#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--contratos', dest='contratos', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--faturas', dest='faturas', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--ajuste', dest='ajuste', type=bool, help='Arquivo importacao',required=False,default=None)

args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q 

from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from lib.utils import datefunc


if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='sgp')


clientes = {} 
contratos = {}
with open(args.clientes, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        clientes[row[1].strip()] = {}
        clientes[row[1].strip()]['cpfcnpj'] = row[3].strip() or row[12].strip() 

with open(args.contratos, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if clientes.get(row[5]):
            contratos[row[3].strip()] = clientes.get(row[5])

if args.ajuste:
    with open(args.faturas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            #print(row)
            if row[12] in ['Pago']:
                #print(row[13])
                contrato = contratos.get(row[13].strip())
                if contrato:
                    print(contrato)
                    cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=contrato.get('cpfcnpj'))
                    if cliente:
                        valor = '%s.%s' %(row[6][0:-2],row[6][-2:])
                        valorpago = '%s.%s' %(row[7][0:-2],row[7][-2:])
                        vencimento = row[16]
                        print(row[13].strip(),vencimento,valor)
                        y,m,d = vencimento.split('-')
                        vencimento = datefunc.getDateValid(int(y),int(m),int(d))
                        titulo = cliente[0].titulo_set.filter(data_vencimento=vencimento,
                                                              valor=valor,
                                                              data_pagamento__isnull=True,
                                                              data_cancela__isnull=True,
                                                              titulogateway__idtransacao=row[27])
                        if titulo:
                            print(titulo)
                            print(titulo.update(data_pagamento=vencimento,
                                                data_baixa=vencimento,
                                                usuario_b=usuario,
                                                status=fmodels.MOVIMENTACAO_PAGA,
                                                valorpago=valorpago))
                            





