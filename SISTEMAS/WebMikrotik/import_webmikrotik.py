#!/usr/bin/python
# -*- coding: utf-8 -*-

#########################################################################################################################################
#   CLIENTES            |  CONTRATOS           |  CONTAS                 |  FATURAS       |  PLANOS      |  CHAMADOS                    #
#-----------------------+----------------------+-------------------------+----------------+--------------+------------------------------#
#   ID                  |  ID                  |  ID                     |  Fatura        |  Nome        |  ID                          #
#   Nome / Razão social |  Número              |  Avulsa                 |  Contrato      |  Valor       |  Titulo                      #
#   Usuario             |  Titular             |  Online                 |  Boleto        |  Download    |  Data Contato                #
#   Cliente desde       |  Status              |  Usuário                |  Vencimento    |  Upload      |  Protocolo                   #
#   Telefone(s)         |  Vencimento          |  Senha                  |  Liquidação    |              |  Origem                      #
#   Tipo                |  Banco               |  Contrato               |  Data Emissão  |              |  Cliente                     #
#   E-mail              |  Endereço            |  Titular                |  Valor         |              |  Técnico designado           #
#   Data do cadastro    |  Numero da casa      |  CPF                    |  Multa e Juros |              |  Relato cliente              #
#   CPF                 |  Bairro              |  Observação             |  Desconto      |              |  Data agendada               #
#   RG                  |  Cidade              |  Endereço               |  Recebido      |              |  Relato Técnico              #
#   CNPJ                |  Estado              |  Número                 |  Banco         |              |  Data atendimento            #
#   Inscrição Estadual  |  Complemento         |  Complemento            |  Apelido       +--------------+  ID cliente                  #
#   Inscrição Municipal |  Emite NF            |  Bairro                 |  Status        |  PORTADORES  |  Data saída                  #
#   Gênero              |  Data de Contratação |  CEP                    |  Observação    +--------------+  Resolvido                   #
#   Data de nascimento  |  Data de Registro    |  Estado                 |  Cliente       |  Id          |  Motivo da falta de solução  #
#   Aniversário         |                      |  Cidade                 |  CPF           |  Nome        |  Obs. pagamento              #
#   Nome fantasia       |                      |  Telefone               |  CNPJ          |  Ativo       |  Satisfação                  #
#   Observação          |                      |  Coordenadas            |                |              |                              #
#   Endereço            |                      |  Plano                  |                |              |                              #
#   Número              |                      |  Método                 |                |              |                              #
#   Complemento         |                      |  IP                     |                |              |                              #
#   Bairro              |                      |  IPv6 - PPPoE (PD)      |                |              |                              #
#   CEP                 |                      |  IPv6 - DHCP (PD)       |                |              |                              #
#   Coordenadas         |                      |  MAC                    |                |              |                              #
#   Estado              |                      |  Auto login             |                |              |                              #
#   Cidade              |                      |  Comodato               |                |              |                              #
#   Vencimento          |                      |  Adquirido pela empresa |                |              |                              #
#                       |                      |  Ativo                  |                |              |                              #
#                       |                      |                         |                |              |                              #
#########################################################################################################################################

from __future__ import unicode_literals
import argparse
import os, sys
from datetime import date, datetime
import copy
from turtle import down
from unicodedata import normalize
import csv
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--contas', dest='contas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--contratos', dest='contratos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--faturas', dest='faturas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='ID do portador',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='ID do NAS',required=False)
parser.add_argument('--pop', dest='pop', type=int, help='POP ID',required=False)
parser.add_argument('--suportes', dest='suportes', type=str, help='Arquivo importacao',required=False)
args = parser.parse_args()

###########################################################################################################################################################
#                                                                                                                                                         #
#   python import_webmikrotik.py --settings=sgp.linkwifi.settings --planos=webmikrotik-planos.csv                                                    #
#   python import_webmikrotik.py --settings=sgp.linkwifi.settings --nas=1 --pop=1 --portador=1 --clientes= --contas= --contratos= --sync=1           #
#   python import_webmikrotik.py --settings=sgp.linkwifi.settings --portador=1 --faturas=webmikrotik-faturas.csv                                     #
#   python import_webmikrotik.py --settings=sgp.linkwifi.settings --suportes=webmikrotik-suportes.csv                                                #
#                                                                                                                                                         #
###########################################################################################################################################################

