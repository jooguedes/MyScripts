from apps.admcore import models as admmodels
import re

fnum = lambda n: re.sub('[^0-9]','',n)

SALVAR = False

for c in admmodels.Contato.objects.all().exclude(tipo='EMAIL'):
  if str(c.contato)[0] == '0':
    c.contato = str(c.contato)[1:]
    print(c.contato)
    if SALVAR:
        try:
            c.save()
        except Exception as e:
           print('Erro ao salvar número: ', e)