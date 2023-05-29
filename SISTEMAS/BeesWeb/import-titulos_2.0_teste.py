
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
fnum2 = lambda n: re.sub('[^0-9]','',n) 
#portador.titulo_set.all().delete()
with open('/tmp/Conv-cobrancas-beesweb.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        print(row)
        if not row[0]:
            continue 
        
        servico = None
        cpfcnpj= fnum(row[2])
        if len(cpfcnpj) < 11:
            cpfcnpj = '0%s'%cpfcnpj

        if len(cpfcnpj) < 11:
            cpfcnpj = '0%s'%cpfcnpj
        try:
            cliente = admmodels.Cliente.objects.filter(Q(pessoa__cpfcnpj__numfilter=cpfcnpj)).order_by('-id')
            if not cliente:
                print 'nao achei Cliente %s' %row[1].strip().lower()
                
            if cliente:
                cliente = cliente[0]
                contrato = cliente.clientecontrato_set.all()
                contrato = contrato[0]
                cobranca = contrato.cobranca
                usuario = authmodels.User.objects.get(username='sgp')
                descricao = row[12]
                nosso_numero_f = None
                d,m,y = row[6].split('/')
                data_vencimento = '%s-%s-%s' %(y,m,d)
                d,m,y = row[15].split('/')
                data_documento = '%s-%s-%s' %(y,m,d)
                data_pagamento = None
                data_cancela = None
                usuario_b = None
                data_baixa = None
                valorpago = None
                status = fmodels.MOVIMENTACAO_GERADA
                valor = row[7].replace(',','.')
                observacao = None
                if row[9]:
                    d,m,y = row[9].split('/')
                    data_pagamento = '%s-%s-%s' %(y,m,d)
                    valorpago = row[8].replace(',', '.')
                    status =  fmodels.MOVIMENTACAO_PAGA
                    usuario_b = usuario 
                    data_baixa = data_pagamento 
                    observacao = ''
                numero_documento = row[0]
                nosso_numero = numero_documento            
                desconto = 0.00
                linha_digitavel = None 
                codigo_barras = None
                djson = {'link': row[14]}
                
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
                                 'nosso_numero_f': nosso_numero,
                                 'linha_digitavel': linha_digitavel,
                                 'codigo_barras': codigo_barras,
                                 'valor': valor,
                                 'valorpago': valorpago,
                                 'desconto': desconto,
                                 'status': status,
                                 'observacao': observacao,
                                 'djson': djson
                                 }
                        #print dados
                        print "Importando boleto",cliente,nosso_numero,data_vencimento,portador
                        try:
                            titulo = fmodels.Titulo(**dados)
                            titulo.save()
                            titulo.data_documento=data_documento

                        except Exception as e:
                            print "Erro cadastrar",e,dados

                    if ('juno' in titulo.djson.get('link') or 'boletofacil' in titulo.djson.get('link') or 'gerencianet' in titulo.djson.get('link') or 'widepay' in titulo.djson.get('link')) and titulo.portador.gateway_boleto:
                        if 'gerencianet' in titulo.djson.get('link') or 'fortunus' in titulo.djson.get('link'):
                            if (len(str(titulo.djson.get('link')).split('emissao')[1].split('/')) < 4 or 'lote' in titulo.djson.get('link')):
                                print('Link referente ao carnê e não ao boleto!')
                                break
                        if ('juno' in titulo.djson.get('link') or 'boletofacil' in titulo.djson.get('link')):
                            if not 'boleto.pdf' in titulo.djson.get('link'):
                                print('Link referente ao carnê e não ao boleto!')
                                break
                        
                        titulogateway = fmodels.TituloGateway()
                        titulogateway.titulo = titulo
                        titulogateway.gateway = titulo.portador.gateway_boleto
                        titulogateway.link = titulo.djson.get('link')
                        titulogateway.idtransacao = numero_documento
                        titulogateway.save()
        except Exception as a:
            print(a)
