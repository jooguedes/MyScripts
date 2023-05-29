#!/usr/bin/python
# -*- coding: utf-8 -*-
#script usado só para sincronizar
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
            cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=row[2]).order_by('id')

            for c in cliente:
                print(c)
                print(row[0],row[7],cliente)
                idtransacao = row[0]
                numero_documento = row[0]
                nosso_numero = row[0]
                nosso_numero_f = row[0]
                demonstrativo = row[5]
                data_documento = strdate(row[6])
                data_vencimento = strdate(row[7])
                data_pagamento = strdate(row[10])
                data_baixa = strdate(row[10])
                data_cancela = None
                status = fmodels.MOVIMENTACAO_GERADA
                valorpago = None
                usuario_b = None
                usuario_c = None
                mes_v=row[7].split("/")[1]
                ano_v=row[7].split("/")[2]
                valor = re.sub('[^0-9.,]','',row[8])
                print('Esse é meu valor: ', valor)
                if len(valor.split('.')) > 2:
                    valor = ''.join(valor.split('.',1))
                print(data_vencimento,cliente)
                #if not strdate2(row[7]):
                #    continue 
                valor=valor.replace(',','.')
            #Gambiarra
            
                #dv_ini=strdate2(row[7])-timedelta(days=3)
                #dv_fim=strdate2(row[7])+timedelta(days=3)
                #titulos = portador.titulo_set.filter(cliente__in=cliente,data_vencimento__gte=dv_ini,data_vencimento__lte=dv_fim,titulogateway__isnull=True)
                
                #fdIM DA GAMBIARRA
                titulos = portador.titulo_set.filter(cliente__id=c.id,
                                                    data_documento=data_documento,
                                                    data_vencimento=data_vencimento,
                                                    #data_vencimento__month=mes_v,
                                                    #data_vencimento__year=ano_v,
                                                    valor=valor,
                                                    titulogateway__isnull=True)
                #data_documento=data_documento
                print(titulos)
                if titulos:
                    print('o titulo existe', titulos)
                    for titulo in titulos:
                        print(titulo)
                        novo_titulogateway = fmodels.TituloGateway()
                        novo_titulogateway.titulo = titulo
                        novo_titulogateway.gateway = titulo.portador.gateway_boleto
                        novo_titulogateway.idtransacao = row[0]
                        novo_titulogateway.link = row[13]
                        print(novo_titulogateway.link)
                        try:
                            novo_titulogateway.save()
                            print(novo_titulogateway)
                        except Exception as e:
                            print(e)
                        
                    
                    
                    
   #python boletofacil-sync-gateway.py --settings=sgp.evolutioninternet.settings --portador=1 --arquivo=Juno_Total_FibernetTelecom.csv          
   #python boletofacil-sync-gateway.py --settings=sgp.nesanet.settings  --portador=1 --arquivo='Cobranca-Total.csv' 
   #python boletofacil-sync-gateway.py --settings=sgp.nesanet.settings  --portador=1 --arquivo='Conv-Cobrancanesanet-02 - 07-02-2022 10-45-19.csv'
   #python boletofacil-sync-gateway.py --settings=sgp.nesanet.settings  --portador=1 --arquivo='Conv-Cobrancanesanet-03 - 07-02-2022 10-47-08.csv'
   #python boletofacil-sync-gateway.py --settings=sgp.nesanet.settings  --portador=1 --arquivo='Conv-Cobrancanesanet-04 - 07-02-2022 10-48-38.csv'
   #python boletofacil-sync-gateway.py --settings=sgp.nesanet.settings  --portador=1 --arquivo='Conv-Cobrancanesanet-05 - 07-02-2022 10-50-10.csv'
   #python boletofacil-sync-gateway.py --settings=sgp.nesanet.settings  --portador=1 --arquivo='Conv-01-12-2020 A 31-12-2021.csv'
   #python import_mkauth.py --settings=sgp.local.settings --nas=1 --portador=1 --vencimentoadd=1 --planoadd=1 --chamados=mkauth-chamados.csv.utf8

#python boletofacil-sync-gateway.py --settings=sgp.asrnetwork.settings --portador=7 --arquivo=Conv-asr-cobranca-01.csv