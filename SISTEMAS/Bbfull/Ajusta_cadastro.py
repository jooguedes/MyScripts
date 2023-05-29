import csv
from pyexpat import model
from turtle import update
from apps.admcore import models

cpfs_ajustados=[]
def convertdata(data):
    try:
        y,m,d = data.split(' ')[0].split('-')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None



with open('/tmp/Conv-Assinantes-2022_10_24_17_47_14.csv', 'rb') as csvfile:
    conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))

    for row in conteudo:
        data_cadastro=convertdata(row[13])
        print('Data cadastro: ', data_cadastro)
        cpfcnpj=row[3]
        cliente=models.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj).update(data_cadastro=data_cadastro)
        



