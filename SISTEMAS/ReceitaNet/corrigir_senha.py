import csv
from apps.admcore import models as admmodels

with open('/tmp/Conv-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[0]
        try:
            admmodels.ServicoInternet.objects.filter(login=login).update(login_password=row[1], login_password_plain=row[1], central_password=row[1])
        except Exception as e :
            print(e)
            continue

