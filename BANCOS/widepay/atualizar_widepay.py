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
        d,m,y = d.split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

PORTADORES = [2]

with open('/tmp/ajuste-widepay-2.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj = row[2]
        if cpfcnpj == '':
            cpfcnpj = row[3]
        clientes = admmodels.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=cpfcnpj))
        for cliente in clientes:
            print(cliente)
            contrato = cliente.clientecontrato_set.all()
            if contrato:    
                contrato = contrato[0]
                cobranca = contrato.cobranca
                idtransacao = row[0]
                numero_documento = row[11]
                nosso_numero = row[11]
                nosso_numero_f = row[11]
                demonstrativo = row[4]
                data_documento = strdate(row[9].split()[0])
                data_vencimento = strdate(row[6])
                data_pagamento = strdate(row[8])
                data_baixa = strdate(row[8])
                link = row[12]

                valor = row[5].replace('.', '').replace(',','.')
                linha_digitavel = row[13]
                codigo_barras = row[14]
                print('Valor: ', valor, ' Data Emissao: ', data_documento, ' Data: ', data_vencimento)
                titulo = fmodels.Titulo.objects.filter(cliente=cliente,
                                                    valor=valor,
                                                    portador__in=PORTADORES,
                                                    #data_documento__date=data_documento,
                                                    data_vencimento=data_vencimento,
                                                    titulogateway__isnull=True).order_by('-data_documento')
                if titulo:
                    try:
                        novo_titulogateway = fmodels.TituloGateway()
                        novo_titulogateway.titulo = titulo[0]
                        novo_titulogateway.gateway = titulo[0].portador.gateway_boleto
                        novo_titulogateway.idtransacao = idtransacao
                        novo_titulogateway.link = link
                        novo_titulogateway.save()
                        print('---------------------------------%s'%titulo)
                    except Exception as a:
                        print ('Erro ao atualizar link da gateway, erro: ', a)
