#!/usr/bin/python
# -*- coding: utf-8 -*-
from unicodedata import normalize
import argparse
import csv
import re
import sys
import os
from apps.admcore import models as admmodels
from django.db.models import Q, Max


with open('/opt/rbx-contatos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj=row[0]
        
        if(row[6]!=''):
            cliente=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=row[0])
            new_contato_celular= admmodels.Contato()
            new_contato_celular.tipo = 'EMAIL'
            new_contato_celular.contato = row[6]
            new_contato_celular.save()
            new_ccontato_celular = admmodels.ClienteContato()
            new_ccontato_celular.cliente = cliente[0]
            new_ccontato_celular.contato = new_contato_celular
            new_ccontato_celular.save()
       