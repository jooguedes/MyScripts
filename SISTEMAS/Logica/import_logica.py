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
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--tiposchamados', dest='tiposchamados', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--setores', dest='setores', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--gerencianet', dest='gerencianet',type=str,required=False)
parser.add_argument('--pop', dest='pop', type=int, help='ID do NAS',required=False)

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
fnum = lambda n: re.sub('[^0-9]','',n) 

usuario = admmodels.User.objects.get(username='sgp')


#python import_logica.py --settings=sgp.fillnet.settings --portador=2 --nas=1 --pop=1 --clientes=Conv-logica-clientes.csv --sync=1
#python import_logica.py --settings=sgp.fillnet.settings --portadores= --sync=1
# python import_logica.py --settings=sgp.fillnet.settings --titulos= --portador= --sync=1
# python import_logica.py --settings=sgp.fillnet.settings --tiposchamados=Conv-logica-chamados-tipos.csv --sync=1
# python import_logica.py --settings=sgp.fillnet.settings --setores=Conv-logica-chamados-setor.csv --sync=1
# python import_logica.py --settings=sgp.fillnet.settings --chamados=Conv-logica-chamados-setor.csv --sync=1
if args.setores:
    with open(args.setores,'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            new_setor = admmodels.Setor()
            new_setor.id = row[0]
            new_setor.nome = row[1]
            new_setor.save()


if args.tiposchamados:
    with open(args.tiposchamados,'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            
            try:
                new_motivo = amodels.MotivoOS()
                new_motivo.id = int(row[0])
                new_motivo.codigo = row[0]
                new_motivo.descricao = row[1]
                new_motivo.save()
            except Exception as e:
                print(e)

            try:
                new_tipo = amodels.Tipo()
                new_tipo.id = int(row[0])
                new_tipo.codigo = row[0]
                new_tipo.descricao = row[1]
                new_tipo.save()
            except Exception as e:
                print(e) 

if args.chamados:
    with open(args.chamados,'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row
            contrato = row[2]
            clientecontrato_object = admmodels.ClienteContrato.objects.filter(id=contrato)
            print(clientecontrato_object)

            if clientecontrato_object:
                clientecontrato_object = clientecontrato_object[0]
            else:
                continue

            numero_chamado = row[3]
            setor = row[4]
            setor_obj = None
            if setor:
                setor_obj = admmodels.Setor.objects.filter(id=setor)
                if setor_obj:
                    setor_obj = setor_obj[0]
                else:
                    setor_obj = None 

            tipochamado = row[5]
            motivoos_obj = amodels.MotivoOS.objects.filter(codigo=100)
            print(motivoos_obj)

            if motivoos_obj:
                motivoos_obj = motivoos_obj[0]
            else:
                continue

            tipo_obj = amodels.Tipo.objects.filter(id=tipochamado)
            if tipo_obj:
                tipo_obj = tipo_obj[0]

            data_chamado = row[7]
            data_finalizacao = row[8]
            if not data_finalizacao:
                data_finalizacao = None
            data_agendamento = row[9]
            if not data_agendamento:
                data_agendamento = None
            prioridade = row[10]
            
            conteudo = row[15]
            observacao = row[16]

            # 
            ocorrencia = amodels.Ocorrencia()
            ocorrencia.numero = numero_chamado
            ocorrencia.setor = setor_obj
            ocorrencia.clientecontrato = clientecontrato_object
            ocorrencia.data_cadastro=data_chamado
            ocorrencia.data_alteracao=data_chamado
            ocorrencia.data_agendamento = data_agendamento
            ocorrencia.data_finalizacao = data_finalizacao
            ocorrencia.usuario = usuario
            ocorrencia.tipo = tipo_obj
            ocorrencia.conteudo = conteudo
            ocorrencia.metodo = amodels.Metodo.objects.get(
                codigo=1)  # telefone
            if data_finalizacao:
                ocorrencia.status = amodels.OCORRENCIA_ENCERRADA
            else:
                ocorrencia.status = amodels.OCORRENCIA_ABERTA
            ocorrencia.save()

            ocorrencia.data_cadastro=data_chamado
            ocorrencia.data_alteracao=data_chamado
            ocorrencia.data_agendamento = data_agendamento
            ocorrencia.data_finalizacao = data_finalizacao

            ocorrencia.save()

            os = amodels.OS()
            if data_finalizacao:
                os.status = amodels.OS_ENCERRADA
            else:
                os.status = amodels.OS_ABERTA
            os.ocorrencia = ocorrencia
            os.usuario = usuario
            os.conteudo = conteudo
            os.observacao = observacao
            os.data_cadastro=data_chamado
            os.data_alteracao=data_chamado
            os_data_finalizacao = data_finalizacao
            os.data_agendamento = data_agendamento
            os.tipoos = amodels.TIPO_OS_EXTERNA
            os.motivoos = motivoos_obj
            os.save()
            os.data_cadastro=data_chamado
            os.data_alteracao=data_chamado
            os_data_finalizacao = data_finalizacao
            os.data_agendamento = data_agendamento
            os.save()




if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if row[2]:
                if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                    print row
                    new_portador = fmodels.Portador()
                    new_portador.id = row[0]
                    new_portador.descricao = 'Banco ID %s' %(row[1])
                    new_portador.cedente = 'PROVEDOR X'
                    new_portador.codigo_banco = row[1]
                    new_portador.agencia = row[2]
                    new_portador.agencia_dv = row[3]
                    new_portador.conta = row[4]
                    new_portador.conta_dv = row[5]
                    new_portador.convenio = row[6]
                    new_portador.carteira = row[7]
                    new_portador.multa = row[9]
                    new_portador.juros = row[10]
                    new_portador.taxa_boleto = row[11]
                    new_portador.inicio_nosso_numero=row[12]
                    new_portador.cedente='PROVEDOR X'
                    new_portador.cpfcnpj = '0'
                    new_portador.save()


if args.clientes:

    formacobranca = fmodels.FormaCobranca.objects.all()[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)

    ri = -1
    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ri += 1
            # IDs 
            idcliente = row[0]
            idcontrato = row[1]
            # Dados Cliente
            tipo = row[2]
            nome = row[3]
            cpfcnpj = row[4]
            rgie = row[5]
            profissao = '' #row[6]
            sexo = row[7]
            data_nasc = row[8]


            # Endereco
            logradouro = ustr(row[9])
            numero = None
            try:
                numero = int(row[10])
            except:
                numero = None
                logradouro += ",%s" %row[10]
            complemento = ustr(row[11])
            bairro = ustr(row[12]).strip()[0:50]
            cep = ustr(row[13]).strip()[0:20]
            cidade = ustr(row[14]).upper()[0:50]
            uf = ustr(row[15])

            contrato_logradouro = ustr(row[16])
            contrato_numero = None
            try:
                contrato_numero = int(row[17])
            except:
                contrato_numero = None
                contrato_logradouro += ",%s" %row[17]
            contrato_complemento = ustr(row[18])
            contrato_bairro = ustr(row[19]).strip()[0:50]
            contrato_cep = ustr(row[20]).strip()[0:20]
            contrato_cidade = ustr(row[21]).upper()[0:50]
            contrato_uf = ustr(row[22])


            #
            # Contato
            #
            celulares = row[23].strip().split('|')
            telefones = row[24].strip().split('|')

            email = ustrl(row[25])
            servico_obs=row[26]

            
            con_obs = ''


            data_cadastro = row[27]
            if data_cadastro=='' or not data_cadastro:
                data_cadastro=datetime.now()


            # 
            # Contrato
            # 
            login = row[30].strip()
            login = normalize('NFKD', unicode(login)).encode('ASCII','ignore')
            senha = row[31]

            # Servico
            plano = '%s' %row[32].strip()
            plano_valor = str(row[33]).strip().replace(',','.')
            try:
                plano_download = int(row[34])
                plano_upload = int(row[35])
            except:
                plano_download = 0
                plano_upload = 0
            conexao_tipo = ustrl(row[36])
            conexao_tipo = 'ppp'
            if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
            if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'


            ip = ustr(row[37])
            if len(ip) < 7: ip = None

            mac = ustr(row[38])
            if len(mac) < 10: mac = None
            
            try:
                vencimento = int(row[39])
            except:
                vencimento = 10
                print 'erro row (%s) - %s' %(row[39],ri)

            comodato = False
            isento = 0


            status_cc = 1
            status_s = 1
            status_c = 1

            status = ustrl(row[40])
            status_bloqueado = ustrl(row[41])

            data_status0 = row[42]
            data_status1 =  row[43]
            data_status2 = row[45]


            senha_central = row[46]

            pontoreferencia = row[47]
            contrato_pontoreferencia = row[48]

            if status == 'ativo':
                status_cc = 1
                status_s = 1
                status_c = 1

                if status_bloqueado == 'suspenso':
                    status_cc = 4
                    status_s = 4
                    status_c = 4

                    data_status2 = row[45]


            if status == 'cancelado':
                status_cc = 3
                status_s = 3
                status_c = 3

                if row[45]:
                    data_status2 = row[44]

            data_status_historico = [6,2,status_cc]

            if status in ['cancelado','suspenso']:
                data_status_historico = [6,2,1,status_cc]


            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                new_plano = admmodels.Plano()
                new_plano.descricao=plano
                new_plano.preco = plano_valor
                new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='fibra')
                new_plano.grupo = admmodels.Grupo.objects.get(nome='fibra')
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano 
                new_plano_internet.download = plano_download
                new_plano_internet.upload = plano_upload
                new_plano_internet.save() 
                print('criado plano %s' %plano)
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]

            '''cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=uf
                new_pop.save()
                pop = new_pop'''
            pop= admmodels.Pop.objects.get(id=args.pop)
            nas = nas_default

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print('corrigindo vencimento %s' %vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 

            #print pop
            #print row

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefones,celulares,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower__unaccent=login).count() == 0:
                print "Import %s" %nome
                # Save Models 

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)
        

                new_endereco = admmodels.Endereco()
                new_endereco.logradouro = logradouro
                new_endereco.numero = numero
                new_endereco.bairro = bairro
                new_endereco.cep = cep
                new_endereco.cidade = cidade
                new_endereco.uf = uf 
                new_endereco.pais = 'BR'
                new_endereco.complemento = complemento
                new_endereco.pontoreferencia=pontoreferencia

                if len(cliente_check) == 0:

                    # Endereco 
                    new_endereco = admmodels.Endereco()
                    new_endereco.logradouro = logradouro
                    new_endereco.numero = numero
                    new_endereco.bairro = bairro
                    new_endereco.cep = cep
                    new_endereco.cidade = cidade
                    new_endereco.uf = uf 
                    new_endereco.pais = 'BR'
                    new_endereco.complemento = complemento
                    new_endereco.pontoreferencia=pontoreferencia

                    new_endereco_inst = admmodels.Endereco()
                    new_endereco_inst.logradouro = contrato_logradouro
                    new_endereco_inst.numero = contrato_numero
                    new_endereco_inst.bairro = contrato_bairro
                    new_endereco_inst.cep = contrato_cep
                    new_endereco_inst.cidade = contrato_cidade
                    new_endereco_inst.uf = contrato_uf 
                    new_endereco_inst.pais = 'BR'
                    new_endereco_inst.complemento = contrato_complemento
                    new_endereco_inst.pontoreferencia=contrato_pontoreferencia

                    new_endereco_cob = copy.copy(new_endereco_inst)

                    new_endereco.save() 
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    
                    

                    
                   
                    if tipo == 'PF':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'
                        
                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.profissao = profissao
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg = rgie
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor=''
                        try:
                            new_pessoa.save()
                        except:
                            try:
                                new_pessoa.datanasc='19%s' %data_nasc[-8:]
                                new_pessoa.save()
                            except:
                                new_pessoa.datanasc=None 
                                new_pessoa.save()
                    
                    if tipo == 'PJ':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = nome
                        
                        new_pessoa.nomefantasia = nome
                        new_pessoa.resempresa = ''
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = ''
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
                    try:
                        new_cliente.save()
                    except:
                        new_cliente.data_cadastro = datetime.now()
                        new_cliente.data_alteracao = datetime.now()
                        new_cliente.save()
                    try:
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.save()
                    except:
                        new_cliente.data_cadastro = datetime.now()
                        new_cliente.data_alteracao = datetime.now()
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
                    
                    for cel in celulares:
                        if len(cel) > 4:
                            new_contato = admmodels.Contato()  
                            new_contato.tipo = 'CELULAR_PESSOAL'
                            new_contato.contato = cel 
                            new_contato.observacao = ''
                            new_contato.save() 
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()
                    
                    for tel in telefones:
                        if len(tel) > 4:
                            new_contato = admmodels.Contato() 
                            new_contato.tipo = 'TELEFONE_FIXO_COMERCIAL'
                            new_contato.contato = tel 
                            new_contato.save() 
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()

                else:

                    new_endereco_inst = admmodels.Endereco()
                    new_endereco_inst.logradouro = contrato_logradouro
                    new_endereco_inst.numero = contrato_numero
                    new_endereco_inst.bairro = contrato_bairro
                    new_endereco_inst.cep = contrato_cep
                    new_endereco_inst.cidade = contrato_cidade
                    new_endereco_inst.uf = contrato_uf 
                    new_endereco_inst.pais = 'BR'
                    new_endereco_inst.complemento = contrato_complemento
                    new_endereco_inst.pontoreferencia=''

                    new_endereco_cob = copy.copy(new_endereco_inst)
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_cob.id = None 
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco_inst.id = None 
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    
                    new_cliente = cliente_check[0]

                
                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob
                new_cobranca.portador = portador
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
                
                contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
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
                
                for ic in data_status_historico:
                    data_status = data_status0
                    if ic in [6,2]:
                        data_status = data_status0
                    elif ic == 1:
                        data_status = data_status1 or data_status0
                    elif ic in [3,4]:
                        data_status = data_status2 or data_status0

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
                    login += str(new_contrato.id)+'duplicado'
                new_servico.login= login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password=senha 
                new_servico.login_password_plain=senha
                new_servico.central_password=senha_central
                if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                    new_servico.mac_dhcp = mac
                    new_servico.mac = mac

                if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                    new_servico.ip = ip 
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.data_cadastro=data_cadastro
                new_servico.observacao=servico_obs
                try:
                    new_servico.save()
                except:
                    continue

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)

        
    from apps.admcore import models as admmodels 
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)



