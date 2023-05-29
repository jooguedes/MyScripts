#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
import csv
from datetime import date, datetime
import copy
from unicodedata import normalize
from decimal import Decimal


parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--historico', dest='historico', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--tiposatendimentos', dest='tiposatendimentos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--atendimentos', dest='atendimentos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--status', dest='status', type=str, help='Arquivo importacao',required=False)
# python import_virgo_ocorrencia.py --settings=sgp.intermix.settings  --atendimentos=vigo-tipoatendimentos.csv.utf8 

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
from apps.atendimento import models as amodels
from apps.cauth import models as authmodels
from apps.financeiro import models as fmodels

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='sgp')

if args.historico:
    with open(args.historico, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            try:
                usuario_set = authmodels.User.objects.get(username__iexact=row[3])
            except:
                usuario_set = usuario 

            dados = {}
            dados['model_name'] = 'cliente'
            dados['app_label'] = 'admcore'
            dados['object_id'] = row[5]
            dados['user'] = usuario_set
            dados['history'] = row[4]
            dados['date_created'] = '%s %s' %(row[1],row[2])
            print dados
            h = admmodels.History(**dados)
            h.save()
            h.date_created='%s %s' %(row[1],row[2])
            h.save()

if args.tiposatendimentos:
    with open(args.tiposatendimentos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {}
            dados['id'] = int(row[0]) + 100
            dados['codigo'] = int(row[0]) + 100
            dados['descricao'] = 'VIGO - %s' %row[1]
            try:
                new_tipo = amodels.Tipo(**dados)
                new_tipo.save()
            except:
                pass
            try:
                new_motivoos = amodels.MotivoOS(**dados)
                new_motivoos.id=int(row[0]) + 100
                new_motivoos.save()
            except:
                pass


if args.atendimentos:
    with open(args.atendimentos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ocorrencia = {} 
            ocorrencia['numero'] = row[4]
            try:
                ocorrencia['clientecontrato'] = admmodels.ClienteContrato.objects.get(pk=row[1])
            except:
                continue
            try:
                ocorrencia['usuario'] = authmodels.User.objects.get(username__iexact=row[11])
            except:
                ocorrencia['usuario'] = authmodels.User.objects.get(username='sgp')

            #ocorrencia['responsavel'] = ocorrencia['usuario']
            ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
            ocorrencia['status'] = 1 if row[5] else 0
            ocorrencia['conteudo'] = row[15]
            try:
                ocorrencia['tipo'] = amodels.Tipo.objects.get(codigo=int(row[3])+100)
            except:
                ocorrencia['tipo'] = amodels.Tipo.objects.get(codigo=107)
            if row[7]:
                ocorrencia['data_agendamento'] = '%s %s' %(row[7],row[8])
            if row[5]:
                ocorrencia['data_finalizacao'] = '%s %s' %(row[5],row[6])
                try:
                    ocorrencia['usuario_finaliza'] = authmodels.User.objects.get(username__iexact=row[12])
                except:
                    ocorrencia['usuario_finaliza'] = authmodels.User.objects.get(username='sgp')
            ocorrencia['data_cadastro'] = '%s %s' %(row[9],row[10])
            ocorrencia['data_alteracao'] = '%s %s' %(row[9],row[10])
            try:
                print ocorrencia
                new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                new_ocorrencia.save()
                new_ocorrencia.data_cadastro='%s %s' %(row[9],row[10])
                new_ocorrencia.data_alteracao='%s %s' %(row[9],row[10])
                new_ocorrencia.save()
            except:
                continue

            o={}
            o['ocorrencia'] = new_ocorrencia
            o['status'] = new_ocorrencia.status
            o['usuario'] = new_ocorrencia.usuario
            o['data_agendamento'] = new_ocorrencia.data_agendamento
            o['conteudo'] = new_ocorrencia.conteudo
            try:
                o['motivoos'] = amodels.MotivoOS.objects.get(codigo=int(row[3])+100)
            except:
                o['motivoos'] = amodels.MotivoOS.objects.get(codigo=30)
            o['data_cadastro'] = new_ocorrencia.data_cadastro
            o['data_alteracao'] = new_ocorrencia.data_alteracao 
            o['data_finalizacao'] = new_ocorrencia.data_finalizacao
            o['observacao'] = row[14]
            print o 

            new_os = amodels.OS(**o)
            new_os.save()
            new_os.data_cadastro=new_ocorrencia.data_cadastro
            new_os.data_alteracao=new_ocorrencia.data_alteracao
            new_os.save()


if args.status:
    with open(args.status, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            login = row[1]
            status = row[42]
            #if status == 'X':
            #    servico=admmodels.ServicoInternet.objects.filter(login=login)
            #    if servico:
            #        s= servico[0]
            #        contrato = s.clientecontrato
            #        s.status=admmodels.SERVICO_CANCELADO
            #        contrato.status.status=admmodels.CONTRATO_CANCELADO
            #        contrato.cobranca.status=fmodels.COBRANCA_CANCELADA
            #        contrato.cobranca.save()
            #        contrato.save()
            #        s.save()
            #        print(login,status)
#
            if status == 'B':
                servico=admmodels.ServicoInternet.objects.filter(login=login)
                if servico:
                    #s= servico[0]
                    #contrato = s.clientecontrato
                    #s.status=admmodels.SERVICO_SUSPENSO
                    #contrato.status.status=admmodels.CONTRATO_SUSPENSO
                    #contrato.cobranca.status=fmodels.COBRANCA_SUSPENSA
                    #contrato.cobranca.save()
                    #contrato.save()
                    #s.save()
                    print(login,status)

