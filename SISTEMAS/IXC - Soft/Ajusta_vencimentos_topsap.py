#!/usr/bin/python
# -*- coding: utf-8 -*-


from unicodedata import normalize
import argparse
import csv
import re
import sys
import os

from mysqlx import Row
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


parser = argparse.ArgumentParser(description='Importação CSV')
parser.add_argument('--settings', dest='settings', type=str,required=True)
parser.add_argument('--sync', dest='sync_db', type=bool,required=False)
parser.add_argument('--arquivo', dest='arquivo', type=str,required=False)

#python import_gnet.py --settings=sgp.gnet.settings --portador=1 --arquivo=Conv-Gnet-Cobrancas.csv
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')


if args.arquivo:
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            id_contrato=row[0]

            vencimento=row[8]

            if vencimento=='35':
                vencimento=30
            elif vencimento=='39':
                vencimento=20
            elif vencimento=='37':
                vencimento=10
            else:
                continue
            
            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento
                
                print('corrigindo vencimento %s' %vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save()

            vencimento= fmodels.Vencimento.objects.get(dia=vencimento)

            cobranca = fmodels.Cobranca.objects.filter(cliente__clientecontrato__id=id_contrato)
            print('Atualizando cobranca ', vencimento, cobranca)
            
            if(args.sync_db):
                fmodels.Cobranca.objects.filter(cliente__clientecontrato__id=id_contrato).update(vencimento=vencimento)
            
           