import csv
from apps.admcore import models
with open('/tmp/Conv-export_gestorisp_contratos_clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cnpj = row[9]
        if cnpj !='':
            login=row[35]
            nome=row[10]
            models.Pessoa.objects.filter(cliente__clientecontrato__servicointernet__login=login).update(tipopessoa='J', cpfcnpj=cnpj, nome=nome)