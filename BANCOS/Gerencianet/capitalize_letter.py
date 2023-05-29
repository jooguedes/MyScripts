from apps.admcore import models


def to_capitalize(name):
    list_name=name.split(' ')
    capitalize_name=''
    for l in list_name:
        capitalize_name+=str(l).capitalize()+' '

    return capitalize_name.strip()



for name in models.Pessoa.objects.all():
    new_name= to_capitalize(name.nome)
    print('Nome Antigo', name.nome)
    print('Novo Nome: ', new_name)
    admmodels.Pessoa.objects.filter(id=name.id).update(nome=new_name)