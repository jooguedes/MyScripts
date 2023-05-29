from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from django.db.models import Q 
import csv
import sys

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
tf = titulofunc.TituloFunc()
ndoc=tf.getNumeroDocumento()
usuario_default = authmodels.User.objects.get(username='sgp')
usuario = usuario_default
with open('/opt/boletos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter=';')
    for row in conteudo:
        try:
            servico = admmodels.ServicoInternet.objects.get(clientecontrato__id=row[0])
        except:
            continue 
        try:
            usuario = authmodels.User.objects.get(username__iexact=row[16].strip.lower())
        except:
            usuario = usuario_default
        ndoc += 1
        print row
        portador = fmodels.Portador.objects.get(descricao__iexact=row[2].lower().strip())
        data_cancela = None
        usuario_c = None 
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        descricao = row[5]
        nosso_numero_f = None
        data_documento = '%s-%s-%s' %(row[5].split('/')[2],row[5].split('/')[1],row[5].split('/')[0])
        data_vencimento = '%s-%s-%s' %(row[6].split('/')[2],row[6].split('/')[1],row[6].split('/')[0])
        if row[7]:
            data_pagamento = '%s-%s-%s' %(row[7].split('/')[2],row[7].split('/')[1],row[7].split('/')[0])
        else:
            data_pagamento = None
        numero_documento = ndoc
        try:
            nosso_numero = int(row[4])
            nosso_numero_f = str(int(row[4]))
        except:
            continue
        valor = row[8]
        if len(valor.split('.')) > 2:
            valor = ''.join(valor.split('.',1))
        valor = valor.replace(',','.')
        desconto = row[9]
        if len(desconto.split('.')) > 2:
            desconto = ''.join(desconto.split('.',1))
        desconto = desconto.replace(',','.')
        valorpago = row[12]
        if valorpago:
            if len(valorpago.split('.')) > 2:
                valorpago = ''.join(valorpago.split('.',1))
            valorpago = row[12].replace(',','.')
        codigo_carne = None
        linha_digitavel = None
        codigo_barras = None
        if data_pagamento:
            status =  fmodels.MOVIMENTACAO_PAGA
            data_baixa = data_pagamento 
            usuario_c = None 
            juros = row[11]
            usuario_b = usuario
        elif 'excluida' in row[14].strip().lower():
            data_cancela = data_vencimento
            data_pagamento = None
            data_baixa = None 
            valorpago = None
            status = fmodels.MOVIMENTACAO_CANCELADA
            usuario_b = None 
            usuario_c = usuario
        elif valor == desconto:
            status =  fmodels.MOVIMENTACAO_PAGA
            data_pagamento=data_vencimento
            data_baixa = data_pagamento 
            usuario_c = None 
            juros = row[11]
            usuario_b = usuario
        else:
            data_cancela = None
            data_pagamento = None
            data_baixa = None 
            valorpago = None
            status = fmodels.MOVIMENTACAO_GERADA
            usuario_b = None 
            usuario_c = None
        tarifas = 0.00
        centrodecusto = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
        if nosso_numero:
            if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                dados = {'cliente': cliente,
                         'cobranca': cobranca,
                         'portador': portador,
                         'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                         'centrodecusto': centrodecusto,
                         'modogeracao': 'l',
                         'usuario_g': usuario,
                         'usuario_b': usuario_b,
                         'usuario_c': usuario_c,
                         'demonstrativo': descricao,
                         'data_documento': data_documento,
                         'data_alteracao': data_documento,
                         'data_vencimento': data_vencimento,
                         'data_pagamento': data_pagamento,
                         'data_cancela': data_cancela,
                         'data_baixa': data_baixa,
                         'numero_documento': numero_documento,
                         'nosso_numero': nosso_numero,
                         'nosso_numero_f': nosso_numero_f,
                         'linha_digitavel': linha_digitavel,
                         'codigo_barras': codigo_barras,
                         'tarifas': tarifas,
                         'valor': valor,
                         'valorpago': valorpago,
                         'desconto': desconto,
                         'status': status,
                         'observacao': row[14].strip().lower()}
                print dados
                try:
                    titulo = fmodels.Titulo(**dados)
                    titulo.save()
                    titulo.data_documento=data_documento
                    titulo.save()
                except:
                    pass




