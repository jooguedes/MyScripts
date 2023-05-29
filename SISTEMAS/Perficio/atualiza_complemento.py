#!/usr/bin/python
# -*- coding: utf-8 -*-
from unicodedata import normalize
import argparse
import csv
import re

from django.conf import settings
from django.db.models import Q, Max
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')


ustr = lambda x: unicode(str(x).upper()).strip()

with open('/tmp/Conv-EXPORTAR_CLIENTES02.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        id=int(row[0])+140
        
        complemento=row[20]
        cb=fmodels.Cobranca.objects.filter(cliente__id=id)
        sv=admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__id=id)
        print(si)
        try:
            admmodels.Endereco.objects.filter(id=cb[0].endereco.id).update(complemento=complemento)
            admmodels.Endereco.objects.filter(id=sv[0].endereco.id).update(complemento=complemento)
        except Exception as e:
            print(e)