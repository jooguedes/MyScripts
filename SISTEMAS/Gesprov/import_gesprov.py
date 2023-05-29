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
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--pop', dest='pop', type=int, help='POP para importar os clientes', required=False)


#python import_gesprov.py --settings=sgp.flexfibra.settings --planos=gesprov-planos.csv  --portadores=gesprov-portadores.csv --sync=1
#python import_gesprov.py --settings=sgp.flexfibra.settings --pop=1 --clientes=gesprov-clientes.csv --sync=1
#python import_gesprov.py --settings=sgp.flexfibra.settings --titulos=gesprov-titulos.csv --sync=1
#python import_gesprov.py --settings=sgp.flexfibra.settings --chamados=gesprov-titulos.csv --sync=1
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

from apps.admcore import models as admmodels
from apps.atendimento import models as amodels
from apps.financeiro import models as fmodels
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


if args.planos:
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(descricao=row[0]).count() == 0:
                print(row)
                new_plano = admmodels.Plano()
                new_plano.id = row[0]
                new_plano.descricao=row[1]
                new_plano.preco = row[4]
                new_plano.grupo = grupo_obj
                new_plano.contrato = contrato_obj
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
                    new_plano_internet.download = int(row[2])

                if 'k' in row[3].lower():
                    new_plano_internet.upload = int(fnum(row[3]))
                elif 'm' in row[3].lower():
                    new_plano_internet.upload = int(fnum(row[3])) * 1024
                else:
                    new_plano_internet.upload = int(row[3])
                new_plano_internet.diasparabloqueio = 15
                new_plano_internet.save() 


if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            codigo_banco = row[2]
            if not row[2]:
                codigo_banco = '999'
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print(row)
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
                if row[12].lower() in ['gerencianet','boletofacil','boleto_facil','fortunus','juno','widepay']:
                    new_gateway_pagamento = fmodels.GatewayPagamento()
                    new_gateway_pagamento.descricao = row[1]
                    new_gateway_pagamento.gerencia_boleto = True
                    if row[13]:
                        new_gateway_pagamento.token = row[13]
                    if row[14]:
                        new_gateway_pagamento.usuario = row[14]
                    if row[15]:
                        new_gateway_pagamento.senha = row[15]
                    if 'gerencianet' in row[12].lower():
                        new_gateway_pagamento.nome = 'gerencianetapi'
                    elif 'juno' in row[12].lower():
                        new_gateway_pagamento.nome =  'boletofacil'
                    else:
                        new_gateway_pagamento.nome =  row[12]
                    new_gateway_pagamento.save()
                    new_portador = fmodels.Portador.objects.get(id=row[0])
                    new_gateway_pagamento.portadores.add(new_portador)


