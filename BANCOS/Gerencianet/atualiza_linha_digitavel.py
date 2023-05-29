from unicodedata import normalize
import argparse
import csv
import re
import sys
import os
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

from django.conf import settings
from django.db.models import Q, Max

from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels


tf = titulofunc.TituloFunc()
fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')
formapagamento = fmodels.FormaPagamento.objects.all()[0]
planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')

def strdate(d):
    try:
        d,m,y = d.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

with open('/tmp/Conv-Relatorio_API2.0-editado.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        #print(row)
        cpfcnpj = row[9]
        #print(cpfcnpj)
        clientes = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj).order_by('id')
        if clientes:
            print(clientes)
            cliente = clientes[0]
            contrato = cliente.clientecontrato_set.all()
            if contrato:
                print('Tenho um contrato')  
                idtransacao = row[0]
                nosso_numero = row[0]
                linha_digitavel=row[15]
                codigo_barras=row[15]
                titulo = fmodels.Titulo.objects.filter(cliente__in=clientes,
                                                       titulogateway__idtransacao=nosso_numero).order_by('-data_documento')
                print('Esse é meu titulo', titulo)
                for t in titulo:
                    print(t, linha_digitavel)
                    fmodels.Titulo.objects.filter(id=t.id).update(codigo_barras=codigo_barras, 
                                                                  linha_digitavel=linha_digitavel)