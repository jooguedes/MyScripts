#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from itertools import count
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv
import re


parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--id_nas', dest='nas_id', type=int, help='Arquivo de Importacao',required=False)
parser.add_argument('--id_portador', dest='portador_id', type=int, help='Arquivo de Importacao',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Arquivo de Importacao',required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Arquivo de importacao',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamadoassuntos', dest='chamadoassuntos', type=str, help='Arquivo de importacao',required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='Arquivo de importacao',required=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
args = parser.parse_args()

#   python import_quazar.py --settings=sgp.local.settings --nas=quazar-nas.csv
#   python import_quazar.py --settings=sgp.local.settings --portadores=quazar-portadores.csv
#   python import_quazar.py --settings=sgp.local.settings --id_nas=1 --id_portador=1 --clientes=quazar-clientes.csv --planoadd=1 --vencimentoadd=1 --sync=1
#   python import_quazar.py --settings=sgp.local.settings --chamadoassuntos=quazar-chamadoassuntos.csv
#   python import_quazar.py --settings=sgp.local.settings --chamados=quazar-chamados.csv





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

fnum = lambda n: re.sub('[^0-9.]','',n) 
fnum2 = lambda n: re.sub('[^0-9]','',n) 


usuario = admmodels.User.objects.get(username='sgp')


if args.nas:
    with open(args.nas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if nmodels.NAS.objects.filter(id=row[0]).count() == 0:
                print row
                new_nas = nmodels.NAS()
                new_nas.id=row[0]
                new_nas.shortname=row[1]
                new_nas.secret = row[4]
                new_nas.xuser= row[3]
                new_nas.xtype = row[5]
                new_nas.xpassword = row[4]
                new_nas.nasname= row[2]
                new_nas.save()


if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            codigo_banco = '999'
            if row[2] in ['Banco Santander', 'Santander']:
                codigo_banco = '033'
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print row
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[1]
                new_portador.codigo_banco = codigo_banco
                new_portador.agencia = row[7] or '0'
                new_portador.agencia_dv = row[8]
                new_portador.conta = row[9] or '0'
                new_portador.conta_dv = row[10]
                new_portador.convenio = row[5]
                new_portador.carteira = row[11]
                new_portador.cedente= row[4] or 'Provedor X'
                new_portador.cpfcnpj = row[3] or '0'
                new_portador.save()

            if fmodels.GatewayPagamento.objects.filter(portadores__id=row[0]).count() == 0:
                if row[12] in ['1']:
                    new_gateway_pagamento = fmodels.GatewayPagamento()
                    new_gateway_pagamento.descricao = row[1]
                    new_gateway_pagamento.gerencia_boleto = True
                    if row[13]:
                        new_gateway_pagamento.token = row[13]
                    if row[14]:
                        new_gateway_pagamento.usuario = row[14]
                    if row[15]:
                        new_gateway_pagamento.senha = row[15]
                    if row[2] in ['Fortunus']:
                        new_gateway_pagamento.nome = 'gerencianet'
                    elif row[2] in ['Gerencianet']:
                        new_gateway_pagamento.nome = 'gerencianetapi'
                    elif row[2] in ['boleto_facil']:
                        new_gateway_pagamento.nome =  'boletofacil'
                    else:
                        new_gateway_pagamento.nome =  row[2]
                    new_gateway_pagamento.save()
                    new_portador = fmodels.Portador.objects.get(id=row[0])
                    new_gateway_pagamento.portadores.add(new_portador)


if args.clientes:
    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='cabo').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='cabo').order_by('-id')[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
    ri = -1

    incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 10000
    if incrementar < 10000:
        incrementar = 10000
    else:
        incrementar += 1

    m = manage.Manage()
    count=0
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            count=count+1
            ri += 1
            idcliente = int(fnum(row[0]))
            idcontrato = int(fnum(row[35]))
            login=row[26]
            if not login or login=='':
                login=str(idcontrato)+'sem_login'
                                                                                                                    
            ######################################################## Dados pessoais ###################################################
                                                                                                                                
            nome = row[2].upper().strip()
            cpfcnpj = row[4].lower().strip()
            rgie = row[7]
            data_nasc=None
            profissao = row[9]
            tipo = row[1].upper().strip()
            sexo= row[9]
            if (row[9] != 'M' or row[9] !='F'):
                if(row[9] == 'Feminino'):
                    sexo = 'F'
                elif row[9] == 'Masculino':
                    sexo = 'M'
            else:
                sexo = row[9]
                data_nasc = None
            try:
                y_,m_,d_ = row[10].strip().split('-')
                if len(y_) == 2:
                    y_ = '19%s' %y_

                date(int(y_),int(m_),int(d_))
                data_nasc='%s-%s-%s' %(y_,m_,d_)
            except:
                pass
            
            logradouro = row[13]
            numero = None
            try:
                numero = int(row[14])
            except:
                numero = None
                logradouro += ",%s" %row[14]
            complemento = row[15] or None
            bairro = row[16].strip()[0:50]
            cep = row[17].strip()[0:20]
            uf = row[18]
            cidade =unicode(str(row[19].upper()[0:50]))
                                                                                                         
            ######################################### Contato ###############################################
                                                                                                          
            celular =row[20]
            telefonecom = row[21]
            email = row[22]

                                                                                                
            # ####################################################DATAS##############################################
                                                                                                                 
            data_cadastro = datetime.now()

            try:
                y_,m_,d_= row[33].strip().split('/')
                if len(y_) == 2:
                    y_ = '20%s' %y_
                date(int(y_),int(m_),int(d_))
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass
                                                                                                                  
            ########################################################Contrato########################################
                                                                                                                 

            # Servico
            plano = row[30].strip()
            #plano_valor = str(row[29]).strip()

            conexao_tipo = row[29]
            conexao_tipo = 'indefinida'
            if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
            if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'
            ip = row[28]
            if len(ip) < 7: ip = None

            mac = row[29]
            if len(mac) < 10: mac = None

            try:
                vencimento = int(row[32])
            except:
                vencimento = 10
                print 'erro row (%s) - %s' %(row[32],ri)
            #=======parte do contrato finalizada========#


            # status 3 == cancelado
            # status 4 == suspenso
            # status 1 == ativo

            status_cc = 1
            status_s = 1
            status_c = 1

            status =int(row[36].strip())
            #status_bloqueado = row[42]

            if(status):
                if(status==1):
                    status_cc = 1
                    status_s = 1
                    status_c = 1

                if (status ==2 or status==3):
                    status_cc = 4
                    status_s = 4
                    status_c = 4

                if (status==4):
                    status_cc = 3
                    status_s = 3
                    status_c = 3
            else:
                print('não existe status')
                continue
            
            if row[27]:
                senha=row[27]
            else:
                senha='quazar2sgp'

            plano_download = 0
            plano_upload = 0
            plano_valor = row[31]

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                if args.planoadd:
                    print(plano,plano_download,plano_upload,plano_valor)
                    new_plano = admmodels.Plano()
                    new_plano.descricao=plano
                    new_plano.preco = plano_valor
                    new_plano.contrato = contrato_obj
                    new_plano.grupo = grupo_obj
                    new_plano.save()

                    new_plano_internet = admmodels.PlanoInternet()
                    new_plano_internet.plano = new_plano
                    new_plano_internet.download = plano_download
                    new_plano_internet.upload = plano_upload
                    new_plano_internet.save()
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                    print('criado plano %s' %plano)
                else:
                    raise Exception('Não localizei plano %s' %plano)

            cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore')
            pop=admmodels.Pop.objects.get(id=1)
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=uf
                new_pop.save()
                pop = new_pop

            nas = nas_default

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save()

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefonecom,celular,email
            print login,senha,ip,mac
            print '####################################################'


            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
                print "Import %s" %nome

                cliente_check = admmodels.Cliente.objects.filter(id=idcontrato)

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
                    new_endereco.pontoreferencia=''

                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco.save()
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    tp = 'f'
                    if len(fnum2(cpfcnpj.strip())) > 12:
                        tp = 'j'

                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'

                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
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

                    if tp == 'j':
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
                    new_cliente.id = idcontrato
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
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
                    print("entrei no else do cliente check")
                    new_endereco = cliente_check[0].endereco

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
                #new_cobranca.isento = isento
                new_cobranca.notafiscal = False
                new_cobranca.data_cadastro = data_cadastro
                new_cobranca.datacobranca1 = data_cadastro
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = status_c
                new_cobranca.save()
                contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
                
                # Contrato
                new_contrato = admmodels.ClienteContrato()

                if len(contrato_check) == 0:
                    new_contrato.id = idcontrato
                else:
                    new_contrato.id = incrementar
                    incrementar += 1

                new_contrato.cliente = new_cliente
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca

                new_contrato.data_inicio = data_cadastro
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

                # Servico
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login__trim=login).count() > 0:
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
                new_servico.modoaquisicao =0
                new_servico.data_cadastro=data_cadastro
                #new_servico.observacao=servico_obs
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)

                #if login != login_pai:
                    #servico_pai = admmodels.ServicoInternet.objects.filter(login=login_pai)
                    #if servico_pai:
                        #new_cobranca.cobranca_unificada=servico_pai[0].clientecontrato.cobranca
                        #new_cobranca.save()

