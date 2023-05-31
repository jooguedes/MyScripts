from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import re 

usuario = authmodels.User.objects.get(username='sgp')

with open('/tmp/ixc-titulos.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
    for row in conteudo:
        print(row[15])
        if row[15].strip() == '10':
            try:
                n_documento = int(row[5])
            except:
                n_documento = int(row[4])
            valorpago = row[9]
            data_pagamento = row[10]
            data_vencimento = row[12]
            if not row[12]:
                data_vencimento = row[11]
            try:
                t = fmodels.Titulo.objects.filter(portador=10, numero_documento=n_documento).exclude(status=fmodels.MOVIMENTACAO_CANCELADA)
            except Exception as e:
                print(e)
                break
            print('Passei aqui')

            if len(t) > 0:
                print(t)
                if data_pagamento.strip() != '' and '0000-00-00' not in data_pagamento:
                    t[0].valorpago = valorpago
                    t[0].data_pagamento = data_pagamento
                    if data_pagamento == '' or data_pagamento == '0000-00-00':
                        t[0].data_pagamento = data_vencimento
                    t[0].data_baixa = data_pagamento
                    t[0].status = fmodels.MOVIMENTACAO_PAGA
                    t[0].usuario_b = usuario
                    t[0].usuario_c = None

                else:
                    t[0].status = fmodels.MOVIMENTACAO_GERADA
                    t[0].data_baixa = None
                    t[0].data_pagamento = None
                    t[0].valorpago = None
                    t[0].usuario_b = None
                t[0].save()