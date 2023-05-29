#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from enum import unique
from operator import truediv

import os, sys
from django.db import transaction
import csv
import re
import hashlib

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
args = parser.parse_args()
#python import_historico_trafego_ProvApp.py --settings=sgp.aslantelecom.settings
PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings

from apps.admcore import models as admmodels
from django.db.models import Q
from apps.cauth.models import User
from apps.netcore import models_radius as rmodels


sgpuser = User.objects.get(username='sgp')

cpfs = []
dados = {}
clientes_conectividade = {}
clientes_trafego = {}

RadAcctId=2000
md5=hashlib.md5()
salvar = False
#servico conectividade
with open('/tmp/ixc-radacct.csv.utf8', 'rb') as csvfile:
    conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
    for row in conteudo:
        usuario = sgpuser
        login = row[3]
        cliente = admmodels.ServicoInternet.objects.filter(login__trim__lower=login)
        radacct = rmodels.Radacct()
        radacct.username = login
        radacct.nasipaddress = row[5]
        radacct.radacctid=RadAcctId
        hash=str(RadAcctId)
        radacct.acctstarttime = row[8]
        radacct.nasipaddress= row[5]
        radacct.acctstoptime= row[9]
        radacct.acctinputoctets = row[15]
        radacct.acctoutputoctets = row[16]
        radacct.calledstationid = row[17]
        radacct.callingstationid = row[18]
        radacct.acctsessionid = row[1]
        radacct.framedipaddress= row[22]
        if row[23]!='':
            radacct.framedipv6prefix=row[23]
            radacct.delegatedipv6prefix=row[24]
        else:
            radacct.framedipv6prefix=''
            radacct.delegatedipv6prefix=''
        md5.update(hash)
        radacct.acctuniqueid = md5.hexdigest()
        print(radacct)
        print(str(radacct.username), radacct.nasipaddress, radacct.acctinputoctets, radacct.acctoutputoctets, radacct.calledstationid, radacct.acctsessionid, radacct.radacctid, radacct.acctuniqueid)
        if  args.sync_db:
            print('salvando histrico de tráfego cliente: ', cliente)
            radacct.save()
            RadAcctId=RadAcctId+1




##DELETAR REGISTROS INSERIDOS##
RadAcctId=2000
from apps.netcore import models_radius as rmodels
with open('/tmp/ixc-radacct.csv.utf8', 'rb') as csvfile:
    conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
    for row in conteudo:
        usuario = sgpuser
        login = row[3]
        cliente = admmodels.ServicoInternet.objects.filter(login__trim__lower=login)
        radacctid=RadAcctId
        
        rmodels.Radacct.objects.filter(radacctid=radacctid, username=login).delete()
        RadAcctId=RadAcctId+1
       
        