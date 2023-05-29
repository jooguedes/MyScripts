from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from datetime import datetime
from decimal import Decimal
import csv

usuario = admmodels.User.objects.get(username='sgp')

with open('/tmp/csv-clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login = row[21]
        valor_plano = row[19].replace('.', '').replace(',', '.').strip()
        servicos = admmodels.ServicoInternet.objects.filter(login__lower=login.lower())
            
        for servico in servicos:
            if Decimal(valor_plano) <= Decimal('49.9'):
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact='Online Radio Residencial 5M'.lower())[0]
                servico.planointernet = planointernet
            elif Decimal(valor_plano) == Decimal('59.9'):
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact='Online Radio Residencial 7M'.lower())[0]
                servico.planointernet = planointernet
            elif Decimal(valor_plano) >= Decimal('69.9') and Decimal(valor_plano) <= Decimal('72.9'):
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact='Online Radio Residencial 10M'.lower())[0]
                servico.planointernet = planointernet
            else:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact='Online Radio Residencial 14M'.lower())[0]
                servico.planointernet = planointernet
            try:
                servico.save()
            except Exception as e:
                print('Erro ao atualizar o plano, erro: ',e)
        
            print(valor_plano, str(servico.planointernet.plano.preco))
            if Decimal(valor_plano) == servico.planointernet.plano.preco:
                continue
            else:
                new_addcobranca = fmodels.ADCobranca(
                    cobranca = servico.clientecontrato.cobranca,
                    valor = Decimal(valor_plano)-servico.planointernet.plano.preco,
                    usuariocad = usuario,
                    data_cadastro = datetime.now(),
                    ativa = True,
                    tipo = fmodels.ADCOBRANCA_FIXO
                )
                try:
                    new_addcobranca.save()
                    print(new_addcobranca)
                except Exception as e:
                    print(e)
