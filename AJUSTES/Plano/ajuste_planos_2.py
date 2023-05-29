from apps.admcore import models as admmodels
import csv 
import re

diasParaAviso = 1
diasParaReduzir = 0
diasParaBloqueio = 4
caminho_arquivo = '/opt/daxinternet/ixc-planos.csv.utf8'

fnum = lambda n: re.sub('[^0-9]','',n) 

with open(caminho_arquivo, 'rb') as csvfile:
  conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
  for row in conteudo:
    plano = row[1].strip()
    download = int(fnum(row[2]))
    upload = int(fnum(row[3]))
    if 'M' in row[2]:
      modo_velocidade = 'mb'
      download = download*1024
      upload = upload*1024
    else:
      modo_velocidade = 'kb'
    
    try:
      admmodels.PlanoInternet.objects \
        .filter(plano__descricao__upper__iexact=plano.strip().upper()) \
              .update(modo_velocidade=modo_velocidade,
                      download=download,
                      upload=upload,
                      diasparaaviso=diasParaAviso,
                      diasparareduzir=diasParaReduzir,
                      diasparabloqueio=diasParaBloqueio)
      print(plano, download, upload)
    except:
      continue