# Para bases em uso increment e adicione a string _import
addIdCliente = 0
addIdContrato = 0
addStringLogin = ''
addNumeroOcorrencia = 0


PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q
from django.db import transaction

from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.atendimento import models as amodels
from apps.netcore.utils.radius import manage
from apps.cauth import models as authmodels

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]','',n)

lista_logins_duplicados=[]
usuario = admmodels.User.objects.get(username='sgp')
if args.portador:
    portador = fmodels.Portador.objects.get(id=args.portador)
formacobranca = fmodels.FormaCobranca.objects.all()[0]
if args.nas:
    nas = nmodels.NAS.objects.get(id=args.nas)
pop_default = None
m = manage.Manage()
if args.pop:
    pop_default = admmodels.Pop.objects.get(id=args.pop)
planodefault = None

logins_alterar = []

def strdate(d):
    try:
        d,m,y = d.strip().split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

def formatar_data(dt):
    if dt:
        try:
            d,m,y = dt.split(' ')[0].split('/')
            if len(y) == 2:
                if int(y) >= 0 and int(y) <= 16:
                    y = '20%s' %y
                else:
                    y = '19%s' %y
            return '%s-%s-%s' %(y,m,d)
        except:
            print('error formatar %s' %dt)
    return ''

def format_cep(cep):
    fnum = lambda n: re.sub('[^0-9]','',n)
    if len(fnum(cep)) > 1 and len(fnum(cep)) < 8:
        while len(fnum(cep)) < 8:
            cep = '0%s'%cep.strip()
        return cep
    elif len(fnum(cep)) == 8:
        return cep.strip()
    else:
        return None

def verifica_vencimento(v):
    try:
        fmodels.Vencimento.objects.get(dia=v)
    except:
        print("erro vencimento %s" %v)
        print('corrigindo vencimento %s' %v)
        new_vencimento = fmodels.Vencimento()
        new_vencimento.dia = v
        new_vencimento.save()


if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__trim__lower=row[0].strip().lower())[0]
            except:
                new_plano = admmodels.Plano()
                new_plano.descricao=row[0].strip()
                new_plano.preco = float(row[1].replace(',','.'))
                new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
                new_plano.grupo = admmodels.Grupo.objects.get(nome='cabo')
                new_plano.save()

                download = row[2]
                upload = row[3]
                
                if download.strip().lower() == 'ilimitado':
                    download = 1024000
                    upload = 1024000

                else:
                    download= int(download.replace('Kbps',"").strip())
                    upload=int(upload.replace('Kbps',"").strip())
                
                if(not download or  download==None):
                    download=1024

                if(not upload or upload==None):
                    upload=1024
                
                print('meu download e upload é :', download, upload)
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano
                new_plano_internet.download = download
                new_plano_internet.upload = upload
                print('meu plano de internet em download ', new_plano_internet.download )
                new_plano_internet.save()
                print('criado plano %s' %row[0].strip())


