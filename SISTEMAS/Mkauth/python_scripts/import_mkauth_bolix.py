from apps.financeiro import models as fmodels
from datetime import timedelta
import requests
import csv 
import re

fnum = lambda n: re.sub('[^0-9]','',n)

SAVE = True

with open('/tmp/mkauth-dados-pix-gerencianet.csv.utf8') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        n_documento = 14785
        PORTADOR = 2
        ID_GATEWAY = 2
        n_numero = 00030390000000008025
        brcode = '00020101021226990014BR.GOV.BCB.PIX2577qrcodes-pix.gerencianet.com.br/bolix/v2/cobv/e729c39b95dc4bebb9a0cc149be65c345204000053039865802BR5914GERENCIANET SA6010OURO PRETO62070503***63048C33'

        print(n_documento, PORTADOR, ID_GATEWAY)
        try:
            titulo = fmodels.Titulo.objects.get(numero_documento=n_documento,
                                                portador=PORTADOR)
            
            if titulo and 'gerencianet' in brcode:
                idTransacao = '%s_%s'%(ID_GATEWAY, fmodels.TituloGateway.objects.get(titulo=titulo).idtransacao)
                tgpix = fmodels.TituloGatewayPix()
                tgpix.gateway = fmodels.GatewayPagamento.objects.get(id=ID_GATEWAY)
                tgpix.titulo = titulo
                tgpix.idtransacao = idTransacao
                tgpix.link = None
                tgpix.data_expiracao = titulo.getVencimento() + timedelta(60)
                tgpix.data_vencimento = titulo.getVencimento()
                tgpix.chave_referencia = idTransacao
                tgpix.dados = brcode
                print(tgpix)
                if SAVE:
                    try:
                        tgpix.save()
                    except Exception as e:
                        print('Erro ao cadastrar pix, erro: ', e)

        except Exception as e:
            print(e)





from apps.financeiro import models as fmodels
from datetime import timedelta

n_documento = 12629
PORTADOR = 2
ID_GATEWAY = 2
brcode = '00020101021226990014BR.GOV.BCB.PIX2577qrcodes-pix.gerencianet.com.br/bolix/v2/cobv/aca4480094954c45ba8b67ae7080be1e5204000053039865802BR5914GERENCIANET SA6010OURO PRETO62070503***6304349D'

print(n_documento, PORTADOR, ID_GATEWAY)
try:
    titulo = fmodels.Titulo.objects.get(numero_documento=n_documento,
                                        portador=PORTADOR)
    
    if titulo and 'gerencianet' in brcode:
        idTransacao = '%s_%s'%(ID_GATEWAY, fmodels.TituloGateway.objects.get(titulo=titulo).idtransacao)
        tgpix = fmodels.TituloGatewayPix()
        tgpix.gateway = fmodels.GatewayPagamento.objects.get(id=ID_GATEWAY)
        tgpix.titulo = titulo
        tgpix.idtransacao = idTransacao
        tgpix.link = None
        tgpix.data_expiracao = titulo.getVencimento() + timedelta(60)
        tgpix.data_vencimento = titulo.getVencimento()
        tgpix.chave_referencia = idTransacao
        tgpix.dados = brcode
        print(tgpix)
        try:
            tgpix.save()
        except Exception as e:
            print('Erro ao cadastrar pix, erro: ', e)
except Exception as e:
            print(e)