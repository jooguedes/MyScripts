from apps.financeiro import models
from django.db.models import F
import csv
with open('/tmp/Conv-receber-correcao.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        numero_documento=row[0]
        pago = row[5]
        portador=row[10]
        if pago =='SIM':
            try:
                models.Titulo.objects.filter(portador=portador,
                                            numero_documento=numero_documento,
                                            usuario_g__username='sgp',
                                            status=models.MOVIMENTACAO_GERADA).update(data_pagamento=F('data_vencimento'),
                                                                                    data_baixa=F('data_vencimento'),
                                                                                    usuario_b=F('usuario_g'),
                                                                                    observacao='cancelado mediante correção de importação solicitada pelo protocolo:  221221172200',
                                                                                    status=models.MOVIMENTACAO_PAGA,
                                                                                    )
            except Exception as e:
                print(e)