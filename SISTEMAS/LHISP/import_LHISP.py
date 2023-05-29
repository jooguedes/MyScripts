if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            codigo_banco = row[2]
            if not row[2]:
                codigo_banco = '999'
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print row
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[1]
                new_portador.codigo_banco = codigo_banco
                new_portador.agencia = row[3] or '0'
                new_portador.agencia_dv = row[4]
                new_portador.conta = row[5] or '0'
                new_portador.conta_dv = row[6]
                new_portador.convenio = row[7]
                new_portador.carteira = row[8]
                new_portador.cedente = 'PROVEDOR X'
                new_portador.cpfcnpj = '0'
                new_portador.save()

            if fmodels.GatewayPagamento.objects.filter(portadores__id=row[0]).count() == 0:
                if row[12] in ['boleto_facil', 'fortunus', 'juno', 'widepay']:
                    new_gateway_pagamento = fmodels.GatewayPagamento()
                    new_gateway_pagamento.descricao = row[1]
                    new_gateway_pagamento.gerencia_boleto = True
                    if row[13]:
                        new_gateway_pagamento.token = row[13]
                    if row[14]:
                        new_gateway_pagamento.usuario = row[14]
                    if row[15]:
                        new_gateway_pagamento.senha = row[15]
                    if row[12] == 'fortunus' and row[13]:
                        new_gateway_pagamento.nome = 'gerencianet'
                    elif row[12] == 'fortunus':
                        new_gateway_pagamento.nome = 'gerencianetapi'
                    elif row[12] == 'boleto_facil':
                        new_gateway_pagamento.nome = 'boletofacil'
                    else:
                        new_gateway_pagamento.nome = row[12]
                    new_gateway_pagamento.save()
                    new_portador = fmodels.Portador.objects.get(id=row[0])
                    new_gateway_pagamento.portadores.add(new_portador)
