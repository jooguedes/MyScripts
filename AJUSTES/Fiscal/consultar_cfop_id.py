from apps.fiscal import models

CFOP_ID_ATUAL = 121
CFOP_ID_CORRETO = 3

models.NotaFiscal.objects.filter(cfop_id=CFOP_ID_ATUAL).update(cfop_id=CFOP_ID_CORRETO)

######################################################################
from apps.fiscal import models

for nf in models.NotaFiscal.objects.all():
    try:
        if len(models.CFOP.objects.filter(id=nf.cfop_id)) == 0:
            print(nf.numero, nf, nf.cfop_id)
    except Exception as e:
        print(e)

#######################################################################
from apps.fiscal import models as fismodels
from apps.admcore import models as admmodels

for nf in fismodels.NotaFiscal.objects.all():
    try:
        if len(admmodels.Empresa.objects.filter(id=nf.empresa_id)) == 0:
            print('Erro de referência de empresa, id de empresa que está presente da nota: ', nf.empresa_id)
    except Exception as e:
        print(e)