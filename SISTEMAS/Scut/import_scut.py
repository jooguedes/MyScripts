#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--material', dest='material', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--caixas', dest='caixas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--pops', dest='pops', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=str, help='Criar vencimento para corrigir',required=False)
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
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))
usuario = admmodels.User.objects.get(username='sgp')
if args.portador:
    portadordefault = fmodels.Portador.objects.get(id=args.portador)


if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[2]:
                if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                    print row
                    new_portador = fmodels.Portador()
                    new_portador.id = row[0]
                    new_portador.codigo_banco = '999'
                    new_portador.descricao = 'banco id %s' %row[0]
                    new_portador.agencia = row[1]
                    new_portador.agencia_dv = ''
                    new_portador.conta = row[2]
                    new_portador.conta_dv = ''
                    new_portador.convenio = row[3]
                    new_portador.carteira = row[4]
                    new_portador.localpag = row[6]
                    new_portador.instrucoes1 = row[7]
                    new_portador.instrucoes2 = row[8]
                    new_portador.instrucoes3 = row[9]
                    new_portador.instrucoes4 = row[10]
                    new_portador.cedente='PROVEDOR X'
                    new_portador.cpfcnpj = '0'
                    new_portador.save()

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

if args.material:
    with open(args.material, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.TipoEquipamento.objects.filter(id=row[0]).count() == 0:
                print row
                new_equipamento = admmodels.TipoEquipamento()
                new_equipamento.id = row[0]
                new_equipamento.grupo = admmodels.Grupo.objects.all()[0]
                new_equipamento.descricao = row[1]
                new_equipamento.save()

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
            if admmodels.Plano.objects.filter(id=row[0]).count() == 0:
                print row
                new_plano = admmodels.Plano()
                new_plano.id = row[0]
                new_plano.descricao=row[1]
                new_plano.preco = row[2]
                new_plano.grupo = admmodels.Grupo.objects.all().order_by('id')[0]
                new_plano.contrato = admmodels.Contrato.objects.all().order_by('id')[0]
                new_plano.pospago = True
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=row[0]
                new_plano_internet.plano = new_plano 
                vel_up,vel_down = row[3].split('/')
                if 'k' in vel_down.lower():
                    new_plano_internet.download = int(fnum(vel_down))
                elif 'm' in vel_down.lower():
                    new_plano_internet.download = int(fnum(int(vel_down))) * 1000
                else:
                    new_plano_internet.download = int(int(vel_down) / 1000.0)

                if 'k' in vel_up.lower():
                    new_plano_internet.upload = int(fnum(vel_up))
                elif 'm' in row[3].lower():
                    new_plano_internet.upload = int(fnum(vel_up)) * 1000
                else:
                    new_plano_internet.upload = int(int(vel_up) / 1000.0)
                new_plano_internet.diasparabloqueio = row[4]
                new_plano_internet.diasparaaviso = row[5]
                new_plano_internet.save() 

if args.nas:
    with open(args.nas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if nmodels.NAS.objects.filter(id=row[0]).count() == 0:
                if row[6] == 'y':
                    print row
                    new_nas = nmodels.NAS()
                    new_nas.id=row[0]
                    new_nas.shortname=row[2]
                    new_nas.secret = row[3]
                    new_nas.xuser= row[4]
                    new_nas.xtype = 'mikrotik'
                    new_nas.xpassword = row[5]
                    new_nas.nasname= row[11]
                    new_nas.save()

if args.clientes:
    nas = nmodels.NAS.objects.all()[0]
    formacobranca = fmodels.FormaCobranca.objects.all()[0]

    m = manage.Manage()

    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            #idcliente = row[0]
            #idcontrato = row[1]   # id
            tipo = row[2]
            nome = row[3]
            nomefantasia = row[3]
            cpfcnpj = row[4]
            if not row[4]:
                cpfcnpj = row[5]
            insc_estadual = row[6]
            data_nasc = row[7]
            data_cadastro = row[8]
            if not data_cadastro:
                data_cadastro = date.today().strftime('%Y-%m-%d')
            data_ativacao = row[9]
            if not data_ativacao:
                data_ativacao = date.today().strftime('%Y-%m-%d')
            status_bloq = row[10]
            status_canc = row[11]

            cli_obs = row[12]
            nao_suspende = row[13] == '1'

            rgie = ''
            sexo = ''
            estadocivil = ''
            profissao = ''

            endereco_inst = {}
            endereco_inst['logradouro'] = row[15] 
            endereco_inst['numero'] = None 
            endereco_inst['complemento'] = row[16]
            endereco_inst['bairro'] = row[17]
            endereco_inst['cep'] = row[18]
            endereco_inst['cidade'] = row[19]
            endereco_inst['uf'] = row[20]
            

            endereco_cob = {}
            endereco_cob['logradouro'] = row[15] 
            endereco_cob['numero'] = None 
            endereco_cob['complemento'] = row[16]
            endereco_cob['bairro'] = row[17]
            endereco_cob['cep'] = row[18]
            endereco_cob['cidade'] = row[19]
            endereco_cob['uf'] = row[20]


            
            email = row[21] # outro_email
            telefonecom = row[22] # telefonecom
            celular = row[23] # celular
            telefone = ''   
            celularcom = ''
            

            nomepai = ''
            nomemae = ''
        

            status = row[27] # A S D 
            login = row[0]
            senha = row[1]
            mac_dhcp = row[24]
            ip = row[25]

            data_ativo = row[27]
            senha_central = row[28]
            portador = row[29]
            vencimento = row[30]
            plano = admmodels.PlanoInternet.objects.get(id=row[31])
            addresslist = row[32]
            respempresa = ''
            insc_municipal = ''

            
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

            pop = admmodels.Pop.objects.all()[0]
            nas = nmodels.NAS.objects.all()[0]

            notafiscal = False

            con_obs=''
            mac = None
            conexao_tipo = 'ppp'

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            if status_bloq and not status_canc:
                status_cc = 4
                status_s = 4
                status_c = 4

            if status_canc:
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
            print status, login, nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print endereco_cob,endereco_inst
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" %nome
                # Save Models 

                cliente_check = admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=row[0])
        
                if len(cliente_check) == 0:

                    # Endereco 
                    new_endereco = admmodels.Endereco(**endereco_cob)
                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    new_endereco.save() 
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    
                    

                    
                    if tipo in ['0','1']:
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
                    
                    if tipo == '2':
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

                    
                    # Cliente
                    new_cliente = admmodels.Cliente()
                    #new_cliente.id = idcliente
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
                    
                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_cob.id = None 
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco_inst.id = None 
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    
                    
                    # Cliente
                    #new_cliente = imodels.Cliente()
                    #new_cliente.endereco = new_endereco
new_cliente.pessoa = new_pessoa
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
                    new_cobranca.portador = portadordefault
                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
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
                #new_contrato.id = idcontrato

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
                    if ic == 1:
                        new_status.data_ativacao = data_ativacao
                    else:
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
                new_servico.central_password=senha_central
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
                new_servico.addresslist=addresslist
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)



