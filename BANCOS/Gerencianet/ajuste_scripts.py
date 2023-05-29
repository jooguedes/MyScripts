from apps.admcore import models
import re


tipos_ignorados=['EMAIL', 'EMAIL_COBRANCA', 'SKYPE', 'TWITTER', 'YAHOO_MESSENGER', 'GOOGLE_TALK', 'URL_SITE', 'MSN_MESSENGER', 'INSTAGRAM']
contatos= models.Contato.objects.all()

for c in contatos:

    if c.tipo not in tipos_ignorados:
        print c.contato, len(c.contato),'digitos'





from apps.admcore import models
import re
tipos_ignorados=['EMAIL', 'EMAIL_COBRANCA', 'SKYPE', 'TWITTER', 'YAHOO_MESSENGER', 'GOOGLE_TALK', 'URL_SITE', 'MSN_MESSENGER', 'INSTAGRAM']
contatos= models.Contato.objects.filter(clientecontato__cliente__clientecontrato__pop_id=ID_POP)
for c in contatos:
    if c.tipo not in tipos_ignorados:
        print c.contato, len(c.contato), 'digitos'



from apps.admcore import models
tipos_ignorados=['EMAIL', 'EMAIL_COBRANCA', 'SKYPE', 'TWITTER', 'YAHOO_MESSENGER', 'GOOGLE_TALK', 'URL_SITE', 'MSN_MESSENGER', 'INSTAGRAM']
contatos=models.Contato.objects.all()

for c in contatos:
    if c.tipo not in tipos_ignorados:
        if len(str(c.contato))< 11 or c.contato =='' or len(str(c.contato))>15:
            try:
                print(c, models.ClienteContato.objects.filter(contato=c.id)[0].cliente)
            except:
                pass