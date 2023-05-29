#!/usr/bin/python
# -*- coding: utf-8 -*-
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
        cpfcnpj=row[11]
        login=row[28]
        try:
            numero_instalacao= fnum(row[13])
            numero_cobranca=fnum(row[13])

            if row[40] and row[43] and row[44]:
                numero_instalacao= fnum(row[41])

            if row[48] and row[51] and row[52]:
                numero_instalacao= fnum(row[49])
            
        except:
            continue
        
        si=admmodels.ServicoInternet.objects.filter(login__trim__lower=login.lower())
        
        endereco_cliente=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)

        for enc in endereco_cliente:
            try:
                admmodels.Endereco.objects.filter(id=enc.endereco.id).update(numero=numero_cobranca)
            except Exception as e:
                print(e)
            
        endereco_cobranca=fmodels.Cobranca.objects.filter(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj)

        for ec in endereco_cobranca:
            try:
                admmodels.Endereco.objects.filter(id=ec.endereco.id).update(numero=numero_cobranca)
            except Exception as e:
                print(e)
        try:
            admmodels.Endereco.objects.filter(id=si[0].endereco.id).update(numero=numero_instalacao)
        
        except Exception as e:
            print(e)