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


args = parser.parse_args()
PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
from apps.financeiro import models as fmodels
from apps.admcore import  models as admmodels
#python ajusta_nosso_numero_ixc.py --settings=sgp.tudon.settings 
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))

portador=6
with open('/tmp/ixc-nosso_numero.csv', 'rb') as csvfile:
        portador=fmodels.Portador.objects.get(id=portador)
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(id=row[0])
           
          
            try:
                numero_documento=int(row[1]) 
            except:
                continue 
            try:
                nosso_numero_update=int(row[2])
            except:
                continue
            
            titulo=fmodels.Titulo.objects.filter(portador=portador,nosso_numero=numero_documento)

            print('esse é o cliente e ,o titulo: ', titulo, 'Novo Nosso Numero: ', nosso_numero_update)

            if args.sync_db and len(str(nosso_numero_update))>0 :	
                print('atalizando nosso_numero do cliente', cliente, 'o titulo é: ',titulo )
                fmodels.Titulo.objects.filter(portador=portador,nosso_numero=numero_documento).update(nosso_numero=0000)
                fmodels.Titulo.objects.filter(portador=portador,nosso_numero=0000).update(nosso_numero=nosso_numero_update)
            