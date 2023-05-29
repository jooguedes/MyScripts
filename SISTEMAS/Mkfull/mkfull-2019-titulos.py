#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv
import re

parser = argparse.ArgumentParser(description='Importação')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--portador', dest='portador', type=int, help='Plans CSV File',default=1,required=False)
parser.add_argument('--subscribers', dest='subscribers', type=str, help='Subscribers CSV File',required=True)
parser.add_argument('--charges', dest='charges', type=str, help='Contracts CSV File',required=True)
parser.add_argument('--boletofacil', dest='boletofacil', type=str, help='Plans CSV File',required=False)
parser.add_argument('--gerencianet', dest='gerencianet', type=str, help='Plans CSV File',required=False)
args = parser.parse_args()

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()


from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
from django.db.models import Q,F

portador = fmodels.Portador.objects.get(pk=args.portador)
user = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n)
boletofacil_titles = {}
gerencianet_titles = {}
subscribers = {}

with open(args.subscribers, 'rb') as csvfile:
    content = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in content:
        print(row)
        subscribers_id = str(row[0])
        subscribers[subscribers_id] = row

if args.boletofacil:
    with open(args.boletofacil, 'rb') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in content:
            title_id = str(row[2])
            boletofacil_titles[title_id] = row

if args.gerencianet:
    with open(args.gerencianet, 'rb') as csvfile:
        content = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in content:
            title_id = str(row[2])
            gerencianet_titles[title_id] = row


with open(args.charges, 'rb') as csvfile:
    content = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in content:
        print(row)
        subscriber_id = row[3]
        subscriber = subscribers.get(str(subscriber_id))
        #print(subscriber)
        if not subscriber:
            continue 
        fullname = subscriber[8]
        fullname = normalize('NFKD', unicode(fullname)).encode('ASCII','ignore')
        contract = admmodels.ClienteContrato.objects.filter(Q(cliente__pessoa__nome__trim__unaccent__iexact=fullname.strip()))
        if contract:
            print(contract)
            contract = contract[0]
            charge = contract.cobranca
            subscriber = contract.cliente
            description = unicode(row[22].decode('latin-1'))
            our_number_f = None
            created_at = row[43].split()[0]
            updated_at = row[44].split()[0]
            due_date = row[24]
            if '/' in due_date:
                d,m,y = row[24].split('/')
                due_date = '%s-%s-%s' %(y,m,d)
            paid_at = row[29].split(' ')[0]
            cancelled_at = row[41].split(' ')[0]
            if cancelled_at == "":
                cancelled_at = None
            if paid_at == '':
                paid_at = None
                data_baixa = None
                status = fmodels.MOVIMENTACAO_GERADA
                user_b = None
            else:
                status =  fmodels.MOVIMENTACAO_PAGA
                user_b = user
                data_baixa = paid_at
                paid_at = paid_at
            document_number = int(row[0])
            our_number = row[25]
            if not our_number or our_number in ['fortunus','fortunu','gerencianet'] or our_number.startswith('for') or our_number.startswith('ge'):
                our_number = document_number
            total = row[27]
            if len(total.split('.')) > 2:
                total = ''.join(total.split('.',1))
            paid_amount = fnum(row[31])
            if not paid_amount:
                paid_amount = None
            else:
                if len(paid_amount.split('.')) > 2:
                    paid_amount = ''.join(paid_amount.split('.',1))
            punctuality_discount = fnum(row[14])
            old_pay_number = row[34]
            codigo_barras = row[37]
            codigo_carne = row[38]
            if data_baixa and data_baixa.startswith('0000-00-00') and paid_amount is not None:
                data_baixa = due_date
                data_pagamento = due_date

            boleto = None
            boleto_gateway = None
            if args.boletofacil:
                boleto = boletofacil_titles.get(str(document_number))
                our_number = document_number
                boleto_gateway = True
            if args.gerencianet:
                boleto = gerencianet_titles.get(str(document_number))
                our_number = document_number
                boleto_gateway = True

            if our_number and (boleto or not boleto_gateway):
                if fmodels.Titulo.objects.filter(numero_documento=document_number,portador=portador).count() == 0:
                    data = {'cliente': subscriber,
                             'cobranca': charge,
                             'portador': portador,
                             'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                             'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                             'modogeracao': 'l',
                             'usuario_g': user,
                             'usuario_b': user,
                             'demonstrativo': description,
                             'data_documento': created_at,
                             'data_alteracao': updated_at,
                             'data_vencimento': due_date,
                             'data_cancela': cancelled_at,
                             'data_pagamento': paid_at,
                             'data_baixa': data_baixa,
                             'numero_documento': document_number,
                             'nosso_numero': our_number,
                             'nosso_numero_f': our_number_f,
                             'linha_digitavel': '',
                             'codigo_barras': '',
                             'valor': total,
                             'valorpago': paid_amount,
                             'desconto': punctuality_discount,
                             'status': status,
                             'observacao': codigo_carne
                             }
                    #print(data)
                    print("Importing charge: ", subscriber, our_number, due_date, portador,)
                    try:
                        title = fmodels.Titulo(**data)
                        title.save()
                        our_number_f = title.getNossoNumero()
                        if our_number_f:
                            title.nosso_numero_f = re.sub('[^0-9A-Z]', '', our_number_f)
                        title.data_documento=created_at
                        title.data_alteracao=updated_at
                        title.save()
                        title.updateDadosFormatados()
                    except Exception as e:
                        print "Error while register", e, data
                        continue

                    if boleto and args.boletofacil:
                        boletofacil_key = boleto[3]
                        link = boleto[8]
                        linha_digitavel = row[9]
                        print(boletofacil_key,link)
                        print(fmodels.Titulo.objects.filter(numero_documento=int(document_number)).update(linha_digitavel=row[9]))
                        gateway = title.portador.gateway_boleto
                        if gateway:
                            print('criando titulo gateway')
                            new_title_gateway = fmodels.TituloGateway()
                            new_title_gateway.titulo = title
                            new_title_gateway.gateway = gateway
                            new_title_gateway.idtransacao = boletofacil_key
                            new_title_gateway.link = link
                            new_title_gateway.save()

                    if boleto and args.gerencianet:
                        gn_key = boleto[3]
                        gn_carne_key = boleto[7]
                        link = boleto[10]
                        link_capa = boleto[11]
                        link_carne = boleto[12]
                        linha_digitavel = row[9]
                        print(gn_key,link)
                        print(fmodels.Titulo.objects.filter(numero_documento=int(document_number)).update(linha_digitavel=row[9]))
                        gateway = title.portador.gateway_boleto
                        if gateway:
                            print('criando titulo gateway')
                            new_title_gateway = fmodels.TituloGateway()
                            new_title_gateway.titulo = title
                            new_title_gateway.gateway = gateway
                            new_title_gateway.idtransacao = gn_key
                            new_title_gateway.link = link
                            new_title_gateway.djson={'carne_link': link_carne,
                                                     'carne_capa':link_capa,
                                                     'carne_id': gn_carne_key}
                            new_title_gateway.save()


