from apps.financeiro import models

PORTADOR = 2
GATEWAY = 1

for tg in models.TituloGateway.objects.filter(gateway__nome__exact='gerencianet',
                                              titulo__portador=PORTADOR,
                                              djson__chave__isnull=False,
                                              gateway_id=GATEWAY):
    chave = tg.djson.get('chave')

    if chave and (tg.idtransacao != chave):
        print (tg.titulo.numero_documento, chave)
        tg.idtransacao = chave
        tg.save()