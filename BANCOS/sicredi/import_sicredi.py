#!/usr/bin/python
# -*- coding: utf-8 -*-


from unicodedata import normalize
import argparse
import csv
import re
import sys
import os
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


parser = argparse.ArgumentParser(description='Importação CSV')
parser.add_argument('--settings', dest='settings', type=str,required=True)
parser.add_argument('--portador', dest='portador', type=int,required=True)
parser.add_argument('--sync', dest='sync', type=bool,required=False)
parser.add_argument('--arquivo', dest='arquivo', type=str,required=False)
parser.add_argument('--baixados', dest='baixados', type=str,required=False)

#python import_sicredi.py --settings=sgp.local.settings --portador=1 --arquivo=Conv-Relatorio-cobrancas-271985-1.csv --sync=1

args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels


tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=args.portador)
fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')
formapagamento = fmodels.FormaPagamento.objects.all()[0]
planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')

def strdate(dt):
    try:
        d,m,y = dt.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

if args.arquivo:
    #portador.titulo_set.all().delete()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            #print(row)
            cpfcnpj = row[7]
            cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
            if cliente:
                print("Esse é meu cliente: ", cliente)
                cliente = cliente[0]
                contrato = cliente.clientecontrato_set.all()
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    numero_documento = fnum(row[5])
                    inicio_nosso_numero = row[4].split('/')[0]
                    nosso_numero = row[4].split('/')[1].split('-')[0]
                    nosso_numero_f = None
                    demonstrativo = ''
                    data_documento = strdate(row[26])
                    data_vencimento = strdate(row[3])
                    data_pagamento = None
                    data_baixa = None
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None
                    juros = ''
                    codigo_barras=''
                    linha_digitavel=''
                    valor = row[6].replace(',','.')
                    '''SE EXISTIR DATA DE PAGAMENTO'''

                    if row[2].strio() !='' or row[1].strip() != '':
                        valorpago = row[48].replace(',','.')
                        if fnum(valorpago) == '':
                            valorpago = valor
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None
                        data_pagamento = strdate(row[2])
                        data_baixa=data_pagamento
                    desconto = 0.00
                    linha_digitavel = ''
                    codigo_carne = ''
        
                    if nosso_numero:
                        print('entrei no nosso numero')
                        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                            dados = {'cliente': cliente,
                                     'cobranca': cobranca,
                                     'portador': portador,
                                     'codigo_barras':codigo_barras, 
                                     'linha_digitavel':linha_digitavel,
                                     'formapagamento': formapagamento,
                                     'centrodecusto': planocontas,
                                     'modogeracao': 'l',
                                     'usuario_g': usuario,
                                     'usuario_b': usuario_b,
                                     'usuario_c': usuario_c,
                                     'demonstrativo': demonstrativo,
                                     'data_documento': data_documento,
                                     'data_alteracao': data_documento,
                                     'data_vencimento': data_vencimento,
                                     'data_cancela': data_cancela,
                                     'data_pagamento': data_pagamento,
                                     'data_baixa': data_baixa,
                                     'numero_documento': numero_documento,
                                     'nosso_numero': nosso_numero,
                                     'nosso_numero_f': nosso_numero_f,
                                     'linha_digitavel': linha_digitavel,
                                     'codigo_barras': codigo_barras,
                                     'valor': valor,
                                     'valorpago': valorpago,
                                     'desconto': desconto,
                                     'status': status,
                                     'observacao': codigo_carne,
                                     'djson': {
                                                'inicio_nosso_numero': inicio_nosso_numero,
                                               'juros': juros
                                            }
                                     }
                            if not args.sync:
                                print(dados)
                            else:
                                print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                                try:
                                    titulo = fmodels.Titulo(**dados)
                                    titulo.save()
                                    titulo.data_documento=data_documento
                                    titulo.data_alteracao=data_documento
                                    titulo.save()

                                except Exception as e:
                                    print "Erro cadastrar",e,dados
                        else:
                            print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)


