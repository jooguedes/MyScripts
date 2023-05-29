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
portador = fmodels.Portador.objects.get(pk=1)
fnum = lambda n: re.sub('[^0-9.]','',n) 
with open('/tmp/mkauth-titulos-1.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            print(row)
            if not row[0]:
                continue 
            if len(row) < 5:
                continue 

            ilike = '%'.join(row[1].strip().lower().split())
            servico = None
            try:
                servico = admmodels.ServicoInternet.objects.filter(Q(clientecontrato__cliente__pessoa__nome__unaccent__ilike='%%%s%%' %ilike))
                if not servico:
                    print 'nao achei Cliente %s' %row[1].strip().lower()
                    continue
                if servico:
                    servico = servico[0]
                    #print servico
                    #portador = servico.clientecontrato.cobranca.portador
                    contrato = servico.clientecontrato
                    cobranca = contrato.cobranca
                    cliente = contrato.cliente
                    usuario = authmodels.User.objects.get(username='sgp')
                    descricao = unicode(row[4].decode('latin-1'))
                    nosso_numero_f = None
                    d,m,y = row[6].split('/')
                    data_vencimento = '%s-%s-%s' %(y,m,d)
                    data_documento = data_vencimento
                    data_pagamento = None
                    data_cancela = None
                    usuario_b = None
                    data_baixa = None
                    valorpago = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valor = float(row[8].replace(',','.'))
                    observacao = None
                    if row[7]:
                        d,m,y = row[7].split('/')
                        data_pagamento = '%s-%s-%s' %(y,m,d)
                        valorpago = fnum(row[9])
                        status =  fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario 
                        data_baixa = data_pagamento 
                        if len(row) > 10:
                            observacao = 'Local pagamento %s' %row[10]
                        else:
                            observacao = ''
                    numero_documento = row[0]
                    nosso_numero = numero_documento    
                    print("esse é nosso numero",nosso_numero) 
                    #nosso_numero = row[1]       
                    desconto = 0.00
                    linha_digitavel = None 
                    codigo_barras = None
                    
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
                                     'linha_digitavel': linha_digitavel,
                                     'codigo_barras': codigo_barras,
                                     'valor': valor,
                                     'valorpago': valorpago,
                                     'desconto': desconto,
                                     'status': status,
                                     'observacao': observacao
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
                print a
        except Exception as e:
            print(e)