from apps.admcore import models as admmodels
from apps.cauth import models as authmodels
import shutil
import os
pasta = '/tmp/arquivos_clientes/'
usuario = authmodels.User.objects.get(username='sgp')

for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        caminho = str(os.path.join(os.path.realpath(diretorio), arquivo))
        id_cliente=caminho.split('/')[3]
        descricao=caminho.split('/')[-1].split('.')[0]
        cliente = admmodels.Cliente.objects.filter(id=id_cliente)
        arquivo = 'arquivos/%s'%caminho.split('/')[-1]
        if cliente:
            if admmodels.ClienteDocumento.objects.filter(cliente=cliente, descricao=descricao).count() == 0:
                try:
                    cliente = cliente[0]
                    print(cliente,descricao, caminho)
                    new_doc = admmodels.ClienteDocumento()
                    new_doc.cliente=cliente
                    new_doc.descricao=descricao[0:200]
                    new_doc.arquivo=arquivo
                    new_doc.usuario = usuario 
                    new_doc.data_cadastro='2023-01-16'
                    new_doc.save()
                    # Para importar os arquivos descomente o trecho abaixo e mova os arquivos dos cliente para uma pasta no tmp com o nome Arquivos_Clientes
                    
                    try:
                        path = str('/usr/local/sgp/media/sgp/%s_arquivos/'%(cliente.id))
                        if not os.path.isdir(path):
                            os.makedirs(path)
                        shutil.copy(caminho, '/usr/local/sgp/media/sgp/%s_arquivos/'%(cliente.id))
                    except OSError as error:
                        print(error)
                    
                except Exception as a:
                    print('Erro ao cadastrar, erro: %s'%a)