from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv
import re 

PORTADOR = 2

usuario = authmodels.User.objects.get(username='sgp')

def strdate(d):
    try:
        d,m,y = d.strip().split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

with open('/tmp/webmikrotik-faturas-binterno.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
    for row in conteudo:
        n_documento = row[0]
        valorpago = row[9].replace('.','').replace(',','.')
        data_pagamento = strdate(row[4])
        data_vencimento = strdate(row[3])
        situacao = row[12]

        try:
            t = fmodels.Titulo.objects.filter(portador=PORTADOR, numero_documento=n_documento)
        except Exception as e:
            print(e)
            break

        if len(t) > 0:
            if situacao.strip().lower() in ['liquidada']:
                t[0].valorpago = valorpago
                t[0].data_pagamento = data_pagamento
                if data_pagamento == '' or data_pagamento == '0000-00-00':
                    t[0].data_pagamento = data_vencimento
                t[0].data_baixa = data_pagamento
                t[0].status = fmodels.MOVIMENTACAO_PAGA
                t[0].usuario_b = usuario
                t[0].usuario_c = None

            elif situacao.strip().lower() in ['cancelada', 'isenta']:
                t[0].data_cancela = data_vencimento
                t[0].status = fmodels.MOVIMENTACAO_CANCELADA
                t[0].data_baixa = None
                t[0].data_pagamento = None
                t[0].usuario_b = None
                t[0].usuario_c = usuario

            elif situacao.strip().lower() in ['aguardando']:
                t[0].data_baixa = None
                t[0].data_pagamento = None

            elif situacao.strip().lower() in ['vencida', 'vencido']:
                t[0].data_baixa = None
                t[0].data_pagamento = None
                t[0].valorpago = None
                t[0].usuario_b = None
            t[0].save()