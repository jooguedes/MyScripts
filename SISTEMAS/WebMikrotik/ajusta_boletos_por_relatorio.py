import csv
from datetime import datetime
import re
from shutil import ExecError
from django.conf import settings
from django.db.models import Q, Max
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels

fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = authmodels.User.objects.get(username='sgp')



with open('/tmp/Conv-22012-FINANCEIRO-FATURAS-MENSAIS-2023-02-03.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            cpfcnpj=row[12] or row[13]
        except Exception as e:
            print(e)
            continue
        status=row[10]
        valorpago=row[8].replace(',','.')
        try:
            d,m,y=row[2].split('/')
            mes=m
            ano=y
            vencimento=str(y+'-'+m+'-'+d)
        except Exception as e:
            print(e)
            continue
        
        try:
            d,m,y=row[3].split('/')
            databaixa=str(y+'-'+m+'-'+d)
        except Exception as e:
            print(e)
            databaixa=None
        
        data_cancela=datetime.now()
        if str(status)=='Liquidada' or str(status)=='Cancelada':
            try:
                
                cliente=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)[0]
                titulo=fmodels.Titulo.objects.filter(data_vencimento__year=ano,
                                                     data_vencimento__month=mes,
                                                     data_vencimento=vencimento, 
                                                     cliente__id=cliente.id, status=fmodels.MOVIMENTACAO_GERADA, portador=2)
                print('Titulo a ser atualizado ====> ', titulo)
                if(str(status)=='Liquidada'):
                    fmodels.Titulo.objects.filter(id=titulo[0].id).update(status=fmodels.MOVIMENTACAO_PAGA, valorpago=valorpago, data_baixa=databaixa,  observacao='Titulo baixado mediante solicitação da ocorrência:    230131100601', usuario_b=usuario)
                elif(str(status)=='Cancelada'):
                    fmodels.Titulo.objects.filter(id=titulo[0].id).update(status=fmodels.MOVIMENTACAO_CANCELADA, data_cancela=data_cancela,  observacao='Titulo cancelado mediante solicitação da ocorrência:    230131100601', usuario_c=usuario)
                else:
                    print('Boleto está vencido')
            except Exception as e:
                print(e)
        