if args.clientes:
    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    if args.portador_id:
        portador = fmodels.Portador.objects.get(pk=args.portador_id)
    ri = -1

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ri += 1
            idcliente = row[0]
            login=ustrl(row[1])
            #login=normalize('NFKD', login).encode('ASCII','ignore')

            #if ':' in login:
            #    continue

            #if not senha:
            #    senha = login

            #
            # Dados pessoais
            #
            tipo = ustr(row[2])
            nome = ustr(row[3])
            idcontrato = row[4]
            cpfcnpj = ustr(row[5])[:20]
            rgie = ustr(row[8])[:20]
            profissao = ustr(row[9])
            sexo = None
            data_nasc = None
            if row[11]:
                data_nasc = row[11]
            fantasia = row[12]

            #
            # Endereço
            #
            pontoreferencia = row[13]
            logradouro = ustr(row[14])
            numero = None
            try:
                numero = int(row[15])
            except:
                numero = None
                logradouro += ",%s" %row[15]
            complemento = ustr(row[16])
            bairro = ustr(row[17]).strip()[0:50]
            cep = ustr(row[18]).strip()[0:20]
            uf = ustr(row[19])
            cidade = ustr(row[20]).upper()[0:50]


            #
            # Contato
            #
            celular = ustr(row[21])
            telefonecom = ustr(row[22])
            email = ustrl(row[23])
            servico_obs=row[24]

            
            
            con_obs = ''
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS
            #

            data_cadastro = row[25].split(" ")[0]
            if not data_cadastro or data_cadastro=='':
                data_cadastro=datetime.now()
            

            #
            # Contrato
            #

            # Servico
            plano_id = row[28]

            #conexao_tipo = ustrl(row[30])
            conexao_tipo = 'ppp'
            if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
            if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'


            ip = ustr(row[31])
            if len(ip) < 7: ip = None

            mac = ustr(row[33])
            if len(mac) < 10: mac = None

            try:
                vencimento = int(row[34])
            except:
                vencimento = 10
                print 'erro row (%s) - %s' %(row[34],ri)

            comodato = ustrl(row[39]).lower()
            if comodato in ['Sim','sim']:
                comodato = True
            elif comodato in ['nao','não','N_o']:
                comodato = False

            isento = ustr(row[40])
            if isento in ['Sim','sim','true','1']:
                isento = 100
            else:
                isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            #status = ustrl(row[41])
            status = ustrl(row[42])

            if status in  ['2']:
                status_cc = 4
                status_s = 4
                status_c = 4
            if status in ['0']:
                status_cc = 3
                status_s = 3
                status_c = 3

            if row[43]:
                senha=row[43]
            else:
                senha='gesprovmigracao'

            try:
                plano_download = int(row[44])
            except:
                plano_download=0
            try:
                plano_upload = int(row[45])

            except:
                plano_upload=0
            plano_valor = row[46]
            portador_id = row[47]

            if not args.portador_id:
                portador = fmodels.Portador.objects.get(id=portador_id)

            telefone = row[48]

            s_logradouro = ustr(row[50])
            s_numero = None
            try:
                s_numero = int(row[51])
            except:
                s_numero = None
                s_logradouro += ",%s" %row[51]
            s_bairro = ustr(row[52]).strip()[0:50]
            s_cidade = ustr(row[53]).upper()[0:50]
            s_cep = ustr(row[54]).strip()[0:20]
            s_uf = ustr(row[55])
            s_complemento = ustr(row[56])

            nome_pai = row[57]
            nome_mae = row[58]
            s_pontoreferencia = row[59]
            cmun = row[60]
            s_cmun = row[61]
            login_central = row[62]
            senha_central = row[63]
            #idservico = row[64]
            map_ll = None
            if row[65] and row[66]:
                map_ll = '%s,%s' %(row[65],row[66])

            planointernet = admmodels.PlanoInternet.objects.get(plano__id=plano_id)

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
            #POP PARA IMPORTACAO DOS CLIENTES
            pop=admmodels.Pop.objects.get(id=args.pop)

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
            print nome_pai, nome_mae
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', planointernet
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
                print "Import %s" %nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)

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
                    new_endereco.cmun = cmun

                    new_endereco_inst = admmodels.Endereco()
                    new_endereco_inst.logradouro = s_logradouro
                    new_endereco_inst.numero = s_numero
                    new_endereco_inst.bairro = s_bairro
                    new_endereco_inst.cep = s_cep
                    new_endereco_inst.cidade = s_cidade
                    new_endereco_inst.uf = s_uf
                    new_endereco_inst.pais = 'BR'
                    new_endereco_inst.complemento = s_complemento
                    new_endereco_inst.pontoreferencia= s_pontoreferencia
                    new_endereco_inst.cmun = s_cmun
                    new_endereco_inst.map_ll = map_ll

                    new_endereco_cob = copy.copy(new_endereco_inst)
                    new_endereco.save()
                    new_endereco_cob.save()
                    new_endereco_inst.save()

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
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.nomepai = nome_pai
                        new_pessoa.nomemae = nome_mae
                        new_pessoa.rg = rgie
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor=''
                        new_pessoa.save()

                    if tp == 'j':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = nome

                        new_pessoa.nomefantasia = fantasia
                        new_pessoa.resempresa = ''
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = ''
                        new_pessoa.tipo = 8
                        new_pessoa.save()

                    # Cliente
                    try:
                        new_cliente = admmodels.Cliente()
                        new_cliente.id = idcliente
                        new_cliente.endereco = new_endereco
                        new_cliente.pessoa = new_pessoa
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.data_alteracao = data_cadastro
                        new_cliente.ativo = True
                        new_cliente.save()
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.save()
                    except:
                        data_cadastro=datetime.now()
                        data_cadastro=datetime.now()
                        new_cliente.data_cadastro= datetime.now()
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

                    new_cliente = cliente_check[0]


                contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato).first()
                if contrato_check:
                    new_contrato = contrato_check
                else:
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
                    new_contrato.data_alteracao = data_cadastro
                    new_contrato.save()
                    
                    for ic in [6,2,status_cc]:
                        new_status = admmodels.ClienteContratoStatus()
                        new_status.cliente_contrato = new_contrato
                        new_status.status = ic
                        new_status.modo=2
                        new_status.usuario = usuario
                        new_status.data_cadastro = data_cadastro
                        new_status.save()

                        new_status.data_cadastro = data_cadastro
                        new_status.save()

                    try:
                        new_clientecontrato_central = admmodels.ClienteContratoCentralAcesso()
                        new_clientecontrato_central.central_login = login_central
                        new_clientecontrato_central.central_password = senha_central
                        new_clientecontrato_central.cliente_contrato = new_contrato
                        new_clientecontrato_central.usuario_cadastro = usuario
                        new_clientecontrato_central.usuario_alteracao = usuario
                        new_clientecontrato_central.mudar_password = False

                        new_clientecontrato_central.save()
                    except:
                        new_clientecontrato_central.central_login = None
                        new_clientecontrato_central.central_password =None
                        new_clientecontrato_central.cliente_contrato = new_contrato
                        new_clientecontrato_central.usuario_cadastro = usuario
                        new_clientecontrato_central.usuario_alteracao = usuario
                        new_clientecontrato_central.mudar_password = False
                        new_clientecontrato_central.save()

                # Servico
                new_servico = admmodels.ServicoInternet()
                #new_servico.id = idservico
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() > 0:
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
                new_servico.save()

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
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            contrato = admmodels.ClienteContrato.objects.filter(cliente__pessoa__cpfcnpj__numfilter=row[5]).first()
            if contrato:
                cliente = contrato.cliente
                cobranca = contrato.cobranca
                print(contrato)
                portador = fmodels.Portador.objects.filter(id=row[1]).first()
                if not portador:
                    print('nao achei portador', row[1])
                    continue 
                #print(row)
                nosso_numero=row[3]
                if nosso_numero=='':
                    continue
                print('filtrando', row[3])
                if portador.titulo_set.filter(nosso_numero=nosso_numero).count() == 0:
                    tdata = {} 
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['numero_documento'] = row[2]
                    tdata['nosso_numero'] = row[3]
                    tdata['parcela'] = row[4] or 1
                    tdata['portador'] = portador
                    tdata['demonstrativo'] = row[7] or 'FATURA %s' %row[2]
                    tdata['valor'] = row[8]
                    tdata['valorpago'] = row[9]
                    tdata['data_documento'] = row[10].split(' ')[0]
                    tdata['data_vencimento'] = row[11].split(' ')[0]
                    tdata['data_pagamento'] = row[12].split(' ')[0]
                    tdata['data_baixa'] = row[13].split(' ')[0]
                    tdata['data_cancela'] = row[14].split(' ')[0]
                    tdata['motivocancela'] = row[15]
                    tdata['usuario_g'] = usuario
                    tdata['usuario_c'] = usuario
                    tdata['usuario_b'] = usuario
                    tdata['linha_digitavel'] = row[16]
                    tdata['codigo_barras'] = row[17]
                    tdata['centrodecusto'] = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
                    tdata['status'] = fmodels.MOVIMENTACAO_GERADA
                    tdata['modogeracao'] = 'a'

                    if tdata['valorpago'] == '0' or tdata['valorpago'] == '' or tdata['valorpago'] == '0.00':
                        tdata['valorpago'] = None

                    if tdata['data_cancela']:
                        tdata['usuario_b'] = None
                        tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA

                    if tdata['data_pagamento']:
                        tdata['usuario_c'] = None
                        tdata['status'] = fmodels.MOVIMENTACAO_PAGA


                    for k in tdata:
                        if tdata[k] in ['NULL','0000-00-00','']:
                            tdata[k] = None

                    tdata['djson'] = {'g_idtransacao': row[20],
                                      'g_link': row[21]}
                    print(tdata)
                    new_titulo = fmodels.Titulo(**tdata)
                    new_titulo.save()
                    new_titulo.data_documento = tdata['data_documento']
                    new_titulo.save()

                    if new_titulo.portador.gateway_boleto:
                        titulogateway = fmodels.TituloGateway()
                        titulogateway.titulo = new_titulo
                        titulogateway.gateway = new_titulo.portador.gateway_boleto
                        titulogateway.idtransacao = row[20]
                        titulogateway.link = row[21]
                        titulogateway.save()
                    else:
                        print('Não há gateway de boletos')


