from apps.financeiro import models as fmodels
from apps.fiscal import models as fismodels
import re

fnum = lambda n: re.sub('[^0-9]','',n) 

arq = open("/tmp/notafiscaltitulos.txt")
linhas = arq.readlines()
for linha in linhas:
    linha = linha.split('VALUES')[1]
    id = fnum(str(linha).split(',')[0])
    notafiscal_id = fnum(str(linha).split(',')[1])
    titulo_id = fnum(str(linha).split(',')[2])
    print(id,notafiscal_id,titulo_id)
    try:
        nftitulo=fismodels.NotaFiscalTitulo.objects.filter(notafiscal__id=notafiscal_id)
        for nt in nftitulo:
            titulo_id=int(titulo_id) + 20035
            fismodels.NotaFiscalTitulo.objects.filter(id=nt.id).update(titulo=titulo_id)
            print(nt, titulo_id)
    except Exception as e:
            print(e)