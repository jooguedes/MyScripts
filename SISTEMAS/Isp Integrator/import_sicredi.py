
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import re
import sys

tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=1)
#nosso_numero = tf.getNossoNumero(portador) +
usuario = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n)
def formatar_data(dt):
    d,m,y = dt.split('/')
    if len(y) == 2:
        if int(y) >= 0 and int(y) <= 16:
            y = '20%s' %y
        else:
            y = '19%s' %y
    return '%s-%s-%s' %(y,m,d)

#portador.titulo_set.all().delete()
with open('/tmp/Conv-titulos-sicredi.csv', 'rb') as csvfile:
  conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
  for row in conteudo:    
    try:
        nome=row[4]
        try:
            print('esse é o nome: ', nome)
            servico = admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__pessoa__nome__lower=nome.lower())
        except Exception as e:
            print('nao achei cpfcnpj %s : %s' %(nome,e))
            continue

        print('esse é o servico', servico)
        contrato = admmodels.ClienteContrato.objects.get(servicointernet__id=servico[0].id)
        cobranca = contrato.cobranca
        cliente = contrato.cliente
        print('dados do contrato, cobranca e cliete',contrato, cobranca, cliente)
        usuario = authmodels.User.objects.get(username='sgp')
        print('usuario: ', usuario)
        descricao = ''
        nosso_numero_f = None
        data_documento = formatar_data(row[5])
        data_vencimento = formatar_data(row[6])
        data_pagamento = None
        status=row[9]
        
        data_cancela = None
        valor = float(row[7].replace(',', '.').strip())

        if 'BAIXADO POR SOLICITACAO' in status:
            data_pagamento = None
            data_baixa = None 
            status = fmodels.MOVIMENTACAO_CANCELADA
            usuario_b = None 
            data_cancela = data_vencimento
            usuario_c=usuario
    
        elif 'LIQUIDADO COMPE' in status:
            data_pagamento = data_vencimento
            data_baixa = data_vencimento
            status = fmodels.MOVIMENTACAO_PAGA
            usuario_b = usuario
            valorpago=float(row[8].replace(',', '.').strip())

        else:
            status =  fmodels.MOVIMENTACAO_GERADA
            usuario_g = usuario 
            data_baixa = None
            data_pagamento =None
            valorpago=None

        numero_documento = fnum(row[1])
    
        nosso_numero = row[2].split('/')[1].split('-')[0]
        desconto = 0.00
        linha_digitavel = ''
        codigo_barras = ''
        codigo_carne = ''

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
                        'observacao': codigo_carne
                        }
                #print dados
                print("Importando boleto",cliente,nosso_numero,data_vencimento,portador, data_pagamento)
                try:
                    titulo = fmodels.Titulo(**dados)
                    titulo.save()
                    nosso_numero_f = titulo.getNossoNumero()
                    if nosso_numero_f:
                        titulo.nosso_numero_f = re.sub('[^0-9A-Z]', '', nosso_numero_f) 
                    titulo.data_documento=data_documento
                    titulo.data_alteracao=data_documento
                    titulo.save()
                    titulo.updateDadosFormatados()
                except Exception as e:
                    print("Erro cadastrar",e,dados)
    except Exception as a:
        print(a)