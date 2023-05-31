#!/usr/bin/python
# -*- coding: utf-8 -*-
from unicodedata import normalize 
import argparse
import csv
import re
import sys
import os

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


parser = argparse.ArgumentParser(description='Importação CSV')
parser.add_argument('--settings', dest='settings', type=str,required=True)
parser.add_argument('--portador', dest='portador', type=int,required=True)
parser.add_argument('--arquivo', dest='arquivo', type=str,required=False)


args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
from datetime import date, datetime, timedelta

def strdate(d):
    try:
        d,m,y = d.split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

def strdate2(d):
    try:
        d,m,y = d.split('/')
        return date(int(y),int(m),int(d))
    except:
        return None


portador = fmodels.Portador.objects.get(pk=args.portador)

if args.arquivo:
    #portador.titulo_set.all().delete()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            clientes = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=row[2])
            print(row[0],row[7],clientes)
            idtransacao = row[0]
            numero_documento = row[0]
            nosso_numero = row[0]
            nosso_numero_f = row[0]
            demonstrativo = row[5]
            data_documento = strdate(row[9].split()[0])
            data_vencimento = strdate2(row[6])
            data_pagamento = None
            data_baixa = None
            data_cancela = None
            status = fmodels.MOVIMENTACAO_GERADA
            valorpago = None
            usuario_b = None
            usuario_c = None

            valor = row[5].replace('.', '').replace(',', '.').strip()

            #if not strdate2(row[7]):
            #    continue 
	    #Gambiarra
	    
            #dv_ini=strdate2(row[7])-timedelta(days=3)
            #dv_fim=strdate2(row[7])+timedelta(days=3)
            #titulos = portador.titulo_set.filter(cliente__in=cliente,data_vencimento__gte=dv_ini,data_vencimento__lte=dv_fim,titulogateway__isnull=True)
            
            #fdIM DA GAMBIARRA
            #titulos = portador.titulo_set.filter(cliente__in=cliente, data_documento__date=data_documento, data_vencimento=data_vencimento, valor=valor, titulogateway__isnull=True)
            for cliente in clientes:
                titulos = portador.titulo_set.filter(cliente=cliente, 
                                                    #data_documento__date=data_documento,
                                                    data_vencimento=data_vencimento, 
                                                    valor=valor, 
                                                    titulogateway__isnull=True).order_by('-data_documento')
                try:
                    if titulos:
                        print('o titulo existe', titulos)
                        for titulo in titulos:
                            #if str(data_vencimento).split('-')[:2] == str(titulo.data_vencimento).split('-')[:2]:
                            novo_titulogateway = fmodels.TituloGateway()
                            novo_titulogateway.titulo = titulo
                            novo_titulogateway.gateway = titulo.portador.gateway_boleto
                            novo_titulogateway.idtransacao = row[0]
                            novo_titulogateway.link = row[12]
                            print(novo_titulogateway.link)
                            try:
                                novo_titulogateway.save()
                                print(novo_titulogateway)
                            except Exception as e:
                                print(e)
                                break
                            
                            # 01/01/2020 - 30/06/2020
                            # 01/07/2020 - 31/12/2020
                            # 01/01/2021 - 30/06/2021
                            # 01/07/2021 - 31/12/2021
                            # 01/01/2022 - 30/06/2022
                            # 01/07/2022 - 31/12/2022
                            # 01/01/2023 - 30/06/2023
                            # 01/07/2023 - 31/12/2023
                            
                            #   python atualiza-galaxpay.py --settings=sgp.wendor.settings --portador=2069 --arquivo=
                            #   OBS.: ORDERNAR NUMERO DOCUMENTO DO MAIOR PARA O MENOR
                except:
                    continue