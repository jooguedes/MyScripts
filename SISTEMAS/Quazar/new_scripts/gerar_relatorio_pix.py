#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests, ast
from base64 import b64decode
import json
import csv
import sys

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

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

erros = []
with open('pix-txids.csv', 'w') as csvfilew:
    values = csv.writer(csvfilew, delimiter='|', quotechar='"')
    values.writerow(['BRCODE', 'TXID', 'VENCIMENTO', 'VALIDADE APÓS VENCIMENOT'])
    with open('quazar-titulos-pix.csv.utf8', 'r') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            brcode = row[26].strip()
            try:
                dados = consultar_txid(brcode)
            except:
                 erros.append(brcode)
                 continue
            if dados != None:
                values.writerow([str(brcode), str(dados['txid']), str(dados['calendario']['dataDeVencimento']), str(dados['calendario']['validadeAposVencimento'])])
            print(dados)
        
print('Lista dos que deram errado')
for e in erros:
     print(e)