from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import sys
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')
usuario = authmodels.User.objects.get(username='sgp')
for cob in fmodels.Cobranca.objects.all():
    titulos = cob.titulo_set.filter(data_pagamento__isnull=True,data_cancela__isnull=True,carnetitulo__isnull=True).order_by('data_vencimento')
    if titulos:
        new_carne = fmodels.Carne()
        new_carne.cobranca=cob
        new_carne.usuario=usuario
        new_carne.save()
        for t in titulos.order_by('data_vencimento'):
            new_carne_t = fmodels.CarneTitulo()
            new_carne_t.carne=new_carne
            new_carne_t.titulo=t
            new_carne_t.save()
        new_carne.data_cadastro=titulos[0].data_documento
        new_carne.data_alteracao=titulos[0].data_documento
        new_carne.save()


carnes = open('/opt/carnes.txt','r').readlines()
portador = fmodels.Portador.objects.get(pk=1)

for c in carnes:
    d = c.strip().split(',')
    link_gnet = d[1]
    id_gnet = d[2]
    cd,cm,ca = d[3].split('/')
    data_emissao = datetime(int(ca),int(cm),int(cd),0,0,1)
    login = d[4]
    codigo_carne = d[5]
    for carne in fmodels.Carne.objects.filter(carnetitulo__titulo__observacao=codigo_carne).distinct():
        print carne,data_emissao,codigo_carne,link_gnet,id_gnet
        carne.data_cadastro=data_emissao
        carne.data_alteracao=data_emissao
        carne.save()
        novo_carnegateway = fmodels.CarneGateway()
        novo_carnegateway.carne = carne 
        novo_carnegateway.gateway = portador.gateway_boleto
        novo_carnegateway.link=link_gnet
        novo_carnegateway.idtransacao=id_gnet
        novo_carnegateway.save()
        parcela = 1
        titulos = list(carne.titulos.all().order_by('data_vencimento'))
        for i in range(len(titulos)):
            titulo = titulos[i]
            novo_titulogateway = fmodels.TituloGateway()
            novo_titulogateway.titulo = titulo
            novo_titulogateway.gateway = portador.gateway_boleto
            novo_titulogateway.idtransacao=None
            titulo.parcela = parcela
            titulo.save()
            novo_titulogateway.save()
            parcela +=1

