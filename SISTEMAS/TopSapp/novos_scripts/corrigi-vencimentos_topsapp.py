from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
import csv

#################################################################
#       UTILIZE OS ARQUIVOS ENVIADOS PELO PROPRIO TOPSSAP       #
#       servico_clientes.csv                                    #
#       vencimento.csv                                          #
#                                                               #
#################################################################

with open('/tmp/servicos_clientes.csv', 'rb') as csvfile:
  conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
  for row in conteudo:
    cliente_id=row[2]
    venciment_id=row[7]
    with open('/tmp/vencimentos.csv', 'rb') as csvfile:
        vencimentos = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in vencimentos:

            if venciment_id==row[0]:
              vencimento=row[1]
              try:
                v=fmodels.Vencimento.objects.get(dia=vencimento)
                fmodels.Cobranca.objects.filter(cliente__id=cliente_id).udpate(vencimento=v)
              except Exception as e:
                print(e)
                try:
                  print "erro vencimento %s" %vencimento 
                
                  print('corrigindo vencimento %s' %vencimento)
                  new_vencimento = fmodels.Vencimento()
                  new_vencimento.dia = vencimento
                  new_vencimento.save() 
                  v=fmodels.Vencimento.objects.get(dia=vencimento)
                
                  fmodels.Cobranca.objects.filter(cliente__id=cliente_id).update(vencimento=v)
                except Exception as e:
                  print(e)
                  continue