import csv
import re
from django.db.models import Q, Max
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]','',n)
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-exporta_contratos.csv', 'rU') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        produto=row[11]

        if('Desconto' in produto):
            try:
                print('Produto: >>>>>>>> ', row[11])
                valor=int(fnum(row[11]))
                id_cliente=int(row[0])
                cliente=admmodels.Cliente.objects.filter(id=id_cliente)
                new_desconto=fmodels.ADCobranca()
                new_desconto.cobranca=fmodels.Cobranca.objects.filter(cliente__id=cliente[0].id, cobranca_unificada__isnull=True)[0]
                print('esse é o valor', valor)
                new_desconto.valor='-'+str(valor)
                new_desconto.tipo=fmodels.ADCOBRANCA_FIXO
                print('id do usuario: ', usuario.id)
                new_desconto.usuariocad=usuario
                new_desconto.save()
            except Exception as e:
                print(e)
                continue
from apps.financeiro import models
models.ADCobranca.objects.all().delete()