if args.clientes and args.contratos and args.contas:
    contratos = {}
    contas = {}
    clientes = {}

    # load contas
    with open(args.contas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            if contas.get(row[6]):
                contas[row[6]].append(row)
            else:
                contas[row[6]] = [row]

    # load contratos
    with open(args.contratos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            if contratos.get(row[2]):
                contratos[row[2]].append(row)

    # load clientes
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            if clientes.get(row[1]):
                clientes[row[1]].append(row)
            else:
                clientes[row[1]] = [row]

    for cliente in clientes:
        print('Esse é meu cliente:', cliente)
        for row in clientes[cliente]:
            #print(row)
            #
            # CLIENTE 
            # 
            idcliente = int(row[0])+addIdCliente
            nome = ustr(row[1])
            data_cadastro = formatar_data(row[7][:10])
            
            celulares = []
            for f in row[4].split('/'):
                celulares.append(f)
            
            telefone = fnum(celulares[0])
            try:
                celular = fnum(celulares[1])
            except: 
                celular = ''

            try:
                telefonecom = fnum(celulares[2])
            except: 
                telefonecom = ''

            try:
                celularcom = fnum(celulares[3])
            except:
                celularcom = ''

            email = row[6]
            cpfcnpj = row[8]
            rgie = row[16]
            if row[8] == '':
                cpfcnpj = fnum(row[10])
            insc_estadual = row[11]
            insc_municipal = row[12]
            sexo = row[13]
            if sexo == 'feminino':
                sexo = 'F'
            if sexo == 'masculino':
                sexo = 'M'
            data_nasc = formatar_data(row[14])
            nomefantasia = row[16]
            cli_obs = row[17]

            endereco_cliente = {}
            endereco_cliente['logradouro'] = ustr(row[18])
            try:
                endereco_cliente['numero'] = int(row[19])
            except:
                endereco_cliente['numero'] = None
            endereco_cliente['complemento'] = ustr(row[20][0:255])
            endereco_cliente['bairro'] = ustr(row[21][0:50])
            endereco_cliente['cep'] = format_cep(row[22])
            endereco_cliente['uf'] = row[24][0:3]
            try:
                endereco_cliente['cidade'] = ustr(row[25][0:50])
            except:
                endereco_cliente['cidade'] = ''

            cliente_vencimento = row[26] or 10
            verifica_vencimento(cliente_vencimento)
            nomepai = ''
            nomemae = ''
            profissao = ''
            respempresa = ''
            respcpf = ''

            # 
            # SERVICO
            # 
            print("Passei aqui antes das contas")

            if not contas.get(cliente):
                contas[cliente] = [['', '', '', 'SEM_CONTA', '123456']]
                print(contas[cliente])
            for contarow in contas[cliente]:
                print('---------------------------')
                print(contarow)
                login = '%s%s'%(str(contarow[3]).strip(), addStringLogin)
                if login == '':
                    login = 'SEM_LOGIN_%s%s'%(cpfcnpj, addStringLogin)
                if 'SEM_CONTA' in login:
                    login += str(cpfcnpj)
                senha = contarow[4]

                if not login:
                    print("DEU ERROOO")
                    break
                endereco_servico = {}
                try:
                    endereco_servico['logradouro'] = ustr(contarow[9][0:255])
                    try:
                        endereco_servico['numero'] = int(contarow[10])
                    except:
                        endereco_servico['numero'] = None
                    endereco_servico['complemento'] = ustr(contarow[11][0:255])
                    endereco_servico['bairro'] = ustr(contarow[12][0:50])
                    endereco_servico['cep'] = format_cep(contarow[13]) or endereco_cliente['cep']
                    endereco_servico['uf'] = contarow[14][0:50]
                    endereco_servico['cidade'] = ustr(contarow[15][0:50])
                except:
                    endereco_servico = endereco_cliente

                print("Passei aqui")
                cidade_q = normalize('NFKD', unicode(endereco_servico['cidade'])).encode('ASCII','ignore')

                pop = pop_default

                try:
                    plano = contarow[18] or "Default"
                except:
                    plano = "Default"
                    try:
                        planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__trim__lower=plano.strip().lower())[0]
                    except:
                        new_plano = admmodels.Plano()
                        new_plano.descricao=plano
                        new_plano.preco = 0.00
                        new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
                        new_plano.grupo = admmodels.Grupo.objects.get(nome='cabo')
                        new_plano.save()
                        new_plano_internet = admmodels.PlanoInternet()
                        new_plano_internet.plano = new_plano
                        new_plano_internet.download = 204800
                        new_plano_internet.upload = 102400
                        new_plano_internet.save()
                        print('criado plano Default')

        
                try:
                    ip = contarow[20]
                except:
                    ip = ''
                try:
                    mac_dhcp = contarow[23]
                except:
                    mac_dhcp = ''
                try:
                    status = contarow[27]
                except:
                    status = 'Ativo'

                senha_central = cpfcnpj
    

                addresslist = ''
                respempresa = ''
                comodato = False
                notafiscal = False

                con_obs=''
                mac = None
                conexao_tipo = 'ppp'

                isento = 0
                nao_suspende = False

                status_cc = 1
                status_s = 1
                status_c = 1

                if status == 'Não':
                    status_cc = 4
                    status_s = 4
                    status_c = 4

                if status == 'c':
                    status_cc = 3
                    status_s = 3
                    status_c = 3

                status_criar = [6,2,status_cc]
                try:
                    idcontrato = int(fnum(contarow[0].strip()))+addIdContrato
                except:
                    idcontrato = admmodels.ClienteContrato.objects.all().order_by('-id')[0].id+addIdContrato+10000

                print status, login, nome, cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
                print endereco_cliente,endereco_servico
                print 'vencimento: ', cliente_vencimento, 'Plano: ', plano
                print telefone,telefonecom,celular,email,con_obs
                print login,senha,ip,mac
                if args.sync_db:
                    print("#############################Import %s - %s #############################"%(nome, cpfcnpj))
                    # Save Models

                    cliente_check = admmodels.Cliente.objects.filter(id=idcliente)
                    if cliente_check.count() == 0:
                        # Endereco
                        new_endereco = admmodels.Endereco(**endereco_cliente)
                        new_endereco_cob = admmodels.Endereco(**endereco_cliente)
                        new_endereco_inst = admmodels.Endereco(**endereco_servico)
                        new_endereco.save()
                        new_endereco_cob.save()
                        new_endereco_inst.save()

                        # Pessoa
                        if len(fnum(cpfcnpj)) > 12:
                            new_pessoa = admmodels.Pessoa()
                            new_pessoa.tipopessoa='J'
                            new_pessoa.nome = nome

                            new_pessoa.nomefantasia = nomefantasia
                            new_pessoa.respempresa = respempresa
                            new_pessoa.respcpf = respcpf
                            new_pessoa.cpfcnpj = cpfcnpj
                            new_pessoa.insc_estadual = insc_estadual
                            new_pessoa.tipo = 8
                            new_pessoa.save()
                        else:
                            new_pessoa = admmodels.Pessoa()
                            new_pessoa.tipopessoa='F'

                            new_pessoa.nome = nome
                            new_pessoa.sexo = sexo
                            new_pessoa.datanasc = data_nasc
                            new_pessoa.profissao = profissao
                            new_pessoa.nomepai = nomepai
                            new_pessoa.nomemae = nomemae
                            new_pessoa.nacionalidade = 'BR'
                            new_pessoa.rg = rgie
                            new_pessoa.cpfcnpj = cpfcnpj
                            new_pessoa.rg_emissor=''
                            try:
                                new_pessoa.save()
                            except:
                                try:
                                    new_pessoa.save()
                                except:
                                    new_pessoa.datanasc=None
                                    new_pessoa.save()

                        # Cliente
                        new_cliente = admmodels.Cliente()
                        new_cliente.id = idcliente
                        new_cliente.endereco = new_endereco
                        new_cliente.pessoa = new_pessoa
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.data_alteracao = data_cadastro
                        new_cliente.ativo = True
                        new_cliente.observacao = cli_obs
                        new_cliente.save()
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.save()

                        # contato 1
                        if len(email) > 4:
                            new_contato = admmodels.Contato()
                            new_contato.tipo = 'EMAIL'
                            new_contato.contato = email
                            new_contato.save()
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()

                        # contato 2
                        if len(celular)>4:
                            new_contato = admmodels.Contato()
                            new_contato.tipo = 'CELULAR_PESSOAL'
                            new_contato.contato = celular
                            new_contato.observacao = ''
                            new_contato.save()
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()

                        # contato 3
                        if len(telefone) > 4:
                            new_contato = admmodels.Contato()
                            new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                            new_contato.contato = telefone
                            new_contato.save()
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()

                        # contato 4
                        if len(telefonecom) > 4:
                            new_contato = admmodels.Contato()
                            new_contato.tipo = 'TELEFONE_FIXO_COMERCIAL'
                            new_contato.contato = telefonecom
                            new_contato.save()
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()

                        # Cobranca
                        new_cobranca = fmodels.Cobranca()
                        new_cobranca.cliente = new_cliente
                        new_cobranca.endereco = new_endereco_cob
                        new_cobranca.portador =portador
                        new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=cliente_vencimento)
                        new_cobranca.isento = isento
                        new_cobranca.notafiscal = False
                        new_cobranca.data_cadastro = data_cadastro
                        new_cobranca.datacobranca1 = data_cadastro
                        new_cobranca.usuariocad = usuario
                        new_cobranca.formacobranca = formacobranca
                        new_cobranca.nao_suspende=nao_suspende
                        new_cobranca.status = status_c
                        new_cobranca.save()

                        new_cobranca.data_cadastro = data_cadastro
                        new_cobranca.save()

                        # Contrato
                        new_contrato = admmodels.ClienteContrato()

                        new_contrato.id = idcontrato
                        new_contrato.cliente = new_cliente
                        new_contrato.pop = pop
                        new_contrato.cobranca = new_cobranca

                        new_contrato.data_inicio = data_cadastro
                        new_contrato.data_cadastro = data_cadastro
                        new_contrato.data_alteracao = data_cadastro
                        new_contrato.save()
                        new_contrato.data_cadastro = data_cadastro
                        new_contrato.save()
                        
                        # Status
                        for ic in status_criar:
                            new_status = admmodels.ClienteContratoStatus()
                            new_status.cliente_contrato = new_contrato
                            new_status.status = ic
                            new_status.modo=2
                            new_status.usuario = usuario
                            new_status.data_cadastro = data_cadastro
                            new_status.save()
                            new_status.data_cadastro = data_cadastro
                            new_status.save()
                        
                        # Servico
                        new_servico = admmodels.ServicoInternet()
                        new_servico.clientecontrato = new_contrato
                        new_servico.status = status_s
                        if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
                            print('Já existe serviço com o login %s. Ajustando login para: %s_import' %(login, login))
                            login = '%s_import'%login
                            
                        new_servico.login= login
                        new_servico.endereco = new_endereco_inst
                        new_servico.login_password=senha
                        new_servico.login_password_plain=senha
                        new_servico.central_password=senha_central
                        if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                            new_servico.mac_dhcp = mac_dhcp
                            new_servico.mac = mac
                        try:
                            if ip and admmodels.ServicoInternet.objects.filter(ip=ip).count() == 0:
                                new_servico.ip = ip
                        except:
                            new_servico.ip=None
                        new_servico.tipoconexao = conexao_tipo
                        new_servico.nas = nas
                        new_servico.planointernet = admmodels.PlanoInternet.objects.get(plano__descricao__trim__lower=plano.strip().lower())
                        new_servico.modoaquisicao = 1 if comodato == True else 0
                        new_servico.data_cadastro=data_cadastro
                        new_servico.addresslist=addresslist
                        new_servico.save()
                        new_servico.data_cadastro=data_cadastro
                        new_servico.save()

                    else:
                        # Adicionando Serviços adicionais ao cliente
                        endereco_servico = {}
                        endereco_servico['id']=None
                        endereco_servico['logradouro'] = ustr(contarow[9][0:255])
                        try:
                            endereco_servico['numero'] = int(contarow[10])
                        except:
                            endereco_servico['numero'] = None
                        endereco_servico['complemento'] = ustr(contarow[11][0:255])
                        endereco_servico['bairro'] = ustr(contarow[12][0:50])
                        endereco_servico['cep'] = format_cep(contarow[13]) or endereco_cliente['cep']
                        endereco_servico['uf'] = contarow[14][0:50]
                        endereco_servico['cidade'] = ustr(contarow[15][0:50])
                        new_endereco_cob = admmodels.Endereco(**endereco_cliente)
                        new_endereco_inst = copy.copy(new_endereco_cob)
                        new_endereco_cob.save()
                        new_endereco_inst.save()

                        new_cliente = cliente_check[0]

                        # Cobranca
                        new_cobranca = fmodels.Cobranca()
                        new_cobranca.cliente = new_cliente
                        new_cobranca.endereco = new_endereco_cob
                        new_cobranca.portador =portador
                        new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=cliente_vencimento)
                        new_cobranca.isento = isento
                        new_cobranca.notafiscal = False
                        new_cobranca.data_cadastro = data_cadastro
                        new_cobranca.datacobranca1 = data_cadastro
                        new_cobranca.usuariocad = usuario
                        new_cobranca.formacobranca = formacobranca
                        new_cobranca.nao_suspende=nao_suspende
                        new_cobranca.status = status_c
                        new_cobranca.save()

                        # Contrato
                        new_contrato = admmodels.ClienteContrato()

                        new_contrato.id = idcontrato
                        new_contrato.cliente = new_cliente
                        new_contrato.pop = pop
                        new_contrato.cobranca = new_cobranca

                        new_contrato.data_inicio = data_cadastro
                        new_contrato.data_cadastro = data_cadastro
                        new_contrato.data_alteracao = data_cadastro
                        new_contrato.save()

                        for ic in status_criar:
                            new_status = admmodels.ClienteContratoStatus()
                            new_status.cliente_contrato = new_contrato
                            new_status.status = ic
                            new_status.modo=2
                            new_status.usuario = usuario
                            new_status.data_cadastro = data_cadastro
                            new_status.save()

                            new_status.data_cadastro = data_cadastro
                            new_status.save()
                        
                        # Servico
                        new_servico = admmodels.ServicoInternet()
                        new_servico.clientecontrato = new_contrato
                        new_servico.status = status_s
                        if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
                            print('Já existe serviço com o login %s. Ajustando login para: %s_import' %(login, login))
                            login = '%s_import'%login
                            lista_logins_duplicados.append(login) 

                        new_servico.login= login
                        new_servico.endereco = new_endereco_inst
                        new_servico.login_password=senha
                        new_servico.login_password_plain=senha
                        new_servico.central_password=senha_central
                        if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                            new_servico.mac_dhcp = mac_dhcp
                            new_servico.mac = mac
                        try:
                            if ip and admmodels.ServicoInternet.objects.filter(ip=ip).count() == 0:
                                new_servico.ip = ip
                        except:
                            new_servico.ip=None
                        new_servico.tipoconexao = conexao_tipo
                        new_servico.nas = nas
                        new_servico.planointernet = admmodels.PlanoInternet.objects.get(plano__descricao__trim__lower=plano.strip().lower())
                        new_servico.modoaquisicao = 1 if comodato == True else 0
                        new_servico.data_cadastro=data_cadastro
                        new_servico.addresslist=addresslist
                        new_servico.save()

                        new_servico.data_cadastro=data_cadastro
                        new_servico.save()
                        print("Cliente Já importado %s Adicionado serviço adicional"%nome)
                    
                    m.addRadiusServico(new_servico)
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
    
    if len(lista_logins_duplicados) > 0:
        print('Segue lista de logins duplicados')
        for lld in lista_logins_duplicados:
            print(lld)


