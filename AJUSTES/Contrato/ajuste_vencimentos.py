#AJUSTE DE VENCIMENTO DOS CLIENTES PELO ARQUIVO DE BACKUP

from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
import csv 


with open('/tmp/beesweb-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if row[8] != '': #row onde esta a data vencimento
            try:
                new_vencimento = fmodels.Vencimento.objects.get(dia=row[8]) #row onde esta a data vencimento
            except:
                try:
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = row[8] #row onde esta a data vencimento
                    new_vencimento.save()
                except:
                    new_vencimento = fmodels.Vencimento.objects.get(dia=10)
            
            try:
                cliente = admmodels.Cliente.objects.get(id=row[0]) # row do filtro utilizado
                obrancas = fmodels.Cobranca.objects.filter(cliente=cliente).update(vencimento=new_vencimento)
            except Exception as e:
                print('Erro em atualizar vencimento, erro: ', e)