if args.titulos:
    portador = fmodels.Portador.objects.get(id=args.portador_id)
    with open(args.titulos, 'rb') as csvfile:       
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            contrato = admmodels.ClienteContrato.objects.filter(id=row[2])
            if contrato:
                contrato = contrato[0]
                cliente = contrato.cliente
                cobranca = contrato.cobranca

                if fmodels.Titulo.objects.filter(nosso_numero=row[8],portador=portador).count() == 0:
                    print row
                    tdata = {} 
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[8] # nrboleto
                    tdata['numero_documento'] = row[8] # documento
                    tdata['parcela'] = 1
                    tdata['portador'] = portador
                    tdata['valor'] = row[7]
                    tdata['observacao'] = row[8]
                    tdata['demonstrativo'] = row[8]
                    tdata['valorpago'] = row[6]
                    tdata['data_baixa'] = row[5]
                    tdata['data_pagamento'] = row[5]
                    tdata['data_documento'] = date.today()
                    tdata['data_vencimento'] = row[4] # vencimento
                    tdata['data_cancela'] = ''
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

                    if row[10] in ['5','6','10','11','14','15','19','20']:
                        tdata['usuario_c'] = usuario
                        tdata['data_cancela'] = tdata['data_vencimento']


                    if tdata['data_baixa']:
                        tdata['status'] = fmodels.MOVIMENTACAO_PAGA
                    elif tdata['data_cancela']:
                        tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA
                    else:
                        tdata['status'] = fmodels.MOVIMENTACAO_GERADA
                    tdata['demonstrativo'] = row[11]

                    tdata['observacao'] = 'status=%s' %row[10]
                    print tdata
                    if args.sync_db:                        
                        new_titulo = fmodels.Titulo(**tdata)
                        new_titulo.save()
                        new_titulo.data_documento = tdata['data_documento']
                        new_titulo.save()

                        try:
                            new_titulo.updateDadosFormatados()
                        except:
                            pass


if args.gerencianet:
    with open(args.gerencianet,'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for r in conteudo:
            titulos = fmodels.Titulo.objects.filter(numero_documento=r[0],titulogateway__isnull=True)
            for t in titulos:
                print(t,r[0],r[1])
                if t.portador.gateway_boleto:
                    print(t)
                    ntg = fmodels.TituloGateway()
                    ntg.gateway=t.portador.gateway_boleto
                    ntg.titulo=t
                    ntg.idtransacao=r[1]
                    ntg.save()
                    print(ntg)



