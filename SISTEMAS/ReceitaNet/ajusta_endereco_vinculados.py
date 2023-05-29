import csv
from datetime import date, datetime
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels

with open('/tmp/Conv-vinculados.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login_primario=row[0]
        login_secundario=row[1]
        cep=row[4]

        if not cep or cep =='' or cep =='NULL' :
            endereco_principal= admmodels.Endereco.objects.filter(cliente__clientecontrato__servicointernet__login=login_primario)[0]

            
            logradouro= endereco_principal.logradouro
            cidade=endereco_principal.cidade
            estado= endereco_principal.uf
            bairro=endereco_principal.bairro
            numero=endereco_principal.numero



            endereco_cliente=admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login_secundario)

            for enc in endereco_cliente:
                admmodels.Endereco.objects.filter(id=enc.endereco.id).update(uf=estado,logradouro=logradouro, numero=numero, cidade=cidade, bairro=bairro)

            
            endereco_cobranca=fmodels.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__login=login_secundario)

            for ec in endereco_cobranca:
                admmodels.Endereco.objects.filter(id=ec.endereco.id).update(uf=estado,logradouro=logradouro, numero=numero, cidade=cidade, bairro=bairro)

            endereco_servico= admmodels.ServicoInternet.objects.filter(clientecontrato__servicointernet__login=login_secundario)
            
            for es in endereco_servico:
                admmodels.Endereco.objects.filter(id=es.endereco.id).update(uf=estado, logradouro=logradouro, numero=numero, cidade=cidade, bairro=bairro)
        else:
            print('não precisa atualizar endereco')