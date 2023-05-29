from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
import csv
import re
import sys
tf = titulofunc.TituloFunc()    
portador = fmodels.Portador.objects.get(pk=1)
#nosso_numero = tf.getNossoNumero(portador) +
usuario = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n) 
#portador.titulo_set.all().delete()
with open('/tmp/Conv-exporta_boletos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        id_contrato=int(row[3])
        print(id_contrato)
        try:
            try:
                servico = admmodels.ServicoInternet.objects.filter(clientecontrato__id=id_contrato)[0]
                print(servico)
            except Exception as e:
                print('nao achei login %s : %s' %(id_contrato,e))
                continue
            contrato = servico.clientecontrato 
            cobranca = contrato.cobranca
            cliente = contrato.cliente
            usuario = authmodels.User.objects.get(username='sgp')
            descricao = unicode(row[11].decode('latin-1'))
            nosso_numero_f = None
            data_documento = row[6]
            data_vencimento = row[8]
            if data_vencimento=='0000-00-00':
                data_vencimento=data_documento
            data_pagamento = row[7]
            data_cancela = None
            valor = row[9] 
            if data_pagamento=='0000-00-00':
                data_pagamento = None
                data_baixa = None 
                status = fmodels.MOVIMENTACAO_GERADA
                usuario_b = None 
            else:
                status =  fmodels.MOVIMENTACAO_PAGA
                usuario_b = usuario 
                data_baixa = data_pagamento 
                data_pagamento = data_pagamento
            numero_documento = int(row[4])
            nosso_numero = int(row[16])
            print('Esse é o nosso numero ', nosso_numero )
            
        
            #valor = row[11]
          
            valorpago = fnum(row[9])

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
                             'valor': valor,
                             'valorpago': valorpago,
                             'status': status,
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