if args.chamadoassuntos:
    with open(args.chamadoassuntos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')

        for row in conteudo:
            # Incrementado em 500 para não sobrescrever os Tipos e Motivos padrões do próprio SGP
            if row[0] != '' and row[1] != '' and row[2] != '':
                dados = {}
                dados['id'] = int(row[0])+500
                dados['codigo'] = int(row[1])+500
                dados['descricao'] = row[2]
                try:
                    new_tipo = amodels.Tipo(**dados)
                    new_tipo.save()

                    new_motivoos = amodels.MotivoOS(**dados)
                    new_motivoos.id= None
                    new_motivoos.save()
                except:
                    continue


if args.chamados:
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.chamados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                idContrato = row[2]
                clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=idContrato)
                if clientecontrato:
                    print(row)
                    ocorrencia = {} 
                    ocorrencia['id'] = int(fnum(row[0]))
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                    try:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(id=int(row[3])+500)
                    except:
                        ocorrencia['tipo'] = amodels.Tipo.objects.get(id=1)
                    ocorrencia['usuario'] = usuario
                    ocorrencia['metodo'] = metodo
                    ocorrencia['numero'] = row[4]
                    if row[5] != '':
                        ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA
                    else:
                        ocorrencia['status'] = amodels.OCORRENCIA_ABERTA
                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['data_cadastro'] = row[6]
                    ocorrencia['data_agendamento'] = row[7]
                    ocorrencia['data_finalizacao'] = row[5]
                    ocorrencia['conteudo'] = row[8]
                    for ok in ocorrencia:
                        if ocorrencia[ok] == '0000-00-00 00:00:00':
                            ocorrencia[ok] = None
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()
                    new_ocorrencia.data_cadastro = row[6]
                    new_ocorrencia.data_agendamento = row[7]
                    new_ocorrencia.data_finalizacao = row[5]
                    if new_ocorrencia.data_agendamento == '0000-00-00 00:00:00':
                        new_ocorrencia.data_agendamento = None
                    if new_ocorrencia.data_finalizacao == '0000-00-00 00:00:00':
                        new_ocorrencia.data_finalizacao = None
                    new_ocorrencia.save()
        
                    ordem = {}
                    ordem['id'] = int(row[0])
                    ordem['ocorrencia'] = amodels.Ocorrencia.objects.get(id=int(row[0]))
                    ordem['status'] = amodels.OS_ENCERRADA if row[5] != '' else amodels.OS_ABERTA
                    ordem['usuario'] = usuario
                    ordem['setor'] = ocorrencia['setor']
                    try:
                        ordem['motivoos'] = amodels.MotivoOS.objects.get(codigo=int(row[3])+500)
                    except:
                        ordem['motivoos'] = amodels.MotivoOS.objects.get(codigo=40)
                    ordem['data_cadastro'] = ocorrencia['data_cadastro']
                    ordem['data_agendamento'] = ocorrencia['data_agendamento']
                    ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                    ordem['conteudo'] = ocorrencia['conteudo']
                    ordem['observacao'] = row[9]
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
