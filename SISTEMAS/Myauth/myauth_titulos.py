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
portador = fmodels.Portador.objects.get(id=1)
with open('/tmp/myauth-titulos.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        print row
        login = row[1].strip().lower()
        #logins = ['cicera@palestina']
        #if login in logins:
        #    login = '%s1' %login
        try:
            servico = admmodels.ServicoInternet.objects.get(login__trim__lower=login)
        except:
            continue 
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        usuario = authmodels.User.objects.get(username='sgp')
        descricao = unicode(row[3].decode('latin-1'))
        numero_documento = row[4]
        nosso_numero = row[4]
        nosso_numero_f = None
        #if nosso_numero == '0':
        #nosso_numero = tf.getNossoNumero(portador) + 1
        data_documento = row[6]
        data_vencimento = row[7]
        valor = row[8]
        valorpago = row[9]
        data_pagamento = row[10]
        if not data_pagamento or not valorpago or valorpago == '0':
            data_pagamento = None
            data_baixa = None 
            status = fmodels.MOVIMENTACAO_GERADA
            usuario_b = None 
        else:
            status =  fmodels.MOVIMENTACAO_PAGA
            usuario_b = usuario 
            data_baixa = data_pagamento 
            data_pagamento = data_pagamento.split(' ')[0]
        desconto = 0.00
        linha_digitavel = ''
        codigo_barras = ''
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
                 'data_documento': data_documento,
                 'data_vencimento': data_vencimento,
                 'status': status,
                 }
        print dados
        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero).count() == 0:
            titulo = fmodels.Titulo(**dados)
            titulo.save()
            titulo.data_documento=data_documento
            titulo.save()
        else:
            dados['numero_documento']= int(fmodels.Titulo.objects.filter(portador=1).order_by('-numero_documento')[0].numero_documento) + 10000
            dados['nosso_numero']= int(fmodels.Titulo.objects.filter(portador=1).order_by('-numero_documento')[0].numero_documento) + 10000
            titulo = fmodels.Titulo(**dados)
            try:
                titulo.save()
                titulo.data_documento=data_documento
                titulo.save()
            except Exception as e:
                print('error')
                break