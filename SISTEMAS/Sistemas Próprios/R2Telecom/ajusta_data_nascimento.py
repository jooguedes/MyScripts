from apps.admcore import models as admmodels
import csv
with open('/tmp/Conv-exporta_clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        id=row[0]
        data_nascimento=row[15]
        sexo=row[16]
        if data_nascimento in '0000-00-00' or data_nascimento.split('-')[1] in '00' or data_nascimento.split('-')[2] in '00':
            continue
        admmodels.Pessoa.objects.filter(cliente__id=id).update(sexo=sexo, datanasc=data_nascimento)