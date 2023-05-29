from apps.admcore import models
from apps.financeiro import models as fmodels
from apps.atendimento import models as amodels
from apps.cauth.models import User
from django.db import transaction
#################################################
#ID_CLIENTE = 183
#CPF_CLIENTE = '47819880678'
#################################################

DB_BACKUP = 'backup'
DB_DEFAULT = 'default'

with transaction.atomic():
    # ID_CLIENTE = models.Cliente.objects.using(DB_BACKUP) \
    #     .get(pessoa__cpfcnpj__numfilter=CPF_CLIENTE.strip()).id

    ID_CLIENTE = 630

    cliente_backup = models.Cliente.objects.using(DB_BACKUP) \
        .get(id=ID_CLIENTE)
    pessoa_backup = models.Pessoa.objects.using(DB_BACKUP) \
        .get(cliente=cliente_backup)
    endereco_cliente_backup = models.Endereco.objects.using(DB_BACKUP) \
        .get(id=cliente_backup.endereco.id)
       
    # base
    endereco_cliente_backup.save(using=DB_DEFAULT)
    pessoa_backup.save(using=DB_DEFAULT)
    cliente_backup.save(using=DB_DEFAULT)
    
    cliente = models.Cliente.objects.get(id=ID_CLIENTE)

    # contatos
    cliente_contato_backup = models.ClienteContato.objects.using(DB_BACKUP) \
        .filter(cliente=cliente_backup)

    for cc_backup in cliente_contato_backup:
        cc_backup.contato.save(using=DB_DEFAULT)

        contato = models.Contato.objects.get(id=cc_backup.contato.id)
        
        models.ClienteContato.objects \
            .get_or_create(cliente=cliente,
                           contato=contato)

    # cobranca
    cobrancas_backup = fmodels.Cobranca.objects.using(DB_BACKUP) \
        .filter(cliente=cliente_backup)
    
    for cobranca_backup in cobrancas_backup:
        endereco_cobranca_backup = models.Endereco.objects.using(DB_BACKUP) \
            .get(id=cobranca_backup.endereco.id)

        endereco_cobranca_backup.save(using=DB_DEFAULT)
        cobranca_backup.save(using=DB_DEFAULT)

        cobranca = fmodels.Cobranca.objects \
            .get(id=cobranca_backup.id)

        # titulos
        titulos_backup = fmodels.Titulo.objects.using(DB_BACKUP) \
            .filter(cobranca=cobranca_backup)

        for titulo_backup in titulos_backup:
            titulo_backup.save(using=DB_DEFAULT)

    # clientecontrato
    clientecontratos_backup = models.ClienteContrato.objects.using(DB_BACKUP) \
        .filter(cliente=cliente_backup)
    
    for clientecontrato_backup in clientecontratos_backup:
        clientecontrato = clientecontrato_backup
        clientecontrato.status = None
        clientecontrato.save(using=DB_DEFAULT)

        clientecontrato = models.ClienteContrato.objects \
            .get(id=clientecontrato_backup.id)

        clientecontrato.status = None
        clientecontrato.save()
        clientecontrato.clientecontratostatus_set.all().delete()

        clientecontrato_status_backup = models.ClienteContratoStatus.objects.using(DB_BACKUP) \
            .filter(clientecontrato=clientecontrato_backup) \
            .order_by ('id')
        
        for status_backup in clientecontrato_status_backup:
            models.ClienteContratoStatus.objects \
                .get_or_create(cliente_contrato=clientecontrato,
                               status=status_backup.status,
                               motivo=status_backup.motivo,
                               modo=status_backup.modo,
                               observacao=status_backup.observacao,
                               usuario=User.objects.get(username=status_backup.usuario.username),
                               defaults={
                                   "data_cadastro": status_backup.data_cadastro
                               })

        clientecontrato = clientecontrato.clientecontratostatus_set.last()
        clientecontrato.save()

        # servico base
        bases_backup = models.ServicoBase.objects.using(DB_BACKUP) \
            .filter(clientecontrato=clientecontrato_backup)

        for base_backup in bases_backup:
            base_backup.save(using=DB_DEFAULT)

        # servico internet
        internets_backup = models.ServicoInternet.objects.using(DB_BACKUP) \
            .filter(clientecontrato=clientecontrato_backup)

        for internet_backup in internets_backup:
            endereco_internet_backup = models.Endereco.objects.using(DB_BACKUP) \
                .get(id=internet_backup.endereco.id)

            endereco_internet_backup.save(using=DB_DEFAULT)
            internet_backup.save(using=DB_DEFAULT)

        for cc in cliente.clientecontrato_set.all():
            # ocorrencias
            ocorrencias_backup = amodels.Ocorrencia.objects.using(DB_BACKUP) \
                .filter(clientecontrato=cc)

            for ocorrencia_backup in ocorrencias_backup:
                ocorrencia_backup.save(using=DB_DEFAULT)
                oc = amodels.Ocorrencia.objects.get(id=ocorrencia_backup.id) 

                oc.data_cadastro = ocorrencia_backup.data_cadastro
                oc.data_agendamento = ocorrencia_backup.data_agendamento
                oc.data_finalizacao = ocorrencia_backup.data_finalizacao
                oc.save()

                oss_backup = amodels.OS.objects.using(DB_BACKUP) \
                    .filter(ocorrencia=oc)

                for os_backup in oss_backup:
                    os_backup.save(using=DB_DEFAULT)
                    os = amodels.OS.objects.get(id=os_backup.id) 

                    os.data_cadastro = os_backup.data_cadastro
                    os.data_agendamento = os_backup.data_agendamento
                    os.data_finalizacao = os_backup.data_finalizacao
                    os.save()