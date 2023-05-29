from apps.financeiro import models

GATEWAY_ID = 14
STATUS = models.MOVIMENTACAO_GERADA

for titulo in models.Titulo.objects.filter(titulogateway__gateway__id=GATEWAY_ID,
                                           status=STATUS):
    print(titulo, titulo.portador, titulo.titulogateway.gateway.descricao)