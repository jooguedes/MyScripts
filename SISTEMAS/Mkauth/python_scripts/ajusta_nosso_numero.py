import csv
from apps.financeiro import models

titulos=[]
#nosso_numero_02=''
with open('/tmp/mkauth-titulos-correcao-portador-3.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        try:
            print('Atualizando nosso_numero do Titulo: ', models.Titulo.objects.filter(numero_documento=row[0]))
            nosso_numero_01= row[1][2:]
            nosso_numero_02= nosso_numero_01[:-1]
            print(nosso_numero_02)

            models.Titulo.objects.filter(portador=3,numero_documento=row[0]).update(nosso_numero=nosso_numero_02)
        except:
            try:
                titulos.append(models.Titulo.objects.filter(numero_documento=row[0])[0].numero_documento)
                print('titulos conflitantes: ', titulos)
            except:
                continue



with open('/tmp/mkauth-titulos-4-corrigidos.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if row[0] in titulos:
            print('Atualizando Nosso Dos Titulos conflitantes')
            models.Titulo.objects.filter(portador=3,numero_documento=row[9]).update(nosso_numero=row[10])