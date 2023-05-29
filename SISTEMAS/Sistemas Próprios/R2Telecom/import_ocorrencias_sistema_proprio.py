from pickle import NONE
from apps.financeiro.utils import titulofunc
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from apps.atendimento import models as amodels
from unicodedata import normalize
import csv
import re
import sys

metodo = amodels.Metodo.objects.all()[0]
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-exporta_chamados.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            clientecontrato = admmodels.ClienteContrato.objects.filter(
                cliente__id=row[0])
            print(row)
            if clientecontrato:
                if amodels.Ocorrencia.objects.filter(numero=row[2]).count()==0:
                    print(row)
                    ocorrencia = {}
                    ocorrencia['id'] = int(row[2])
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                    try:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(
                            id=6)
                    except:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(id=5)
                
                    ocorrencia['usuario'] = usuario
                    ocorrencia['metodo'] = metodo

                    
                    ocorrencia['numero'] = row[2]
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA


                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['status'] = 1 
                    ocorrencia['data_cadastro'] = row[3]
                    ocorrencia['data_agendamento'] = row[5]
                    ocorrencia['data_finalizacao'] = row[5]
                    if str(row[5]) in '0000-00-00 00:00:00':
                        ocorrencia['status'] = amodels.OCORRENCIA_ABERTA
                        ocorrencia['data_agendamento'] = None
                        ocorrencia['data_finalizacao'] = None
                    
                    ocorrencia['conteudo'] = row[4]
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()
                else:
                    ocorrencia=amodels.Ocorrencia.objects.filter(numero__=row[2])
                    new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                    new_ocorrencia_anotacao.ocorrencia= ocorrencia
                    new_ocorrencia_anotacao.anotacao=row[4]
                    new_ocorrencia_anotacao.usuario= usuario
                    new_ocorrencia_anotacao.save()
        except Exception as e:
            print(e)
            pass