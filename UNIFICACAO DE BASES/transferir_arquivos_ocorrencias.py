from apps.atendimento import models
from django.conf import settings
import os
#######################################################
POPS_ID = [1, 2]
PREFIXO = "A"
#######################################################
PERFIl = 'local'
DESTINO = '/usr/local/sgp/media/%s' % PERFIl
#######################################################
SSH_PORT = '1822'
SSH_USER = 'root'
SSH_HOST = '45.234.218.2'
RSA = '/root/.ssh/id_rsa'
#######################################################

ocorrencias = models.OcorrenciaAnexo.objects \
    .filter(ocorrencia__clientecontrato__pop__in=POPS_ID) \
    .order_by('ocorrencia', 'data_cadastro') \
    .select_related('ocorrencia__clientecontrato__cliente__pessoa')

total = ocorrencias.count()
print ('total: %s' % total)
print ('--------')

for doc in ocorrencias:
    origem = str(doc.arquivo.path)
    destino = '%s/%s' % (DESTINO, origem.replace(settings.MEDIA_ROOT, ''))
    destino_ = destino.split('/')[:-2]
    destino_.append('A%s' % doc.ocorrencia.numero[0:13])
    destino_.append(destino.split('/')[-1])
    destino = '/'.join(destino_)
    
    if os.path.exists(origem):
        cmd = 'ssh -i %(rsa)s %(user)s@%(host)s -p %(port)s mkdir -p %(path)s' % \
            {'rsa': RSA,
             'user': SSH_USER, 'host': SSH_HOST, 'port': SSH_PORT, 
             'path': os.path.dirname(destino)}
        os.system(cmd)
        #
        cmd = 'rsync --ignore-existing -e \'ssh -i %(rsa)s -p %(port)s\' %(origem)s %(user)s@%(host)s:%(destino)s' % \
            {'rsa': RSA,
             'port': SSH_PORT, 'origem': origem, 'user': SSH_USER, 
             'host': SSH_HOST, 'destino': destino}
        os.system(cmd)

        print ('ocorrencia: %s : %s >> %s' % (doc.ocorrencia, origem, destino))        

    total -= 1
    print ('-------- restam %s -----------' % total)