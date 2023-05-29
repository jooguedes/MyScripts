#!/usr/bin/python
# -*- coding: utf-8 -*-
import csv 
from apps.admcore import models as admmodels
with open('/tmp/Conv-CLIENTE.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        condominio=row[22]
        try:
            if admmodels.Condominio.objects.filter(nome__lower__trim__iexact=str(condominio).lower().strip()).count()==0:
                new_condominio= admmodels.Condominio()
                new_condominio.nome=condominio
                new_condominio.save()

                login=row[1]
                admmodels.Endereco.objects.filter(cobranca__cliente__clientecontrato__servicointernet__login=login).update(condominio=new_condominio)
                admmodels.Endereco.objects.filter(cliente__clientecontrato__servicointernet__login=login).update(condominio=new_condominio)
                admmodels.Endereco.objects.filter(servicointernet__login=login).update(condominio=new_condominio)
            else:
                login=row[1]
                condominio=admmodels.Condominio.objects.filter(nome__lower__trim__iexact=str(condominio).lower().strip())
                print('esse é meu condominio', condominio)
                try:
                    print(admmodels.Endereco.objects.filter(cobranca__cliente__clientecontrato__servicointernet__login=login).update(condominio=condominio[0].id))
                    print(admmodels.Endereco.objects.filter(cliente__clientecontrato__servicointernet__login=login).update(condominio=condominio[0].id))
                    print(admmodels.Endereco.objects.filter(servicointernet__login=login).update(condominio=condominio[0].id))
                except Exception as e:
                    print(e)
        except Exception as e:
            print(e)