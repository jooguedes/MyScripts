from apps.admcore import models

for cc in models.ClienteContrato.objects.all():
    servicointernet = models.ServicoInternet.objects.filter(clientecontrato=cc).order_by('id')
    if len(servicointernet) > 1:
        login = ''
        for si in servicointernet:
            if login == '':
                login = si.login
            if login in si.login:
                if len(si.login) > len(login):
                    si.delete()
                    print('Login %s removido!'%si.login)