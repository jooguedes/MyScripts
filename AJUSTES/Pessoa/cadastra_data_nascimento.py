import csv
from apps.admcore import models

with open('/tmp/mkauth-clientes-ativados2.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        data_nascimento=row[11]

        if data_nascimento!='':
            if '/' in data_nascimento:
                try:
                    d,m,y=data_nascimento.split('/')
                    data_nascimento=str(y)+'-'+str(m)+'-'+str(d)
                except:
                    continue
            elif '-' in data_nascimento:
                data_nascimento=data_nascimento

            try:
                models.Pessoa.objects.filter(cliente__clientecontrato__servicointernet__login__lower=row[1].lower()).update(datanasc=data_nascimento)
            except Exception as e:
                print(e)


