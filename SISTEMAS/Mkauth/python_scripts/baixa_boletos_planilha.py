from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
import csv
import re
import sys

usuario = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n) 

#FUNCAO PARA CONVERSÃO DE DATA
def convertdata(dt):
    y,m,d=dt.split(' ')[0].split('-')
    data=str(y)+'-'+(m)+'-'+(d)
    print(data)
    return data





with open('/tmp/mkauth-titulos-1.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cpfcnpj=row[10]

        try:
            cliente=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)[0]
        except Exception as e:
            print(e)
        
        usuario = authmodels.User.objects.get(username='sgp')
        data_documento = row[6]
        data_vencimento = convertdata(row[15])
        data_pagamento = row[17]
        observação='Titulos baixados mediante solicitação da ocorrência de protocolo: '

        if data_pagamento!='':
            titulos=fmodels.Titulo.objects.filter(portador=XXX, status=fmodels.MOVIMENTACAO_GERADA)
            for t in titulos:
                fmodels.Titulo.objects.filter(id=t.id).update(status =  fmodels.MOVIMENTACAO_PAGA,
                                                        usuario_b = usuario, 
                                                        data_baixa = data_pagamento, 
                                                        data_pagamento = data_pagamento.split(' ')[0])

