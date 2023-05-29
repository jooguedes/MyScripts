from apps.financeiro import models as fmodels
from datetime import timedelta
import csv 
import re

fnum = lambda n: re.sub('[^0-9.]','',n)

SAVE = True

with open('/tmp/quazar-titulos-pix.csv.utf8') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        with open('/tmp/pix-txids.csv') as csvfile:
            conteudo2 = csv.reader(csvfile, delimiter='|', quotechar='"')
            for row2 in conteudo2:
                if row[26] == row2[0]:
                    n_documento = fnum(row[2])
                    portador = 3
                    idGateway = 2
                    n_numero = fnum(row[2])
                    idtransacao = row2[1]
                    link = None
                    dados = row2[0]
                    print(n_documento, portador, idGateway, idtransacao)
                    try:
                        titulo = fmodels.Titulo.objects.get(numero_documento=n_documento,
                                                            portador=portador)
                        
                        if titulo and dados.strip() != '':
                            tgpix = fmodels.TituloGatewayPix()
                            tgpix.gateway = fmodels.GatewayPagamento.objects.get(id=idGateway)
                            tgpix.titulo = titulo
                            tgpix.idtransacao = idtransacao
                            tgpix.link = link
                            tgpix.data_expiracao = titulo.getVencimento() + timedelta(365)
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