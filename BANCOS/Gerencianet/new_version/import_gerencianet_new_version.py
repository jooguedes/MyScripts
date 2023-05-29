
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
#python import_gnet.py --settings=sgp.conectamcz.settings --portador=2 --arquivo=Conv-Portador-2.csv --sync=1
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
        d,m,y = d.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None


if args.arquivo:
    #portador.titulo_set.all().delete()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            #print(row)
            cpfcnpj = row[6]
            cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
            if cliente:
                print("Esse é meu cliente: ", cliente)
                cliente = cliente[0]
                contrato = cliente.clientecontrato_set.all()
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    
                    idtransacao = row[0]
                    numero_documento = tf.getNumeroDocumento() + 1
                    nosso_numero = row[0]
                    nosso_numero_f = row[0]
                    demonstrativo = ''
                    data_documento = strdate(row[3])
                    data_vencimento = strdate(row[7])
                    data_pagamento = strdate(row[9])
                    data_baixa = strdate(row[9])
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None

                    link = row[10] or row[11]
                    juros = ''
                    codigo_barras=row[12]
                    linha_digitavel=row[12]
                    valor = row[1].replace('.','').replace(',','.')
                    carne_id = row[17]
                    carne_link =row[18]
                    #carne_id = ''
                    #carne_link =''

                    if row[2].strip() in ['Pago','Marcado como pago']:
                        valorpago = row[8].replace('.','').replace(',','.')
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None

                    elif 'Cancelado' == row[2].strip():
                        data_cancela = data_vencimento
                        status = fmodels.MOVIMENTACAO_CANCELADA
                        data_baixa = None
                        data_pagamento = None
                        usuario_b = None
                        usuario_c = usuario

                    elif 'Aguardando' == row[2].strip():
                        data_baixa = None
                        data_pagamento = None

                    elif 'Vencido' == row[2].strip():
                        data_baixa = None
                        data_pagamento = None
                        valorpago = None
                        usuario_b = None

                    desconto = 0.00
                    linha_digitavel = row[12]
                    codigo_carne = ''
                    chave = ''
                    if link:
                        try:
                            chave = "-".join(link.split('/')[-1].split('-')[-3:]).strip()
                        except Exception as e:
                            print(e)

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
                                    titulo.save()
                                    titulo.data_documento=data_documento
                                    titulo.data_alteracao=data_documento
                                    titulo.save()

                                    novo_titulogateway = fmodels.TituloGateway()
                                    novo_titulogateway.titulo = titulo
                                    novo_titulogateway.gateway = titulo.portador.gateway_boleto
                                    novo_titulogateway.idtransacao = idtransacao
                                    novo_titulogateway.link = link
                                    novo_titulogateway.djson={'carne_id': carne_id,'carne_link': carne_link,'chave': chave}
                                    novo_titulogateway.save()

                                except Exception as e:
                                    print "Erro cadastrar",e,dados
                        else:
                            print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)


