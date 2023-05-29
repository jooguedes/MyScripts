from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
import csv
import re
import sys
from datetime import date, datetime

tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=5)
#nosso_numero = tf.getNossoNumero(portador) +
usuario = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n) 



with open('/tmp/ajustes_saf2pay/Conv-Boletos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj = row[2]
    
        try:
            servico = admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__pessoa__cpfcnpj__numfilter=cpfcnpj)[0]
        except Exception as e:
            print('nao achei o cpf %s : %s' %(cpfcnpj,e))
            continue
        #portador = servico.clientecontrato.cobranca.portador
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        usuario = authmodels.User.objects.get(username='sgp')
        usuario_c = None
        usuario_g = usuario
        usuario_b = None
        descricao = row[4]
        nosso_numero_f = None
        data_documento = row[12]

        try:
            d_,m_,y_ = row[12].strip().split('/')
            date(int(y_.split(' ')[0]),int(m_),int(d_))
            data_documento='%s-%s-%s' %(y_.split(' ')[0],m_,d_)
        except Exception as e:
            print(e)

        data_vencimento = row[13]

        try:
            d_,m_,y_ = row[13].strip().split('/')
            date(int(y_.split(' ')[0]),int(m_),int(d_))
            data_vencimento='%s-%s-%s' %(y_.split(' ')[0],m_,d_)
        except Exception as e:
            print(e)
            

        data_pagamento = None
        data_baixa = None
        data_cancela = None
        valorpago = None
        status = fmodels.MOVIMENTACAO_GERADA

        if row[11]!='':
            data_pagamento = row[11]
            try:
                d_,m_,y_ = row[11].strip().split('/')
                date(int(y_.split(' ')[0]),int(m_),int(d_))
                data_pagamento='%s-%s-%s' %(y_.split(' ')[0],m_,d_)
            except Exception as e:
                print(e)
            status =  fmodels.MOVIMENTACAO_PAGA
            usuario_b = usuario 
            data_baixa = data_pagamento 
            data_pagamento = data_pagamento.split(' ')[0]
            try:
                valorpago = float(row[7].replace('R$','').replace(',','.').replace(',','.').strip())
            except:
                valorpago=float(fnum(row[7]))
        numero_documento = row[0]
        nosso_numero = numero_documento 
      
        #nosso_numero_f = str(nosso_numero)
        try:
            valor = float(row[7].replace('R$','').replace(',','.').replace(',','.').strip()) # calculado
        except:
            valorpago=float(fnum(row[7]))
        desconto = 0.00
        linha_digitavel = None
        codigo_barras = None
        codigo_carne = None

        remessa = row[10]
        g_link = None
        g_id = row[0]


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
                        novo_titulogateway.djson= {'linkpagamento': None}
                        novo_titulogateway.save()

                except Exception as e:
                    print("Erro cadastrar",e,dados)