if args.faturas:
    with open(args.faturas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            portador = fmodels.Portador.objects.get(id=args.portador)
            usuario = authmodels.User.objects.get(username='sgp')
            formapagamento = fmodels.FormaPagamento.objects.all()[0]
            planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
            cpfcnpj = row[11].strip()
            if cpfcnpj == '':
                try:
                    cpfcnpj = row[12].strip()
                except:
                    continue
            clientes = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)
            if clientes:
                cliente = clientes[0]
                contrato = cliente.clientecontrato_set.all()
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    idtransacao = row[0]
                    numero_documento = row[0]
                    nosso_numero = row[0]
                    nosso_numero_f = row[0]
                    demonstrativo = ''
                    data_documento = strdate(row[5])
                    if data_documento == None:
                        data_documento = strdate(row[3])
                    data_vencimento = strdate(row[3])
                    data_pagamento = None
                    data_baixa = None
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None
                    juros = 0.00
                    valor = row[6].replace('.','').replace(',','.')

                    if row[9].strip().lower() in ['liquidada']:
                        valorpago = row[8].replace('.','').replace(',','.')
                        data_pagamento = strdate(row[4])
                        if data_pagamento == '' or data_pagamento == '0000-00-00':
                            data_pagamento = data_vencimento
                        data_baixa = data_pagamento
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None

                    elif row[9].strip().lower() in ['cancelada', 'isenta']:
                        data_cancela = data_vencimento
                        status = fmodels.MOVIMENTACAO_CANCELADA
                        data_baixa = None
                        data_pagamento = None
                        usuario_b = None
                        usuario_c = usuario

                    elif row[9].strip().lower() in ['aguardando']:
                        data_baixa = None
                        data_pagamento = None

                    elif row[9].strip().lower() in ['vencida', 'vencido']:
                        data_baixa = None
                        data_pagamento = None
                        valorpago = None
                        usuario_b = None

                    desconto = row[7].replace('.','').replace(',','.')
                    if desconto == '':
                        desconto = 0.00
                    linha_digitavel = ''
                    codigo_barras = ''
                    codigo_carne = ''
                    chave = ''
                    if nosso_numero:
                        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                            dados = {'cliente': cliente,
                                    'cobranca': cobranca,
                                    'portador': portador,
                                    'formapagamento': formapagamento,
                                    'centrodecusto': planocontas,
                                    'modogeracao': 'l',
                                    'usuario_g': usuario,
                                    'usuario_b': usuario_b,
                                    'usuario_c': usuario_c,
                                    'demonstrativo': demonstrativo,
                                    'data_documento': data_documento,
                                    'data_alteracao': data_documento,
                                    'data_vencimento': data_vencimento,
                                    'data_cancela': data_cancela,
                                    'data_pagamento': data_pagamento,
                                    'data_baixa': data_baixa,
                                    'numero_documento': numero_documento,
                                    'nosso_numero': nosso_numero,
                                    'nosso_numero_f': nosso_numero_f,
                                    'linha_digitavel': linha_digitavel,
                                    'codigo_barras': codigo_barras,
                                    'valor': valor,
                                    'valorpago': valorpago,
                                    'desconto': desconto,
                                    'status': status,
                                    'observacao': codigo_carne,
                                    'djson': {'juros': juros }
                                    }
                            # if fmodels.TituloGateway.objects.filter(idtransacao=idtransacao).count() > 0:
                            #     continue
                            print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                            try:
                                titulo = fmodels.Titulo(**dados)
                                titulo.save()
                                titulo.data_documento=data_documento
                                titulo.data_alteracao=data_documento
                                titulo.save()

                            except Exception as e:
                                print("Erro cadastrar",e,dados)
                        else:
                            print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)
        
    
