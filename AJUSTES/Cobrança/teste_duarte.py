from apps.financeiro import models

ALTERAR = True

for c in models.Cobranca.objects\
                        .filter(clientecontrato__isnull=False,
                                titulo__status=models.MOVIMENTACAO_PAGA) \
                                .prefetch_related('titulo_set').distinct():

    t = c.titulo_set.filter(status=models.MOVIMENTACAO_PAGA,
                            cobranca__isnull=False).order_by('-data_vencimento').first()
    
    if t:
        titulo_portador = t.portador_id

        if titulo_portador != c.portador_id:
            new_portador = t.portador_id

            if new_portador:
                print (c.cliente.pessoa.nome,'|Contrato ID:', c.clientecontrato.id , c.portador_id, '|| novo portador', new_portador, '\n', t, '\n')

                if ALTERAR:
                    c.portador_id = new_portador
                    c.save()