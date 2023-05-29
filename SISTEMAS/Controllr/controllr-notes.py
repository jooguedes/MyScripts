#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 

csv.field_size_limit(sys.maxsize)

parser = argparse.ArgumentParser(description='Importação anotacoes controllr')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='anotacoes',required=True)
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

from apps.admcore import models as admmodels

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
usuario = admmodels.User.objects.get(username='admin')

with open(args.arquivo, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in conteudo:
        idcliente = int(row[0])
        anotacao = row[1]
        cliente = admmodels.Cliente.objects.filter(id=idcliente)
        if cliente:
            n_anotacao = admmodels.ClienteAnotacao()
            n_anotacao.cliente = cliente[0]
            n_anotacao.anotacao = anotacao
            n_anotacao.usuario = usuario
            n_anotacao.save()
            print(cliente)


