from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels

titulos = [45976, 45977, 45978, 45979, 45980, 45981, 45982, 45983, 45984, 45985]

portador_id = 1
cliente_id = 71
contrato_id = 71

try:
    cliente = admmodels.Cliente.objects.get(id=cliente_id)
    contrato = admmodels.ClienteContrato.objects.get(id=contrato_id)
    fmodels.Titulo.objects.filter(numero_documento__in=titulos) \
    								.update(cliente=cliente, cobranca=contrato.cobranca)
except Exception as e:
    print(e)