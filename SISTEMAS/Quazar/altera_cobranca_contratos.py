import csv
from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels

with open('/tmp/quazar-titulos-banco-convencional-id-06-sem-duplicidade.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login = row[0].strip().lower()
        try:
            id_cliente=admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login)[0].id
            if admmodels.ClienteContrato.objects.filter(cliente__id=id_cliente).count() > 1:
                cobranca= fmodels.Cobranca.objects.filter(clientecontrato__servicointernet__login=login)[0]
                fmodels.Titulo.objects.filter(usuario_g__username='sgp',numero_documento=row[2], nosso_numero=row[2], cliente=admmodels.Cliente.objects.filter(id=id_cliente)).update(cobranca=cobranca.id)
                print('Atualizando o titulo: ',fmodels.Titulo.objects.filter(usuario_g__username='sgp',numero_documento=row[2], nosso_numero=row[2], cliente=admmodels.Cliente.objects.filter(id=id_cliente)[0].id), 'com a cobrança', cobranca)
        except Exception as e:
            continue