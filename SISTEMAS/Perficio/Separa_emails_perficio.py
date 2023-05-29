from apps.admcore import models


emails=models.Contato.objects.filter(tipo='EMAIL')

for e in emails:
    
    #print('Contatos unidos: ',e)
    #print('contatos separados: ',str(e).split()[0], str(e).split()[1])
    
    email01=str(e).split()[0]
    email02=str(e).split()[1]
    if(len(str(email02))> 6):
        print('email01: ', email01, 'Email02: ', email02)
        try:
            cliente=models.Cliente.objects.filter(id=e.clientecontato.cliente.id)
            print(cliente)
            new_contato_celular= models.Contato()
            new_contato_celular.tipo = 'EMAIL'
            new_contato_celular.contato = email02
            new_contato_celular.save()
            new_ccontato_celular = models.ClienteContato()
            new_ccontato_celular.cliente = cliente[0]
            new_ccontato_celular.contato = new_contato_celular
            new_ccontato_celular.save()
            
            models.Contato.objects.filter(id=e.id).update(contato=email01)
        except Exception as e:
            print(e)
                