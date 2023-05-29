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
usuario_default = authmodels.User.objects.get(username='sgp')
usuario = usuario_default
portador = fmodels.Portador.objects.get(pk=9)
with open('/tmp/vigo-titulos-09-BRADESCO-MAXXNET-MULTIGLOBAL-EIRELI.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        print row
        servico = admmodels.ServicoInternet.objects.filter(Q(clientecontrato__cliente__pessoa__cpfcnpj__numfilter=row[2]))
        if len(servico) == 1:
            servico = servico[0]
        else:
            servico = None
        if not servico:
            servico = admmodels.ServicoInternet.objects.filter(clientecontrato__id=row[1])
            if servico:
                servico = servico[0]
        if not servico:
            continue
        data_cancela = None
        usuario_c = None 
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        descricao = row[5]
        nosso_numero_f = None
        data_documento = row[6]
        data_vencimento = row[7].split(' ')[0]
        data_pagamento = row[8]
        numero_documento = row[9]
        if portador.codigo_banco == '104':
            nosso_numero = row[10][2:].split('-')[0]
        elif portador.codigo_banco in ['341','237']:
            nosso_numero = row[10].split('/')[1].split('-')[0]
        else:
            nosso_numero = row[10].split('-')[0]
        nosso_numero_f = row[10].replace('-','')
        if not nosso_numero:
            nosso_numero = numero_documento
            nosso_numero_f = numero_documento 
        valor = row[11]
        if len(valor.split('.')) > 2:
            valor = ''.join(valor.split('.',1))
        valorpago = row[12]
        if not valorpago:
            valorpago = None 
        else:
            if len(valorpago.split('.')) > 2:
                valorpago = ''.join(valorpago.split('.',1))
        desconto = 0.00
        codigo_carne = row[15]
        linha_digitavel = row[16]
        codigo_barras = row[17]        
        ativo = row[18]
        plano_conta = row[19].split('-')[0].strip()
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
            try:
                usuario_b = authmodels.User.objects.get(username__iexact=row[22].strip().lower())
            except:
                usuario_b = usuario_default
        tarifas = row[20]
        local_pagamento = row[21]
        try:
            centrodecusto = fmodels.CentrodeCusto.objects.get(codigo=plano_conta)
        except:
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
                         'observacao': plano_conta}
                print dados
                try:
                    titulo = fmodels.Titulo(**dados)
                    titulo.save()
                    titulo.data_documento=data_documento
                    titulo.save()
                except Exception as e:
                    print e




