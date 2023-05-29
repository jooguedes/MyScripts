import csv
from datetime import date, datetime
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.fiscal import constants as fisconstants
from apps.fiscal import models as fismodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
 
import copy




usuario = admmodels.User.objects.get(username='sgp')

formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

addStringLogin = 'import_receitanet_4679'
idPlano = 21
idPortador = 3
idPop = 2
idNas = 2

m = manage.Manage()
with open('/tmp/receitanet-vinculados.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:   

        """SENTANDO STATUS, ATIVOS POR DEFAULT"""
        conexao_tipo = 'ppp'
        status_cc = 1
        status_s = 1
        status_c = 1


        login_primario='%s%s'%(row[0], addStringLogin)
        login_secundario='%s%s'%(row[1], addStringLogin)
        senha=row[2]

        if admmodels.ServicoInternet.objects.filter(login=login_secundario).count()==0:

            try:
                cliente= admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login_primario)[0]
            except Exception as e:
                print('cliente não identificado')
            

            #ENDERECO
          
          
            end_pai=admmodels.Endereco.objects.filter(servicointernet__login=login_primario)[0]
            new_endereco= admmodels.Endereco()

            new_endereco.logradouro= end_pai.logradouro
            new_endereco.cidade= end_pai.cidade
            new_endereco.uf= end_pai.uf
            new_endereco.bairro= end_pai.bairro
            new_endereco.numero= end_pai.numero

            new_endereco_cob= copy.copy(new_endereco)
            new_endereco_intal=copy.copy(new_endereco)
            new_endereco.save()
            new_endereco_cob.save()
            new_endereco_intal.save()
    



            #BUSCANDO O PLANO DO CLIENTE PELO NOME
            
            planointernet=admmodels.PlanoInternet.objects.filter(plano__id=idPlano)[0]

            new_cobranca = fmodels.Cobranca()
            new_cobranca.cliente = cliente
            new_cobranca.endereco = new_endereco_cob
            new_cobranca.portador = fmodels.Portador.objects.filter(id=idPortador)[0]

            vencimento=None
            try:
                cobranca_primaria=fmodels.Cobranca.objects.filter(cliente__clientecontrato__servicointernet__login=login_primario)[0]
                vencimento=fmodels.Vencimento.objects.filter(id=cobranca_primaria.vencimento)
            except Exception as e:
                print('Erro ao identificar vencimento, cadastrando vencimento padrão', e)
                vencimento=10

            try:
                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=10) 

            
            new_cobranca.isento = 0
            new_cobranca.notafiscal = False
            new_cobranca.data_cadastro = datetime.now()
            new_cobranca.datacobranca1 = datetime.now()
            new_cobranca.usuariocad = usuario
            new_cobranca.formacobranca = formacobranca
            new_cobranca.status = status_c
            new_cobranca.save()

            new_cobranca.data_cadastro = datetime.now()
            new_cobranca.save()

            
            # Contrato
            new_contrato = admmodels.ClienteContrato()
            new_contrato.cliente = cliente
            new_contrato.pop = admmodels.Pop.objects.filter(id=idPop)[0]
            new_contrato.cobranca = new_cobranca

            new_contrato.data_inicio = datetime.now()
            new_contrato.data_cadastro = datetime.now()
            new_contrato.data_alteracao = datetime.now()
            new_contrato.save()

            for ic in [6,2,status_cc]:
                new_status = admmodels.ClienteContratoStatus()
                new_status.cliente_contrato = new_contrato
                new_status.status = ic
                new_status.modo=2
                new_status.usuario = usuario
                new_status.data_cadastro = datetime.now()
                new_status.save()

                new_status.data_cadastro = datetime.now()
                new_status.save()

            # Servico
            new_servico = admmodels.ServicoInternet()
            new_servico.clientecontrato = new_contrato
            new_servico.status = status_s
            if admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=login_secundario).count() > 0:
                print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login_secundario,
                                                                                    login_secundario,
                                                                                    str(new_contrato.id))
                login_secundario += str(new_contrato.id)
            new_servico.login= login_secundario
            new_servico.endereco = new_endereco_intal
            new_servico.login_password=senha
            new_servico.login_password_plain=senha
            new_servico.central_password=senha
            new_servico.tipoconexao = conexao_tipo
            new_servico.nas = nmodels.NAS.objects.get(pk=idNas)
            new_servico.ip=None
            new_servico.mac=None
            new_servico.planointernet = planointernet
            new_servico.modoaquisicao =  0
            new_servico.data_cadastro=datetime.now()
            #new_servico.observacao=cli_obs
            new_servico.save()

            new_servico.data_cadastro=datetime.now()
            new_servico.save()

            m.addRadiusServico(new_servico)
        else:
            print('login já existe no sistema')