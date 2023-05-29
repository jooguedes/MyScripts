#!/usr/bin/python
# -*- coding: utf-8 -*-
from msilib.schema import ServiceControl
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
usuario = authmodels.User.objects.get(username='sgp')

with open('/tmp/ixc-clientes.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        data_cadastro=row[37]
        login=row[28]

        admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login).update(data_cadastro=data_cadastro)
        admmodels.ClienteContrato.objects.filter(servicointernet__login=login).update(data_cadastro=data_cadastro)
