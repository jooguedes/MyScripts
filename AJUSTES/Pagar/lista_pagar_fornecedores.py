from apps.financeiro import models as fmodels
from datetime import date
import csv

fnum = lambda n: re.sub('[^0-9.]','',n) 

with open('/tmp/ajuste-contas-pagar.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        for p in fmodels.Pagar.objects.filter(fornecedor__isnull=True):
            if row[0].strip().lower() == str(p.descricao).strip().lower():
                #y, m, d = str(p.data_vencimento).split(',')
                dt_vencimento = '%s/%s/%s'%(p.data_vencimento.day, p.data_vencimento.month, p.data_vencimento.year)
                print(p, row, dt_vencimento)



from apps.financeiro import models as fmodels
from datetime import date
import csv
import re

fnum = lambda n: re.sub('[^0-9]','',n) 

with open('/tmp/ajuste-contas-pagar.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        for p in fmodels.Pagar.objects.filter(fornecedor__isnull=True):
            dt_vencimento = '%s/%s/%s'%(p.data_vencimento.day, p.data_vencimento.month, p.data_vencimento.year)
            if row[0].strip().lower() == str(p.descricao).strip().lower() and dt_vencimento == row[6].strip():      
                try:   
                    nome_fornecedor = row[3]
                    fornecedor = fmodels.Fornecedor.objects.filter(nome__lower__in=nome_fornecedor.lower())[0]
                    p.fornecedor=fornecedor
                    try:
                        p.save()
                        print(fornecedor, nome_fornecedor, p)
                    except Exception as a:
                        print('Erro ao salvar alteração de empresa, erro: ', a)
                    print(p, row, dt_vencimento)
                except Exception as e:
                    print('Erro ao vincular, erro: ', e, fornecedor, p)


from apps.financeiro import models as fmodels
from datetime import date
import csv
import re

fnum = lambda n: re.sub('[^0-9]','',n) 

with open('/tmp/ajuste-contas-pagar.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            nome_fornecedor = row[3].split('-')[0].strip()
            print(nome_fornecedor)
            fornecedor = fmodels.Fornecedor.objects.filter(nome__lower__icontains=nome_fornecedor.lower())[0]
            print(fornecedor.nome)
        except Exception as e:
            print('Erro ao localizar empresa', e)