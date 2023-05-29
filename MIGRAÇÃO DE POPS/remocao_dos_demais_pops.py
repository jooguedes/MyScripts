# -------------------------------------------------------#
MIGRAR_POP_ID = 111 #(ID POP)
DELETE = True
# -------------------------------------------------------#
from apps.admcore import models
from apps.precadastro import models as pmodels
from apps.estoque2 import models as e2models
from apps.cobranca import models as cobmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as netmodels
from apps.fiscal import models as fismodels
from django.db.models import Q, F, Count, Sum
from django.db.models.functions import Concat
from django.db import transaction, connection

clientes = models.Cliente.objects.all()
error = False

if DELETE:
    # clientes
    for c in clientes:
        print (c)

        with transaction.atomic():
            try:
                for cc in c.clientecontrato_set.filter(~Q(pop__id=MIGRAR_POP_ID)):
                    cc.servicointernet_set.all().delete()
                    cc.servicomultimidia_set.all().delete()
                    cc.servicotv_set.all().delete()
                    cc.servicotelefonia_set.all().delete()

                    for titulo in cc.cobranca.titulo_set.all():
                        for caixalancamentotitulo in titulo.caixalancamentotitulo_set.all():
                            caixalancamentotitulo.caixa_lancamento.delete()
                            caixalancamentotitulo.delete()
                        titulo.delete()

                    cc.delete()

                    if models.ClienteContrato.objects.filter(cliente=c).count() == 0:
                        c.venda_set.all().delete()
                        c.comodato_set.all().delete()
                        e2models.Local_lacamento.objects.filter(cliente=c).delete()
                        
                        c.delete()
                        
            except Exception as e:
                print (str(e))
                error = True
            
    if not error:
        # portador
        portadores = fmodels.Portador.objects \
            .annotate(total_t=Count('titulo'), 
                      total_c=Count('cobranca')) \
            .filter(total_t=0, 
                    total_c=0)

        for p in portadores:
            try:
                pontos = fmodels.PontoRecebimento.objects \
                    .filter(Q(portador=p)|Q(portadores=p))

                for ponto in pontos:
                    ponto.caixalancamento_set.all().delete()
                    ponto.ponto_recebimento_origem.all().delete()
                    ponto.ponto_recebimento_destino.all().delete()
                    ponto.delete()
                
                p.delete()
            except Exception as e:
                print (str(e))

        pagar = fmodels.Pagar.objects.all().delete()

        # nota fiscal
        nf55 = fismodels.NFe.objects \
            .filter(cliente__isnull=True).delete()

        nd = fismodels.NotaDebito.objects \
            .filter(cliente__isnull=True).delete()
        
        nf = fismodels.NotaFiscal.objects \
            .filter(destinatario__cliente__isnull=True).delete()

        fismodels.SpedArquivo.objects.all().delete()
        fismodels.SintegraArquivo.objects.all().delete()
        fismodels.NotaFiscalArquivo.objects.all().delete()

        # net
        nas = netmodels.NAS.objects \
            .annotate(total=Count('servicointernet')) \
            .filter(total=0).delete()

        onu = netmodels.ONU.objects \
            .filter(service__isnull=True).delete()

        cto = netmodels.Splitter.objects \
            .annotate(total=Count('onu')) \
            .filter(total=0).delete()

        pon = netmodels.OltPon.objects \
            .annotate(total=Count('onu')) \
            .filter(total=0).delete()

        olt = netmodels.OLT.objects \
            .annotate(total=Count('oltpon')) \
            .filter(total=0).delete()
        
        ap = netmodels.AP.objects \
            .annotate(total=Count('servicointernet')) \
            .filter(total=0).delete()

        # planos
        planos = []
        
        planos += list(models.PlanoInternet.objects \
            .annotate(total=Count('servicointernet')) \
            .filter(total=0))

        planos += list(models.PlanoTV.objects \
            .annotate(total=Count('servicotv')) \
            .filter(total=0))

        planos += list(models.PlanoMultimidia.objects \
            .annotate(total=Count('servicomultimidia')) \
            .filter(total=0))

        planos += list(models.PlanoTelefonia.objects \
            .annotate(total=Count('servicotelefonia')) \
            .filter(total=0))

        for p in planos:
            with transaction.atomic():
                try:
                    p.plano.delete()
                    p.delete()
                except Exception as e:
                    print (str(e))

        # pre cadastro
        with transaction.atomic():
            try:
                pmodels.PessoaFisica.objects.all().delete()
                pmodels.PessoaJuridica.objects.all().delete()
            except Exception as e:
                print (str(e))

        # financeiro
        with transaction.atomic():
            try:
                fmodels.GatewayPagamento.objects.all() \
                    .update(token=None, usuario=None, 
                            senha=None, chave_pix=None)
                # fmodels.Vencimento.objects.all() \
                #     .update(dia=F('dia') + 100)
            except Exception as e:
                print (str(e))

        # outros
        models.GatewayAssinaturaEletronica.objects.all().delete()
        models.ConfigSms.objects.all().delete()
        models.ConfigSmtp.objects.all().delete()
        models.Funcionario.objects.all().delete()
        cobmodels.EmailAviso.objects.all().delete()
        cobmodels.SMSAviso.objects.all().delete()
        models.EmailHistory.objects.all().delete()
        netmodels.SMS.objects.all().delete()

        # pop
        with transaction.atomic():
            try:
                models.Pop.objects.filter(~Q(id=MIGRAR_POP_ID)).delete()
            except Exception as e:
                print (str(e))