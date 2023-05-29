from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
from django.db.models import Q
import csv
import re
import sys
from datetime import date, datetime, timedelta
tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=1)
fnum = lambda n: re.sub('[^0-9.]','',n) 
formapagamento = fmodels.FormaPagamento.objects.all()[0]
with open('/opt/titulos-2021-09-0910.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        print(row)
        cpfcnpj = row[10] or row[11]
        cliente = normalize('NFKD', unicode(row[9])).encode('ASCII','ignore')
        cobranca = None
        if cpfcnpj.strip():
            contrato = admmodels.ClienteContrato.objects.filter(Q(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj)|
                                                                Q(cliente__pessoa__nome__unaccent__trim__lower=cliente.strip().lower()))
        else:
            contrato = admmodels.ClienteContrato.objects.filter(Q(cliente__pessoa__nome__unaccent__trim__lower=cliente.strip().lower()))
        if contrato:
            cobranca = contrato[0].cobranca
            clientecontrato = contrato
        if cobranca:
            cobranca = cobranca
            cliente = cobranca.cliente
            usuario = authmodels.User.objects.get(username='sgp')
            descricao = 'Fatura %s' %row[0]
            nosso_numero_f = None                
            d_,m_,a_ = row[1].split('/')
            data_vencimento = date(int(a_),int(m_),int(d_))
            if row[3]:
                d_,m_,a_ = row[3].split('/')
                data_documento = date(int(a_),int(m_),int(d_))
            else:
                data_documento = data_vencimento
            #data_vencimento = row[0].split(' ')[0]
            data_pagamento = None
            data_baixa = None
            data_cancela = None
            status = fmodels.MOVIMENTACAO_GERADA
            usuario_b = None
            usuario_c = None
            formapag = None
            numero_documento = row[0]
            #nosso_numero = numero_documento 
            nosso_numero = row[0]
            valor = row[4].replace("'","").replace('.','').replace(',','.')
            valorpago = row[7].replace("'","").replace('.','').replace(',','.')
            print('ok1')
            if not valorpago:
                valorpago = None
            if row[8] == 'Liquidada':
                print('ok2',row[2])
                d_,m_,a_ = row[2].split('/')
                data_pagamento = date(int(a_),int(m_),int(d_))
                data_baixa = data_pagamento
                status = fmodels.MOVIMENTACAO_PAGA
                usuario_b = usuario
                formapag = formapagamento
                print('ok2 fim')
            if row[8] in ['Cancelada','Isenta']:
                print('ok3', row[8])
                data_pagamento = None
                data_baixa = None
                status = fmodels.MOVIMENTACAO_CANCELADA
                usuario_c = usuario
                formapag = None
                data_cancela = data_vencimento
            desconto = 0.00
            linha_digitavel = None
            codigo_barras = None
            codigo_carne = None
            print('ok4', nosso_numero)
            if nosso_numero:
                if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                    print('ok3')
                    dados = {'cliente': cliente,
                             'cobranca': cobranca,
                             'portador': portador,
                             'formapagamento': formapag,
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
                             }
                    print(dados)
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
                    except Exception as e:
                        print "Erro cadastrar",e,dados