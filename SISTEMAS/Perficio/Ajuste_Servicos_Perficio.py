from datetime import date, datetime
from http import client
from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
from apps.cauth import models as authmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
import csv
import re
import copy

formacobranca = fmodels.FormaCobranca.objects.all()[0]
def strdate(d):
    try:
        d,m,y = d.split()[0].split('/')
        if len(d) < 2:
            d = '0%s'%d
        if len(m) < 2:
            m = '0%s'%m
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

fnum = lambda n: re.sub('[^0-9]', '', n)
usuario = authmodels.User.objects.get(username='sgp')
m = manage.Manage()
with open('/tmp/Conv-contas_acesso-perficio.csv', 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        login=row[5]
        senha=row[6]
        portador=1
        plano=7
        if admmodels.ServicoInternet.objects.filter(login__trim__lower=login.lower()).count() == 0:
            try:
                print('Cadastrando serviço referente ao login ', login)
                idcliente=int(row[2])
                cliente=admmodels.Cliente.objects.get(id=idcliente)


                endereco=admmodels.Endereco.objects.get(id=cliente.endereco.id)

                #################Enderecos##########
                endereco_cobranca=copy.copy(endereco)
                endereco_cobranca.id=None
                endereco_cobranca.save()

                endereco_servico=copy.copy(endereco)
                endereco_servico.id=None
                endereco_servico.save()

            

                ########COBRANCA########
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = cliente
                new_cobranca.endereco = endereco_cobranca
                
                new_cobranca.portador = fmodels.Portador.objects.get(id=portador)
                            
                
                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=10)
                    #new_cobranca.isento = isento
                new_cobranca.notafiscal = False
                new_cobranca.data_cadastro = datetime.now()
                new_cobranca.datacobranca1 = datetime.now()
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = 1
                new_cobranca.save()

                #############CONTRATO###############
                new_contrato = admmodels.ClienteContrato()

                new_contrato.cliente = cliente
                new_contrato.pop = admmodels.Pop.objects.filter(id=1)[0]
                new_contrato.cobranca = new_cobranca

                new_contrato.data_inicio = datetime.now()
                new_contrato.data_cadastro = datetime.now()
                new_contrato.data_alteracao = datetime.now()
                new_contrato.save()
                new_status = admmodels.ClienteContratoStatus()
                new_status.cliente_contrato = new_contrato
                new_status.status = 1
                new_status.modo=2
                new_status.usuario = usuario
                new_status.data_cadastro = datetime.now()
                new_status.save()
                

                

                new_contrato.data_cadastro = datetime.now()
                new_contrato.data_alteracao = datetime.now()
                new_contrato.save()

                #########SERVICO#############################
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = 1

                new_servico.login= login
                new_servico.endereco = endereco_servico
                new_servico.login_password=senha
                new_servico.login_password_plain=senha
                new_servico.central_password=senha
                new_servico.mac_dhcp = None
                new_servico.mac = None

                new_servico.ip = None
                new_servico.tipoconexao = 'ppp'
                new_servico.nas = nmodels.NAS.objects.get(pk=1)


                new_servico.planointernet = admmodels.PlanoInternet.objects.get(id=plano)
                new_servico.modoaquisicao =  0
                new_servico.data_cadastro=datetime.now()
                    #new_servico.observacao=servico_obs
                
                new_servico.save()


                m.addRadiusServico(new_servico)
            except Exception as e:
                print(e)
                continue
        else:
            print('Já exite um servico')
            continue
        
