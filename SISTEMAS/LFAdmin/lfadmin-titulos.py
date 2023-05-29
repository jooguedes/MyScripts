from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import re
import sys
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=1)
fnum = lambda n: re.sub('[^0-9.]','',n) 
#portador.titulo_set.all().delete()
with open('/opt/lfadmin-titulos.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        print row
        try:
            try:
                servico = admmodels.ServicoInternet.objects.get(login__trim__lower=row[1].strip().lower())
            except Exception as e:
                print 'nao achei login %s : %s' %(row[1].strip().lower(),e)
                continue
            #portador = servico.clientecontrato.cobranca.portador
            contrato = servico.clientecontrato
            cobranca = contrato.cobranca
            cliente = contrato.cliente
            usuario = authmodels.User.objects.get(username='sgp')
            descricao = unicode(row[5].decode('latin-1'))
            nosso_numero_f = None
            data_documento = row[6]
            data_vencimento = row[7].split(' ')[0]
            data_pagamento = row[8]
            data_cancela = None
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
            numero_documento = row[9]
            nosso_numero = numero_documento                                         
            #nosso_numero = str(int(numero_documento) + 600000000000000)
            
            #if row[10]:
            #    if row[10].startswith('24000'):
            #        nosso_numero = row[10][2:].strip()
            #    else:
            #        nosso_numero = row[10].strip()
            #else:
            #    nosso_numero = int(numero_documento)

            #nosso_numero = row[10][0:-1]
            #nosso_numero = row[9]
            #nosso_numero_f = row[10]
            #nosso_numero = int(numero_documento) + 900000001000000
            #nosso_numero_f = str(int(numero_documento) + 1)
            #nosso_numero = int(numero_documento)
            #nosso_numero_f = str(nosso_numero)
            valor = row[19]
            if len(valor.split('.')) > 2:
                valor = ''.join(valor.split('.',1))
            valorpago = fnum(row[12])
            if not valorpago:
                valorpago = None 
            else:
                if len(valorpago.split('.')) > 2:
                    valorpago = ''.join(valorpago.split('.',1))
            desconto = 0.00
            linha_digitavel = row[16]
            codigo_barras = row[17]
            codigo_carne = row[15]

            if data_baixa and data_baixa.startswith('0000-00-00') and valorpago is not None:
                data_baixa = data_vencimento
                data_pagamento = data_vencimento

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



from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import re
import sys

usuario = authmodels.User.objects.get(username='sgp')
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

with open('/opt/intercom01/mkauth-gnet-titulos.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login = row[0]
        numero_documento = row[1]
        chave_gnet = row[2]
        titulos = fmodels.Titulo.objects.filter(numero_documento=numero_documento,
                                                cobranca__clientecontrato__servicointernet__login__trim__lower=login.strip().lower(),
                                                titulogateway__isnull=True)
        if len(titulos) == 1:
            titulo = titulos[0]
            if titulo.portador.gateway_boleto:
                print titulo
                novo_titulogateway = fmodels.TituloGateway()
                novo_titulogateway.titulo = titulo
                novo_titulogateway.gateway = titulo.portador.gateway_boleto
                novo_titulogateway.idtransacao = chave_gnet
                novo_titulogateway.link = '' 
                novo_titulogateway.save()


carnes = {}
with open('/opt/intercom01/mkauth-gnet-carnes.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login = row[0]
        numero_documento = row[1]
        chave_gnet = row[2]
        codigo_carne = row[3]
        titulos = fmodels.Titulo.objects.filter(numero_documento=numero_documento,
                                                cobranca__clientecontrato__servicointernet__login__trim__lower=login.strip().lower())
        if len(titulos) == 1:
            titulo = titulos[0]
            if titulo.portador.gateway_boleto:
                if titulo.cobranca:
                    if codigo_carne not in carnes:
                        carnes[codigo_carne] = [numero_documento]
                    else:
                        carnes[codigo_carne].append(numero_documento)
                    print codigo_carne
                print titulo,chave_gnet
                if not getattr(titulo,'titulogateway',None):
                    novo_titulogateway = fmodels.TituloGateway()
                    novo_titulogateway.titulo = titulo
                    novo_titulogateway.gateway = titulo.portador.gateway_boleto
                    novo_titulogateway.idtransacao = chave_gnet
                    novo_titulogateway.link = '' 
                    novo_titulogateway.save()


for carne in carnes:
    titulos = fmodels.Titulo.objects.filter(numero_documento__in=carnes[carne],carnetitulo__isnull=True).order_by('data_vencimento').distinct()
    if titulos:
        parcela = 1
        new_carne = fmodels.Carne()
        new_carne.cobranca = titulos[0].cobranca
        new_carne.usuario = usuario
        new_carne.save()
        for t in titulos:
            print
            fmodels.CarneTitulo.objects.create(carne=new_carne,titulo=t)
            fmodels.Titulo.objects.filter(id=t.id).update(parcela=parcela)
            parcela += 1
        new_carne_gateway = fmodels.CarneGateway()
        new_carne_gateway.carne=new_carne
        new_carne_gateway.carne = new_carne
        new_carne_gateway.gateway = t.portador.gateway_boleto
        new_carne_gateway.link = ''
        new_carne_gateway.idtransacao = ''
        new_carne_gateway.save()


from apps.financeiro import models as fmodels
gnet = open('/opt/gnet-titulos.txt','r').readlines()
for g in gnet:
    try:
        login,documento,link = g.strip().split(' ')
        fmodels.TituloGateway.objects.filter(titulo__cobranca__clientecontrato__servicointernet__login__iexact=login.strip(),
                                          titulo__numero_documento=documento,
                                          link=''
                                          ).update(link=link)
    except:
        print g
    print link


from apps.financeiro import models as fmodels
gnet = open('/opt/intercom01/gnet-carnes.txt','r').readlines()
for g in gnet:
    print g
    login,documento,carneid,link = g.strip().split(' ')
    chave_id = link.split('/')[-1:][0]
    fmodels.CarneGateway.objects.filter(carne__carnetitulo__titulo__cobranca__clientecontrato__servicointernet__login__trim__lower=login.strip().lower(),
                                        carne__carnetitulo__titulo__numero_documento=documento,
                                        link='',idtransacao=''
                                        ).update(link=link,idtransacao=chave_id)
