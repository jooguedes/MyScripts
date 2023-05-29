from apps.admcore import models
from django.db.models import Q

logins = models.Cliente.objects.filter(Q(clientecontrato__isnull=True))

for c in logins:
    endereco=models.Endereco.objects.filter(cliente__id=c.id)
    contato=models.Contato.objects.filter(clientecontato__cliente__id=c.id)
    print('cliente: ',c, 'cpf/cnpj: ', c.pessoa.cpfcnpj, 'Endereco: ',
                                                          endereco[0].cidade, endereco[0].uf,
                                                          endereco[0].logradouro, endereco[0].bairro, endereco[0].numero)

    for cc in contato:
        print("Contatos do Cliente: ", cc.contato)
