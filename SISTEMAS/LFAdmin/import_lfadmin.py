#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 
import re
from decimal import Decimal
import codecs

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--fornecedores', dest='fornecedores', type=str, help='criar fornecedores', required=False)
parser.add_argument('--planocontas', dest='planocontas', type=str, help='criar plano contas',required=False)
parser.add_argument('--descontos', dest='descontos', type=str, help='criar descontos',required=False)
parser.add_argument('--pagar', dest='pagar', type=str, help='criar contas a pagar',required=False)
parser.add_argument('--caixas', dest='caixas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--pops', dest='pops', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=str, help='Criar vencimento para corrigir',required=False)
parser.add_argument('--setores', dest='setores', type=str, help='chamado setores',required=False)
parser.add_argument('--chamadoassuntos', dest='chamadoassuntos', type=str, help='chamado assuntos',required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='chamado',required=False)
parser.add_argument('--chamadosarquivos', dest='chamadosarquivos', type=str, help='chamadosarquivos',required=False)
parser.add_argument('--olts', dest='olts', type=str, help='olts',required=False)
parser.add_argument('--pons', dest='pons', type=str, help='pons',required=False)
parser.add_argument('--ctos', dest='ctos', type=str, help='ctos',required=False)
parser.add_argument('--onutemplates', dest='onutemplates', type=str, help='onutemplates',required=False)
parser.add_argument('--onus', dest='onus', type=str, help='onus',required=False)
parser.add_argument('--loginsonu', dest='loginsonu', type=str, help='loginsonu',required=False)
parser.add_argument('--historico', dest='historico', type=str, help='historico',required=False)
parser.add_argument('--fixdata', dest='fixdata', type=str, help='fixdata',required=False)
parser.add_argument('--fixfilial', dest='fixfilial', type=str, help='fixfilial',required=False)
parser.add_argument('--anotacoes', dest='anotacoes', type=str, help='anotacoes',required=False)

#python import_lfadmin --settings=sgp.riosnetba.settings --planos=lfadmin-planos.csv --sync=1
#python import_lfadmin.py --settings=sgp.riosnetba.settings --clientes=lfadmin-clientes.csv --sync=1
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q 

from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.fiscal import models as fismodels, constants as fisconstants
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
from apps.atendimento import models as amodels

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))
fnum2 = lambda n: re.sub('[^0-9\-]', '', unicode(n))
usuario = admmodels.User.objects.get(username='sgp')
if args.portador:
    portador = fmodels.Portador.objects.get(id=args.portador)


if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            codigo_banco = row[2]
            if not row[2]:
                codigo_banco = '999'
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print row
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[1]
                new_portador.codigo_banco = codigo_banco
                new_portador.agencia = row[3] or '0'
                new_portador.agencia_dv = row[4]
                new_portador.conta = row[5] or '0'
                new_portador.conta_dv = row[6]
                new_portador.convenio = row[7]
                new_portador.carteira = row[8]
                new_portador.cedente='PROVEDOR X'
                new_portador.cpfcnpj = '0'
                new_portador.save()

            if fmodels.GatewayPagamento.objects.filter(portadores__id=row[0]).count() == 0:
                if row[12] in ['boleto_facil','fortunus','juno','widepay']:
                    new_gateway_pagamento = fmodels.GatewayPagamento()
                    new_gateway_pagamento.descricao = row[1]
                    new_gateway_pagamento.gerencia_boleto = True
                    if row[13]:
                        new_gateway_pagamento.token = row[13]
                    if row[14]:
                        new_gateway_pagamento.usuario = row[14]
                    if row[15]:
                        new_gateway_pagamento.senha = row[15]
                    if row[12] == 'fortunus' and row[13]:
                        new_gateway_pagamento.nome = 'gerencianet'
                    elif row[12] == 'fortunus':
                        new_gateway_pagamento.nome = 'gerencianetapi'
                    elif row[12] == 'boleto_facil':
                        new_gateway_pagamento.nome =  'boletofacil'
                    else:
                        new_gateway_pagamento.nome =  row[12]
                    new_gateway_pagamento.save()
                    new_portador = fmodels.Portador.objects.get(id=row[0])
                    new_gateway_pagamento.portadores.add(new_portador)


