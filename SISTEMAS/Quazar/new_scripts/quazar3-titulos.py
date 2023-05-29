from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
import csv
import re
import sys

tf = titulofunc.TituloFunc()
#portador = fmodels.Portador.objects.get(pk=1)
#nosso_numero = tf.getNossoNumero(portador) +
usuario = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n) 


with open('/tmp/quazar-titulos-banco-convencional-id-06.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login = row[0].strip()
        if login:
            #login = normalize('NFKD', unicode(login)).encode('ASCII','ignore')
            print(login)
            #login = '%s@quaza2' %login
            #login = '%s@infolink' %login
            #login = '%s@mkauth' %login
        try:
            try:
                servico = admmodels.ServicoInternet.objects.get(login__trim__lower=login.strip().lower())
            except Exception as e:
                print('nao achei login %s : %s' %(login,e))
                continue
            portador = fmodels.Portador.objects.get(id=row[20])
            contrato = servico.clientecontrato
            cobranca = contrato.cobranca
            cliente = contrato.cliente
            usuario = authmodels.User.objects.get(username='sgp')
            usuario_c = None
            usuario_g = usuario
            usuario_b = None
            descricao = row[4]
            nosso_numero_f = None
            data_documento = row[5].split()[0]
            data_vencimento = row[13]
            if data_vencimento == '0000-00-00':
                data_vencimento=data_documento
            data_pagamento = None
            data_baixa = None
            data_cancela = None
            valorpago = None
            status = fmodels.MOVIMENTACAO_GERADA

            if row[11] and '0000-00-00 00:00:00' not in row[11]:
                data_pagamento = row[11]
                status =  fmodels.MOVIMENTACAO_PAGA
                usuario_b = usuario 
                data_baixa = data_pagamento 
                data_pagamento = data_pagamento.split()[0]
                valorpago = row[12]

            if row[17] == '1':
                data_cancela = row[18].split()[0]
                status = fmodels.MOVIMENTACAO_CANCELADA
                usuario_c = usuario
                valorpago = None
                data_pagamento = None

            numero_documento = fnum(row[2])
            nosso_numero = row[2] 
            valor = row[7] # calculado
            if not valor:
                valor = row[11]
            if len(valor.split('.')) > 2:
                valor = ''.join(valor.split('.',1))
            valorpago = fnum(row[12])
            if not valorpago:
                valorpago = None 
            else:
                if len(valorpago.split('.')) > 2:
                    valorpago = ''.join(valorpago.split('.',1))
            desconto = 0.00
            linha_digitavel = row[9]
            codigo_barras = row[8]
            codigo_carne = row[15]

            remessa = row[10]
            g_link = row[14]
            g_id = row[15]



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
                             'usuario_b': usuario_b,
                             'usuario_c': usuario_c,
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
                             'djson': {'idremessa': remessa},
                             'observacao': codigo_carne
                             }
                    #print dados
                    print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                    titulo = None
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
                        if titulo.portador.gateway_boleto:
                            print(cliente,data_vencimento,valor,titulo)
                            novo_titulogateway = fmodels.TituloGateway()
                            novo_titulogateway.titulo = titulo
                            novo_titulogateway.gateway = titulo.portador.gateway_boleto
                            novo_titulogateway.idtransacao = g_id
                            novo_titulogateway.link = g_link
                            novo_titulogateway.djson= {'linkpagamento': row[19]}
                            novo_titulogateway.save()

                    except Exception as e:
                        print("Erro cadastrar",e,dados)



        except Exception as a:
            print(a)

