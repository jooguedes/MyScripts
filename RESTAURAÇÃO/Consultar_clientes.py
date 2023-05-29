from apps.admcore import models
from apps.financeiro import models as fmodels
from apps.atendimento import models as amodels
from apps.cauth.models import User
from django.db import transaction
#################################################
#ID_CLIENTE = 183
#CPF_CLIENTE = '47819880678'
#################################################

DB_BACKUP = 'backup'
DB_DEFAULT = 'default'

with transaction.atomic():
    # ID_CLIENTE = models.Cliente.objects.using(DB_BACKUP) \
    #     .get(pessoa__cpfcnpj__numfilter=CPF_CLIENTE.strip()).id

    ID_CLIENTE = 630

    cliente_backup = models.Cliente.objects.using(DB_BACKUP) \
        .get(id=ID_CLIENTE)
    pessoa_backup = models.Pessoa.objects.using(DB_BACKUP) \
        .get(cliente=cliente_backup)
    endereco_cliente_backup = models.Endereco.objects.using(DB_BACKUP) \
        .get(id=cliente_backup.endereco.id)
    
    print(cliente_backup, pessoa_backup, endereco_cliente_backup)



'''
'backup': {
        'ENGINE':   'django.db.backends.postgresql_psycopg2',
        'NAME':     'dbturbonetjardin_old',
        'USER':     'userturbonetjardin',
        'PASSWORD': 'turbonetjardin',
        'HOST':     'localhost',
        'PORT':     '5432',
    }
'''



