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

path = '/tmp/beesweb-gnet.csv'
PORTADOR = 1

def strdate(d):
    try:
        d,m,y = d.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None
with open(path, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        #print(row)
        cpfcnpj = row[9]
        #print(cpfcnpj)
        clientes = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj).order_by('id')
        if clientes:
            print(clientes)
            cliente = clientes[0]
            contrato = cliente.clientecontrato_set.all()
            if contrato:
                #print(contrato)
                #print(row)
                contrato = contrato[0]
                cobranca = contrato.cobranca
                idtransacao = row[0]
                nosso_numero = row[0]
                nosso_numero_f = row[0]
                demonstrativo = row[7]
                data_documento = strdate(row[4])
                data_vencimento = strdate(row[10])
                try:
                    mes_vencimento=data_vencimento.split('-')[1]
                    ano_vencimento=data_vencimento.split('-')[0]
                except:
                    pass
                data_pagamento = strdate(row[12])
                data_baixa = strdate(row[12])
                data_cancela = None
                status = fmodels.MOVIMENTACAO_GERADA
                valorpago = None
                usuario_b = None
                usuario_c = None
                codigo_barras=row[15]
                linha_digitavel=row[15]
                #link = row[21] or row[13]
                #juros = row[15]
                #carne_id = row[19]
                #carne_link = row[20]
                link = row[13] or row[14]
                #juros = row[16]
                juros = ''
                carne_id = ''
                carne_link = ''
                #carne_id = ''
                #carne_link = ''
                valor = row[1].replace('.','').replace(',','.')
                try:
                    titulo = fmodels.Titulo.objects.filter(portador=PORTADOR, 
                                                           cliente__in=clientes,
                                                           #data_documento__date=data_documento,
                                                           data_vencimento=data_vencimento,
                                                           data_vencimento__year=ano_vencimento,
                                                           data_vencimento__month=mes_vencimento,
                                                           valor=valor,
                                                           #linha_digitavel=linha_digitavel,
                                                           titulogateway__isnull=True).order_by('-data_documento')
                except Exception as e:
                    print(e)
                    continue
                print("esse é meu titulo ", titulo)
                if titulo:
                    print("entrei no if do titulo")
                    print(titulo)
                    t = titulo[0]
                    #fmodels.Titulo.objects.filter(id=t.id).update(codigo_barras=codigo_barras, linha_digitavel=linha_digitavel)
                    print("Esse é meu portador gateway boleto: ", t.portador.gateway_boleto)
                    if t.portador.gateway_boleto:
                        print('entrei no if do gateway de boleto')
                        print(cliente,data_vencimento,valor,t)
                        novo_titulogateway = fmodels.TituloGateway()
                        novo_titulogateway.titulo = t
                        novo_titulogateway.gateway = t.portador.gateway_boleto
                        novo_titulogateway.idtransacao = idtransacao
                        novo_titulogateway.link = link
                        novo_titulogateway.djson={'carne_id': carne_id,'carne_link': carne_link}
                        chave = None
                        try:
                            chave = "-".join(link.split('/')[-1].split('-')[-3:]).strip()
                        except Exception as e:
                            print(e)
                        if chave:
                            t.titulogateway.djson={'chave': chave,'carne_id': carne_id, 'carne_link': carne_link}
                            print('chave',chave)
                        novo_titulogateway.save()
        else:
            print('Cliente não encontrado')