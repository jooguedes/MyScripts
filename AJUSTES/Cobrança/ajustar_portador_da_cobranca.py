from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels

ALTERAR = False

for cc in admmodels.ClienteContrato.objects.all():
    t = fmodels.Titulo.objects.filter(cliente=cc.cliente).order_by('-id')[0]
    if cc.plano
