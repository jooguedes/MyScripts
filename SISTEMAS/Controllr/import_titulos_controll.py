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

#python import_titulos_controll.py --settings=sgp.masterconnect.settings --portador=1 --arquivo=

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


def strdate(d):
    try:
        y,m,d = str(d).split('-')
        return '%s-%s-%s' %(y,m,d)
    except:
        return d

if args.arquivo:
    counter=1
    #portador.titulo_set.all().delete()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cpfcnpj = row[1]
            if(len(cpfcnpj)<11):
                cpfcnpj = '0%s'%cpfcnpj
            cliente = admmodels.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=cpfcnpj))[:1]
            if cliente:
                print("Esse é meu cliente: ", cliente)
                cliente = cliente[0]
                contrato = cliente.clientecontrato_set.all()
                if contrato:
                    
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    
                    idtransacao = row[0]
                    numero_documento = tf.getNumeroDocumento() + 1
                    nosso_numero = counter
                    nosso_numero_f = None
                    demonstrativo = ''
                    data_documento = strdate(str(row[5]).split(" ")[0])
                    print('Essa é minha data do documento', data_documento)
                    data_vencimento = strdate(row[4])
                    if(row[6][:10] != ''):
                      data_pagamento = strdate(row[6][:10])
                      data_baixa = strdate(row[6][:10])
                      data_baixa = strdate(row[6][:10])
                    else:
                      data_pagamento = None
                      data_baixa = None
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None

                    juros = 0.00
                    valor = row[7][:5]

                    if data_pagamento != None:
                        valorpago = float(row[8])
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None

                    desconto = 0.00
                    linha_digitavel = ''
                    codigo_barras = ''
                    codigo_carne = ''
                    chave = ''

                    if nosso_numero:

                        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                            dados = {'cliente': cliente,
                                     'cobranca': cobranca,
                                     'portador': portador,
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
                                     'djson': {'juros': juros }
                                     }
                            if not args.sync:
                                print(dados)
                            else:
                                if fmodels.TituloGateway.objects.filter(idtransacao=idtransacao).count() > 0:
                                    continue
                                print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                                try:
                                    titulo = fmodels.Titulo(**dados)
                                    titulo.data_documento=data_documento
                                    titulo.data_alteracao=data_documento
                                    titulo.save()
                                    counter=counter+1
                                except Exception as e:
                                    print "Erro cadastrar",e,dados
                        else:
                            print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)
else:
    print('------------------ O Erro está AQUI --------------------------------')
