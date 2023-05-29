from apps.financeiro import models 
from django.db import transaction
for t in models.Titulo.objects.filter(data_baixa__isnull=False,caixalancamentotitulo__isnull=True,valorpago__gt=0):
    pontorecebimento=models.PontoRecebimento.objects.filter(portador=t.portador)
    if pontorecebimento:
        pontorecebimento=pontorecebimento[0]
        with transaction.atomic():
            caixalanc = models.CaixaLancamento()
            caixalanc.ponto_recebimento = pontorecebimento
            caixalanc.centrodecusto = t.centrodecusto
            caixalanc.usuario = t.usuario_b
            caixalanc.tipo_operacao = models.CAIXA_OPERACAO_ENTRADA
            caixalanc.forma_pagamento = t.formapagamento
            caixalanc.observacao = None
            caixalanc.valor = t.valorpago
            caixalanc.data_competencia = t.data_baixa
            caixalanc.data_cadastro=t.data_baixa
            caixalanc.save()
            caixalanc.data_competencia=t.data_baixa
            caixalanc.data_cadastro=t.data_baixa
            caixalanc.save()
            caixalanctitulo = models.CaixaLancamentoTitulo()
            caixalanctitulo.titulo = t
            caixalanctitulo.caixa_lancamento = caixalanc
            caixalanctitulo.save()
            print t,caixalanctitulo
