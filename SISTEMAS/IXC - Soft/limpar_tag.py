from apps.financeiro import models 
models.TituloGateway.objects.filter(titulo__portador=8, titulo__usuario_g__username='sgp', link='', idtransacao='').delete() 