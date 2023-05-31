from apps.financeiro import models as fmodels
from apps.cauth.models import User
from datetime import date, datetime
from django.db import transaction
import csv

file = '/tmp/beesweb-gnet.csv'
PORTADOR = 2

sgpuser = User.objects.get(username="sgp")
data_cadastro = date.today()

with transaction.atomic():
    with open(file, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for l in conteudo:          
            idtransacao = l[0]
            cliente = l[8]
            carne_parcela = l[19]
            carne_idtransacao = l[20]
            carne_link = l[21]
            if carne_idtransacao and carne_parcela:
                #print(l)
                titulogateway_obj = fmodels.TituloGateway.objects \
                    .filter(idtransacao=idtransacao,
                            titulo__carnetitulo__isnull=True, titulo__portador=PORTADOR) \
                    .first()
                if titulogateway_obj:
                    print ('Cliente: %s, Id: %s' % (cliente, idtransacao))
                    titulo_obj = titulogateway_obj.titulo
                    carne_obj = fmodels.Carne.objects \
                        .filter(carnegateway__idtransacao=carne_idtransacao) \
                        .first()
                    if not carne_obj:
                        if not titulo_obj.cobranca:
                            continue
                        carne_obj = fmodels.Carne.objects \
                            .create(cobranca=titulo_obj.cobranca,
                                    usuario=sgpuser,
                                    data_cadastro=data_cadastro)
                        fmodels.CarneGateway.objects \
                            .create(carne=carne_obj,
                                    gateway=titulogateway_obj.gateway,
                                    link=carne_link.replace('"', ""),
                                    idtransacao=carne_idtransacao)
                    fmodels.CarneTitulo.objects \
                        .create(carne=carne_obj,
                                titulo=titulo_obj)
                    titulo_obj.parcela = carne_parcela
                    titulo_obj.modogeracao = fmodels.MODO_GERA_CARNE_LOTE
                    titulo_obj.save()
        carnesgateways = fmodels.CarneGateway.objects \
            .filter(gateway__nome__icontains="gerencianet",
                    resposta__isnull=True,
                    carne__carnetitulo__titulo__titulogateway__idtransacao__isnull=False).distinct()
        print ("total %s" % carnesgateways.count())
        for carnegateway in carnesgateways:
            charges = []
            for carne_titulo in carnegateway.carne.carnetitulo_set.all():
                titulo = carne_titulo.titulo
                charges.append({
                    "parcel": str(titulo.parcela),
                    "charge_id": titulo.titulogateway.idtransacao
                })
            carnegateway.resposta = {
                "importado": True,
                "data": {
                    "charges": charges
                }
            }
            carnegateway.save()
        print(" --- fim ---")       