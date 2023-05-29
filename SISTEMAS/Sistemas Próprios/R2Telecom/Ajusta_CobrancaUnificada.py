from shutil import ExecError
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from apps.atendimento import models as amodels
from django.db.models import Q, Max
import csv
metodo = amodels.Metodo.objects.all()[0]
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-exporta_clientes.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if (row[18]=='1'):
            id=row[0]
            servico=None
            contrato=admmodels.ClienteContrato.objects.filter(cliente__id=id)
           
            
            try:
                servico=admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__id=id)
                cobranca=fmodels.Cobranca.objects.filter(cliente__id=id)
                print('Esse é meu servico de internet: ', servico[0])
                print('Lista de cobrancas ', cobranca)
                for co in cobranca:
                    print('essa é minha cobranca', co)
                    cobranca_unificada=fmodels.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__id=servico[0].id)[0]
                    fmodels.Cobranca.objects.filter(id=co.id).update(cobranca_unificada=cobranca_unificada.id)
                    #fmodels.Cobranca.objects.filter(id=cobranca_unificada.id).update(cobranca_unificada=None)
            except Exception as e:
                print(e)

        '''try:
            sv=admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__id=row[0]).order_by('-id')
            
            fmodels.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__id=sv[0].id).update(cobranca_unificada=None)
        except Exception as e:
            print(e)'''

        
        
        