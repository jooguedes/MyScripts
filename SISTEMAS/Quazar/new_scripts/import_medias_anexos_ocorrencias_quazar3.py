from apps.atendimento import models as amodels
from apps.cauth import models as authmodels
from datetime import date,datetime
import shutil
import os

pasta = '/tmp/media/suporte-atendimento'
usuario = authmodels.User.objects.get(username='sgp')
nome_perfil = 'oknet' # Para máquina local coloque nome_perfil='local'
save = True # Execute como falso para conferir se os dados estão corretos, depois mude para True

# import arquivos clientes radiusnet
for diretorio, subpastas, arquivos in os.walk(pasta):
    for arquivo in arquivos:
        try:
            caminho = str(os.path.join(os.path.realpath(diretorio), arquivo))
            id_ocorrencia=int(caminho.split('/')[4])
            descricao=caminho.split('/')[-1].split('.')[0]
            ocorrencia = amodels.Ocorrencia.objects.filter(id=id_ocorrencia)
            arquivo = 'ocorrencias/%s'%caminho.split('/')[-1]
            print(ocorrencia,descricao, caminho)
        
            if ocorrencia and save:
                if amodels.OcorrenciaAnexo.objects.filter(ocorrencia=ocorrencia, descricao=descricao).count() == 0:
                    try:
                        print(ocorrencia,descricao, caminho)
                        ocorrenciaanexo = amodels.OcorrenciaAnexo()
                        ocorrenciaanexo.ocorrencia = ocorrencia[0]
                        ocorrenciaanexo.descricao = descricao
                        ocorrenciaanexo.arquivo = arquivo
                        ocorrenciaanexo.usuario = usuario
                        ocorrenciaanexo.save()                       
                        try:
                            path = str('/usr/local/sgp/media/%s/ocorrencias/'%(nome_perfil))
                            if not os.path.isdir(path):
                                os.makedirs(path)
                            shutil.copy(caminho, '/usr/local/sgp/media/%s/ocorrencias/'%(nome_perfil))
                        except OSError as error:
                            print(error)
                        
                    except Exception as a:
                        print('Erro ao cadastrar, erro: %s'%a)
        except Exception as e:
            print(e)