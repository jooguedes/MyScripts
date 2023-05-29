
from apps.admcore import models
import re

fnum = lambda n: re.sub('[^0-9]', '', str(n))
contato=models.Contato.objects.filter(tipo__in=['TELEFONE_FIXO_RESIDENCIAL',
										'TELEFONE_FIXO_COMERCIAL',
										'TELEFONE_RESPONSAVEL',
										'CELULAR_PESSOAL',
										'CELULAR_COMERCIAL',
										'CELULAR_COBRANCA', 
										'CELULAR_RESPONSAVEL'])
for c in contato:
	contato=fnum(c.contato)
	cliente=models.Cliente.objects.filter(clientecontato__contato__id=c.id)
	if len(contato)==12:
		if(int(contato[3])==9):
			print("Removendo contato: ", contato, " Do Cliente: ", cliente)
			new_contato=list(contato).pop(3)
			new_contato=''.join(map(str,new_contato))
			models.Contato.objects.filter(id=c.id).update(contato=new_contato)









from apps.admcore import models
contato=models.Contato.objects.filter(clientecontato__cliente__isnull=True)
for c in contato:

    print('Removendo contato: ',c, 'de ID: ', c.id)
    models.Contato.objects.filter(id=c.id).delete()