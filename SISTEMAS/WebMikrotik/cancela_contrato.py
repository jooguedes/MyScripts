import csv
import re
from apps.admcore import models as admmodels
with open('/tmp/WEBMIKROTIK-CANCELADOS.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        nome=row[3]
        admmodels.ClienteContratoStatus.objects.filter(clientecontrato__cliente__pessoa__nome__lower__iexact=nome.lower()).update(status=3)










#CONTRATOS SUSPENSOS

import csv
import re
from apps.admcore import models as admmodels
with open('/tmp/Conv-20041-Contas-2023-01-09.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        if row[27]=='Não':
            login=row[3]
            admmodels.ClienteContratoStatus.objects.filter(clientecontrato__servicointernet__login=login).update(status=4)





#AJUSTA PPOPE
import csv
import re
from apps.admcore import models as admmodels
#removeleading = []
def zero_remove(word):
    while word[0] == "0":
        word = word[1:]
    #removeleading.append(word)
    #print(removeleading)
    return word


with open('/tmp/Conv-planilha_usuario_ppoe_02.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[0]
        login_sem_zero=zero_remove(login)
        cliente=admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login_sem_zero)
        
        try:
            print('Atualizando Login do Cliente: ', cliente[0].pessoa.nome, 'Com Login: ', login)
            admmodels.ServicoInternet.objects.filter(login=login_sem_zero).update(login=login)
        except Exception as e:
            print(e)

        

