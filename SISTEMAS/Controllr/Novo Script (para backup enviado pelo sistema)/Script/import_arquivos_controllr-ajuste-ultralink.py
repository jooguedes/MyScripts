from apps.admcore import models as admmodels
from apps.cauth import models as authmodels
from datetime import date,datetime
import csv
import shutil
import os

pasta = '/tmp/cliente-arquivos'
usuario = authmodels.User.objects.get(username='sgp')
nome_perfil = 'sgp' # Para máquina local coloque nome_perfil='local'
save = False # Execute como falso para conferir se os dados estão corretos, depois mude para True

# Ler ids e incular ao cliente;
clientes = {}

with open('/tmp/controllr.client.ajuste.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    indice = 0
    for row in conteudo:
        cliente={
        	'idcliente': row[0],
            'cpfcnpj': row[12]
        }
        clientes[indice]=cliente
        indice +=1


# import arquivos clientes radiusnet
for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        try:
            caminho = str(os.path.join(os.path.realpath(diretorio), arquivo))
            for c in clientes:
                if clientes[c]['idcliente'] == caminho.split('/')[3]:
                    cpfcnpj = clientes[c]['cpfcnpj']
                    descricao=caminho.split('/')[-1].split('.')[0]
                    cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
                    arquivo = 'arquivos/%s'%caminho.split('/')[-1]
                    print(cliente,cpfcnpj, descricao, caminho)
                
                    if cliente and save:
                        if admmodels.ClienteDocumento.objects.filter(cliente=cliente, descricao=descricao).count() == 0:
                            try:
                                cliente = cliente[0]
                                print(cliente,cpfcnpj, descricao, caminho)
                                new_doc = admmodels.ClienteDocumento()
                                new_doc.cliente=cliente
                                new_doc.descricao=descricao[0:200]
                                new_doc.arquivo=arquivo
                                new_doc.usuario = usuario 
                                new_doc.data_cadastro=datetime.now()
                                new_doc.save()                        
                                try:
                                    path = str('/usr/local/sgp/media/%s/%s_arquivos/'%(nome_perfil, cliente.id))
                                    if not os.path.isdir(path):
                                        os.makedirs(path)
                                    shutil.copy(caminho, '/usr/local/sgp/media/%s/%s_arquivos/'%(nome_perfil, cliente.id))
                                except OSError as error:
                                    print(error)
                                
                            except Exception as a:
                                print('Erro ao cadastrar, erro: %s'%a)
        except:
            continue