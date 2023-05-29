from apps.financeiro import models as fmodels
import csv

PORTADOR_ATUAL = 1
NOVO_PORTADOR = 2

with open('/tmp/titulos-widepay-fernando-santos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        n_documento = row[0]

        try:
            fmodels.Titulo.objects \
                            .filter(portador=PORTADOR_ATUAL, 
                                    numero_documento=n_documento) \
                                    .update(portador=NOVO_PORTADOR)
        except Exception as e:
            print(e)