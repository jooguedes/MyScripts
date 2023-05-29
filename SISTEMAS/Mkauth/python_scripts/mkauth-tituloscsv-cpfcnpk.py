from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
import csv
import re
import sys

tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=4)
#nosso_numero = tf.getNossoNumero(portador) +
usuario = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n) 
#portador.titulo_set.all().delete()
with open('/tmp/mkauth-titulos-4.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:

        cpfcnpj = row[2]
        if cpfcnpj:
            print(cpfcnpj)
        try:
            try:
                cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)[0]
            except Exception as e:
                print('nao achei cliente pelo cpfcnpj %s : %s' %(cpfcnpj,e))
                continue
            contrato = admmodels.ClienteContrato.objects.filter(cliente=cliente)[0]
            cobranca = contrato.cobranca
            cliente = cliente
            usuario = authmodels.User.objects.get(username='sgp')
            descricao = unicode(row[5].decode('latin-1'))
            nosso_numero_f = None
            data_documento = row[6]
            data_vencimento = row[7].split(' ')[0]
            data_pagamento = row[8]
            data_cancela = None
            if data_pagamento == '':
                data_pagamento = None
                data_baixa = None 
                status = fmodels.MOVIMENTACAO_GERADA
                usuario_b = None 
            else:
                status =  fmodels.MOVIMENTACAO_PAGA
                usuario_b = usuario 
                data_baixa = data_pagamento 
                data_pagamento = data_pagamento.split(' ')[0]
            numero_documento = int(row[9]) 
            nosso_numero = numero_documento
            #nosso_numero = fnum(row[10][:-1])
            #if nosso_numero=='':
            #    nosso_numero=numero_documento
            #nosso_numero = row[10]
            valor = row[11]
            #valor = row[11]
            if len(valor.split('.')) > 2:
                valor = ''.join(valor.split('.',1))
            valorpago = fnum(row[12])
            if not valorpago:
                valorpago = None 
            else:
                if len(valorpago.split('.')) > 2:
                    valorpago = ''.join(valorpago.split('.',1))
            desconto = 0.00
            linha_digitavel = row[16]
            codigo_barras = row[17]
            codigo_carne = row[15]

            if data_baixa and data_baixa.startswith('0000-00-00') and valorpago is not None:
                data_baixa = data_vencimento
                data_pagamento = data_vencimento

            if nosso_numero:
                if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                    dados = {'cliente': cliente,
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
                    #print dados
                    print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                    try:
                        titulo = fmodels.Titulo(**dados)
                        titulo.save()
                        nosso_numero_f = titulo.getNossoNumero()
                        if nosso_numero_f:
                            titulo.nosso_numero_f = re.sub('[^0-9A-Z]', '', nosso_numero_f) 
                        titulo.data_documento=data_documento
                        titulo.data_alteracao=data_documento
                        titulo.save()
                        titulo.updateDadosFormatados()
                    except Exception as e:
                        print("Erro cadastrar",e,dados)

        except Exception as a:
            print(a)