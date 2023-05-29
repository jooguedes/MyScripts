import csv 
import re 
from apps.financeiro import models
with open('/tmp/Conv-gerenet-clientes-isentos.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            isento=row[67]
            login=row[69]
            if isento=='ISENTO':
                try:
                    cliente=models.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__login=login).update(isento=100, nao_suspende=True)
                    print(cliente[0].cliente)
                except Exception as e:
                    print(e)
                    




import csv 
import re
from apps.admcore import models
with open('/tmp/gerenet-clientes.csv.utf8', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            isento=row[67]
            login=row[69]
            if isento=='CANCELADO':
                try:
                    cliente=models.ServicoInternet.objects.filter(login=login)#.update(status=3)
                    print(cliente[0].cliente)
                except Exception as e:
                    print(e)
                    