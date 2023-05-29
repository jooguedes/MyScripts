from decimal import Decimal
from unicodedata import decimal
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from apps.atendimento import models as amodels
from django.db.models import Q, Max
import csv
metodo = amodels.Metodo.objects.all()[0]
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-exporta_contratos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:


        if str(row[8])!='0.00':
            try:
                
                contrato_id=row[3]
                valor_contrato=row[8].replace('-','')

               
                fmodels.Cobranca.objects.filter(clientecontrato__id=contrato_id).update(valorfixo=valor_contrato)
            except Exception as e:
                print(e)



#METODO 02

from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from apps.atendimento import models as amodels
from django.db.models import Q, Max
import csv
from decimal import Decimal

metodo = amodels.Metodo.objects.all()[0]
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-exporta_contratos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if str(row[8])!='0.00':
            try:
                negativo='-'
                contrato_id=row[3]
                valor_contrato=row[8].replace('-','')
                sv=admmodels.ServicoInternet.objects.filter(clientecontrato__id=contrato_id)
                valorplano=sv[0].planointernet.plano.preco
                print('esse é o valor do plano e: ',float(valorplano), 'esse é o valor do contrato: ',float(valor_contrato))
                
                valor_desconto=float(valor_contrato) - float(valorplano) 
                print('Valor: ', valor_desconto)
                if valor_desconto==0:
                    continue
                
                cliente=admmodels.Cliente.objects.filter(clientecontrato__id=contrato_id)
                new_desconto=fmodels.ADCobranca()
                new_desconto.cobranca=fmodels.Cobranca.objects.filter(cliente__clientecontrato__id=contrato_id)[0]
                #print('esse é o valor', valor_desconto)
                new_desconto.valor=str(valor_desconto)
                new_desconto.tipo=fmodels.ADCOBRANCA_FIXO
                print('id do usuario: ', usuario.id)
                new_desconto.usuariocad=usuario
                new_desconto.save()
            except Exception as e:
                print(e)