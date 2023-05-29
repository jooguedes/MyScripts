from apps.financeiro import models
from django.db.models import F
from datetime import datetime 
print models.Titulo.objects.filter(portador__in=[32,31],usuario_g__username='sgp', status=models.MOVIMENTACAO_CANCELADA, usuario_c=None).update(usuario_c=F('usuario_g'), data_cancela=datetime.now())