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
portador = fmodels.Portador.objects.get(pk=4)
with open('/opt/vigo-titulosBANCO5-cancelados.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            servico = admmodels.ServicoInternet.objects.get(clientecontrato__id=row[1])
        except:
            continue 
        data_cancela = None
        usuario_c = usuario_default 
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        descricao = row[5]
        nosso_numero_f = None
        data_documento = row[6]
        data_vencimento = row[7].split(' ')[0]
        data_cancela = data_vencimento
        data_pagamento = row[8]
        numero_documento = row[9]
        if portador.codigo_banco == '104':
            nosso_numero = row[10][2:].split('-')[0]
        else:
            nosso_numero = row[10].split('-')[0]
        nosso_numero_f = row[10].replace('-','')
        if not nosso_numero:
            nosso_numero = numero_documento
            nosso_numero_f = numero_documento 
        valor = row[11]
        if len(valor.split('.')) > 2:
            valor = ''.join(valor.split('.',1))
        valorpago = None
        desconto = 0.00
        codigo_carne = row[15]
        linha_digitavel = row[16]
        codigo_barras = row[17]        
        ativo = row[18]
        plano_conta = row[19].split('-')[0].strip()
        data_pagamento = None
        data_baixa = None 
        status = fmodels.MOVIMENTACAO_CANCELADA
        usuario_b = None 
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
                         'formapagamento': None,
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
                except:
                    pass




