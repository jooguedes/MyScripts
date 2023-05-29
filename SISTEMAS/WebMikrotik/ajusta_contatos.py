from apps.admcore import models as admmodels
import re
telefones = admmodels.ClienteContato.objects.all()
for c in telefones:
    try:
      cliente = admmodels.Cliente.objects.filter(id=c.cliente.id)
        
          
      if(len(re.sub('[^0-9]','',c.contato.contato))>11 and c.contato.tipo!='EMAIL'):
          
          new_contato = admmodels.Contato()
          new_contato.tipo = 'CELULAR_PESSOAL'
          new_contato.contato = str(re.sub('[^0-9]','',c.contato.contato))[10:22]
          new_contato.save()
          new_ccontato = admmodels.ClienteContato()
          new_ccontato.cliente = cliente[0]
          new_ccontato.contato = new_contato
          new_ccontato.save()
          
      admmodels.Contato.objects.filter(id=c.contato.id).update(contato=c.contato.contato[:10])
    except:
        continue