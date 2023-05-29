from apps.admcore import models
from apps.estoque import models as e2models
from django.db.models import Q
from django.db import connection, transaction

POP_ID = [3]

contratos = models.ClienteContrato.objects \
    .filter(Q(pop__id__in=POP_ID))
       
print ('total: %s' % contratos.count())
       
with transaction.atomic():
    for cc in contratos:
        try:
            cliente = cc.cliente
            cc.delete()
            
            if cliente.clientecontrato_set.all().count() == 0:
                try:
                    cliente.delete()
                except:
                    cliente.is_deleted = True
                    cliente.save()
        except Exception as e:
            print ('erro => %s' % cc)
            print (str(e))

models.Pop.objects.filter(id__in=POP_ID).delete()