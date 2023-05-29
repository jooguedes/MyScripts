from apps.atendimento import models

for oc in models.Ocorrencia.objects.filter(clientecontrato__cliente__id='165813'):
    print(oc)


from apps.atendimento import models 

models.Ocorrencia.objects.filter(tipo_id='710').update(tipo_id=306)