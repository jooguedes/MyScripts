from apps.admcore import models
import csv

ALTERAR = False
POP_DESTINO = 1  #Id do pop que os contratos devem ser migrados

count = 0
with open('/tmp/ixc-clientes-filial-1.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            cliente_id = int(row[0])
        except:
            continue
        for c in models.ClienteContrato.objects.filter(cliente__id=row[0]):
            c.pop_id = POP_DESTINO
            try:
                if ALTERAR:
                    c.save()
            except Exception as e:
                print('Erro ao alterar POP, erro: ', e)
            print (c, c.cliente.endereco.cidade, c.pop)
            count +=1

print('Total de clientes: %s'%count)