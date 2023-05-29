from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
import csv 


with open('/tmp/beesweb-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login = row[24].lower().strip()
        vencimento = row[8]
        if vencimento != '' and login != '': #row onde esta a data vencimento
            try:
                new_vencimento = fmodels.Vencimento.objects.get(dia=vencimento) #row onde esta a data vencimento
            except:
                try:
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento #row onde esta a data vencimento
                    new_vencimento.save()
                except:
                    new_vencimento = fmodels.Vencimento.objects.get(dia=10)
            

            fmodels.Cobranca.objects.filter(clientecontrato__servicointernet__login__lower=login).update(vencimento=new_vencimento)