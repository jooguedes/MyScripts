from apps.financeiro import models
import csv



with open('/tmp/Cobrancas-Total-Mikiweb.csv', 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            titulo=models.Titulo.objects.filter(portador=1, numero_documento=row[0], status=models.MOVIMENTACAO_PAGA)
            try:
                print(titulo[0].valor,titulo[0].valorpago)
                valorpago = row[9].replace(',', '.')
                valorpago_sistema=titulo[0].valorpago
                print('Valor pago arquivo: ',valorpago)
                
                if(float(valorpago)!=float(valorpago_sistema)):
                    models.Titulo.objects.filter(id=titulo[0].id).update(valorpago=valorpago)

            except Exception as e:
                print(e)
                continue
            
