from apps.admcore import models as admmodels
import csv

nao_atualizados = []

with open('/tmp/ajuste_planos.csv', 'rb') as csvfile:
  conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
  for row in conteudo:
    plano = row[1].strip()
    download = int(row[6].replace('K', ''))
    upload = int(row[5].replace('K', ''))
    try:
      print (admmodels.PlanoInternet.objects \
        .filter(plano__descricao__lower__iexact=plano.lower()) \
          .update(download=download,
                  upload=upload))
    except:
      nao_atualizados.append(plano)
      continue

print('Planos não atualizados: ')
for na in nao_atualizados:
  print(na)