#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from hashlib import new
from logging import exception
import os, sys
from pydoc import cli
from datetime import date, datetime
import copy
from traceback import print_tb
from unicodedata import normalize
import csv
import re
parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Cobrancas', required=False)
args = parser.parse_args()


#########################IMPORT GERAL################################
#python import_perfacio_titulos.py --settings=sgp.econecttelecom.settings --nas=1 --planoadd=1 --clientes=Conv-clientes-perfacio.csv --titulos=Conv-recebiveis-perfacio.csv --sync=1

##################### ARQUIVOS NECESSARIOS ###########################
#                     clientes.csv                                   #
#                     recebiveis.csv                                 #
######################################################################


PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.db.models import Q
from django.conf import settings
from django.db.models import Q, Max
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
from apps.cauth import models as authmodels
from apps.fiscal import models as fismodels, constants as fisconstants

usuario = authmodels.User.objects.get(username='sgp')
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

fnum = lambda n: re.sub('[^0-9]', '', unicode(n))

def strdate(d):
    try:
        d,m,y = d.split()[0].split('.')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

usuario = admmodels.User.objects.get(username='sgp')
if args.clientes:
    clientes= {}
    titulos={}
    dados={}
    
    #load clientes
    with open(args.clientes, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            cliente={
                'id': row[0],
                'nome': row[1],
                'cpfcnpj':row[3],
                'rg': row[5],
                'sexo':row[7],
                'incricao_estadual': row[9],
                'inscricao_municipal': row[10],
                'nome_pai': row[11],
                'nome_mae': row[12],
                'nome_fantasia': row[13],
                'email': row[14],
                'telefone_fixo': row[15],
                'telefone_celular': row[16],
                'logradouro': row[18],
                'numero': row[19],
                'complemento':row[20],
                'bairro': row[22],
                'cep': row[23],
                'cidade': row[24],
                'estado': row[26],
                'observacao': row[29]
                }
            clientes[indice]=cliente
            indice=indice+1

    #load titulos
    
    if args.titulos:
        with open(args.titulos, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
            indice=0
            for row in conteudo:
                titulo={
                    'id': row[0],
                    'id_cliente': row[1],
                    'id_carteira':row[3],
                    'data_vencimento': row[4],
                    'valor': row[5],
                    'valor_pago': row[6],
                    'pago': row[8],
                    'cancelado': row[9],
                    'nosso_numero': row[10],
                    'data_cadastro': row[14]
                    }
                titulos[indice]=titulo
                indice=indice+1

for t in titulos:
    if args.titulos:
        try:
            
            for cliente in clientes:
                if titulos[t]['id_cliente']==clientes[cliente]['id']:
                    print("Entrei no IF")
                    servico = admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__pessoa__cpfcnpj__numfilter=str(clientes[cliente]['cpfcnpj']))[0]
                    contrato = servico.clientecontrato 
                    cobranca = contrato.cobranca
                    cliente = contrato.cliente
                    usuario = authmodels.User.objects.get(username='sgp')
                    descricao = unicode(row[5].decode('latin-1'))
                    nosso_numero_f = None
                    data_documento = strdate(titulos[t]['data_cadastro'])
                    data_vencimento = strdate(titulos[t]['data_vencimento'])
                    data_pagamento = strdate(titulos[t]['data_vencimento'])
                    data_cancela = None
                   
                    pago=str(titulos[t]['pago'])
                    
                    if pago =='false' and str(row[9])=='false':
                        print('Entrei no IF do pago')
                        data_pagamento = None
                        data_baixa = None 
                        status = fmodels.MOVIMENTACAO_GERADA
                        usuario_g = usuario
                        numero_documento = titulos[t]['id']
                        nosso_numero = titulos[t]['nosso_numero']
                        linha_digitavel = None
                        codigo_barras = None
                        codigo_carne = None
                        valor = str(titulos[t]['valor']).replace(',','.')
                        valorpago=None
                        desconto = 0.00
                        print('esse é o nosso_numero:', nosso_numero)
                    
                    elif str(row[9])=='true':
                        status =  fmodels.MOVIMENTACAO_CANCELADA
                        usuario_g = usuario
                        numero_documento = titulos[t]['id']
                        nosso_numero = titulos[t]['nosso_numero']
                        linha_digitavel = None
                        codigo_barras = None
                        codigo_carne = None
                        valor = str(titulos[t]['valor']).replace(',','.')
                        valorpago=None
                        desconto = 0.00
                        
                    else:
                        status =  fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario 
                        usuario_g = usuario 
                        data_baixa = data_pagamento 
                        data_pagamento = data_pagamento
                        numero_documento = titulos[t]['id']
                        nosso_numero = titulos[t]['nosso_numero']
                        valor = str(titulos[t]['valor']).replace(',','.')
                        valorpago= str(titulos[t]['valor_pago']).replace(',','.')
                        linha_digitavel = None
                        codigo_barras = None
                        codigo_carne = None
                        desconto = 0.00
                        
                    if nosso_numero:
                        portador=fmodels.Portador.objects.get(id=titulos[t]['id_carteira'])
                        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                            print("entrei no if dos dados")
                            dados = {
                                'cliente': cliente,
                                'cobranca': cobranca,
                                'portador': portador,
                                'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                                'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                                'modogeracao': 'l',
                                'usuario_g': usuario,
                                'usuario_b': usuario,
                                'demonstrativo': descricao,
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
                                'observacao': codigo_carne
                                    }
                            print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                            try:
                                if args.sync_db:
                                    titulo = fmodels.Titulo(**dados)
                                    titulo.save()
                        
                            except Exception as e:
                                print("Erro cadastrar",e,dados)
        except Exception as e:
            print(e)
            
