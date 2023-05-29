
from apps.financeiro import models as fmodels
import csv
from django.db.models import F

fnum = lambda n: re.sub('[^0-9]', '', unicode(n))

with open('/tmp/ixc-titulos-corrigidos-portador-35.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            nosso_numero_atual=row[5]
            novo_nosso_numero=row[4]

            titulo=fmodels.Titulo.objects.filter(nosso_numero=nosso_numero_atual, portador=35, usuario_g__username='sgp')
            for t in titulo:
                print("Atualizando titulo: ", t)
                try:
                    fmodels.Titulo.objects.filter(nosso_numero=nosso_numero_atual, portador=35, usuario_g__username='sgp').update(nosso_numero=novo_nosso_numero)
                except Exception as e:
                    try:
                        print('Excessão tentando atualizar nosso numero para 96669666')
                        fmodels.Titulo.objects.filter(nosso_numero=novo_nosso_numero, portador=35, usuario_g__username='sgp').update(nosso_numero=96669666)
                        fmodels.Titulo.objects.filter(nosso_numero=nosso_numero_atual, portador=35, usuario_g__username='sgp').update(nosso_numero=novo_nosso_numero)
                        fmodels.Titulo.objects.filter(nosso_numero=96669666, portador=35, usuario_g__username='sgp').update(nosso_numero=F('numero_documento'))
                    except Exception as e:
                        print(e)
                        break
                    print(e)
                    continue