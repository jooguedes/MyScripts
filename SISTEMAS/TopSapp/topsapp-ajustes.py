from apps.admcore import models
from apps.financeiro import models as fmodels 

cnpjlista = []

l = []

for cnpj in cnpjlista:
    if cnpj in l:
        continue
    l.append(cnpj)
    clientes = models.Cliente.objects.filter(pessoa__cpfcnpj__trim=cnpj.strip()).order_by('id')
    if len(clientes) > 1:
        c0 = clientes[0]
        lv = models.Cliente.objects.filter(pessoa__cpfcnpj__trim=cnpj.strip(),
                                           pessoa__nome__trim__upper=unicode(c0.pessoa.nome.strip().upper()))
        if len(lv) > 1:
            print(c0.id, c0)
            ids = [c.id for c in lv]
            models.ClienteContrato.objects.filter(cliente__in=lv).update(cliente=c0)
            fmodels.Cobranca.objects.filter(cliente__in=lv).update(cliente=c0)
            fmodels.Titulo.objects.filter(cliente__in=lv).update(cliente=c0)
            models.History.objects.filter(app_label='admcore',model_name='cliente',object_id__in=ids).update(object_id=c0.id)



from apps.admcore import models
from apps.financeiro import models as fmodels 

cpflista = []

l = []

for cpf in cpflista:
    if cpf in l:
        continue
    l.append(cpf)
    clientes = models.Cliente.objects.filter(pessoa__cpfcnpj__trim=cpf.strip()).order_by('id')
    if len(clientes) > 1:
        c0 = clientes[0]
        lv = models.Cliente.objects.filter(pessoa__cpfcnpj__trim=cpf.strip(),pessoa__nome=c0.pessoa.nome)
        if len(lv) > 1:
            print(c0)
            ids = [c.id for c in lv]
            models.ClienteContrato.objects.filter(cliente__in=lv).update(cliente=c0)
            fmodels.Cobranca.objects.filter(cliente__in=lv).update(cliente=c0)
            fmodels.Titulo.objects.filter(cliente__in=lv).update(cliente=c0)
            models.History.objects.filter(app_label='admcore',model_name='cliente',object_id__in=ids).update(object_id=c0.id)

            