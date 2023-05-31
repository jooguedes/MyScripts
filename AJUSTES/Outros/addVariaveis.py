from apps.admcore import models as admmodels
from django.db import connection

usuario = admmodels.User.objects.get(username='sgp')

#COORDENADAS = '-12.9704,-38.5124'
COORDENADAS = ''
# adcionar url sem '/' no final
URL = 'https://wendor.sgp.tsmx.com.br/'
# Apenas para SGPs instalados em máquinas locais
NOME_PROVEDOR = ''

if URL[-1] == '/':
    URL = URL[:-1]

if admmodels.Config.objects.filter(var='BLOQUEIO_DESATIVADO').count() == 0:
    new_var = admmodels.Config()
    new_var.var='BLOQUEIO_DESATIVADO'
    new_var.description='BLOQUEIO_DESATIVADO'
    new_var.value='1'
    new_var.user=usuario
    new_var.active=True
    new_var.save()

if admmodels.Config.objects.filter(var='ANATEL_DICI_QT_ACESSOS').count() == 0:
    new_var = admmodels.Config()
    new_var.var='ANATEL_DICI_QT_ACESSOS'
    new_var.description='ANATEL_DICI_QT_ACESSOS'
    new_var.value='ACESSOS'
    new_var.user=usuario
    new_var.active=True
    new_var.save()

if admmodels.Config.objects.filter(var='ANATEL_DICI_BOOM').count() == 0:
    new_var = admmodels.Config()
    new_var.var='ANATEL_DICI_BOOM'
    new_var.description='ANATEL_DICI_BOOM'
    new_var.value='1'
    new_var.user=usuario
    new_var.active=True
    new_var.save()

if len(COORDENADAS) > 4 and admmodels.Config.objects.filter(var='GOOGLE_MAPS_CENTER').count() == 0:
    new_var = admmodels.Config()
    new_var.var='GOOGLE_MAPS_CENTER'
    new_var.description='GOOGLE_MAPS_CENTER'
    new_var.value=COORDENADAS
    new_var.user=usuario
    new_var.active=True
    new_var.save()
    
    
if len(URL) > 4:
    if admmodels.Config.objects.filter(var='SMS_FATURA_URL').count() == 0:
        new_var = admmodels.Config()
        new_var.var='SMS_FATURA_URL'
        new_var.description='SMS_FATURA_URL'
        new_var.value=URL
        new_var.user=usuario
        new_var.active=True
        new_var.save()
    if admmodels.Config.objects.filter(var='EMAIL_FATURA_URL').count() == 0:
        new_var = admmodels.Config()
        new_var.var='EMAIL_FATURA_URL'
        new_var.description='EMAIL_FATURA_URL'
        new_var.value=URL
        new_var.user=usuario
        new_var.active=True
        new_var.save()

if len(NOME_PROVEDOR) > 4:
    if admmodels.Config.objects.filter(var='SMS_PROVEDOR_NOME').count() == 0:
        new_var = admmodels.Config()
        new_var.var='SMS_PROVEDOR_NOME'
        new_var.description='SMS_PROVEDOR_NOME'
        new_var.value=NOME_PROVEDOR
        new_var.user=usuario
        new_var.active=True
        new_var.save()

    if admmodels.Config.objects.filter(var='EMAIL_PROVEDOR_NOME').count() == 0:
        new_var = admmodels.Config()
        new_var.var='EMAIL_PROVEDOR_NOME'
        new_var.description='EMAIL_PROVEDOR_NOME'
        new_var.value=NOME_PROVEDOR
        new_var.user=usuario
        new_var.active=True
        new_var.save()

for var in admmodels.Config.objects.all():
    print(var)

F_="""
DELETE FROM financeiro_feriado WHERE tipo=3 and data >= '2021-01-01' and data <= '2022-12-31';
INSERT INTO financeiro_feriado VALUES (default, 'Confraternização Universal', '2023-01-01', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Carnaval', '2023-02-20', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Carnaval', '2023-02-21', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Paixão de Cristo', '2023-04-07', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Tiradentes', '2023-04-21', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Dia do trabalhador', '2023-05-01', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Corpus Christi', '2023-06-08', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Independência do Brasil', '2023-09-07', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Nossa Sr.a Aparecida - Padroeira do Brasil', '2023-10-12', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Finados', '2023-11-02', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Proclamação da República', '2023-11-15', 3);
INSERT INTO financeiro_feriado VALUES (default, 'Natal', '2023-12-25', 3);
"""
with connection.cursor() as cursor:
    cursor.execute(F_)