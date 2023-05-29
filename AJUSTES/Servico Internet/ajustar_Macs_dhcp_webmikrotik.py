#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from cmath import log
import os, sys
from datetime import date, datetime
import copy
from traceback import print_tb
from unicodedata import normalize
import csv
import re
from unicodedata import normalize
parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--mac', dest='mac', type=bool, help='cadastra os macs que faltam',required=False)
parser.add_argument('--changelogin',dest='changelogin', type=bool, help='muda os logins para ficarem igual os macs',default=False)
parser.add_argument('--deleteMac',dest='deleteMac', type=bool, help='deleta o mac controle',default=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
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
from apps.atendimento import models as amodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


usuario = admmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n) 
ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()


with open(args.arquivo, 'rU') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login =row[3].strip().lower()
        mac = ustr(row[10])
    
        if admmodels.ServicoInternet.objects.filter(login__trim__lower=login):
            print("esse é o login e foi encontrado", login)

            if args.mac:
                if args.sync_db and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count()>0 and admmodels.ServicoInternet.objects.filter(mac_dhcp=mac, mac=mac).count()==0:
                    print("Fazendo cadastro do Mac do Cliente", login)
                    admmodels.ServicoInternet.objects.filter(login__trim__lower=login).update(mac_dhcp=mac, mac=mac)


            if args.changelogin:
                if args.sync_db and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count()>0 and admmodels.ServicoInternet.objects.filter(login__trim__lower=mac)==0:
                    print("alterando o o login para ser o mac", login)
                    admmodels.ServicoInternet.objects.filter(login__trim__lower=login).update(login=mac)
           
            if args.deleteMac:
                if admmodels.ServicoInternet.objects.filter(mac__isnull=False).count()>0:
                    l=admmodels.ServicoInternet.objects.filter(mac=mac)
                    print('o login da match com o mac',l)
               
                if args.sync_db and admmodels.ServicoInternet.objects.filter(login__trim__lower=str(mac).lower()).count>0:
                    
                    admmodels.ServicoInternet.objects.filter(login__trim__lower=str(mac).lower()).update(mac='')
        else:
            #print('não achei o login ', login)
            continue