if args.caixas:
    with open(args.caixas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if fmodels.PontoRecebimento.objects.filter(id=row[0]).count() == 0:
                print row
                new_ponto = fmodels.PontoRecebimento()
                new_ponto.id = row[0]
                new_ponto.descricao = row[1]
                new_ponto.save()

if args.pops:
    with open(args.pops, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Pop.objects.filter(id=row[0]).count() == 0:
                print row
                new_pop = admmodels.Pop()
                new_pop.id = row[0]
                new_pop.cidade=row[1].split('/')[0].upper()
                new_pop.uf = row[1].split('/')[1].upper()
                new_pop.save()

if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(descricao=row[0]).count() == 0:
                print(row)
                new_plano = admmodels.Plano()
                new_plano.id = row[0]
                new_plano.descricao=row[1]
                new_plano.preco = row[4]
                new_plano.grupo = admmodels.Grupo.objects.all().order_by('id')[0]
                new_plano.contrato = admmodels.Contrato.objects.all().order_by('id')[0]
                new_plano.pospago = True
                new_plano.djson = {'codigo': row[5]}
                new_plano.data_cadastro = date.today().strftime('%Y-%m-%d')
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=row[0]
                new_plano_internet.plano = new_plano 
                if 'k' in row[2].lower():
                    new_plano_internet.download = int(fnum(row[2]))
                elif 'm' in row[2].lower():
                    new_plano_internet.download = int(fnum(row[2])) * 1024
                else:
                    new_plano_internet.download = int(row[2])

                if 'k' in row[3].lower():
                    new_plano_internet.upload = int(fnum(row[3]))
                elif 'm' in row[3].lower():
                    new_plano_internet.upload = int(fnum(row[3])) * 1024
                else:
                    new_plano_internet.upload = int(row[3])
                new_plano_internet.diasparabloqueio = 15
                new_plano_internet.data_cadastro = date.today().strftime('%Y-%m-%d')
                new_plano_internet.save() 

if args.nas:
    with open(args.nas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if nmodels.NAS.objects.filter(id=row[0]).count() == 0:
                print row
                new_nas = nmodels.NAS()
                #new_nas.id=row[0]
                new_nas.shortname=row[2]
                new_nas.secret = row[3]
                new_nas.xuser= row[5]
                new_nas.xtype = 'mikrotik'
                new_nas.xpassword = row[6]
                new_nas.nasname= row[1]
                new_nas.save()


if args.clientes:
    nas = nmodels.NAS.objects.all()[0]
    formacobranca = fmodels.FormaCobranca.objects.all()[0]

    m = manage.Manage()

    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            idcliente = row[0]
            idcontrato = row[1]   # id
            
            nome = row[2]
            nomefantasia = row[3]
            insc_estadual = row[4]
            tipo = row[5]
            rgie = row[4][0:20]
            sexo = row[6]
            data_nasc = row[7]
            estadocivil = row[9]
            profissao = row[10]
            cpfcnpj = row[11][0:20]

            endereco_inst = {}
            endereco_inst['logradouro'] = row[12] # tipo_insta,endereco_insta
            try:
                endereco_inst['numero'] = int(row[13]) # numero_insta
            except:
                endereco_inst['numero'] = None 
            endereco_inst['complemento'] = row[14]
            endereco_inst['bairro'] = row[15][0:40]
            endereco_inst['cidade'] = row[16][0:40]
            endereco_inst['uf'] = row[17]
            endereco_inst['cep'] = fnum2(row[18])
            endereco_inst['pontoreferencia'] = row[19]
            endereco_cob = {} 
            endereco_cob['logradouro'] = row[12] # tipo_insta,endereco_insta
            try:
                endereco_cob['numero'] = int(row[13]) # numero_insta
            except:
                endereco_cob['numero'] = None 
            endereco_cob['complemento'] = row[14]
            endereco_cob['bairro'] = row[15][0:40]
            endereco_cob['cidade'] = row[16][0:40]
            endereco_cob['uf'] = row[17]
            endereco_cob['cep'] = fnum2(row[18])
            endereco_cob['pontoreferencia'] = row[19]

            celular = row[20] # celular
            telefonecom = row[21] # telefonecom
            telefone = ''   
            celularcom = ''
            email = row[22] # outro_email
            anotacao = row[23]
            nomepai = row[24]
            nomemae = row[25]
            cli_obs = row[26]

            ativo = row[27]
            status = row[28] # A S D 
            login = row[29]
            print('login',login)
            if not login:
                login = 'semlogin_%s' %idcontrato
            senha = row[30]
            if not senha:
                senha = login
            ip = row[31].replace('"','').strip()
            if ip and ':' in ip:
                ip = None
            if ip and '.' not in ip:
                ip = None
            mac_dhcp = row[32]
            plano = admmodels.PlanoInternet.objects.filter(id=row[33])
            if plano:
                plano = plano[0]
            elif args.planopadrao:
                plano = admmodels.PlanoInternet.objects.get(id=args.planopadrao)

            if not plano:
                continue
            portador = row[34]
            vencimento = row[35] or 10
            respempresa = row[36]
            insc_municipal = row[37]
            data_cadastro = row[38]
            if not data_cadastro:
                data_cadastro = date.today().strftime('%Y-%m-%d')
            if '-' not in data_cadastro:
                data_cadastro = date.today().strftime('%Y-%m-%d')
            data_ativacao = row[39]
            #idservico = row[39]


            if row[41] and row[44] and row[45]:
                endereco_inst = {}
                endereco_inst['logradouro'] = row[41] # tipo_insta,endereco_insta
                try:
                    endereco_inst['numero'] = int(row[42]) # numero_insta
                except:
                    endereco_inst['numero'] = None 
                endereco_inst['complemento'] = row[43]
                endereco_inst['bairro'] = row[44][0:40]
                endereco_inst['cidade'] = row[45][0:40]
                endereco_inst['uf'] = row[46]
                endereco_inst['cep'] = fnum2(row[47])
                endereco_inst['pontoreferencia'] = row[48]

            if row[49] and row[52] and row[53]:
                endereco_inst = {}
                endereco_inst['logradouro'] = row[49] # tipo_insta,endereco_insta
                try:
                    endereco_inst['numero'] = int(row[50]) # numero_insta
                except:
                    endereco_inst['numero'] = None 
                endereco_inst['complemento'] = row[51]
                endereco_inst['bairro'] = row[52][0:40]
                endereco_inst['cidade'] = row[53][0:40]
                endereco_inst['uf'] = row[54]
                endereco_inst['cep'] = fnum2(row[55])
                endereco_inst['pontoreferencia'] = row[56]

            if not data_ativacao:
                data_ativacao = date.today().strftime('%Y-%m-%d')

            if vencimento == '0':
                vencimento = 1
            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 


            comodato = False
            respempresa = ''
            respcpf = ''

            pop = admmodels.Pop.objects.filter(id=1)[0]
            nas = nmodels.NAS.objects.all()[0]

            notafiscal = False

            con_obs=''
            mac = None
            conexao_tipo = 'ppp'

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            if status in ['CM','CA']:
                status_cc = 4
                status_s = 4
                status_c = 4

            if status == 'D':
                status_cc = 3
                status_s = 3
                status_c = 3

            status_criar = [6,2,status_cc]

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save() 

            #print pop
            #print row
            print (status, login, nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc)
            print (endereco_cob,endereco_inst)
            print ('vencimento: ', vencimento, 'Plano: ', plano)
            print ('login',login)
            print (telefone,telefonecom,celular,email,con_obs)
            print (login,senha,ip,mac)
            print ('####################################################')
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" %nome
                # Save Models 

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)
        
                if len(cliente_check) == 0:

                    # Endereco 
                    new_endereco = admmodels.Endereco(**endereco_cob)
                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    new_endereco.save() 
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    try:
                        fmodels.Portador.objects.get(pk=portador)
                    except:
                        portador=1
                    
                    

                    
                    if tipo == 'F':
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
                        if estadocivil:
                            new_pessoa.estadocivil=estadocivil.upper()[0]
                        try:
                            new_pessoa.save()
                        except:
                            try:
                                new_pessoa.save()
                            except:
                                new_pessoa.datanasc=None 
                                new_pessoa.save()
                    
                    if tipo == 'J':
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


                    if tipo == 'E':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='E'
                        new_pessoa.nome = nome
                        new_pessoa.nomefantasia = nomefantasia
                        new_pessoa.respempresa = respempresa
                        new_pessoa.respcpf = respcpf
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = insc_estadual
                        new_pessoa.tipo = 8
                        new_pessoa.save()

                    # Cliente
                    if '0000-00-00' in str(data_cadastro):
                        data_cadastro=datetime.now()
                    new_cliente = admmodels.Cliente()
                    new_cliente.id = idcliente
                    new_cliente.pessoa = new_pessoa
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
                    if len(celular) > 4:
                        new_contato = admmodels.Contato()  
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular 
                        new_contato.observacao = con_obs
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                    
                    
                    # contato 5
                    if len(celularcom) > 4:
                        new_contato = admmodels.Contato()  
                        new_contato.tipo = 'CELULAR_COMERCIAL'
                        new_contato.contato = celularcom 
                        new_contato.observacao = con_obs
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

                else:
                    new_endereco = cliente_check[0].endereco
                    
                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    
                    
                    # Cliente
                    #new_cliente = imodels.Cliente()
                    #new_cliente.endereco = new_endereco
                    #new_cliente.pessoa = new_pessoa
                    #new_cliente.data_cadastro = data_cadastro
                    #new_cliente.data_alteracao = data_cadastro
                    #new_cliente.ativo = True 
                    #new_cliente.save()
                    #new_cliente.data_cadastro = data_cadastro
                    #new_cliente.save()
                    new_cliente = cliente_check[0]

                
                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob
                
                try:
                    new_cobranca.portador = fmodels.Portador.objects.get(pk=portador)
                except:
                    new_cobranca.portador = fmodels.Portador.objects.all()[0]

                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
                new_cobranca.isento = isento
                new_cobranca.notafiscal = False
                new_cobranca.data_cadastro = data_cadastro 
                new_cobranca.datacobranca1 = data_cadastro
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
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
                    print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                      login,
                                                                                      str(new_contrato.id))
                    login += str(new_contrato.id)
                new_servico.login= login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password=senha 
                new_servico.login_password_plain=senha
                new_servico.central_password=senha
                if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                    new_servico.mac_dhcp = mac_dhcp
                    new_servico.mac = mac

                if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                    new_servico.ip = ip 
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = plano
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)



