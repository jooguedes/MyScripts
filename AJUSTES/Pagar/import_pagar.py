#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from turtle import down
from unicodedata import normalize
import csv
import re
parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--fornecedores', dest='fornecedores', type=str, help='Arquivo de Importacao',required=False)
parser.add_argument('--contasapagar', dest='contasapagar', type=str, help='Arquivo de Importacao',required=False)

args = parser.parse_args()

#python import_contaspagar.py --settings=sgp.local.settings --fornecedores= --contasapagar= --pagar=

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings

from apps.admcore import models as admmodels
from apps.atendimento import models as amodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

fnum = lambda n: re.sub('[^0-9]','',n) 

usuario = admmodels.User.objects.get(username='sgp')

if args.fornecedores:
    with open(args.fornecedores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if '0' in row[0] or fmodels.Fornecedor.objects.filter(id=row[0]).count() > 0:
                continue
            dados = {}
            dados['id'] = int(row[0])
            dados['nome'] = row[1]
            dados['nomefantasia'] = row[2]
            dados['telefones'] = '%s; %s'%(row[41], row[42])
            dados['fax'] = row[50]
            dados['responsavelempresa'] = row[3]
            dados['insc_estadual'] = row[5]
            dados['cpfcnpj'] = row[4]
            dados['logradouro'] = row[31]
            dados['bairro'] = row[34]
            dados['cep'] = row[30]
            dados['cidade'] = row[36]
            dados['uf'] = row[38]
            dados['email'] = row[44]
            dados['observacao'] = row[52]
            if 'N' in row[62]:
                dados['ativo'] = False
            else:
                dados['ativo'] = True
            try:
                novo_fornecedor = fmodels.Fornecedor(**dados)
                
                novo_fornecedor.save()
            except Exception as e:
                print(e, dados)


if args.contasapagar:
    with open(args.contasapagar, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                dados = {}
                #dados['id'] = row[0]
                # row[1] - caixa
                # row[2] - empresa
                try:
                    dados['fornecedor'] = fmodels.Fornecedor.objects.get(pk=int(row[32]))
                except:
                    dados['fornecedor'] = None

                try:
                    dados['descricao'] = '%s'%(row[17])
                except:
                    print ("ERROR UTF8 enconding", row[2])

                dados['valor'] = row[4]
                dados['forma_pagamento'] = fmodels.FormaPagamento.objects.get(id=1)

                try:
                    dados['centrodecusto'] = fmodels.CentrodeCusto.objects.get(id=51)
                except:
                    continue

                dados['data_emissao'] = row[6]
                dados['data_cadastro'] = row[6]
                dados['data_alteracao'] = row[6]
                #dados['data_vencimento'] = row[7]

                dados['usuario'] = usuario

                print(dados)
                # dados.pop('data_vencimento')
                pagar = fmodels.Pagar(**dados)
                pagar.save()
                pagar.data_cadastro = pagar.data_emissao
                pagar.save()

                dadosparcela = {}
                dadosparcela['pagar'] = pagar
                dadosparcela['valor'] = dados['valor']
                dadosparcela['parcela'] = 1
                dadosparcela['status'] = fmodels.PAGAR_STATUS_PENDENTE
                dadosparcela['data_vencimento'] = row[7]
                dadosparcela['data_cadastro'] = dados['data_cadastro']
                dadosparcela['juros'] = row[10]
                dadosparcela['multa'] = row[12]
                dadosparcela['desconto'] = 0
                dadosparcela['usuario'] = dados['usuario']

                print(dadosparcela)
                pagaritem = fmodels.PagarItem(**dadosparcela)
                pagaritem.save()

            except Exception as e:
                print '------------------- ERROR ------------------------'
                print row, e
                print '--------------------------------------------------'

if args.pagar:
    with open(args.pagar, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                dados = {}
                #dados['id'] = row[0]
                # row[1] - caixa
                # row[2] - empresa
                try:
                    dados['fornecedor'] = fmodels.Fornecedor.objects.get(pk=int(row[32]))
                except:
                    dados['fornecedor'] = None

                try:
                    dados['descricao'] = '%s'%(row[17])
                except:
                    print ("ERROR UTF8 enconding", row[2])

                dados['valor'] = row[4]
                dados['forma_pagamento'] = fmodels.FormaPagamento.objects.get(id=1)

                try:
                    dados['centrodecusto'] = fmodels.CentrodeCusto.objects.get(id=51)
                except:
                    continue

                dados['data_emissao'] = row[6]
                dados['data_cadastro'] = row[6]
                dados['data_alteracao'] = row[6]
                #dados['data_vencimento'] = row[7]

                dados['usuario'] = usuario

                print(dados)
                # dados.pop('data_vencimento')
                pagar = fmodels.Pagar(**dados)
                pagar.save()
                pagar.data_cadastro = pagar.data_emissao
                pagar.save()

                dadosparcela = {}
                dadosparcela['pagar'] = pagar
                dadosparcela['valor'] = dados['valor']
                dadosparcela['parcela'] = 1
                dadosparcela['status'] = fmodels.PAGAR_STATUS_PENDENTE
                dadosparcela['data_vencimento'] = row[7]
                dadosparcela['data_cadastro'] = dados['data_cadastro']
                dadosparcela['juros'] = row[10]
                dadosparcela['multa'] = row[12]
                dadosparcela['desconto'] = 0
                dadosparcela['usuario'] = dados['usuario']

                print(dadosparcela)
                pagaritem = fmodels.PagarItem(**dadosparcela)
                pagaritem.save()

            except Exception as e:
                print '------------------- ERROR ------------------------'
                print row, e
                print '--------------------------------------------------'