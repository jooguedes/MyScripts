from apps.admcore import models

contatos=models.Contato.objects.all()
fnum = lambda n: re.sub('[^0-9]', '', n)
for c in contatos:
    #print(c, c.contato, c.clientecontato.cliente)
    if(str(c.tipo)!='EMAIL' and len(str(fnum(c.contato))) > 20):
    	print(c)
        models.Contato.objects.filter(id=c.id).delete()