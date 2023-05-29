from apps.atendimento import models as amodels
from datetime import datetime
import csv
with open('/opt/importacao/arquivos_importacao/suporte.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in conteudo:
        numero = int(row[0])+200
        print(int(row[0])+200)
        print(row[2])
        print(amodels.Ocorrencia.objects.filter(numero=numero))
        if row[2] == 'ABERTO':
            amodels.Ocorrencia.objects.filter(numero=numero).update(status=amodels.OCORRENCIA_ABERTA, data_finalizacao=None)
        if row[2] =='FECHADO':
            try:
                amodels.Ocorrencia.objects.filter(numero=numero).update(status=amodels.OCORRENCIA_ENCERRADA, data_finalizacao = row[5])
            except Exception as e:
                amodels.Ocorrencia.objects.filter(numero=numero).update(status=amodels.OCORRENCIA_ENCERRADA, data_finalizacao = datetime.now() )
