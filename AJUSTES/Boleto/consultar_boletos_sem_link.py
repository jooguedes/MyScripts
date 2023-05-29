from apps.financeiro import models as fmodels

ID_PORTADOR = ID_PORTADOR

cf = fmodels.Titulo.objects.filter(portador=ID_PORTADOR,
                                   titulogateway__idtransacao__isnull=True,
                                   status=1) \
									.exclude(cobranca__clientecontrato__status__status=3).order_by('cliente')

portador = fmodels.Portador.objects.get(id=ID_PORTADOR)

print("Portador: %s | ID: %s | Quantidade de Boletos: %s\n" % (portador.descricao, 
                                                               portador.id, cf.count()))

for i in cf:
    print("%s || N. Doc: %s || Contrato id: %s || D. Vencimento: %s || Valor: %s || D. Emissão: %s"%(i.cliente.pessoa.nome,
                                                                                                    i.numero_documento, 
                                                                                                    i.cobranca.clientecontrato.id, 
                                                                                                    i.data_vencimento, 
                                                                                                    i.valor, 
                                                                                                    i.data_documento))