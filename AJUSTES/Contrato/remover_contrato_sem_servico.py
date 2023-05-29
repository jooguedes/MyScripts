from apps.admcore import models as admmodels

for cc in admmodels.ClienteContrato.objects.all():
    if admmodels.ServicoInternet.objects.filter(clientecontrato=cc).count() == 0:
        print (cc)
        cc.delete()