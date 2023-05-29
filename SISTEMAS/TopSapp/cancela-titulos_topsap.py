#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import argparse
import csv
from turtle import update 
import re
parser = argparse.ArgumentParser(description='Ajustes_Nosso_Numero_Titulos')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--arquivo',dest='arquivo', type=str, help='arquivo_de_ajuste',default=False)


args = parser.parse_args()
PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from apps.financeiro import models as fmodels

#python estornar_boleto_pelo_express.py --settings=sgp.local.settings --arquivo=Conv-gnet-express.csv
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))

with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            restado=row[31]

            if restado=='1':
                fmodels.Titulo.objects.filter(nosso_numero=row[0], status=fmodels.MOVIMENTACAO_GERADA).update(status=fmodels.MOVIMENTACAO_CANCELADA)
            else:
                print('Boleto Não precisa ser cancelado')
                