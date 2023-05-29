from apps.cauth import models as authmodels
from apps.atendimento import models as amodels
from django.db.models import Q, Max
import csv

metodo = amodels.Metodo.objects.all()[0]
usuario = authmodels.User.objects.get(username='sgp')
with open('/tmp/Conv-exporta_andamentos_chamados.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        for row in conteudo:
            nu_ocorrencia=row[2]
            #ocorrencia=amodels.Ocorrencia.objects.get(numero=nu_ocorrencia)
            
            usuario= usuario
            try:
                data=str(row[3])+'.956413-03'
                ocorrencia=amodels.Ocorrencia.objects.get(numero=nu_ocorrencia)
                print(ocorrencia, usuario)
                print(data)
                new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                new_ocorrencia_anotacao.ocorrencia= ocorrencia
                new_ocorrencia_anotacao.anotacao=str(row[3])+": "+"\n"+str(row[4])
                new_ocorrencia_anotacao.data_cadastro=data
                new_ocorrencia_anotacao.usuario= usuario
                print(new_ocorrencia_anotacao)
                new_ocorrencia_anotacao.save()
            except Exception as e:
                print(e)




from apps.atendimento import models
models.OcorrenciaAnotacao.objects.all().delete()
