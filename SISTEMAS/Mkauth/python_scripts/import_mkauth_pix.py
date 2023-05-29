from apps.financeiro import models as fmodels
from datetime import timedelta
import requests
import csv 
import re

fnum = lambda n: re.sub('[^0-9]','',n)

SAVE = True

def consultar_txid(BRCODE):
        brcode = BRCODE
        dados = {}
        pos = 0

        while pos < len(brcode):
            chave = str(brcode[pos:pos+2])
            pos += 2
            size = str(brcode[pos:pos+2])
            pos +=2
            _size = int(size)
            data = str(brcode[pos:pos+_size])
            pos += _size
            dados[chave] = data
        payload = 'None'
        response = requests.get("https://"+dados['26'][22:])

        if response.status_code == 200:
            payload = response.text.split('.')[1]

            for i in range(3):
                try:
                    pad = ''.ljust(i,'=')
                    payload = b64decode(payload+pad).decode('utf-8')
                    break
                except Exception as e:
                    pass
        try:
            payload=json.loads(payload)
            return payload
        except:
            return None

with open('/tmp/mkauth-dados-pix-gerencianet.csv.utf8') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        n_documento = fnum(row[6])
        PORTADOR = 2
        ID_GATEWAY = 5
        n_numero = fnum(row[7])
        brcode = row[8]
        link = None
        dados = consultar_txid(brcode)
        print(dados)
        if dados != None:
            idtransacao = dados['txid']
            validadeAposVencimento = dados['calendario']['validadeAposVencimento']
            print(n_documento, PORTADOR, ID_GATEWAY, idtransacao)
            try:
                titulo = fmodels.Titulo.objects.get(numero_documento=n_documento,
                                                    portador=PORTADOR)
                
                if titulo and dados.strip() != '':
                    tgpix = fmodels.TituloGatewayPix()
                    tgpix.gateway = fmodels.GatewayPagamento.objects.get(id=ID_GATEWAY)
                    tgpix.titulo = titulo
                    tgpix.idtransacao = idtransacao
                    tgpix.link = link
                    tgpix.data_expiracao = titulo.getVencimento() + timedelta(validadeAposVencimento)
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