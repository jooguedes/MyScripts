import csv
from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
import re

PORTADOR=58

usuario = admmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-logica-titulos-58.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            numero_documento=re.sub('[^0-9]', '',row[8])
            data_pagamento=row[5]
            valorpago=row[6]
            data_baixa=data_pagamento
            titulos=fmodels.Titulo.objects.filter(portador=PORTADOR,
                                                  status=fmodels.MOVIMENTACAO_GERADA,
                                                  numero_documento=numero_documento,
                                                  usuario_g__username='sgp')
            

            fmodels.Titulo.objects.filter(portador=PORTADOR,
                                                  status=fmodels.MOVIMENTACAO_GERADA,
                                                  numero_documento=numero_documento,
                                                  usuario_g__username='sgp').update(status=fmodels.MOVIMENTACAO_PAGA,
                                                  usuario_b=usuario,
                                                  observacao='boleto baixado mediante solicitacao do protocolo:  230327122800',
                                                  valorpago=valorpago,
                                                  data_pagamento=data_pagamento,
                                                  data_baixa=data_pagamento)
            print(titulos)
            for t in titulos:
                print("titulo",t)
            