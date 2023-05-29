from apps.admcore import models

cidades = ['SANTA']  #nome da cidade
ID_POP_ESP = 1  #só altera contratos que estejam nesse pop
ID_POP = 8  #Id do pop que os contratos devem ser migrados


for c in models.ClienteContrato.objects.filter(pop_id=ID_POP_ESP):
    if cidades[0] in c.cobranca.endereco.cidade:
        c.pop_id = ID_POP
        c.save()
        print c, c.cliente.endereco.cidade, c.pop