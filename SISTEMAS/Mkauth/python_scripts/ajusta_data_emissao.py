import csv
from apps.financeiro import models

titulos=[]
#nosso_numero_02=''
with open('/tmp/mkauth-titulos-2.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        data_emissao=row[6]
        try:
            models.Titulo.objects.filter(portador=2, numero_documento=row[9]).update(data_documento=data_emissao)
        except Exception as e:
            print(e)