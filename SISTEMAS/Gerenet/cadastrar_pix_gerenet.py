from apps.financeiro import models as fmodels
from datetime import timedelta
import csv 

SAVE = True

with open('/tmp/gerenet-areceber-29.csv.utf8') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        n_documento = int(row[0])
        portador = 1
        idGateway = 1
        n_numero = int(row[5])
        idtransacao = row[18]
        link = row[20]
        dados = row[19]
        try:
            titulo = fmodels.Titulo.objects.get(numero_documento=n_documento,
                                                portador=portador,
                                                nosso_numero=n_numero)
            
            if titulo and row[18].strip() != '':
                tgpix = fmodels.TituloGatewayPix()
                tgpix.gateway = fmodels.GatewayPagamento.objects.get(id=idGateway)
                tgpix.titulo = titulo
                tgpix.idtransacao = idtransacao
                tgpix.link = link
                tgpix.data_expiracao = titulo.getVencimento() + timedelta(60)
                tgpix.data_vencimento = titulo.getVencimento()
                tgpix.chave_referencia = idtransacao
                tgpix.dados = dados
                print(tgpix)
                if SAVE:
                    try:
                        tgpix.save()
                    except Exception as e:
                        print('Erro ao cadastrar pix, erro: ', e)

        except Exception as e:
            print(e)