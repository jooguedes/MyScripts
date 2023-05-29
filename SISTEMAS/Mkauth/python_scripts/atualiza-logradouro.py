#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv
from apps.admcore import models as admmodels
with open('/tmp/mkauth-clientes-desativados.csv.utf8', 'rU') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=str(row[1]).lower().strip()

        bairro=row[52]

        print('Atualizando o logradouro: ', logradouro,   ' do login: ', login)
        try:
            admmodels.Endereco.objects.filter(cobranca__cliente__clientecontrato__servicointernet__login=login).update(bairro=bairro)
        
            admmodels.Endereco.objects.filter(servicointernet__login=login).update(bairro=bairro)

            admmodels.Endereco.objects.filter(cliente__clientecontrato__servicointernet__login=login).update(bairro=bairro)
        except Exception as e:
            print(e)