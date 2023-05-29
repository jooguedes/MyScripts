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


with open('/tmp/ajustes_saf2pay/Conv-links_novos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        #print(row)
        cpfcnpj = row[2]
        #print(cpfcnpj)
        clientes = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
        if clientes:
            print(clientes)
            cliente = clientes[0]
            contrato = cliente.clientecontrato_set.all()
            if contrato:
                idtransacao = row[0]
                nosso_numero = row[0]
                link = row[4]
                titulo = fmodels.Titulo.objects.filter(cliente__in=clientes,
                                                        titulogateway__idtransacao=idtransacao)
                print("esse é meu titulo ", titulo)
                if titulo:

                    fmodels.TituloGateway.objects.filter(titulo=titulo[0].id).update(link=link,djson= {'linkpagamento': link})
                    '''print("entrei no if do titulo")
                    print(titulo)
                    t = titulo[0]
                    if t.portador.gateway_boleto:
                        print('entrei no if do gateway de boleto')
                        print(cliente,t)
                        novo_titulogateway = fmodels.TituloGateway()
                        #novo_titulogateway.titulo = t
                        novo_titulogateway.gateway = t.portador.gateway_boleto
                        novo_titulogateway.idtransacao = idtransacao
                        novo_titulogateway.link = link
                        #novo_titulogateway.djson={'carne_id': carne_id,'carne_link': carne_link}
                        chave = None
                        novo_titulogateway.save()'''
        else:
            print('Cliente não encontrado')
		 


