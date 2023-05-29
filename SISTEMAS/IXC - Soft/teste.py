from apps.admcore import models
titulo=models.Contato.objects.exclude(tipo='EMAIL')

for t in titulo:
    if(t.contato[:2]!='81'):
        print(t)
        old_contato=str(t.contato)
        if(len(old_contato)==8):
            new_contato='819'+old_contato
            models.Contato.objects.filter(id=t.id).update(contato=new_contato)
        if(len(old_contato)==9):
             new_contato='81'+old_contato
             models.Contato.objects.filter(id=t.id).update(contato=new_contato)