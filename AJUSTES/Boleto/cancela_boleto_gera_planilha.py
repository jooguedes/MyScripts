from apps.financeiro import models as fmodels
from django.conf import settings
from apps.cauth import models as authmodels
from datetime import date, datetime
import csv

ID_PORTADOR = 16
CANCELAR = False
VENCIMENTO_DE = '2023-06-10'
VENCIMENTO_ATE = '2029-12-31'
NOME_ARQUIVO = 'lista_boletos_cancelados_juno.csv'

usuario = authmodels.User.objects.get(username='sgp')
url = '%s/media/%s'%(request.META['HTTP_ORIGIN'], NOME_ARQUIVO)

with open('%s%s'%(settings.MEDIA_ROOT, NOME_ARQUIVO), 'w') as csvfile:
    values = csv.writer(csvfile, delimiter='|', quotechar='"')
    values.writerow(['CLIENTE', 'COBRANCA', 'BOLETO'])
    for boleto in fmodels.Titulo.objects.filter(portador=ID_PORTADOR,
                              titulogateway__idtransacao__isnull=True,
                              data_vencimento__gte=VENCIMENTO_DE,
                              data_vencimento__lte=VENCIMENTO_ATE,
                              status=fmodels.MOVIMENTACAO_GERADA) \
                                .exclude(cobranca__clientecontrato__status__status=3):
            values.writerow([str(boleto.cliente), str(boleto.cobranca), str(boleto)])

if CANCELAR:
    fmodels.Titulo.objects.filter(portador=ID_PORTADOR,
                              titulogateway__idtransacao__isnull=True,
                              data_vencimento__gte=VENCIMENTO_DE,
                              data_vencimento__lte=VENCIMENTO_ATE,
                              status=fmodels.MOVIMENTACAO_GERADA) \
                                .exclude(cobranca__clientecontrato__status__status=3) \
                                    .update(status=fmodels.MOVIMENTACAO_CANCELADA,
                                            usuario_c=usuario,
                                            data_cancela=date.today(),
                                            motivocancela="Boleto cancelado mediante ocorrência importação-protocolo: 230527110500, autorizaddo pelo Sr(a). Evaristo Damasceno.")

print(url)



