from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
import csv 
import re

usuario = authmodels.User.objects.get(username='sgp')

fnum = lambda n: re.sub('[^0-9.]','',n)

def strdate(dt):
    try:
        d,m,y = dt.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

with open('/tmp/ajuste-sicredi.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if row[2].strip() !='' or row[1].strip() != '':
            nosso_numero = row[4].split('/')[1].split('-')[0]
            if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=1).count() > 0:
                titulo = fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=1)[0]
                valorpago = row[48].replace(',','.')
                if fnum(valorpago) == '':
                    valorpago = row[6].replace(',','.')
                status = fmodels.MOVIMENTACAO_PAGA
                usuario_b = usuario
                usuario_c = None
                if row[2].strip() !='':
                    data_pagamento = strdate(row[2])
                else:
                    data_pagamento = strdate(row[1])
                data_baixa=data_pagamento
                
                titulo.valorpago=valorpago
                titulo.status=status
                titulo.usuario_b=usuario_b
                titulo.usuario_c=usuario_c
                titulo.data_pagamento=data_pagamento
                titulo.data_baixa=data_baixa
                try:
                    titulo.save()
                    print('Status da cobrança atualizado!')
                except Exception as e:
                    print('Erro ao atualizar status da cobrança, erro: ', e)
