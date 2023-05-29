from datetime import date, datetime
from http import client
from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
from apps.cauth import models as authmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
import csv
import re
import copy

formacobranca = fmodels.FormaCobranca.objects.all()[0]

fnum = lambda n: re.sub('[^0-9]', '', n)
usuario = authmodels.User.objects.get(username='sgp')
m = manage.Manage()
with open('/tmp/Perficio-gerencianet-cancela-titulos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        numero_documento=row[0]

        if str(row[9])=='true':

            titulo=fmodels.Titulo.objects.filter(numero_documento=numero_documento, portador=2)

            for t in titulo:
                data=datetime.now()
                fmodels.Titulo.objects.filter(id=t.id).update(status=fmodels.MOVIMENTACAO_CANCELADA,
            data_cancela=data, observacao='cancelado mediante ajuste solicitado pelo protocolo: ')







#Extorna boletos

from datetime import date, datetime
from http import client
from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
from apps.cauth import models as authmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
import csv
import re
import copy

formacobranca = fmodels.FormaCobranca.objects.all()[0]


def strdate(d):
    try:
        d,m,y = d.split()[0].split('.')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None
fnum = lambda n: re.sub('[^0-9]', '', n)
usuario = authmodels.User.objects.get(username='sgp')
m = manage.Manage()
with open('/tmp/Conv-recebiveis.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        numero_documento=row[0]
        portador=1
        data_pagamento=strdate(row[11])
        valor_pago=row[6]
        usuario = authmodels.User.objects.get(username='sgp')
        if str(row[8])=='true' and str(row[9])=='false':

            titulo=fmodels.Titulo.objects.filter(numero_documento=numero_documento, portador=portador)

            for t in titulo:
                fmodels.Titulo.objects.filter(id=t.id).update(status=fmodels.MOVIMENTACAO_PAGA,
            data_pagamento=data_pagamento,valorpago=valorpago, usuario_b=usuario, observacao='boleto extornado mediante ajuste de importação:')

