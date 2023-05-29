from apps.admcore import models
cliente=models.Cliente.objects.filter(titulo__isnull=True, clientecontrato__clientecontratostatus__status=models.CONTRATO_ATIVO)
lista_duplicados=[]
for cc in cliente:
    cpfcnpj=cc.pessoa.cpfcnpj
    if models.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj).count() > 1:
        clientes_duplicados=models.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj, titulo__isnull=False)
        for cd in clientes_duplicados:
            if cd.pessoa.cpfcnpj in '00000000000':
                continue
            else:
                if cd.pessoa.cpfcnpj in lista_duplicados:
                    continue
                else:
                    lista_duplicados.append(cd.pessoa.cpfcnpj)


for l in lista_duplicados:
    print(l)