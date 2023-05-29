import csv
import re


#python import_gnet.py --settings=sgp.gnet.settings --portador=1 --arquivo=Conv-Gnet-Cobrancas.csv

from django.conf import settings
from django.db.models import Q, Max
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')



with open('/tmp/Conv-16063-GERENCIAMENTO-DE-CLIENTES-2023-03-22.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj=fnum(row[8])
        login=row[2]
        vencimento=row[26]
        print(cpfcnpj)
        
        try:
            vencimento=fmodels.Vencimento.objects.get(dia=vencimento)
            
        except:
            if vencimento=='':
                continue
            print "erro vencimento %s" %vencimento
                
            print('corrigindo vencimento %s' %vencimento)
            new_vencimento = fmodels.Vencimento()
            new_vencimento.dia = vencimento
            new_vencimento.save()
                
            vencimento= fmodels.Vencimento.objects.get(dia=vencimento)
                
            cobranca = fmodels.Cobranca.objects.filter(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj, cliente__clientecontrato__pop=2)
            print('Atualizando cobranca ', vencimento, cobranca)
            fmodels.Cobranca.objects.filter(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj, cliente__clientecontrato__pop=2).update(vencimento=vencimento)
            continue
        fmodels.Cobranca.objects.filter(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj, cliente__clientecontrato__pop=2).update(vencimento=vencimento)          
                    