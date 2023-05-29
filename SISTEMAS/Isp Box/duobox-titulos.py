from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from django.db.models import Q 
import csv
import re
import sys
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
tf = titulofunc.TituloFunc()

#0 c.id as 'cliente_id',
#1 ci.pppoe_login,
#2 bo.bancos_id,
#3 bo.nosso_numero,
#4 bo.numero_documento,
#5 bo.data_gerado,
#6 bo.data_vencimento,
#7 bo.data_hora_baixa,
#8 bo.data_pagamento,
#9 bo.data_cancelado,
#10 bo.motivo_cancelado,
#0 bo.valor_documento,
#0 bo.valor_pago

#portador = fmodels.Portador.objects.get(id=row[2])
portador = fmodels.Portador.objects.get(id=2)
usuario = authmodels.User.objects.get(username='sgp')
ccusto = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
fpagamento = fmodels.FormaPagamento.objects.all()[0]

with open('/tmp/duobox-titulos-cobranca-gerencianet.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        print row
        servico = None 
        cobranca = None
        cliente = admmodels.Cliente.objects.filter(id=row[0])
        if cliente:
            cliente = cliente[0]
            if row[1]:
                servico = admmodels.ServicoInternet.objects.filter(clientecontrato__id=row[1],
                                                                   clientecontrato__cliente=cliente)
                if servico:
                    servico = servico[0]
                    contrato = servico.clientecontrato
                    cobranca = contrato.cobranca
        try:
            #descricao = unicode(row[5].decode('latin-1'))
            descricao = ''
            nosso_numero_f = None
            data_documento = row[5]
            data_vencimento = row[6]
            data_pagamento = row[8]
            data_cancela = row[9]
            valorpago = None 
            if '0000-00-00' in data_cancela:
                data_cancela = None 
            if '0000-00-00' in data_pagamento:
                data_pagamento = None
            motivo_cancela = row[10]
            if data_cancela:
                status = fmodels.MOVIMENTACAO_CANCELADA
                data_pagamento = None
                data_cancela = data_cancela.split(' ')[0]
                data_baixa = None 
                usuario_b = None
            elif not data_pagamento:
                data_pagamento = None
                data_cancela = None 
                data_baixa = None 
                status = fmodels.MOVIMENTACAO_GERADA
                usuario_b = None 
            elif data_pagamento:
                status =  fmodels.MOVIMENTACAO_PAGA
                usuario_b = usuario 
                data_cancela = None
                data_baixa = data_pagamento 
                data_pagamento = data_pagamento.split(' ')[0]
                valorpago = row[12]

            #ALTERAR QUANDO FOR 
            #numero_documento = row[4]
            #nosso_numero = numero_documento
            #nosso_numero = str(int(numero_documento) + 100)
            #nosso_numero = row[10][2:]
            #nosso_numero = row[10][0:-1]
            nosso_numero = row[3]
            numero_documento = row[3]
            nosso_numero_f = row[3]
            #nosso_numero = int(numero_documento) + 900000001000000
            #nosso_numero_f = str(int(numero_documento) + 1)
            #nosso_numero = int(numero_documento)
            #nosso_numero_f = str(nosso_numero)
            valor = row[11]
            desconto = '0.00'
            if not valorpago:
                valorpago = None
            if not data_cancela:
                data_cancela = None
            print cliente,cobranca,portador

            if not numero_documento:
                numero_documento = tf.getNumeroDocumento() + 1
            
            if not nosso_numero:
                nosso_numero = tf.getNossoNumero(portador) + 1
            
            if nosso_numero and numero_documento:
                if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                    dados = {'cliente': cliente,
                             'cobranca': cobranca,
                             'portador': portador,
                             'formapagamento': fpagamento,
                             'centrodecusto': ccusto,
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
                             'motivocancela': motivo_cancela,
                             'valor': valor,
                             'valorpago': valorpago,
                             'desconto': desconto,
                             'status': status
                             }
                    #print dados
                    print "Importando boleto",cliente,nosso_numero,data_vencimento,portador
                    try:
                        titulo = fmodels.Titulo(**dados)
                        titulo.save()
                        nosso_numero_f = titulo.getNossoNumero()
                        if nosso_numero_f:
                            titulo.nosso_numero_f = re.sub('[^0-9A-Z]', '', nosso_numero_f) 
                        titulo.data_documento=data_documento
                        titulo.data_alteracao=data_documento
                        titulo.save()
                    except Exception as e:
                        print "Erro cadastrar",e,dados
        except Exception, a:
            print 'erro',a




