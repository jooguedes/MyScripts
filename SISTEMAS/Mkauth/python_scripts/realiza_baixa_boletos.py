from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from unicodedata import normalize
import csv
import re
import sys

tf = titulofunc.TituloFunc()
portador = fmodels.Portador.objects.get(pk=1)
#nosso_numero = tf.getNossoNumero(portador) +
usuario = authmodels.User.objects.get(username='sgp')
fnum = lambda n: re.sub('[^0-9.]','',n) 
#portador.titulo_set.all().delete()
with open('/tmp/mkauth-titulos-1.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        
        numero_documento = int(row[9])

        usuario = authmodels.User.objects.get(username='sgp')
        data_documento = row[6]
        data_vencimento = row[7].split(' ')[0]
        data_pagamento = row[8]


        titulos=fmodels.Titulo.objects.filter(numero_documento=numero_documento, portador=1, status=fmodels.MOVIMENTACAO_GERADA)
        for t in titulos:
            fmodels.Titulo.objects.filter(id=t.id).update(status =  fmodels.MOVIMENTACAO_PAGA,
                                                    usuario_b = usuario, 
                                                    data_baixa = data_pagamento, 
                                                    data_pagamento = data_pagamento.split(' ')[0])
