
import csv
from apps.admcore import models as admmodels
from apps.netcore import models as nmodels

with open('/tmp/Conv-ONUS.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            login = row[14]
            serial = row[5]
            servico = admmodels.ServicoInternet.objects.filter(
                login=login, onu__isnull=True)
            if servico:
                onu = nmodels.ONU.objects.filter(phy_addr=serial)
                if onu:
                    onu = onu[0]
                    onu.service = servico[0]
                    onu.save()
                    print(servico[0], serial[0:12])