if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            cobranca = fmodels.Cobranca.objects.filter(clientecontrato__servicointernet__login=row[1])
            if cobranca:
                cobranca = cobranca[0]
                cliente = cobranca.cliente

                if fmodels.Titulo.objects.filter(id=row[0]).count() == 0:
                    print row
                    tdata = {} 
                    tdata['id'] = row[0]
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[0]
                    tdata['numero_documento'] = row[0]

                    try:
                        tdata['portador'] = portadordefault
                    except:
                        continue

                    tdata['observacao'] = ''
                    tdata['demonstrativo'] = row[4]
                    tdata['data_documento'] = row[5] # emissao
                    tdata['data_vencimento'] = row[6] # vencimento
                    tdata['data_baixa'] = row[7]
                    tdata['data_pagamento'] = row[7]
                    tdata['valor'] = row[8]
                    tdata['valorpago'] = row[9]
                    tdata['desconto'] = row[10]
                    tdata['juros'] = row[11]
                    tdata['parcela'] = row[12] # parcela
                    if not row[12]:
                        tdata['parcela'] = 1

                    tdata['data_cancela'] = None
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
                    print tdata
                    new_titulo = fmodels.Titulo(**tdata)
                    new_titulo.save()
                    new_titulo.data_documento = tdata['data_documento']
                    new_titulo.save()

