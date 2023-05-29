from apps.financeiro import models as fmodels
from apps.admcore import models as admodels
import csv


from apps.admcore import models as admmodels
from django.db.models import Q, Max
with open('/tmp/Conv-gerencianet-atuallink.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        codigo_barras=row[15]
        try:
            titulo=fmodels.Titulo.objects.filter(titulogateway__idtransacao=row[0], usuario_g__username='sgp', linha_digitavel=None, codigo_barras=None )
            fmodels.Titulo.objects.filter(titulogateway__idtransacao=row[0], usuario_g__username='sgp', linha_digitavel=None, codigo_barras=None ).update(linha_digitavel=codigo_barras, codigo_barras=codigo_barras)
            print('Atualizando: ', titulo)
        except Exception as e:
            print(e)
        #print(cobranca)