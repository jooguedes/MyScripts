from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
from django.db.models import F, Q

servico=admmodels.ServicoInternet.objects.filter(login__icontains='semlogin')

for s in servico:
    print(s)
    try:
        cliente_contrato=admmodels.ClienteContrato.objects.filter(servicointernet=s.id)
        print(cliente_contrato)
        old_cobranca=fmodels.Cobranca.objects.filter(clientecontrato__id=cliente_contrato[0].id, cliente__clientecontrato__servicointernet__id=s.id)
        print(old_cobranca)
        new_cobranca=fmodels.Cobranca.objects.filter(Q(cliente=s.clientecontrato.cliente.id),~Q(id=old_cobranca[0].id), Q(clientecontrato__isnull=False))
        print(new_cobranca)
        fmodels.Titulo.objects.filter(cobranca=old_cobranca[0].id, cliente=s.clientecontrato.cliente.id).update(cobranca=new_cobranca[0].id)
    except Exception as e:
        print(e)

