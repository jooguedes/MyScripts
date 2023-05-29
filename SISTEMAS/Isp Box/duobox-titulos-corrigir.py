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
portador = fmodels.Portador.objects.get(id=1)
usuario = authmodels.User.objects.get(username='sgp')
ccusto = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
fpagamento = fmodels.FormaPagamento.objects.all()[0]
c_ = 0
with open('/opt/upnet/duobox-titulos-cancelados.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        c_ += 1 
        print(c_)
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
        if row[13]:
            titulo = fmodels.Titulo.objects.filter(titulogateway__idtransacao=row[13])
        else:
            titulo = fmodels.Titulo.objects.filter(cliente__id=row[0],
                                                   cobranca__clientecontrato__id=row[1],
                                                   data_documento__date=data_documento.split()[0],
                                                   data_vencimento=data_vencimento,
                                                   valor=valor)
        if titulo:
            titulo = titulo[0]
            print(titulo,row)
            #if str(titulo.cliente.id) != row[0]:
            #    cliente = admmodels.Cliente.objects.filter(id=row[0])
            #    if cliente:
            #        cliente = cliente[0]
            #        if cliente.getCPFCNPJNumero() == titulo.cliente.getCPFCNPJNumero():
            #            print('SGP',titulo.cliente.id,titulo.cliente.getNome())
            #            print('ISP',cliente.id,cliente.getNome())
            #            print('DEFINIR CLIENTE',cliente)
            #            print('verificar contrato %s' %row[1])
            #            contrato = cliente.clientecontrato_set.filter(id=row[1])
            #            if contrato:
            #                titulo.cliente=cliente
            #                titulo.cobranca=contrato[0].cobranca
            #                titulo.save()
            if not titulo.data_pagamento:
                if data_cancela:
                    print('SGP',titulo.cliente.id,str(titulo.data_documento).split()[0],str(titulo.data_vencimento),str(titulo.valor))
                    print('ISP',row[0],data_documento.split()[0],data_vencimento,valor)
                    print(titulo.cliente)
                    print('CORRIGIR PARA DEFINIR CANCELADO NO SGP')
                    print(row[10])
                    print(row)
                    tc = titulo
                    tc.motivocancela=row[10]
                    tc.data_cancela=data_cancela
                    tc.status=fmodels.MOVIMENTACAO_CANCELADA
                    tc.usuario_c=usuario
                    tc.save()
                elif not data_cancela:
                    print('SGP',titulo.cliente.id,str(titulo.data_documento).split()[0],str(titulo.data_vencimento),str(titulo.valor))
                    print('ISP',row[0],data_documento.split()[0],data_vencimento,valor)
                    print(titulo.cliente)
                    print('CORRIGIR PARA DEFINIR PAGO NO SGP')
                    tb = titulo
                    tb.data_pagamento=data_pagamento
                    tb.data_baixa = data_baixa
                    tb.status=fmodels.MOVIMENTACAO_PAGA
                    tb.usuario_b=usuario
                    tb.save()            


print('ok')




