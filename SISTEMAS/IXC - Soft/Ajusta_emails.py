from apps.admcore import models as admmodels
contato=admmodels.Contato.objects.filter(tipo='EMAIL')

for cc in contato:
    #print(cc.contato)
    new_email=str(cc.contato).split(';')
    try:
        cliente=admmodels.Cliente.objects.filter(clientecontato__contato=cc.id)
        
    except Exception as e:
        print(e)
        continue
    if len(new_email) > 1:
        print(new_email)
        print(cliente)
        for i in len(new_email):
            try:
                new_contato_email= admmodels.Contato()
                new_contato_email.tipo = 'EMAIL'
                new_contato_email.contato = new_email[i]
                new_contato_email.save()
                new_ccontato_email = admmodels.ClienteContato()
                new_ccontato_email.cliente = cliente[0]
                new_ccontato_email.contato = new_contato_email
                new_ccontato_email.save()
            except Exception as e:
                print(e)
                continue

        admmodels.Contato.objects.filter(id=cc.id).delete()
    else:
        continue