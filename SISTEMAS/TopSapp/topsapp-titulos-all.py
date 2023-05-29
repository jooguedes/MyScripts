from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from decimal import Decimal
import csv
import sys
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

tf = titulofunc.TituloFunc()
#nnumero = tf.getNossoNumero(portador)
#ndoc = tf.getNumeroDocumento()
with open('/opt/topsapp-titulos-all.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        #print row[1].split('@')[0].strip().lower()
        try:
            #servico = admmodels.ServicoInternet.objects.get(login__splitdomain__trim__lower=row[1].split('@')[0].strip().lower())
            servico = admmodels.ServicoInternet.objects.get(login__trim__lower=row[1])
        except:
            continue
        #nnumero += 1
        #ndoc += 1
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        usuario = authmodels.User.objects.get(username='sgp')
        descricao = unicode(row[5].strip().decode('latin-1'))
        #if nosso_numero == '0':
        #nosso_numero = tf.getNossoNumero(portador) + 1
        data_documento = row[6]
        data_vencimento = row[7].split(' ')[0]
        data_pagamento = row[8]
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
        numero_documento = row[9]
        nosso_numero = row[10]
        nosso_numero_f = row[10]
        #if nosso_numero == 'gerencianet':
        #    continue
        #else:
        #    nosso_numero = row[10][2:]
        #if not nosso_numero:
        #    nosso_numero = '%s' %(str(24900000010000000 + int(numero_documento)))
        #    nosso_numero = nosso_numero[2:]
        #nosso_numero_f = row[10]
        valor = row[19]
        if len(valor.split('.')) > 2:
            valor = ''.join(valor.split('.',1))
        valorpago = row[12]
        if not valorpago:
            valorpago = None 
        else:
            if len(valorpago.split('.')) > 2:
                valorpago = ''.join(valorpago.split('.',1))
        desconto_vencimento = row[20]
        if not desconto_vencimento:
            desconto_vencimento = Decimal('0.00')
        desconto = 0.00
        linha_digitavel = None
        codigo_barras = None
        if not row[21]:
            continue
        portador = fmodels.Portador.objects.filter(id=row[21])
        if not portador:
            print(row[21],'nao achei portador')
        else:
            portador = portador[0]
        if nosso_numero and portador:
            dados = {'cliente': cliente,
                     'cobranca': cobranca,
                     'portador': portador,
                     'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                     'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                     'modogeracao': 'l',
                     'usuario_g': usuario,
                     'usuario_b': usuario_b,
                     'demonstrativo': descricao,
                     'data_documento': data_documento,
                     'data_alteracao': data_documento,
                     'data_vencimento': data_vencimento,
                     'data_pagamento': data_pagamento,
                     'desconto_venc': desconto_vencimento,
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
                     }
            print dados
            if fmodels.Titulo.objects.filter(portador=portador,nosso_numero=nosso_numero).count() == 0:
                try:
                    titulo = fmodels.Titulo(**dados)
                    titulo.save()
                    titulo.data_documento=data_documento
                    titulo.save()
                except:
                    pass 