if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        if args.portador:
            portador=fmodels.Portador.objects.get(id=args.portador)
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            cliente = admmodels.Cliente.objects.filter(id=row[0])
            cobranca = None 
            contrato = None

            if cliente:
                cliente = cliente[0]
                if row[1]:
                    contrato = admmodels.ClienteContrato.objects.filter(id=row[1])
                    if contrato:
                        contrato = contrato[0]
                        cobranca = contrato.cobranca

                if not args.portador:
                    if not row[15]:
                        continue 

                    portador = fmodels.Portador.objects.filter(id=row[15])
                    if not portador:
                        continue 
                    else:
                        portador = portador[0]

                if fmodels.Titulo.objects.filter(portador=portador,nosso_numero=row[4]).count() == 0:
                    print row
                    tdata = {} 
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[4] # nrboleto
                    if row[5]:
                        #if row[6]:
                        #    tdata['numero_documento'] = fnum('%s%s' %(row[5].split('/')[0],row[6]))
                        #else:
                        tdata['numero_documento'] = fnum(row[5].split('/')[0])
                    else:
                        tdata['numero_documento'] = row[4] # documento
                    tdata['parcela'] = row[6] # parcela
                    if not row[6]:
                        tdata['parcela'] = 1
                    tdata['portador'] = portador
                    tdata['valor'] = row[7]
                    tdata['observacao'] = row[8]
                    tdata['demonstrativo'] = row[8]
                    tdata['valorpago'] = row[9]
                    tdata['data_baixa'] = row[10]
                    tdata['data_pagamento'] = row[10]
                    tdata['data_documento'] = row[11] # emissao
                    tdata['data_vencimento'] = row[12] # vencimento
                    tdata['data_cancela'] = row[13]
                    if tdata['valorpago'] == '0' or tdata['valorpago'] == '' or tdata['valorpago'] == '0.00':
                        tdata['valorpago'] = None
                    tdata['usuario_b'] = usuario # usuariobaixa 28 
                    tdata['usuario_g'] = usuario # usuariogerou 29
                    tdata['usuario_c'] = usuario # usuariocancela 30 
                    tdata['modogeracao'] = 'l'
                    tdata['motivocancela'] = None
                    tdata['motivodesconto'] = None

                    tdata['centrodecusto'] = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
                    for k in tdata:
                        if tdata[k] in ['NULL','0000-00-00','']:
                            tdata[k] = None
                    if tdata['data_baixa'] is None:
                        tdata['usuario_b'] = None
                    if tdata['data_cancela'] is None:
                        tdata['usuario_c'] = None

                    if tdata['data_baixa']:
                        tdata['status'] = fmodels.MOVIMENTACAO_PAGA
                    elif tdata['data_cancela']:
                        tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA
                    else:
                        tdata['status'] = fmodels.MOVIMENTACAO_GERADA
                    if tdata['demonstrativo'] is None:
                        tdata['demonstrativo'] = ''

                    if row[14] == 'C':
                        if not tdata['data_cancela']:
                            tdata['data_cancela'] = tdata['data_vencimento']
                            tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA
                    tdata['djson'] = {'nn_boleto': row[16],
                                      'link': row[17]}
                    print tdata
                    new_titulo = fmodels.Titulo(**tdata)
                    new_titulo.save()
                    new_titulo.data_documento = tdata['data_documento']
                    new_titulo.save()

                    if new_titulo.portador.gateway_boleto:
                        titulogateway = fmodels.TituloGateway()
                        titulogateway.titulo = new_titulo
                        titulogateway.gateway = new_titulo.portador.gateway_boleto
                        titulogateway.link = row[17]
                        titulogateway.idtransacao = row[16]
                        titulogateway.save()


