from apps.admcore import models 
import copy

#Caso deseje fazer em um contrato apenas, substitua para models.ClienteContrato.objects.filter(id=IDCONTRATO): e descomente a linha abaixo, informando o id do contrato
IDCONTRATO = 331

for c in models.ClienteContrato.objects.filter(id=IDCONTRATO):
    servicos = []
    for s in c.servicointernet_set.all():
        servicos.append(s)
    for s in c.servicotv_set.all():
        servicos.append(s)
    for s in c.servicomultimidia_set.all():
        servicos.append(s)
    for s in c.servicotelefonia_set.all():
        servicos.append(s)
   
    if len(servicos) > 1:
        for s in servicos[1:]:
            try:
                print s
                new_endereco = copy.copy(c.cobranca.endereco)
                new_endereco.id = None 
                new_endereco.save()
                new_cobranca = copy.copy(c.cobranca)
                new_cobranca.id = None
                new_cobranca.endereco = new_endereco
                new_cobranca.save() 
                new_contrato = copy.copy(c)
                status = new_contrato.status.status
                usuario = new_contrato.status.usuario
                data_cadastro = new_contrato.status.data_cadastro
                new_contrato.id = None
                new_contrato.status = None 
                new_contrato.cobranca = new_cobranca
                new_contrato.save()
                for ic in [6,2,status]:
                    new_status = models.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario 
                    new_status.data_cadastro = data_cadastro 
                    new_status.save()             
                    new_status.data_cadastro = data_cadastro 
                    new_status.save() 
                s.clientecontrato=new_contrato
                s.save()
                print s
            except Exception as e:
                print (e)