if args.suportes:
    cdtipo = 300
    cdmotivo = 300

    max_tipo = amodels.Tipo.objects.all().order_by('-id')[0]
    if max_tipo.codigo > 200:
        cdtipo = max_tipo.codigo + 1
    max_motivo = amodels.MotivoOS.objects.all().order_by('-id')[0]
    if max_motivo.codigo > 200:
        cdmotivo = max_motivo.codigo + 1

    metodo = amodels.Metodo.objects.all()[0]

    def format_data(n):
        try:
            date = n.strip().split()[0]
            d_,m_,y_ = date.split('/')
            return '%s-%s-%s'%(y_,m_,d_)
        except:
            return n
        

    with open(args.suportes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            protocolo = int(fnum(row[0]))+addNumeroOcorrencia
            protocolo = str(protocolo)
            if len(protocolo) > 14:
                protocolo = protocolo[0:13]
            idcliente = int(row[11])+addIdCliente
            assunto = row[1]
            status = 'Aberto'
            #if row[14].strip() == '':
            status = 'Finalizado'
            data_cadastro = format_data(row[2])
            if fnum(row[8]) == '':
                data_agendamento = None
            else:
                data_agendamento = format_data(row[8])
            
            if fnum(row[10]) == '':
                data_finalizacao = datetime.now()
            else:
                data_finalizacao = format_data(row[10])
            conteudo = row[7]
            if conteudo == "" or conteudo is None:
                conteudo = "Campo conteúdo vazio no WebMikoritk."
            servicoprestado = row[9]

            if admmodels.ClienteContrato.objects.filter(cliente__id=idcliente).count() > 0:
                try:
                    clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=idcliente)[0]
                except:
                    continue
                tipo_obj = amodels.Tipo.objects.filter(descricao=assunto)
                motivo_obj = amodels.MotivoOS.objects.filter(descricao=assunto)

                if tipo_obj:
                    tipo_obj = tipo_obj[0]
                else:
                    tipo_obj = amodels.Tipo()
                    tipo_obj.codigo=cdtipo
                    tipo_obj.descricao=assunto[:99]
                    tipo_obj.save()
                    cdtipo += 1

                if motivo_obj:
                    motivo_obj = motivo_obj[0]
                else:
                    motivo_obj = amodels.MotivoOS()
                    motivo_obj.codigo=cdmotivo
                    motivo_obj.descricao=assunto
                    try:
                        motivo_obj.save()
                        cdmotivo += 1
                    except:
                        continue

                if amodels.Ocorrencia.objects.filter(numero=protocolo).count() == 0:
                    print(row)
                    ocorrencia = {}
                    ocorrencia['clientecontrato'] = clientecontrato
                    ocorrencia['tipo'] = tipo_obj
                    ocorrencia['usuario'] = usuario
                    ocorrencia['metodo'] = metodo
                    ocorrencia['numero'] = protocolo
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if status == 'Finalizado' else amodels.OCORRENCIA_ABERTA
                    ocorrencia['responsavel'] = ocorrencia['usuario']

                    ocorrencia['data_cadastro'] = data_cadastro
                    if str(ocorrencia['data_cadastro']) in ['0000-00-00 00:00:00','0000-00-00','']:
                        ocorrencia['data_cadastro'] = datetime.now()
                    ocorrencia['data_agendamento'] = data_agendamento
                    ocorrencia['data_finalizacao'] = data_finalizacao
                    ocorrencia['conteudo'] = conteudo
                    for ok in ocorrencia:
                        if ocorrencia[ok] in ['0000-00-00 00:00:00','0000-00-00','']:
                            ocorrencia[ok] = None

                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()

                    new_ocorrencia.data_cadastro = data_cadastro
                    new_ocorrencia.data_agendamento = data_agendamento
                    new_ocorrencia.data_finalizacao = data_finalizacao

                    if str(new_ocorrencia.data_agendamento) in ['0000-00-00 00:00:00','0000-00-00','']:
                        new_ocorrencia.data_agendamento = None
                    if str(new_ocorrencia.data_finalizacao) in ['0000-00-00 00:00:00','0000-00-00','']:
                        new_ocorrencia.data_finalizacao = None
                    if str(new_ocorrencia.data_cadastro) in ['0000-00-00 00:00:00','0000-00-00','']:
                        new_ocorrencia.data_cadastro = datetime.now()
                    try:
                        new_ocorrencia.save()
                    except:
                        new_ocorrencia.data_agendamento = None
                        new_ocorrencia.data_finalizacao = None
                        new_ocorrencia.data_cadastro = datetime.now()


                    ordem = {}
                    ordem['ocorrencia'] = new_ocorrencia
                    ordem['status'] = amodels.OS_ENCERRADA if status == 'Finalizado' else amodels.OS_ABERTA
                    ordem['usuario'] = usuario
                    ordem['motivoos'] = motivo_obj
                    ordem['data_cadastro'] = ocorrencia['data_cadastro']
                    ordem['data_agendamento'] = ocorrencia['data_agendamento']
                    ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                    ordem['conteudo'] = ocorrencia['conteudo']

                    for oser in ordem:
                        if ordem[oser] in ['0000-00-00 00:00:00','0000-00-00']:
                            ordem[oser] = None

                    new_ordem = amodels.OS(**ordem)
                    new_ordem.save()
                    new_ordem.data_cadastro = ocorrencia['data_cadastro']
                    new_ordem.data_agendamento = ocorrencia['data_agendamento']
                    new_ordem.data_finalizacao = ocorrencia['data_finalizacao']
                    if str(new_ordem.data_agendamento) in ['0000-00-00 00:00:00','0000-00-00','']:
                        new_ordem.data_agendamento = None
                    if str(new_ordem.data_finalizacao) in ['0000-00-00 00:00:00','0000-00-00','']:
                        new_ordem.data_agendamento = None
                    try:
                        new_ordem.save()
                    except:
                        new_ordem.data_cadastro = datetime.now()
                        new_ordem.data_agendamento = None
                        new_ordem.data_finalizacao = None

                    if servicoprestado != '':
                        new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                        new_ocorrencia_anotacao.ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
                        new_ocorrencia_anotacao.anotacao=servicoprestado
                        new_ocorrencia_anotacao.usuario= usuario
                        new_ocorrencia_anotacao.save()