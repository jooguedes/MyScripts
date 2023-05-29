#!/usr/bin/python
# -*- coding: utf-8 -*-
import codecs
import argparse
import csv
from hashlib import new
import os,sys
from datetime import date, datetime
from django.db.models import Q

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='arquivo para atualizar data nascimento',  required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

#python import_contas_a_pagar.py --settings=sgp.jvnnet.settings --sync=1
if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
from apps.atendimento import models as amodels

usuario = admmodels.User.objects.get(username='sgp')
with codecs.open(args.arquivo, 'rb', encoding='utf-8') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    metodo = amodels.Metodo.objects.all()[0]
    assunto = 'TOP_ZAP_OCORRECIA'
    for row in conteudo:
        try:
            clientecontrato= admmodels.ClienteContrato.objects.filter(cliente__id=row[13])[0]
        except:
            continue
        if amodels.Ocorrencia.objects.filter(numero=row[0]).count() == 0:
            print(row)
            status=row[2]
            ocorrencia = {}
            ocorrencia['clientecontrato'] = clientecontrato
            ocorrencia['tipo'] = amodels.Tipo.objects.filter(codigo=8000)[0]
            ocorrencia['usuario'] = usuario 
            ocorrencia['numero'] = row[0]
            ocorrencia['metodo']= metodo
            ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if status == 'FECHADO' else amodels.OCORRENCIA_ABERTA
            ocorrencia['responsavel'] = ocorrencia['usuario']

            ocorrencia['data_cadastro'] = row[3]
            
            ocorrencia['data_finalizacao'] = row[5]
            ocorrencia['conteudo'] = 'Operador: ' + str(row[12]) + '\n' + ' Mensagem: ' + str(row[1]) + '\n' + ' Data Agendamento: ' + str(row[16])
            #ocorrencia['observacoes'] = servicoprestado
            new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
            if str(new_ocorrencia.data_finalizacao)=='':
                new_ocorrencia.data_finalizacao = None
            new_ocorrencia.data_agendamento = row[16]

            if new_ocorrencia.data_agendamento=='':
                new_ocorrencia.data_agendamento=None
                
            new_ocorrencia.save()
        else:
            print('ocorrência já existe')
            