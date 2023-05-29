from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import sys
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
tf = titulofunc.TituloFunc()
tf.getNumeroDocumento()
usuario = authmodels.User.objects.get(username='sgp')
portador = fmodels.Portador.objects.get(pk=9)
with open('/opt/topsapp-titulos-gerencianet-9.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            servico = admmodels.ServicoInternet.objects.get(login=row[1])
        except:
            continue
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        descricao = unicode(row[5].decode('latin-1'))
        nosso_numero_f = None
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
        #if nosso_numero == 'gerencianet':
        #    continue
        #else:
        #    nosso_numero = row[10][2:]
        #if not nosso_numero:
        #    nosso_numero = '%s' %(str(24900000010000000 + int(numero_documento)))
        #    nosso_numero = nosso_numero[2:]
        nosso_numero_f = row[10]
        valor = row[19]
        if len(valor.split('.')) > 2:
            valor = ''.join(valor.split('.',1))
        valorpago = row[12]
        if not valorpago:
            valorpago = None 
        else:
            if len(valorpago.split('.')) > 2:
                valorpago = ''.join(valorpago.split('.',1))
        desconto = 0.00
        linha_digitavel = None
        codigo_barras = None
        gnet_url = row[20]
        gnet_chave = row[22]        
        if nosso_numero and portador.gateway_boleto:
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
                    titulogateway = fmodels.TituloGateway()
                    titulogateway.titulo = titulo
                    titulogateway.gateway = portador.gateway_boleto
                    titulogateway.link = gnet_url
                    titulogateway.idtransacao = gnet_chave
                    titulogateway.save()
                except Exception as e:
                    print(e)

