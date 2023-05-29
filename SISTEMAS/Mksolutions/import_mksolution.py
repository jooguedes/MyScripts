#!/usr/bin/python
# -*- coding: utf-8 -*-
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
parser.add_argument('--semcontrato', dest='semcontrato', type=bool, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--plano', dest='plano', type=str, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=str, help='Criar vencimento para corrigir',required=False)
parser.add_argument('--ocorrenciatipo', dest='ocorrenciatipo', type=str, help='tipo atendimento',required=False)
parser.add_argument('--motivoos', dest='motivoos', type=str, help='tipo atendimento',required=False)
parser.add_argument('--atendimentos', dest='atendimentos', type=str, help='atendimentos',required=False)
parser.add_argument('--os', dest='os', type=str, help='ordens de servico',required=False)
parser.add_argument('--os2', dest='os2', type=str, help='ordens de servico',required=False)
parser.add_argument('--postes', dest='postes', type=str, help='postes',required=False)
parser.add_argument('--cto', dest='cto', type=str, help='CTO',required=False)
parser.add_argument('--tsuspensos',dest='tsuspensos',type=str,required=False)
parser.add_argument('--tsubstituidos',dest='tsubstituidos',type=str,required=False)
parser.add_argument('--fornecedores',dest='fornecedores',type=str,required=False)
parser.add_argument('--historicocontrato',dest='historicocontrato',type=str,required=False)
parser.add_argument('--loginsliberados',dest='loginsliberados',type=str,required=False)
parser.add_argument('--loginssuspensos',dest='loginssuspensos',type=str,required=False)
parser.add_argument('--loginsdados',dest='loginsdados',type=str,required=False)
parser.add_argument('--updateplanopolicy',dest='updateplanopolicy',type=str,required=False)
parser.add_argument('--naslote', dest='naslote', type=str, help='Criar plano para corrigir',required=False)


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
from apps.atendimento import models as amodels
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
nasdefault = None 
planodefault = None

if args.semcontrato:
    idcontrato_seq = admmodels.ClienteContrato.objects.all().order_by('-id')[0].id
    idcontrato_seq += 1

if args.portador:
    portador = fmodels.Portador.objects.get(id=args.portador)

if args.nas:
    nasdefault = nmodels.NAS.objects.get(id=args.nas)

if args.plano:
    planodefault = admmodels.PlanoInternet.objects.get(id=args.plano)


if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[2]:
                if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                    print row
                    new_portador = fmodels.Portador()
                    new_portador.id = row[0]
                    new_portador.descricao = row[2]
                    new_portador.codigo_banco = '999'
                    new_portador.agencia = row[3]
                    new_portador.agencia_dv = row[4]
                    new_portador.conta = row[5]
                    new_portador.conta_dv = row[6]
                    new_portador.convenio = row[7]
                    new_portador.carteira = row[9][0:5]
                    new_portador.cedente=row[12]
                    new_portador.cpfcnpj = row[13]
                    new_portador.localpag = row[14]
                    new_portador.instrucoes1 = row[15]
                    new_portador.instrucoes2 = row[16]
                    new_portador.instrucoes3 = row[17]
                    new_portador.instrucoes4 = row[18]
                    new_portador.save()

if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(id=row[0]).count() == 0:
                print row
                new_plano = admmodels.Plano()
                new_plano.id = row[0]
                new_plano.descricao=row[1]
                if row[2]:
                    new_plano.preco = row[2]
                else:
                    new_plano.preco = 0.00
                new_plano.grupo = admmodels.Grupo.objects.all().order_by('id')[0]
                new_plano.contrato = admmodels.Contrato.objects.all().order_by('id')[0]
                new_plano.pospago = True
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=row[0]
                new_plano_internet.plano = new_plano
                new_plano_internet.policy_out=row[14] 
                new_plano_internet.policy_in=row[15]
                if row[3]:
                    new_plano_internet.download = int(fnum(row[3]))
                else:
                    new_plano_internet.download = 0

                if row[4]:
                    new_plano_internet.upload = int(fnum(row[4]))
                else:
                    new_plano_internet.upload = 0
                new_plano_internet.diasparabloqueio = 15
                new_plano_internet.save() 

if args.updateplanopolicy:
    with open(args.updateplanopolicy, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            plano = admmodels.PlanoInternet.objects.filter(id=row[0])[:1]
            if plano:
                plano = plano[0]
                plano.policy_out=row[14] 
                plano.policy_in=row[15]
                plano.policyv6_out=row[16] 
                plano.policyv6_in=row[17]
                plano.policy_out_red=row[18] 
                plano.policy_in_red=row[19]
                plano.policyv6_out_red=row[20] 
                plano.policyv6_in_red=row[21]
                plano.save()
                print(plano)
                print(row) 

if args.naslote:
    with open(args.naslote, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if nmodels.NAS.objects.filter(nasname=row[1].strip()).count() == 0:
                print(row)
                new_nas = nmodels.NAS()
                new_nas.nasname=row[1].strip()
                new_nas.shortname=row[2].strip()
                new_nas.description= row[3].strip()
                new_nas.secret = row[4].strip()
                new_nas.xuser= row[5].strip()
                new_nas.xtype = 'mikrotik'
                new_nas.xpassword = row[6].strip()
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
            tipo = row[2]
            nome = row[3]
            nomefantasia = ''
            cpf = row[4]
            cnpj = row[5]
            rgie = row[6]
            insc_estadual = row[7]
            insc_municipal = row[8]
            data_nasc = row[9]

            nomepai = row[11]
            nomemae = row[12]
            cli_obs = row[13]

            email = row[15] # outro_email
            celular = row[16] # celular
            telefonecom = row[17] # telefonecom
            telefone = ''   
            celularcom = ''

            sexo = ''

            estadocivil = ''
            profissao = ''
            cpfcnpj = cpf
            if cnpj:
                cpfcnpj = cnpj

            endereco_inst = {}
            endereco_inst['logradouro'] = row[19] # tipo_insta,endereco_insta
            try:
                endereco_inst['numero'] = int(row[20]) # numero_insta
            except:
                endereco_inst['numero'] = None 
            endereco_inst['complemento'] = row[21]
            endereco_inst['bairro'] = row[22]
            endereco_inst['cep'] = row[23]
            endereco_inst['cidade'] = row[24]
            endereco_inst['uf'] = row[25]
            endereco_inst['pontoreferencia'] = ''

            endereco_cob = {} 
            endereco_cob['logradouro'] = row[26] # tipo_insta,endereco_insta
            try:
                endereco_cob['numero'] = int(row[27]) # numero_insta
            except:
                endereco_cob['numero'] = None 
            endereco_cob['complemento'] = row[28]
            endereco_cob['bairro'] = row[29]
            endereco_cob['cidade'] = row[30]
            endereco_cob['uf'] = row[31]
            endereco_cob['cep'] = row[23]
            endereco_cob['pontoreferencia'] = ''
            
            vencimento = row[32] or 10
            senha_central = row[33]

            data_cancela = row[34]
            data_suspenso = row[35]
            data_ativacao = row[36]

            comodato = False
            if row[37]:
                comodato = True
            pre_pago = False
            if row[38]:
                pre_pago = True

            plano_id = row[39]
            try:
                plano = admmodels.PlanoInternet.objects.get(plano__id=plano_id)
            except:
                plano = planodefault

            login = row[40]
            if not login:
                login = 'login_%s' %idcontrato
            senha = row[41]
            if not senha:
                senha = '123456'
            
            mac_dhcp = row[42]
            ip = row[43]
            servico_obs = row[44]
            inativo = row[45]
            observacoes2 = row[46]
            nf21 = row[47]

            respempresa = ''
            data_cadastro = data_ativacao
            if not data_cadastro:
                data_cadastro=date.today().strftime("%Y-%m-%d")

            if vencimento in ['0','']:
                vencimento = 1
            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento 
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 

            respempresa = ''
            respcpf = ''

            cidade_q = normalize('NFKD', unicode(endereco_inst['cidade'])).encode('ASCII','ignore')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=endereco_inst['uf']
                new_pop.save()
                pop = new_pop

            if nasdefault:
                nas = nasdefault

            #nas = nmodels.NAS.objects.all()[0]

            notafiscal = False

            con_obs=''
            mac = None
            conexao_tipo = 'ppp'

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            if data_suspenso:
                status_cc = 4
                status_s = 4
                status_c = 4

            if data_cancela:
                status_cc = 3
                status_s = 3
                status_c = 3

            if inativo == 'S':
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
            login = normalize('NFKD', unicode(login)).encode('ASCII','ignore').decode('ascii')

            print status_cc, login, nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print endereco_cob,endereco_inst
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
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

                    #try:
                    #    fmodels.Portador.objects.get(pk=portador)
                    #except:
                    #    portador = 1
                    #
                    

                    
                    if tipo == '1':
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
                    
                    else:
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = nome
                        
                        new_pessoa.nomefantasia = nomefantasia
                        new_pessoa.respempresa = respempresa
                        new_pessoa.respcpf = respcpf
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = insc_estadual
                        new_pessoa.insc_municipal = insc_municipal
                        new_pessoa.tipo = 8
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

                    if observacoes2:
                        new_cliente.observacao='\n%s' %(observacoes2)

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
                if args.semcontrato and new_cliente.cobranca_set.all().count() > 0:
                    new_cobranca.portador = new_cliente.cobranca_set.all()[0].portador
                else:
                    new_cobranca.portador = portador
                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
                new_cobranca.isento = isento
                new_cobranca.notafiscal = False
                new_cobranca.data_cadastro = data_cadastro 
                new_cobranca.datacobranca1 = data_cadastro
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = status_c
                if nf21.lower() in ['s','sim']:
                    new_cobranca.notafiscal=True
                new_cobranca.save()
                
                new_cobranca.data_cadastro = data_cadastro 
                new_cobranca.save()
                
                # Contrato 
                new_contrato = admmodels.ClienteContrato()
                if args.semcontrato:
                    new_contrato.id=idcontrato_seq
                    idcontrato_seq += 1
                else:
                    new_contrato.id=idcontrato
                new_contrato.cliente = new_cliente 
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca
                 
                new_contrato.data_inicio = data_cadastro 
                new_contrato.data_cadastro = data_cadastro 
                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()

                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()

                
                for ic in status_criar:
                    data_status = data_cadastro
                    if ic == 3:
                        data_status = data_cancela or data_cadastro
                    elif ic == 4:
                        data_status = data_suspenso or data_cadastro

                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario 
                    new_status.data_cadastro = data_status 
                    new_status.save() 
                
                    new_status.data_cadastro = data_status 
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
                new_servico.observacao = servico_obs
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)



if args.titulos:
    #portador = fmodels.Portador.objects.get(id=args.portador)
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            cliente = admmodels.Cliente.objects.filter(id=row[0])
            cobranca = None 
            contrato = None
            if not row[17]:
                continue

            portador = fmodels.Portador.objects.filter(id=row[17])
            if not portador:
                continue 

            if portador:
                portador = portador[0]
            if cliente:
                cliente = cliente[0]
                print('consultando cliente')
                print(cliente)
                if row[1]:
                    contrato = admmodels.ClienteContrato.objects.filter(id=row[1])
                    if contrato:
                        contrato = contrato[0]
                        cobranca = contrato.cobranca

                if not row[8]:
                    continue 
                
                if fmodels.Titulo.objects.filter(portador=portador,nosso_numero=row[8]).count() == 0:
                    print('importando boleto')
                    tdata = {} 
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['demonstrativo'] = row[3]
                    tdata['data_documento'] = row[4].split(' ')[0]
                    tdata['data_vencimento'] = row[5].split(' ')[0]
                    tdata['data_pagamento'] = row[6].split(' ')[0]
                    tdata['data_baixa'] = row[6].split(' ')[0]                    
                    tdata['numero_documento'] = row[7] or row[8]
                    tdata['nosso_numero'] = row[8] 
                    tdata['parcela'] = 1
                    tdata['portador'] = portador
                    tdata['valor'] = row[9].replace(',','.')
                    tdata['valorpago'] = row[10]
                    if tdata['valorpago']:
                        tdata['valorpago'] = tdata['valorpago'].replace(',','.')
                    tdata['usuario_b'] = usuario # usuariobaixa 28 
                    tdata['usuario_g'] = usuario # usuariogerou 29
                    tdata['usuario_c'] = usuario # usuariocancela 30 
                    tdata['modogeracao'] = 'l'
                    tdata['motivocancela'] = None
                    tdata['motivodesconto'] = None
                    tdata['data_cancela'] = row[14].split(' ')[0]

                    if row[16] == 'S':
                        tdata['data_cancela'] = tdata['data_vencimento']

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
                        if row[13] == 'S':
                            tdata['observacao'] = 'mk=suspensa'
                        if row[16] == 'S':
                            tdata['observacao'] = 'mk=substituida'
                    else:
                        tdata['status'] = fmodels.MOVIMENTACAO_GERADA
                    if tdata['demonstrativo'] is None:
                        tdata['demonstrativo'] = ''
                    print tdata
                    new_titulo = fmodels.Titulo(**tdata)
                    new_titulo.save()
                    new_titulo.data_documento = tdata['data_documento']
                    new_titulo.save()
                    new_titulo.updateDadosFormatados()
                    print('Feito')
            else:
                print 'nao achei', row


if args.ocorrenciatipo:
    with open(args.ocorrenciatipo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {}
            dados['id'] = int(row[0])
            dados['codigo'] = int(row[0])
            dados['descricao'] = row[1]
            new_tipo = amodels.Tipo(**dados)
            new_tipo.save()


if args.motivoos:
    with open(args.motivoos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {}
            dados['id'] = int(row[0])
            dados['codigo'] = int(row[0])
            dados['descricao'] = row[1]
            new_motivoos = amodels.MotivoOS(**dados)
            new_motivoos.save()



#COPY ( 
#select 
#0 a.codatendimento,
#1 a.cliente_cadastrado,
#2 a.classificacao_atendimento,
#3 '' as setor,
#4 a.protocolo,
#5 a.finalizado,
#6 a.operador_abertura, 
#7 a.operador_atendimento,
#8 a.dt_abertura::text || ' '||hr_abertura::text as data_cadastro,
#9 '' as data_agendamento,
#10 a.dt_finaliza::text || ' ' || hr_finaliza::text as data_finalizacao,
#11 a.info_cliente || a.texto_encerramento
#
#12 FROM mk_atendimento a 
#13 inner join mk_atendimento_classificacao tipo on (tipo.codatclass=a.classificacao_atendimento)
#14 where a.cliente_cadastrado is not null
#15 ) TO '/tmp/mksolution-atendimentos.csv' DELIMITER '|' CSV;
#

if args.atendimentos:
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.atendimentos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=row[1])
                if clientecontrato:
                    if amodels.Ocorrencia.objects.filter(id=int(row[0])).count() == 0:
                        print(row)
                        new_ocorrencia = amodels.Ocorrencia()
                        new_ocorrencia.id = int(row[0])
                        new_ocorrencia.clientecontrato = clientecontrato[0]
                        new_ocorrencia.setor = None 

                        try:
                            new_ocorrencia.tipo = amodels.Tipo.objects.get(codigo=row[2].strip())
                        except:
                            new_ocorrencia.tipo = amodels.Tipo.objects.get(codigo=999)

                        if row[3]:
                            try:
                                new_ocorrencia.setor = admmodels.Setor.objects.get(id=row[3])
                            except:
                                pass
                        new_ocorrencia.usuario = usuario
                        new_ocorrencia.metodo = metodo
                        new_ocorrencia.numero = row[4]
                        new_ocorrencia.status = amodels.OCORRENCIA_ENCERRADA if row[5].strip() == 'S' else amodels.OCORRENCIA_ABERTA
                        new_ocorrencia.responsavel = usuario
                        new_ocorrencia.data_cadastro = row[8]
                        new_ocorrencia.data_agendamento = None
                        new_ocorrencia.data_finalizacao = row[10]


                        if not row[10]:
                            new_ocorrencia.data_finalizacao = None

                        new_ocorrencia.conteudo = 'Operador: %s \n %s' %(row[6],row[11])
                        if row[12]:
                            new_ocorrencia.conteudo += '\n %s' %row[12]

                        if new_ocorrencia.data_agendamento == '0000-00-00 00:00:00':
                            new_ocorrencia.data_agendamento = None
                        if new_ocorrencia.data_finalizacao == '0000-00-00 00:00:00':
                            new_ocorrencia.data_finalizacao = None

                        new_ocorrencia.save()
                        new_ocorrencia.data_cadastro = row[8]
                        new_ocorrencia.data_agendamento = None
                        new_ocorrencia.data_finalizacao = row[10]

                        if not row[10]:
                            new_ocorrencia.data_finalizacao=None
                        if new_ocorrencia.data_agendamento == '0000-00-00 00:00:00':
                            new_ocorrencia.data_agendamento = None
                        if new_ocorrencia.data_finalizacao == '0000-00-00 00:00:00':
                            new_ocorrencia.data_finalizacao = None
                        new_ocorrencia.save()
            except Exception as e2:
                print(e2)

if args.os:
    n = 999900001
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.os, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            if amodels.OS.objects.filter(id=row[0]).count() > 0:
                continue 

            clientecontrato = None 
            ocorrencia = None
            if row[13]:
                cliente = admmodels.Cliente.objects.filter(id=row[13])
                if cliente:
                    clientecontrato = cliente[0].clientecontrato_set.all()
            if len(row[2]) > 14:
                row[2] = ''.join(row[2][-14:])

            if clientecontrato:
                if row[1]:
                    ocorrencia = amodels.Ocorrencia.objects.filter(id=row[1],os__isnull=True)
                elif row[2]:
                    ocorrencia = amodels.Ocorrencia.objects.filter(numero=row[2],os__isnull=True)
                if ocorrencia:
                    ocorrencia = ocorrencia[0]
                    print(row)
                else:
                    print(row)
                    new_ocorrencia = amodels.Ocorrencia()
                    new_ocorrencia.id = int(row[0])
                    new_ocorrencia.clientecontrato = clientecontrato[0]
                    new_ocorrencia.setor = None 

                    new_ocorrencia.tipo = amodels.Tipo.objects.get(codigo=999)

                    #if row[3]:
                    #    try:
                    #        new_ocorrencia.setor = admmodels.Setor.objects.get(id=row[3])
                    #    except:
                    #        pass
                    new_ocorrencia.usuario = usuario
                    new_ocorrencia.metodo = metodo

                    new_ocorrencia.numero = n
                    n += 1

                    new_ocorrencia.status = amodels.OCORRENCIA_ENCERRADA if row[5].strip() == 'S' else amodels.OCORRENCIA_ABERTA
                    new_ocorrencia.responsavel = usuario
                    new_ocorrencia.data_cadastro = row[6]
                    new_ocorrencia.data_agendamento = row[7]
                    new_ocorrencia.data_finalizacao = row[8]


                    if not row[8]:
                        new_ocorrencia.data_finalizacao = None

                    new_ocorrencia.conteudo = 'Protocolo OS: %s\n Operador: %s \n %s' %(row[2],row[4],row[9])
                    if row[12]:
                        new_ocorrencia.conteudo += '\n %s' %row[12]

                    if new_ocorrencia.data_agendamento == '0000-00-00 00:00:00':
                        new_ocorrencia.data_agendamento = None
                    if new_ocorrencia.data_finalizacao == '0000-00-00 00:00:00':
                        new_ocorrencia.data_finalizacao = None
                    if not new_ocorrencia.data_agendamento:
                        new_ocorrencia.data_agendamento = None 
                    new_ocorrencia.save()
                    new_ocorrencia.data_cadastro = row[6]
                    new_ocorrencia.data_agendamento = row[7]
                    new_ocorrencia.data_finalizacao = row[8]
                    if new_ocorrencia.data_agendamento == '0000-00-00 00:00:00':
                        new_ocorrencia.data_agendamento = None
                    if new_ocorrencia.data_finalizacao == '0000-00-00 00:00:00':
                        new_ocorrencia.data_finalizacao = None
                    if not new_ocorrencia.data_agendamento:
                        new_ocorrencia.data_agendamento = None 
                    if not new_ocorrencia.data_finalizacao:
                        new_ocorrencia.data_finalizacao = None
                    new_ocorrencia.save()

                    ocorrencia = new_ocorrencia

                ordem = {}
                ordem['id'] = int(row[0])
                ordem['ocorrencia'] = ocorrencia
                ordem['status'] = amodels.OS_ENCERRADA if row[5].strip() == 'S' else amodels.OS_ABERTA
                ordem['usuario'] = usuario
                ordem['setor'] = ocorrencia.setor
                try:
                    ordem['motivoos'] = amodels.MotivoOS.objects.get(id=row[3])
                except:
                    ordem['motivoos'] = amodels.MotivoOS.objects.get(id=4)
                ordem['conteudo'] = 'Operador: %s \n' %(row[4])
                if row[9]:
                    ordem['conteudo'] += 'Problema Relatado: %s\n' %(row[9])
                if row[10]:
                    ordem['conteudo'] += 'Constatado: %s\n' %(row[10])
                if row[12]:
                    ordem['conteudo'] += 'Serviço Realizado: %s\n' %(row[12])

                if row[11]:
                    ordem['observacao'] = row[11]

                for oser in ordem:
                    if ordem[oser] == '0000-00-00 00:00:00':
                        ordem[oser] = None
                new_ordem = amodels.OS(**ordem)

                new_ordem.data_cadastro = row[6]
                new_ordem.data_agendamento = row[7]
                new_ordem.data_finalizacao = row[8]

                if not row[7]:
                    new_ordem.data_agendamento = None

                if not row[8]:
                    new_ordem.data_finalizacao = None

                if new_ordem.data_agendamento == '0000-00-00 00:00:00':
                    new_ordem.data_agendamento = None
                if new_ordem.data_finalizacao == '0000-00-00 00:00:00':
                    new_ordem.data_agendamento = None

                new_ordem.save()
                new_ordem.data_cadastro = row[6]
                new_ordem.data_agendamento = row[7]
                new_ordem.data_finalizacao = row[8]

                if not row[7]:
                    new_ordem.data_agendamento = None

                if not row[8]:
                    new_ordem.data_finalizacao = None

                if new_ordem.data_agendamento == '0000-00-00 00:00:00':
                    new_ordem.data_agendamento = None
                if new_ordem.data_finalizacao == '0000-00-00 00:00:00':
                    new_ordem.data_agendamento = None
                new_ordem.save()




if args.postes:
    with open(args.postes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)

            new_poste = nmodels.StreetPole()
            new_poste.id=row[0]
            new_poste.ident=row[1]
            new_poste.map_ll=row[2]
            new_poste.localization='%s\n%s,%s,%s,%s,%s-%s' %(row[3],
                                                            row[4],
                                                            row[5],
                                                            row[6],
                                                            row[7],
                                                            row[8])

            new_poste.save()


if args.cto:
    with open(args.cto, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            new_cto = nmodels.Splitter()
            new_cto.ident = row[0]
            new_cto.map_ll = row[1]
            poste = nmodels.StreetPole.objects.filter(id=row[2])
            if poste:
                new_cto.streetpole = poste[0]
            new_cto.ports = row[3]
            new_cto.save()


if args.tsuspensos:
    with open(args.tsuspensos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            nn = row[8]
            portador = fmodels.Portador.objects.filter(id=row[17])
            if not portador:
                continue 
            print(fmodels.Titulo.objects.filter(nosso_numero=nn,
                                              portador=portador).update(status=fmodels.MOVIMENTACAO_CANCELADA,
                                                                        motivocancela='mk=suspensa',
                                                                        usuario_c=usuario,
                                                                        data_cancela=row[3].split()[0]))

if args.tsubstituidos:
    with open(args.tsubstituidos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            nn = row[8]
            portador = fmodels.Portador.objects.filter(id=row[17])
            if not portador:
                continue 
            print(fmodels.Titulo.objects.filter(nosso_numero=nn,
                                               portador=portador).update(status=fmodels.MOVIMENTACAO_CANCELADA,
                                                                         motivocancela='mk=substituida',
                                                                         usuario_c=usuario,
                                                                         data_cancela=date.today().strftime('%Y-%m-%d')))




if args.fornecedores:
    with open(args.fornecedores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {} 
            dados['id'] = int(row[0])
            dados['tipo_pessoa'] = 'F'
            dados['nome'] = row[2]
            dados['cpfcnpj'] = row[3]
            if row[4]:
                dados['tipo_pessoa'] = 'J'
                dados['cpfcnpj'] = row[4]
            dados['rg'] = row[5]
            dados['insc_estadual'] = row[6]
            dados['insc_municipal'] = row[7]           
            dados['email'] = row[14]
            dados['telefones'] = ','.join(row[15:17])
            dados['nomefantasia'] = row[2]            
            dados['observacao'] = row[12]
            dados['logradouro'] = row[17]
            dados['numero'] = row[18]
            dados['complemento'] = row[19]
            dados['bairro'] = row[20]
            dados['cep'] = row[21]
            dados['cidade'] = row[22]
            dados['uf'] = row[23]
            dados['data_cadastro'] = row[24]
            dados['ativo'] = True
            novo_fornecedor = fmodels.Fornecedor(**dados)
            novo_fornecedor.save()

if args.historicocontrato:
    with open(args.historicocontrato, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            clientecontrato = admmodels.ClienteContrato.objects.filter(id=row[0])
            if clientecontrato:
                cliente_id = clientecontrato[0].cliente.id
                usuario_set = usuario 

                usuario = admmodels.User.objects.filter(username=row[2].strip().lower())
                if usuario:
                    usuario = usuario[0]
                else:
                    usuario = admmodels.User()
                    usuario.username=row[2].strip().lower()
                    usuario.name='Usuario Historico'
                    usuario.password='12375127653761253765123'
                    usuario.save()

                dados = {}
                dados['model_name'] = 'cliente'
                dados['app_label'] = 'admcore'
                dados['object_id'] = cliente_id
                dados['user'] = usuario
                dados['history'] = '%s\n%s' %(row[3],row[4])
                dados['date_created'] = row[1]
                print dados

                if args.sync_db:
                    h = admmodels.History(**dados)
                    h.save()
                    h.date_created=row[1]
                    h.save()


if args.loginsliberados:
    with open(args.loginsliberados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row[0])
            s = admmodels.ServicoInternet.objects.filter(login=row[0])
            if s:
                s = s[0]
                print(s)
                s.status=admmodels.SERVICO_ATIVO
                s.save()
                s.clientecontrato.status.status=admmodels.CONTRATO_ATIVO
                s.clientecontrato.status.save()
                s.clientecontrato.cobranca.status=fmodels.COBRANCA_ATIVA
                s.clientecontrato.cobranca.save()


if args.loginssuspensos:
    with open(args.loginssuspensos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            s = admmodels.ServicoInternet.objects.filter(login=row[0])
            if s:
                s = s[0]
                s.status=admmodels.SERVICO_SUSPENSO
                s.save()
                s.clientecontrato.status.status=admmodels.CONTRATO_SUSPENSO
                s.clientecontrato.status.save()
                s.clientecontrato.cobranca.status=fmodels.COBRANCA_SUSPENSA
                s.clientecontrato.cobranca.save()


if args.loginsdados:
    with open(args.loginsdados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            s = admmodels.ServicoInternet.objects.filter(login=row[0])
            if s:
                try:
                    s = s[0]
                    s.ip = row[2]
                    s.mac_dhcp = row[1]
                    s.save()
                except Exception as e:
                    print(s,e)


#from apps.financeiro import models as fmodels
#from django.db.models import Q 
#from apps.admcore import models
#for c in models.Cliente.objects.all():
#    t=c.titulo_set.filter(Q(cobranca__isnull=False),
#                         ~Q(cobranca__in=c.cobranca_set.all()))
#    if t:
#        cobativa = c.cobranca_set.filter(clientecontrato__status__status=models.CONTRATO_ATIVO)
#        if len(cobativa) == 1:
#            print t.update(cobranca=cobativa[0])
#        elif len(cobativa) > 1:
#            print t.update(cobranca=cobativa[0])
#        else:
#            coball = c.cobranca_set.all()
#            if coball:
#                print t.update(cobranca=coball[0])
#        print(c)
        