if args.chamados:
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.chamados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(
                    cliente__id=row[1])
                if clientecontrato and amodels.Ocorrencia.objects.filter(numero=row[0]).count()==0:
                    print(row)
                    ocorrencia = {}
                    ocorrencia['id'] = int(row[0])
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                    ocorrencia['tipo'] = amodels.Tipo.objects.get(id=5)
                 
                    ocorrencia['usuario'] = usuario
                    ocorrencia['metodo'] = metodo
                    ocorrencia['numero'] = row[0]
                    if row[4]=='':
                        ocorrencia['status']=amodels.OCORRENCIA_ABERTA
                    else:
                        ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA 
                    

                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['data_cadastro'] = row[3].split(' ')[0]
                    try:
                        ocorrencia['data_agendamento'] = row[4].split(' ')[0]
                        ocorrencia['data_finalizacao'] = row[4].split(' ')[0]
                    except:
                        ocorrencia['data_agendamento'] = None
                        ocorrencia['data_finalizacao'] = None

                    ocorrencia['conteudo'] = 'Aberto pelo usuario: '+ str(row[8]) + "\n"+ str(row[6])+ "\n" + "Fechado encerrada pelo usuario: " + str(row[9]) 
                   
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()
                    new_ocorrencia.data_cadastro = row[3].split(' ')[0]
                    try:
                        new_ocorrencia.data_agendamento = row[4].split(' ')[0]
                        new_ocorrencia.data_finalizacao = row[4].split(' ')[0]
                    except:
                        new_ocorrencia.data_agendamento = None
                        new_ocorrencia.data_finalizacao = None

                    if new_ocorrencia.data_agendamento == '':
                        new_ocorrencia.data_agendamento = None
                    if new_ocorrencia.data_finalizacao == '':
                        new_ocorrencia.data_finalizacao = None
                    new_ocorrencia.save()
                    
                    ocorrencia=amodels.Ocorrencia.objects.get(numero=row[0])
                    new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                    new_ocorrencia_anotacao.ocorrencia= ocorrencia
                    new_ocorrencia_anotacao.anotacao=row[7]
                    new_ocorrencia_anotacao.usuario= usuario
                    new_ocorrencia_anotacao.save()

                    
                else:
                    print('Ocorrencia já importada')
            except Exception as e:
                print(e)
