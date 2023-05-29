import csv
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels

ids_titulos=[]
usuario = admmodels.User.objects.get(username='sgp')
with open('/tmp/Ajuste_cobrancas.csv', 'rb') as csvfile:
    conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
    for row in conteudo:
        cpfcnpj=row[1]
        if len(cpfcnpj) ==10:
            cpfcnpj_pessoafisica='0'+str(cpfcnpj)
        try:
            cliente=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj_pessoafisica)[0]
        except Exception as e:
            try:
                if len(cpfcnpj)==13:
                    cpfcnpj_pessoajuridica='0'+str(cpfcnpj)
                    cliente=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj_pessoajuridica)[0]
                
            except:
                print('Cliente não identificado: ', row[0], ' - ', row[1])
                continue

        print(cliente)
        valor=row[3]
        valor_pago=row[4]
        d,m,y= row[2].split('/')
        vencimento= '%s-%s-%s' %(y,m,d)
        if cliente and row[5]=='pago':
            titulo=fmodels.Titulo.objects.filter(status=fmodels.MOVIMENTACAO_GERADA, 
                                            data_vencimento=vencimento,
                                            cliente=cliente,
                                            valor=valor)
            print('Baixando titulo: ', titulo)
            try:
                ids_titulos.append(titulo[0].id)
            except Exception as e:
                print(e)


            fmodels.Titulo.objects.filter(status=fmodels.MOVIMENTACAO_GERADA, 
                                            data_vencimento=vencimento,
                                            cliente=cliente,
                                            valor=valor).update(status=fmodels.MOVIMENTACAO_PAGA,
                                            usuario_b=usuario,
                                            data_baixa=vencimento,
                                            data_pagamento=vencimento,
                                            valorpago=valor_pago,
                                            observacao='Titulos baixados mediante solicitação do protocolo: 221101163903')
        
        

        

        