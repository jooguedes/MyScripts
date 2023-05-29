import csv
import re
from datetime import datetime
from apps.admcore import models as admmodels
fnum = lambda n: re.sub('[^0-9.]','',n)
usuario = admmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-controllr.client_annotations.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            idCliente = fnum(row[7])
            idContrato = fnum(row[9])
            if idContrato != '':
                try:
                    clientecontrato = admmodels.ClienteContrato.objects.filter(id=int(idContrato)+8000)[0]
                except Exception as a:
                    print('Erro ao consultar idContrato, erro: %s'%a)
            else:
                try:
                    clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=int(idCliente)+8000)[0]
                except Exception as a:
                    print('Erro ao consultar idContrato, erro: %s'%a)

            anotacao = "Importacao Controlr 08032023.\n"+" "+"Usuario: %s \n Conteudo: %s\n"%(row[5].strip(), row[1])
            if row[8].strip() != '':
                anotacao += "Observações: %s"%row[8]
                
            status = 'Ativa' if row[6].strip() == '0' else 'Deletada'
            try:
                data_cadastro = row[3].split()[0]
            except Exception as e:
                print(e,'inserindo data atual')
                data_cadastro=datetime.now()
            if status == 'Ativa' and admmodels.ClienteAnotacao.objects.filter(anotacao=anotacao).count() == 0:
                new_anotacoes = admmodels.ClienteAnotacao()
                new_anotacoes.clientecontrato=clientecontrato
                new_anotacoes.cliente=clientecontrato.cliente
                new_anotacoes.anotacao=anotacao
                new_anotacoes.data_cadastro=datetime.now()
                new_anotacoes.usuario=usuario
                try:
                    new_anotacoes.save()
                    print('Importando Anotação: | %s'%new_anotacoes)
                except Exception as a:
                    print('idCliente: %s - idContrato: %s | Erro: %s'%(idCliente, idContrato, a))
