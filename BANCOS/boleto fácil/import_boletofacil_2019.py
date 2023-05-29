#!/usr/bin/python
# -*- coding: utf-8 -*-
#script usdo para importar
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
#python import_boleto_facil.py --settings=sgp.vipnet.settings --portador=2  --arquivo=JUNO_TOTAL-MTWNET.csv --sync=1

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
        d,m,y = d.split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

if args.arquivo:
    #portador.titulo_set.all().delete()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=row[2]))[:1]
            if cliente:
                cliente = cliente[0]
                contrato = cliente.clientecontrato_set.all()
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca

                    idtransacao = row[0]
                    numero_documento = row[0]
                    nosso_numero = row[0]
                    nosso_numero_f = row[0]
                    demonstrativo = row[5]
                    data_documento = strdate(row[6])
                    data_vencimento = strdate(row[7])
                    data_pagamento = strdate(row[10])
                    data_baixa = strdate(row[10])
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None

                    valor = re.sub('[^0-9.,]','',row[8].replace(',', '.'))
                    if len(valor.split('.')) > 2:
                        valor = ''.join(valor.split('.',1))

                    if 'Pago' in row[11].strip() or 'Pago com valor diferente' in row[11].strip():
                        valorpago = re.sub('[^0-9.,]','',row[9].replace(',','.'))
                        if not valorpago:
                            valorpago = None
                        else:
                            if len(valorpago.split('.')) > 2:
                                valorpago = ''.join(valorpago.split('.',1))
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None

                    elif 'Baixado manualmente' in row[11].strip():
                        valorpago = re.sub('[^0-9.,]','',row[8].replace(',','.'))
                        if not valorpago:
                            valorpago = None
                        else:
                            if len(valorpago.split('.')) > 2:
                                valorpago = ''.join(valorpago.split('.',1))
                        status = fmodels.MOVIMENTACAO_PAGA
                        data_baixa = data_documento
                        data_pagamento = data_documento
                        usuario_b = usuario
                        usuario_c = None
                        demonstrativo = row[5] + " Baixado Manualmente no Boleto Fácil."

                    elif row[11].strip() == 'Cancelado':
                        data_cancela = data_documento
                        status = fmodels.MOVIMENTACAO_CANCELADA
                        data_baixa = None
                        data_pagamento = None
                        usuario_b = None
                        usuario_c = usuario

                    desconto = 0.00
                    linha_digitavel = row[14]
                    codigo_barras = ''
                    codigo_carne = ''


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
                                     'valorpago':valorpago,
                                     'desconto': desconto,
                                     'status': status,
                                     'observacao': codigo_carne
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

                                    novo_titulogateway = fmodels.TituloGateway()
                                    novo_titulogateway.titulo = titulo
                                    novo_titulogateway.gateway = titulo.portador.gateway_boleto
                                    novo_titulogateway.idtransacao = idtransacao
                                    novo_titulogateway.link = row[13]
                                    novo_titulogateway.save()

                                except Exception as e:
                                    print "Erro cadastrar",e,dados
                        else:
                            print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)
                