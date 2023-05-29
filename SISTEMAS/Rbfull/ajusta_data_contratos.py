import csv
from pyexpat import model
from turtle import update
from apps.admcore import models

cpfs_ajustados=[]
def convertdata(data):
    try:
        d,m,y = data.split(' ')[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None



with open('/tmp/Conv-Clientes-2022-desativados.csv', 'rb') as csvfile:
    conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))

    for row in conteudo:
        try:
            data_cadastro=convertdata(row[15])
            data_ativacao=convertdata(row[16])
            id_contrato=row[0]
            models.ClienteContrato.objects.filter(id=id_contrato).update(data_cadastro=data_cadastro)
            models.ClienteContratoStatus.objects.filter(clientecontrato__id=id_contrato).update(data_cadastro=data_ativacao)
        except Exception as e:
            print(e)