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
parser.add_argument('--sync', dest='sync', type=bool,required=False)
parser.add_argument('--arquivo', dest='arquivo', type=str,required=False)
parser.add_argument('--baixados', dest='baixados', type=str,required=False)

#python import_titulos_controll.py --settings=sgp.masterconnect.settings --portador=1 --arquivo=

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


tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=args.portador)
fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')
formapagamento = fmodels.FormaPagamento.objects.all()[0]
planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')


def strdate(d):
    try:
        y,m,d = str(d).split('-')
        return '%s-%s-%s' %(y,m,d)
    except:
        return d

if args.arquivo:
    counter=1
    #portador.titulo_set.all().delete()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cpfcnpj = row[1]
            if(len(cpfcnpj)<11):
                cpfcnpj = '0%s'%cpfcnpj
            cliente = admmodels.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=cpfcnpj))[:1]
            if cliente:
                print("Esse é meu cliente: ", cliente)
                cliente = cliente[0]
                contrato = cliente.clientecontrato_set.all()
                if contrato:
                    nosso_numero = counter
                    data_documento = strdate(str(row[5]).split(" ")[0])
                    print('Essa é minha data do documento', data_documento)
                    data_vencimento = strdate(row[4])
                    
                    fmodels.Titulo.objects.filter(data_vencimento=data_vencimento, nosso_numero=nosso_numero, cliente__id=cliente.id).update(data_documento=data_documento)
                    counter=counter+1
                   
else:
    print('------------------ O Erro está AQUI --------------------------------')
