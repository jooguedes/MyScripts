import csv 
from apps.admcore import models as admmodels
with open('/tmp/Conv-PLANOS_zevo.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
                id=int(row[1])+2500
                plano='importador@'+str(row[4])
                try:
                    planointernet=admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                    admmodels.ServicoInternet.objects.filter(clientecontrato__cliente=id).update(planointernet=planointernet)
                except Exception as e:
                       print(e)