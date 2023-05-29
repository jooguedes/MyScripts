from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
import csv

with open('/tmp/update-titulos-mkauth.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            cliente = admmodels.Cliente.objects.get(id=row[0])
            titulo = fmodels.Titulo.objects.filter(cliente=cliente, numero_documento=row[1])
            print(cliente, titulo)
            try:
                fmodels.Titulo.objects.filter(cliente=cliente, numero_documento=row[1]).update(valor = row[6])
                if titulo[0].status == fmodels.MOVIMENTACAO_PAGA:
                    titulo[0].valorpago=row[6]
                    titulo[0].save()
            except Exception as e:
                print('Erro ao atualizar valor dos boletos! erro: ', e)
        except Exception as e:
            print(e)