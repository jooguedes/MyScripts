#!/usr/bin/python
# -*- coding: utf-8 -*
import csv
import re
from apps.admcore import models as admmodels

with open('/tmp/Ajustes_contatos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        data_cadastro=row[4].split(' ')[0]
        cpfcnpj=row[8]
        try:
            admmodels.Cliente.objects.filter(clientecontrato__cliente__pessoa__cpfcnpj__numfilter=cpfcnpj).update(data_cadastro=data_cadastro)
            admmodels.ClienteContrato.objects.filter(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj).update(data_cadastro=data_cadastro)
        except Exception as e:
            print(e)
            continue