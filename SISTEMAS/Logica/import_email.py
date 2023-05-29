import csv
import re 
from apps.admcore import models as admmodels
from django.db.models import Q, Max


def valida_email(e):
   if e =='':
       return False
   elif admmodels.Contato.objects.filter(contato=str(e).strip()).count()==0:
       return True
   return False

with open('/tmp/Conv-emails-filneta.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        cliente= admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=row[5])
       
        if str(row[2])!='':
            if '|' in str(row[2]):

                emails=row[2].split('|')

                for email in emails:
                    if valida_email(email):
                        try:
                            print(cliente[0])
                        except Exception as e:
                            print(e)
                            continue

                        new_contato_email = admmodels.Contato()
                        new_contato_email.tipo = 'EMAIL'
                        new_contato_email.contato = email
                        new_contato_email.save()
                        new_ccontato_email = admmodels.ClienteContato()
                        new_ccontato_email.cliente = cliente[0]
                        new_ccontato_email.contato = new_contato_email
                        new_ccontato_email.save()

                        print("Importando contato: ", email)
                    else:
                        print("Email já existe na base")
            else:
                if valida_email(row[2]):
                    try:
                        print(cliente[0])
                    except Exception as e:
                        print(e)
                        continue

                    new_contato_email = admmodels.Contato()
                    new_contato_email.tipo = 'EMAIL'
                    new_contato_email.contato = row[2]
                    new_contato_email.save()
                    new_ccontato_email = admmodels.ClienteContato()
                    new_ccontato_email.cliente = cliente[0]
                    new_ccontato_email.contato = new_contato_email
                    new_ccontato_email.save()

                    print ("Importando contato: ", email)
                else:
                    print('Email já existe na base')
                






#CORRIGE DIRETO DA BASE:
from apps.admcore import models
def valida_email(e):
   if admmodels.Contato.objects.filter(contato=str(e).strip()).count()==0:
       return True
   return False

for c in models.Contato.objects.filter(tipo='EMAIL'):
    if '|' in c.contato:
        emails=str(c.contato).split('|')
        cliente=admmodels.Cliente.objects.filter(clientecontato__contato__id=c.id)
        print(cliente[0])
        for email in emails:
            if valida_email(email):
                new_contato_email = admmodels.Contato()
                new_contato_email.tipo = 'EMAIL'
                new_contato_email.contato = email
                new_contato_email.save()
                new_ccontato_email = admmodels.ClienteContato()
                new_ccontato_email.cliente = cliente[0]
                new_ccontato_email.contato = new_contato_email
                new_ccontato_email.save()

                print("Importando contato: ", email)
            else:
                print("Email já existe na base")
        #models.Contato.objects.filter(id=c.id).delete()


#DELETA
from apps.admcore import models
for c in models.Contato.objects.filter(tipo='EMAIL'):
    if '|' in c.contato:
        print('deleteando contato: ', c)
        admmodels.Contato.objects.filter(id=c.id).delete()