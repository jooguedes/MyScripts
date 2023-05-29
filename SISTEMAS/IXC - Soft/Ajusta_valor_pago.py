from apps.financeiro import models as fmodels
from apps.admcore import models as admodels
import csv

from apps.admcore import models as admmodels
from django.db.models import Q, Max
with open('/tmp/ixc-titulos-pagos7.csv.utf8', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        valor_pago=row[9]
        nosso_numero=row[4]
        if "-" in row[18]:
            juros=str(row[18]).split('-')[1]
            fmodels.Titulo.objects.filter(status=fmodels.MOVIMENTACAO_PAGA,nosso_numero=nosso_numero).update(valorpago=valor_pago, juros=juros)
        elif(row[18]!='0.00'):
            desconto=row[18]
            fmodels.Titulo.objects.filter(status=fmodels.MOVIMENTACAO_PAGA,nosso_numero=nosso_numero).update(valorpago=valor_pago, desconto=desconto)
        else:
            fmodels.Titulo.objects.filter(status=fmodels.MOVIMENTACAO_PAGA,nosso_numero=nosso_numero).update(valorpago=valor_pago)
            print('Não é necessário alterações... ')