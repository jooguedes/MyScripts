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
portador = fmodels.Portador.objects.get(pk=1)
usuario = authmodels.User.objects.get(username='sgp')
with open('/opt/controllr-titulos-3-removidos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in conteudo:
        print row
        try:
            servico = admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=row[1].strip().lower())[0]
        except:
            continue
        #if '-' in row[13]:
        #    portador = fmodels.Portador.objects.get(id=3)
        #else:
        #    portador = fmodels.Portador.objects.get(id=4)
        #if fmodels.TituloGateway.objects.filter(idtransacao=row[13]).count() > 0:
        #    continue 
        contrato = servico.clientecontrato
        cobranca = contrato.cobranca
        cliente = contrato.cliente        
        descricao = unicode(row[5].decode('latin-1'))
        nosso_numero_f = None
        data_documento = row[6]
        data_vencimento = row[7].split(' ')[0]
        data_pagamento = row[8]
        formapagamento = None
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
            formapagamento = fmodels.FormaPagamento.objects.all()[0]
        numero_documento = row[9]
        #nosso_numero = row[9]
        #nosso_numero = tf.getNossoNumero(portador) + 1
        #nosso_numero_f = row[9]
        nosso_numero = row[10]
        nosso_numero_f = nosso_numero
        #if not nosso_numero:
        #    numero_documento = numero_documento
        #    nosso_numero_f = numero_documento
        valor = row[11]
        if len(valor.split('.')) > 2:
            valor = ''.join(valor.split('.',1))
        valorpago = row[12]
        if not valorpago:
            valorpago = None 
        else:
            if len(valorpago.split('.')) > 2:
                valorpago = ''.join(valorpago.split('.',1))
        if not valor:
            valor='0.00'
        desconto = 0.00
        linha_digitavel = None
        codigo_barras = None
        codigo_carne = '%s|%s|%s' %(row[15].strip() or '',row[14].strip() or '',row[13].strip() or '')
        #if not nosso_numero:
        #    print(row)
        if numero_documento and nosso_numero:
            print(numero_documento,nosso_numero,data_vencimento)
            dados = {'cliente': cliente,
                     'cobranca': cobranca,
                     'portador': portador,
                     'formapagamento': formapagamento,
                     'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                     'modogeracao': 'l',
                     'usuario_g': usuario,
                     'usuario_b': usuario_b,
                     'demonstrativo': descricao,
                     'data_documento': data_documento,
                     'data_alteracao': data_documento,
                     'data_vencimento': data_vencimento,
                     'data_pagamento': data_pagamento,
                     'data_cancela': data_pagamento or data_vencimento,
                     'usuario_c': usuario,
                     'status': fmodels.MOVIMENTACAO_CANCELADA,
                     'data_baixa': data_baixa,
                     'numero_documento': numero_documento,
                     'nosso_numero': nosso_numero,
                     'nosso_numero_f': nosso_numero_f,
                     'linha_digitavel': linha_digitavel,
                     'codigo_barras': codigo_barras,
                     'valor': valor,
                     'valorpago': valorpago,
                     'desconto': desconto,
                     'djson': {'data_credit': data_pagamento, 'valorpago': valorpago,'removido_controllr': 'sim' },
                     'observacao': 'titulo removido no controllr'
                     }
            if portador.titulo_set.filter(portador=portador,numero_documento=numero_documento).count() == 0:
            #if fmodels.Titulo.objects.filter(portador=portador,nosso_numero=nosso_numero).count() == 0:
                print(dados)
                titulo = fmodels.Titulo(**dados)
                titulo.save()

            #Descomentar quando for gerencianet
            #if portador.titulo_set.filter(portador=portador,numero_documento=numero_documento).count() == 0:
            #    if portador.titulo_set.filter(portador=portador,nosso_numero=numero_documento).count() > 0:
            #        continue 
            #    print dados
            #    titulo = fmodels.Titulo(**dados)
            #    titulo.save()
            #elif portador.titulo_set.filter(portador=portador,numero_documento=numero_documento).count() == 1:
            #    portador.titulo_set.filter(portador=portador,numero_documento=numero_documento).update(observacao=codigo_carne)
#


from apps.cauth import models as authmodels
from apps.financeiro import models as fmodels
from django.db.models import Q 
for t in fmodels.Titulo.objects.filter(titulogateway__isnull=True,observacao__icontains='gerencianet'):
    if t.portador.gateway_boleto:
        dados = t.observacao.split('|')
        link = dados[0]
        idtransacao = dados[2]
        #print dados
        print dados
        fmodels.TituloGateway.objects.filter(titulo=t).update(idtransacao=idtransacao,link=link)
        novo_titulogateway = fmodels.TituloGateway()
        novo_titulogateway.titulo = t
        novo_titulogateway.gateway = t.portador.gateway_boleto
        novo_titulogateway.idtransacao = idtransacao
        novo_titulogateway.link = link 
        novo_titulogateway.save()
        print(t)

carnes=[]
usuario = authmodels.User.objects.get(username='sgp')
for t in fmodels.Titulo.objects.filter(Q(titulogateway__link__contains='lote')|Q(titulogateway__link__contains='carne'),
                                       Q(titulogateway__isnull=False),
                                       Q(carnetitulo__carne__carnegateway__isnull=True)):
    dados = t.observacao.split('|')
    print dados
    if len(dados) > 2:
        if 'carne' in dados[0] or 'lote' in dados[0]:
            dados_dict = {'id':dados[2],'link': dados[0],'cobranca': t.cobranca}
            if dados_dict not in carnes:
                carnes.append(dados_dict)

for carne in carnes:
    titulos = fmodels.Titulo.objects.filter(cobranca=carne.get('cobranca'),observacao__startswith='%s|' %carne['link'],observacao__endswith='|%s' %carne['id']).order_by('data_vencimento').distinct()
    if titulos:
        parcela = 1
        new_carne = fmodels.Carne()
        if not carne.get('cobranca'):
            continue
        new_carne.cobranca = carne['cobranca']
        new_carne.usuario = usuario
        new_carne.save()
        for t in titulos:
            try:
                fmodels.CarneTitulo.objects.create(carne=new_carne,titulo=t)
                fmodels.Titulo.objects.filter(id=t.id).update(parcela=parcela)
                parcela += 1
            except:
                print t
        new_carne_gateway = fmodels.CarneGateway()
        new_carne_gateway.carne=new_carne
        new_carne_gateway.carne = new_carne
        new_carne_gateway.gateway = t.portador.gateway_boleto
        new_carne_gateway.link = carne['link']
        new_carne_gateway.idtransacao = carne['id']
        new_carne_gateway.save()



