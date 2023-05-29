from apps.financeiro import models as fmodels
from apps.cauth import models as authmodels
from apps.netcore.utils.radius import manage
import csv
import re
import copy

def strdate(p):
    try:
        d,m,y = p.split()[0].split('.')
        if len(d) < 2:
            d = '0%s'%d
        if len(m) < 2:
            m = '0%s'%m
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

fnum = lambda n: re.sub('[^0-9]', '', n)
usuario = authmodels.User.objects.get(username='sgp')
m = manage.Manage()
with open('/tmp/Conv-recebiveis-perficio.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        nosso_numero=row[10]
        data_cadastro=strdate(row[14])
        try:
            fmodels.Titulo.objects.filter(nosso_numero=nosso_numero, portador=1).update(data_documento=data_cadastro)
        except Exception as e:
            print(e)
        