if args.fornecedores:
    with open(args.fornecedores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {} 
            dados['id'] = int(row[0])
            dados['nome'] = row[1]
            dados['nomefantasia'] = row[2]
            dados['telefones'] = row[3]
            dados['fax'] = row[4]
            dados['responsavelempresa'] = row[5]
            dados['insc_estadual'] = row[7]
            dados['cpfcnpj'] = row[8]
            dados['logradouro'] = row[9]
            dados['bairro'] = row[10]
            dados['cep'] = row[11]
            dados['cidade'] = row[12]
            dados['uf'] = row[13]
            dados['pontoreferencia'] = row[14]
            dados['email'] = row[15]
            dados['observacao'] = row[16]
            dados['ativo'] = True
            novo_fornecedor = fmodels.Fornecedor(**dados)
            novo_fornecedor.save()


if args.planocontas:
    pi = 1
    with open(args.planocontas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            new_pconta = fmodels.CentrodeCusto()
            new_pconta.id= int(row[0]) + 1000
            new_pconta.descricao = 'IXC - %s' %row[1]
            new_pconta.codigo='02.09.%s' %str(pi).zfill(3)
            new_pconta.tipo = 'D'
            pi += 1
            new_pconta.save()




if args.descontos:
    with open(args.descontos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cobranca = fmodels.Cobranca.objects.filter(clientecontrato__id=row[0])
            if cobranca:
                cobranca = cobranca[0]
                print(cobranca)
                print(row)
                adcobranca_object = fmodels.ADCobranca()
                adcobranca_object.usuariocad = usuario
                adcobranca_object.parcelas = 99
                adcobranca_object.totalparcelas = 99
                adcobranca_object.tipo = fmodels.ADCOBRANCA_TEMPORARIO
                adcobranca_object.cobranca = cobranca
                adcobranca_object.justificativa = row[1]
                adcobranca_object.valor = -1 * Decimal(row[2])
                adcobranca_object.modogeracao = fmodels.MODO_GERA_LOTE
                
                if row[3] == '0000-00-00':
                    adcobranca_object.data_validade = None
                    adcobranca_object.tipo = fmodels.ADCOBRANCA_FIXO
                else:
                    adcobranca_object.data_validade = row[3]
                adcobranca_object.observacao='Validade IXC: %s' %row[3]
                adcobranca_object.ativa = row[4] == '1'
                adcobranca_object.save()


if args.pagar:
    with open(args.pagar, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                dados = {} 
                #dados['id'] = row[0]
                # row[1] - caixa
                # row[2] - empresa
                try:
                     dados['fornecedor'] = fmodels.Fornecedor.objects.get(pk=int(row[1]))
                except:
                     dados['fornecedor'] = None 

                try:
                    dados['descricao'] = row[2][:100]
                except:
                    print "ERROR UTF8 enconding", row[2]

                dados['valor'] = row[3]
                if row[4] == 'Dinheiro':
                    dados['forma_pagamento'] = fmodels.FormaPagamento.objects.get(id=1)
                elif row[4] == 'Cartão':
                    dados['forma_pagamento'] = fmodels.FormaPagamento.objects.get(id=3)
                elif row[4] == 'Débito':
                    dados['forma_pagamento'] = fmodels.FormaPagamento.objects.get(id=4)
                else:
                    dados['forma_pagamento'] = fmodels.FormaPagamento.objects.get(id=1)


                try:
                    dados['centrodecusto'] = fmodels.CentrodeCusto.objects.get(id=int(row[5])+1000)
                except:
                    continue
 
                dados['data_emissao'] = row[6]
                dados['data_cadastro'] = row[6]
                dados['data_alteracao'] = row[6]
                #dados['data_vencimento'] = row[7]

                dados['usuario'] = usuario

                print(dados)
                #dados.pop('data_vencimento')
                pagar = fmodels.Pagar(**dados)
                pagar.save()
                pagar.data_cadastro=pagar.data_emissao
                pagar.save()

                dadosparcela = {} 
                dadosparcela['pagar'] = pagar
                dadosparcela['valor'] = dados['valor']
                dadosparcela['parcela'] = 1
                dadosparcela['status'] = fmodels.PAGAR_STATUS_PENDENTE
                if Decimal(row[8]) > Decimal('0.00'):
                    dadosparcela['status']= fmodels.PAGAR_STATUS_QUITADO
                    dadosparcela['data_pagamento'] = row[7]
                    dadosparcela['valor_pago'] = row[8]
                dadosparcela['data_vencimento'] = row[7]
                dadosparcela['data_cadastro'] = dados['data_cadastro']
                dadosparcela['juros'] = 0
                dadosparcela['multa'] = 0
                dadosparcela['desconto'] = 0
                dadosparcela['usuario'] = dados['usuario']

                print(dadosparcela)
                pagaritem = fmodels.PagarItem(**dadosparcela)
                pagaritem.save()


            except Exception as e:
                print '------------------- ERROR ------------------------'
                print row, e
                print '--------------------------------------------------'    


if args.chamadoassuntos:
    with open(args.chamadoassuntos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {}
            dados['id'] = int(row[0])
            dados['codigo'] = int(row[0])
            dados['descricao'] = row[1]
            new_tipo = amodels.Tipo(**dados)
            new_tipo.save()
            new_motivoos = amodels.MotivoOS(**dados)
            new_motivoos.save()

if args.setores:
    with open(args.setores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {} 
            dados['id'] = int(row[0])
            dados['nome'] = row[1]
            new_setor = admmodels.Setor(**dados)
            new_setor.save()

if args.chamados:
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.chamados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=row[1])
                if clientecontrato:
                    print(row)
                    ocorrencia = {} 
                    ocorrencia['id'] = int(row[0]) + 100
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                    try:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(id=row[2])
                    except:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(id=5)
                    if row[3]:
                        try:
                            ocorrencia['setor'] = admmodels.Setor.objects.get(id=row[3])
                        except:
                            pass
                    ocorrencia['usuario'] = usuario
                    ocorrencia['metodo'] = metodo
                    ocorrencia['numero'] = row[4]
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if row[5] == 'F' else amodels.OCORRENCIA_ABERTA

                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['status'] = 1 if row[5] else 0
                    ocorrencia['data_cadastro'] = row[6]
                    ocorrencia['data_agendamento'] = row[7]
                    ocorrencia['data_finalizacao'] = row[8]
                    ocorrencia['conteudo'] = row[9]
                    for ok in ocorrencia:
                        if ocorrencia[ok] == '0000-00-00 00:00:00':
                            ocorrencia[ok] = None
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()
                    new_ocorrencia.data_cadastro = row[6]
                    new_ocorrencia.data_agendamento = row[7]
                    new_ocorrencia.data_finalizacao = row[8]
                    if new_ocorrencia.data_agendamento == '0000-00-00 00:00:00':
                        new_ocorrencia.data_agendamento = None
                    if new_ocorrencia.data_finalizacao == '0000-00-00 00:00:00':
                        new_ocorrencia.data_finalizacao = None
                    new_ocorrencia.save()
        
                    ordem = {}
                    ordem['id'] = int(row[0]) + 100
                    ordem['ocorrencia'] = amodels.Ocorrencia.objects.get(id=int(row[0]) + 100)
                    ordem['status'] = amodels.OS_ENCERRADA if row[5] == 'F' else amodels.OS_ABERTA
                    ordem['usuario'] = usuario
                    ordem['setor'] = ocorrencia['setor']
                    try:
                        ordem['motivoos'] = amodels.MotivoOS.objects.get(id=row[2])
                    except:
                        ordem['motivoos'] = amodels.MotivoOS.objects.get(id=4)
                    ordem['data_cadastro'] = ocorrencia['data_cadastro']
                    ordem['data_agendamento'] = ocorrencia['data_agendamento']
                    ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                    ordem['conteudo'] = ocorrencia['conteudo']
                    ordem['observacao'] = row[10]
                    for oser in ordem:
                        if ordem[oser] == '0000-00-00 00:00:00':
                            ordem[oser] = None
                    new_ordem = amodels.OS(**ordem)
                    new_ordem.save()
                    new_ordem.data_cadastro = ocorrencia['data_cadastro']
                    new_ordem.data_agendamento = ocorrencia['data_agendamento']
                    new_ordem.data_finalizacao = ocorrencia['data_finalizacao']
                    if new_ordem.data_agendamento == '0000-00-00 00:00:00':
                        new_ordem.data_agendamento = None
                    if new_ordem.data_finalizacao == '0000-00-00 00:00:00':
                        new_ordem.data_agendamento = None
                    new_ordem.save()
            except Exception as e:
                print(e)


if args.chamadosarquivos:
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.chamadosarquivos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ocorrencia = amodels.Ocorrencia.objects.filter(id=int(row[1]) + 100).first()
            if ocorrencia:
                print(row)
                ocorrenciaanexo = amodels.OcorrenciaAnexo()
                ocorrenciaanexo.ocorrencia = ocorrencia
                ocorrenciaanexo.id = row[0]
                ocorrenciaanexo.descricao = row[2]
                ocorrenciaanexo.arquivo = row[3]
                ocorrenciaanexo.usuario = usuario
                ocorrenciaanexo.data_cadastro = row[4]
                ocorrenciaanexo.save()


if args.historico:
    with open(args.historico, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if len(row) < 3:
                continue 
            
            if row[2] in ['0000-00-00','']:
                continue 
            
            if not row[0]:
                continue 
            
            clientecontrato = admmodels.ClienteContrato.objects.filter(id=row[0])
            if clientecontrato:
                cliente_id = clientecontrato[0].cliente.id
                usuario_set = usuario 

                dados = {}
                dados['model_name'] = 'cliente'
                dados['app_label'] = 'admcore'
                dados['object_id'] = cliente_id
                dados['user'] = usuario_set
                dados['history'] = row[1]
                if not row[2]:
                    continue
                dados['date_created'] = row[2]
                print dados
                h = admmodels.History(**dados)
                h.save()
                h.date_created=row[2]
                h.save()



if args.olts:
    with open(args.olts, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            olt = nmodels.OLT()
            olt.olttype = row[1].lower()
            if olt.olttype == 'pk':
                olt.olttype='parksv6'
            olt.id=row[0]
            olt.description = row[2]
            olt.host = row[3]
            olt.telnet_port = row[4]
            olt.notes = "porta_telnet=%s" %row[5]
            olt.username = row[6]
            olt.password = row[7]
            olt.save()


if args.pons:
    with open(args.pons, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            try:
                olt = nmodels.OLT.objects.filter(id=row[1])
                if not olt:
                    continue 
                if not row[4]:
                    continue
                pon = nmodels.OltPon()
                pon.id = row[0]
                pon.olt = olt[0]
                pon.slot = row[2]
                #if not row[2]:
                pon.slot = row[4].split('/')[-2]
                pon.pon = row[3]
                #if not row[3]:
                pon.pon = row[4].split('/')[-1]
                pon.description = row[4]
                pon.vlan = row[5]
                if not row[5]:
                    pon.vlan = None
                pon.save()
            except Exception as e:
                print(e)


if args.ctos:
    with open(args.ctos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            s = nmodels.Splitter()
            s.id = row[0]
            s.ident = '%s %s' %(row[1],row[2])
            s.map_ll = '%s,%s' %(row[3],row[4])
            s.localization = '%s %s %s %s' %(row[5],row[6],row[7],row[8])
            s.ports = row[9]
            s.note=row[10]
            s.save()


if args.onutemplates:
    with open(args.onutemplates, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            onutemplate = nmodels.ONUTemplate()
            onutemplate.onuargs = {'ixc': 1}
            onutemplate.id = row[0]
            onutemplate.description = row[1]
            onutemplate.addcmd=row[2]
            onutemplate.active=True
            onutemplate.save()


if args.onus:
    with open(args.onus, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            phy_addr = row[6] or row[7]
            onutemplate = None
            if nmodels.ONU.objects.filter(phy_addr__trim__iexact=phy_addr).count() > 0:
                continue 
            olt = nmodels.OLT.objects.filter(id=row[1]).first()
            if not olt:
                continue
            cto = None
            if row[2]:
                cto = nmodels.Splitter.objects.filter(id=row[2]).first()
            pon = olt.oltpon_set.filter(slot=row[3],pon=row[4]).first()
            if not pon:
                continue
            if row[12]:
                onutemplate = nmodels.ONUTemplate.objects.filter(id=row[12]).first()
            if not row[5]:
                continue

            onu = nmodels.ONU()
            onu.pon = pon
            onu.id = row[0]
            onu.onuid=row[5]
            onu.phy_addr = phy_addr 
            onu.onutype = row[8]
            onu.vlan = row[9]
            if not row[9]:
                onu.vlan = None
            if cto:
                onu.splitter = cto
            onu.description = row[10]
            if row[11]:
                if row[11] != '0':
                    onu.splitter_port=row[11]
            onu.date_created = datetime.now()
            onu.onutemplate = onutemplate
            onu.save()


if args.loginsonu:
    with open(args.loginsonu, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            login = row[0]
            serial = row[1]
            servico = admmodels.ServicoInternet.objects.filter(login=login,onu__isnull=True)
            if servico:
                onu = nmodels.ONU.objects.filter(phy_addr=serial[0:12])
                if onu:
                    onu = onu[0]
                    onu.service=servico[0]
                    onu.save()
                    print(servico[0],serial[0:12])





