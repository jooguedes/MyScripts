from apps.admcore import models as admmodels
import csv

POPS = [1,2]
NOME_ARQUIVO = 'lista_de_logins.csv'
url = '%s/media/%s'%(request.META['HTTP_ORIGIN'], NOME_ARQUIVO)

with open('%s%s'%(settings.MEDIA_ROOT, NOME_ARQUIVO), 'w') as csvfile:
    values = csv.writer(csvfile, delimiter='|', quotechar='"')
    values.writerow(['CLIENTE', 'LOGIN', 'CONTRATO', 'STATUS'])
    for si in admmodels.ServicoInternet.objects.filter(clientecontrato__pop__in=POPS):
        values.writerow([str(si.clientecontrato.cliente), str(si.login), str(si.clientecontrato), str(si.status)])

print(url)