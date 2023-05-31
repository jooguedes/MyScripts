from apps.financeiro import models as fmodels
import csv

PORTADOR_ID = 10

with open('/tmp/ajuste-links-galaxpay.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        idtransacao = row[0]
        link = row[13]
        if len(link) > 5:
            tg = fmodels.TituloGateway.objects.filter(titulo__portador=PORTADOR_ID, link__in=link)
            if len(tg) > 0:
                tg[0].idtransacao = row[0]
                try:
                    tg[0].save()
                    print(link, idtransacao)
                except Exception as e:
                    print(e)
                    break