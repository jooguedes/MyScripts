from apps.admcore import models

import csv
with open('/tmp/quazar-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        status=row[36]

        login=row[26]
        if status=='1':
            print('Atualizando status do contrato:', models.ClienteContrato.objects.filter(servicointerne__login=login)[0].id , 'Cliente: ', models.ClienteContrato.objects.filter(servicointernet__login=login)[0].cliente.pessoa.nome)
            '''models.ClienteContratoStatus.objects.filter(clientecontrato__servicointernet__login=login, status=3).update(status=1)'''