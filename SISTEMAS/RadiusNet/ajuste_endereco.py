import csv
import re
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels

fnum = lambda n: re.sub('[^0-9]', '', unicode(n))

print('Importando clientes')
with open('/tmp/Conv-clientes.csv', 'rb',  ) as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"', )
    for row in conteudo: 
        row = [entry.decode("utf8") for entry in row]  

        cpfcnpj=row[3]
        end_inst = row[20].split('-') 
        if len(end_inst) == 1:
            end_inst = 'FALTA PREENCHER, 0  - BAIRRO - São Paulo/SP CEP: 02309130'.split('-')

        end_cob = row[21].split('-')
        if len(end_cob) == 1:
                end_cob = end_inst


        print(end_cob)
        endereco_cob = {}
        
        endereco_cob['logradouro'] = end_cob[0].strip()[:50]
        endereco_cob['numero'] = fnum(end_cob[1].strip())[:5]
        if not endereco_cob.get('numero'):
            endereco_cob['numero'] = None
        if len(str(endereco_cob['numero']))>4:
            endereco_cob['numero'] =str(end_cob['numero'])[-4:-1]
        endereco_cob['bairro'] = end_cob[-2].strip()[:50]


        endereco_inst = {}
        endereco_inst['logradouro'] = end_inst[0].strip()[:50]
        endereco_inst['numero'] = fnum(end_inst[1].strip())[:5]
        if not endereco_inst.get('numero'):
            endereco_inst['numero'] = None
        if len(str(endereco_inst['numero']))>4:
            endereco_inst['numero'] =str(endereco_inst['numero'])[-4:-1]

        endereco_inst['bairro'] = end_inst[-2].strip()[:50]
            
      

        try:    
            endereco_cliente=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
            for enc in endereco_cliente:
                admmodels.Endereco.objects.filter(id=enc.endereco.id).update(numero=endereco_inst['numero'], logradouro=endereco_inst['logradouro'], bairro=endereco_inst['bairro'])

        except Exception as e:
            print(e)
        
        endereco_cobranca=fmodels.Cobranca.objects.filter(cliente__pessoa__cpfcnpj__numfilter=cpfcnpj)

        for ec in endereco_cobranca:
            admmodels.Endereco.objects.filter(id=ec.endereco.id).update(numero=endereco_cob['numero'], logradouro=endereco_cob['logradouro'], bairro=endereco_cob['bairro'])

        endereco_servico= admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__pessoa__cpfcnpj__numfilter=cpfcnpj)
        
        for es in endereco_servico:
            admmodels.Endereco.objects.filter(id=es.endereco.id).update(numero=endereco_inst['numero'],logradouro=endereco_inst['logradouro'], bairro=endereco_inst['bairro'])