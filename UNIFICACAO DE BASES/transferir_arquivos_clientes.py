from apps.admcore import models
from django.conf import settings
import os
########################################################
POPS_ID = [1, 2]
########################################################
DESTINO = '/usr/local/sgp/media/sgp'
########################################################
SSH_PORT = '22888'
SSH_USER = 'root'
SSH_HOST = '45.234.218.2'
########################################################

documentos = models.ClienteDocumento.objects \
    .filter(cliente__clientecontrato__pop__in=POPS_ID) \
    .order_by('cliente', 'data_cadastro') \
    .select_related('cliente__pessoa')

total = documentos.count()
print ('total: %s' % total)
print ('--------')

for doc in documentos:
    origem = '%s%s' % (settings.MEDIA_ROOT, doc.arquivo)
    destino = '%s/%s' % (DESTINO, origem.replace(settings.MEDIA_ROOT, ''))
    
    if os.path.exists(origem):
        cmd = 'ssh  %(user)s@%(host)s -p %(port)s mkdir -p %(path)s' % \
            {'user': SSH_USER, 'host': SSH_HOST, 'port': SSH_PORT, 
             'path': os.path.dirname(destino)}
        os.system(cmd)
        #
        cmd = 'rsync --ignore-existing -e \'ssh -p %(port)s\' %(origem)s %(user)s@%(host)s:%(destino)s' % \
            {'port': SSH_PORT, 'origem': origem, 'user': SSH_USER, 
             'host': SSH_HOST, 'destino': destino}
        os.system(cmd)

        print ('cliente: %s >> %s' % (doc.cliente.pessoa.nome, doc))        

    total -= 1
    print ('-------- restam %s -----------' % total)