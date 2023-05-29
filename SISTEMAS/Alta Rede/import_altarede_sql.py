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
parser.add_argument('--clientesfix', dest='clientesfix', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--gerencianet', dest='gerencianet', type=str, help='Arquivo importacao',required=False)
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
parser.add_argument('--onus', dest='onus', type=str, help='chamado',required=False)
parser.add_argument('--historico', dest='historico', type=str, help='historico',required=False)
parser.add_argument('--fixdata', dest='fixdata', type=str, help='fixdata',required=False)
parser.add_argument('--fixfilial', dest='fixfilial', type=str, help='fixfilial',required=False)
parser.add_argument('--anotacoes', dest='anotacoes', type=str, help='anotacoes',required=False)
parser.add_argument('--arquivos', dest='arquivos', type=str, help='arquivos',required=False)
parser.add_argument('--nf2122', dest='nf2122', type=str,help='importar nf21/22', required=False)


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
            if admmodels.Plano.objects.filter(id=row[0]).count() == 0:
                print row
                new_plano = admmodels.Plano()
                new_plano.id = row[0]
                new_plano.descricao=row[1]
                new_plano.preco = row[4]
                new_plano.grupo = admmodels.Grupo.objects.all().order_by('id')[0]
                new_plano.contrato = admmodels.Contrato.objects.all().order_by('id')[0]
                new_plano.pospago = True
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id=row[0]
                new_plano_internet.plano = new_plano 
                if 'k' in row[2].lower():
                    new_plano_internet.download = int(fnum(row[2]))
                elif 'm' in row[2].lower():
                    new_plano_internet.download = int(fnum(row[2])) * 1024
                else:
                    new_plano_internet.download = row[2]

                if 'k' in row[3].lower():
                    new_plano_internet.upload = int(fnum(row[3]))
                elif 'm' in row[3].lower():
                    new_plano_internet.upload = int(fnum(row[3])) * 1024
                else:
                    new_plano_internet.upload = row[3]
                new_plano_internet.diasparabloqueio = 15
                new_plano_internet.save() 

if args.nas:
    with open(args.nas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if nmodels.NAS.objects.filter(id=row[0]).count() == 0:
                print row
                new_nas = nmodels.NAS()
                new_nas.id=row[0]
                new_nas.shortname=row[2]
                new_nas.secret = row[3]
                new_nas.xuser= row[5]
                new_nas.xtype = 'mikrotik'
                new_nas.xpassword = row[6]
                new_nas.nasname= row[1]
                new_nas.save()


if args.clientesfix:
    with open(args.clientesfix, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            models.Pessoa.objects.filter(cliente__id=row[0]).update(nome=row[2])


if args.arquivos:
    with open(args.arquivos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(id=row[0])
            if cliente:
                if admmodels.ClienteDocumento.objects.filter(arquivo=row[2]).count() == 0:
                    try:
                        cliente = cliente[0]
                        print(cliente,row[2])
                        new_doc = admmodels.ClienteDocumento()
                        new_doc.cliente=cliente
                        new_doc.descricao=row[1][0:200]
                        new_doc.arquivo=row[2]
                        new_doc.usuario = usuario 
                        new_doc.data_cadastro=row[3]
                        new_doc.save()
                        new_doc.data_cadastro=row[3]
                        new_doc.save()
                    except:
                        pass

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
            endereco_inst['logradouro'] = '%s %s' %(row[12],row[13]) # tipo_insta,endereco_insta
            try:
                endereco_inst['numero'] = int(row[14])
                endereco_inst['complemento'] = None
            except:
                endereco_inst['numero'] = None
                endereco_inst['complemento'] = row[14]
            endereco_inst['bairro'] = row[15]
            endereco_inst['cidade'] = row[16]
            endereco_inst['uf'] = row[17]
            endereco_inst['cep'] = row[18]
            endereco_inst['pontoreferencia'] = row[19]
            endereco_cob = {} 
            endereco_cob['logradouro'] = '%s %s' %(row[12],row[13]) # tipo_insta,endereco_insta
            try:
                endereco_cob['numero'] = int(row[14])
                endereco_cob['complemento'] = None
            except:
                endereco_cob['numero'] = None
                endereco_cob['complemento'] = row[14]
            endereco_cob['bairro'] = row[15]
            endereco_cob['cidade'] = row[16]
            endereco_cob['uf'] = row[17]
            endereco_cob['cep'] = row[18]
            endereco_cob['pontoreferencia'] = row[19]

            celular = row[20] # celular
            telefonecom = row[21] # telefonecom
            telefone = ''   
            celularcom = ''
            email = row[22] # outro_email

            nomepai = row[23]
            nomemae = row[24]
            cli_obs = row[25]

            ativo = row[26]
            
            login = row[28]
            if not login:
                login = 'semlogin_%s' %idcontrato
            senha = row[29]
            if not senha:
                senha = login
            ip = row[30].replace('"','').strip()
            mac_dhcp = row[31]
            plano = admmodels.PlanoInternet.objects.get(id=row[32])
            portador = row[33]
            vencimento = row[34]
            respempresa = row[35]
            insc_municipal = row[36]
            data_cadastro = row[38]
            if not data_cadastro:
                data_cadastro = date.today().strftime('%Y-%m-%d')
            data_ativacao = row[38]
            #idservico = row[39]


            if row[40] and row[43] and row[44]:
                endereco_inst = {}
                endereco_inst['logradouro'] = row[40] # tipo_insta,endereco_insta
                try:
                    endereco_inst['numero'] = int(row[41]) # numero_insta
                except:
                    endereco_inst['numero'] = None 
                endereco_inst['complemento'] = row[42]
                endereco_inst['bairro'] = row[43]
                endereco_inst['cidade'] = row[44]
                endereco_inst['uf'] = row[45]
                endereco_inst['cep'] = row[46]
                endereco_inst['pontoreferencia'] = row[47]

            if row[48] and row[51] and row[52]:
                endereco_inst = {}
                endereco_inst['logradouro'] = row[48] # tipo_insta,endereco_insta
                try:
                    endereco_inst['numero'] = int(row[49]) # numero_insta
                except:
                    endereco_inst['numero'] = None 
                endereco_inst['complemento'] = row[50]
                endereco_inst['bairro'] = row[51]
                endereco_inst['cidade'] = row[52]
                endereco_inst['uf'] = row[53]
                endereco_inst['cep'] = row[54]
                endereco_inst['pontoreferencia'] = row[55]

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

            pop_nome = row[61]
            if admmodels.Pop.objects.filter(cidade=pop_nome).count() == 0:
                new_pop = admmodels.Pop()
                new_pop.cidade=pop_nome
                new_pop.uf='BA'
                new_pop.save()
                pop = new_pop
            else:
                pop = admmodels.Pop.objects.filter(cidade=pop_nome)[0]

            nas = nmodels.NAS.objects.all()[0]

            notafiscal = False

            con_obs=''
            mac = None
            conexao_tipo = 'ppp'

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            status = row[63] # 1,2,3,8

            if status == '3':
                status_cc = 4
                status_s = 4
                status_c = 4

            if status == '8':
                status_cc = 3
                status_s = 3
                status_c = 3

            permuta = False
            if status == '2':
                permuta = True
                isento = 100

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
                    
                    tp = 'f'
                    if len(fnum(cpfcnpj)) > 12:
                        tp = 'j'
                    

                    
                    if tp == 'f':
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
                    
                    if tp == 'J':
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
                new_cobranca.permuta = permuta
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
                if idcontrato:
                    if admmodels.ServicoInternet.objects.filter(id=idcontrato).count() > 0:
                        idcontrato = int(idcontrato) + 10000
                    new_servico.id=idcontrato
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


if args.gerencianet:
    with open(args.gerencianet, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[2]:
                titulo = fmodels.Titulo.objects.filter(cliente__id=row[0],
                                                       numero_documento__startswith=row[2],
                                                       data_vencimento=row[6],
                                                       titulogateway__isnull=True)
                #if portador:
                #    titulo = titulo.filter(portador=portador)
                if titulo:
                    print titulo
                    titulo  = titulo[0]
                    titulogateway = fmodels.TituloGateway()
                    titulogateway.titulo = titulo
                    titulogateway.gateway = titulo.portador.gateway_boleto
                    titulogateway.link = row[5]
                    titulogateway.idtransacao = row[4]
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
            new_pconta.descricao = 'ALTAREDE - %s' %row[1]
            new_pconta.codigo='02.09.%s' %str(pi).zfill(3)
            new_pconta.tipo = 'D'
            pi += 1
            new_pconta.save()


if args.fixfilial:
    pi = 1
    with open(args.fixfilial, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(id=row[0])
            clientecontrato = None
            filial = row[2]
            if cliente:
                cliente = cliente[0]
                clientecontrato = None
                if row[1] and row[3]:
                    clientecontrato = admmodels.ClienteContrato.objects.filter(id=row[1])
                    if clientecontrato:
                        clientecontrato = clientecontrato[0]
                        filial = row[3]

            if filial == '1':
                pop_id = 2 
            elif filial == '5':
                pop_id = 3
            elif filial == '7':
                pop_id = 4
            elif filial == '8':
                pop_id = 5
            elif filial == '9':
                pop_id = 6
            elif filial == '10':
                pop_id = 7
            elif filial == '11':
                pop_id = 8
            elif filial == '14':
                pop_id = 9

            if clientecontrato:
                admmodels.ClienteContrato.objects.filter(id=clientecontrato.id).update(pop_id=pop_id)
                print(clientecontrato,filial,pop_id)



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


if args.historico:
    with open(args.historico, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[2] in ['0000-00-00','']:
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


if args.onus:
    with open(args.onus, 'rb') as csvfile:
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


if args.anotacoes:
    with codecs.open(args.anotacoes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(id=row[0])
            if cliente:
                new_anotacao = admmodels.ClienteAnotacao()
                new_anotacao.cliente = cliente[0]
                new_anotacao.anotacao=row[1]
                new_anotacao.data_cadastro=cliente[0].data_cadastro
                new_anotacao.usuario=usuario
                new_anotacao.save()
                print(cliente[0],row[1])
                

#0f.id,
#1f.cnpj,
#2c.id,
#3c.cnpj_cpf,
#4v.id_contrato,
#5v.data_emissao,
#6v.data_saida,
#7v.data_cancelamento,
#8v.mot_cancelamento,
#9v.valor_total,
#10v.id_cfop,
#11v.serie,
#12v.serie_nf,
#13v.numero_nf,
#14v.modelo_nf,
#15v.infCpl,
#16v.nfe_chave,
#17r.id,
#18r.documento


if args.nf2122:
    with open(args.nf2122, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            empresa = admmodels.Empresa.objects.filter(cpfcnpj__numfilter=row[1])
            if empresa:
                empresa = empresa[0]
                # nota 
                v_nota = fismodels.NotaFiscal.objects.filter(empresa=empresa,numero=row[13])
                cfop = fismodels.CFOP.objects.get(cfop=row[10])
                if len(v_nota) == 0:

                    # cliente 
                    cliente = admmodels.Cliente.objects.filter(id=row[2],pessoa__cpfcnpj__numfilter=row[3])
                    if cliente:
                        cliente = cliente[0]
                    else:
                        cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=row[3])
                        if cliente:
                            cliente = cliente[0]
                    
                    if cliente:
                        endereco = cliente.endereco 
                        clientecontrato = cliente.clientecontrato_set.filter(id=row[4])
                        if clientecontrato:
                            endereco = clientecontrato[0].cobranca.endereco
                        nfdest = {}
                        nfdest['cliente'] = cliente
                        nfdest['cpfcnpj'] = cliente.getCPFCNPJ()
                        nfdest['inscricaoestadual'] = cliente.getInscricaoEstadual()
                        nfdest['razaosocial'] = cliente.getNome()
                        nfdest['logradouro'] = endereco.logradouro
                        nfdest['numero'] = endereco.numero
                        nfdest['complemento'] = endereco.complemento
                        nfdest['cep'] = endereco.cep
                        nfdest['bairro'] = endereco.bairro
                        nfdest['cidade'] = endereco.cidade
                        nfdest['uf'] = endereco.uf
                        nfdest['telefone'] = '84999999999'
                        nfdest['codigocliente'] = cliente.id
                        nfdest['tipoassinante'] = '1'
                        print(nfdest)
                        nfdest_obj = fismodels.NFDestinatario(**nfdest)
                        nfdest_obj.save()
                        nf = {}
                        nf['empresa'] = empresa
                        nf['destinatario'] = nfdest_obj
                        nf['data_emissao'] = row[5]
                        nf['data_saida'] = row[6]
                        nf['modelo'] = row[14]
                        nf['tipoutilizacao'] = '4'
                        nf['serie'] = row[11]
                        nf['numero']= row[13]
                        nf['valortotal'] = row[9]
                        nf['icms'] = '0.00'
                        nf['outrosvalores'] = row[9]
                        nf['djson'] = {}
                        if row[7]:
                            nf['status'] = fisconstants.NOTAFISCAL_CANCELADA
                            nf['djson']['motivocancela'] = row[8]
                            nf['data_cancela'] = row[7]
                        else:
                            nf['status'] = fisconstants.NOTAFISCAL_GERADA
                        nf['bcicms'] = '0.00'
                        nf['tipo_es'] = fisconstants.NOTAFISCAL_TIPO_SAIDA
                        nf['tipo_nf'] = fisconstants.NOTAFISCAL_SERVICO
                        nf['cfop'] = cfop
                        nf['usuario_g'] = usuario
                        nf['usuario_c'] = usuario
                        nf['djson']['idreceber'] = row[17]
                        nf['djson']['documento'] = row[18]
                        nf['djson']['contrato'] = row[4]
                        print(nf)
                        new_nf = fismodels.NotaFiscal(**nf)
                        new_nf.save()
                        new_nf.data_emissao=nf['data_emissao']
                        new_nf.data_saida=nf['data_saida']
                        new_nf.save()
                        nfitem = {}
                        nfitem['notafiscal'] = new_nf
                        nfitem['descricao'] = row[15]
                        nfitem['codigoservico'] = '010101'
                        nfitem['classificacao'] = '0104'
                        nfitem['unidade'] = '1'
                        nfitem['qt_contratada'] = '1'
                        nfitem['qt_fornecida'] = '1'
                        nfitem['valortotal'] = nf['valortotal']
                        nfitem['desconto'] = '0.00'
                        nfitem['acrescimo_despesa'] = '0.00'
                        nfitem['bcicms'] = '0.00'
                        nfitem['icms'] = '0.00'
                        nfitem['outrosvalores'] = nf['valortotal']
                        nfitem['aliquotaicms'] = '0.00'
                        nfitem['item'] = '1'
                        nfitem['data_cadastro'] = nf['data_emissao']
                        nfitem['data_alteracao'] = nf['data_emissao']
                        print(nfitem)
                        new_nfitem = fismodels.NotaFiscalItem(**nfitem)
                        new_nfitem.save()
                        new_nfitem.data_cadastro=nf['data_emissao']
                        new_nfitem.data_alteracao=nf['data_emissao']
                        new_nfitem.save()
                        if row[17]:
                            titulo = fmodels.Titulo.objects.filter(Q(cliente=cliente),
                                                                   Q(nosso_numero__endswith=row[17],valor=row[9]))
                            if len(titulo) == 1:
                                # Cria nota fiscal com titulo
                                nft = fismodels.NotaFiscalTitulo()
                                nft.titulo = titulo[0]
                                nft.notafiscal = new_nf
                                nft.save()

