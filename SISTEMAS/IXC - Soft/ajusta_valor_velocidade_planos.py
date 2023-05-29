#!/usr/bin/python
# -*- coding: utf-8 -*-
from shutil import ExecError
from unicodedata import normalize
import argparse
import csv
import re
import sys
import os
from django.conf import settings
from django.db.models import Q, Max

from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

fnum = lambda n: re.sub('[^0-9.]','',n)
def fnum(n): return re.sub('[^0-9]', '', unicode(n))
usuario = authmodels.User.objects.get(username='sgp')

with open('/tmp/ixc-planos.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:

        if str(row[2])!='0':
            nome=row[1]
            if 'M' in row[3]:
                upload=int(fnum(row[3]))*1024
            else:
                upload=fnum(row[3])
            try:
                
                admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=nome).update(upload=upload)
            except Exception as e:
                print(e)

