#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import codecs
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--msg_chamados', dest='msg_chamados', type=str, help='Arquivo importacao',  required=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
parser.add_argument('--adcobranca', dest='adcobranca', type=str, help='adicionar remover acrescimos',required=False)
parser.add_argument('--coordenadas', dest='coordenadas', type=str, help='adicionar remover acrescimos',required=False)
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

ust = lambda x: unicode(str(x))
ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]','',n)

usuario = admmodels.User.objects.get(username='sgp')

if args.clientes:
    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
    pop_default = admmodels.Pop.objects.get(pk=args.pop_id)

    ri = -1

    incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 10000
    if incrementar < 10000:
        incrementar = 10000
    else:
        incrementar += 1

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ri += 1
            idcontrato = int(row[0]) + 20
            
                #'.mkauth_%s'%
            login= row[1]
            if login == '':
                login = 'SEM_LOGIN_%s'%idcontrato
            '''descomentar isso ingnora acentos em logins'''
            #login=normalize('NFKD', login).encode('ASCII','ignore')

            #if ':' in login:
            #    continue

            #if not senha:
            #    senha = login

            #
            # Dados pessoais
            #
            nome = ustr(row[3])
            cpfcnpj = ustr(row[5])[:20]
            rgie = ustr(row[8])[:20]
            profissao = ustr(row[9])
            tipo = ustr(row[2])

            if row[10] == 'Masculino':
                sexo = 'M'
            elif row[10] == 'Feminino':
                sexo = 'F'
            else:
                sexo = None
            data_nasc = None
            try:
                d_,m_,y_ = row[11].strip().split('/')
                if len(y_) == 2:
                    y_ = '19%s' %y_
                date(int(y_),int(m_),int(d_))
                data_nasc='%s-%s-%s' %(y_,m_,d_)
            except:
                pass

            #
            # Endereço
            #
            logradouro = ustr(row[14])[:50]
            numero = None
            numero = fnum(row[15])
            if len(numero) > 5:
                if len(logradouro.split('N.')) >1:
                    numero = fnum(logradouro.split('N.')[1])
                elif len(logradouro.split('casa')) >1:
                    numero = fnum(logradouro.split('casa')[1])
                elif len(logradouro.split('Casa')) >1:
                    numero = fnum(logradouro.split('Casa')[1])
                else:
                    numero = None

            if not numero or numero =='':
                numero = None

            complemento = ustr(row[16])[:50]
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
            telefone = row[48]
            servico_obs=ust(row[24])[:50]
            con_obs = ''
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS
            #

            data_cadastro = datetime.now()
            try:
                d_,m_,y_ = row[26].strip().split('/')
                if len(y_) == 2:
                    y_ = '20%s' %y_
                date(int(y_),int(m_),int(d_))
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass


            #
            # Contrato
            #

            # Servico
            plano = '@mkauth_QUINTA_DON_RICARDO%s'%ust(row[28]).strip()
            #plano_valor = str(row[29]).strip()

            conexao_tipo = ustrl(row[30])
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
            if isento in ['Sim','sim']:
                isento = 100
            else:
                isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            status = ustrl(row[41])
            status_bloqueado = ustrl(row[42])

            if status in  ['Sim','sim','s']:
                status_cc = 1
                status_s = 1
                status_c = 1

                if status_bloqueado in ['Sim','sim']:
                    status_cc = 4
                    status_s = 4
                    status_c = 4

            if status in ['Não','Nao','nao','não','n']:
                status_cc = 3
                status_s = 3
                status_c = 3

            if row[43]:
                senha=row[43]
            else:
                senha='mkauth2sgp'

            plano_download = int(fnum(row[44]))
            plano_upload = int(fnum(row[45]))
            plano_valor = row[46].replace(',', '.')

            login_pai = row[49]

            if len(ustr(row[14])) == 0 and len(cidade.strip()) == 0:
                logradouro = ustr(row[50])[:50]
                numero = None
                numero = fnum(row[51])
                if len(numero) > 5:
                    if len(logradouro.split('N.')) >1:
                        numero = fnum(logradouro.split('N.')[1])
                    elif len(logradouro.split('casa')) >1:
                        numero = fnum(logradouro.split('casa')[1])
                    elif len(logradouro.split('Casa')) >1:
                        numero = fnum(logradouro.split('Casa')[1])
                    else:
                        numero = None

                if not numero or numero =='':
                    numero = None
                complemento = ustr(row[56])[:50]
                bairro = ustr(row[52]).strip()[0:50]
                cep = ustr(row[54]).strip()[0:20]
                uf = ustr(row[55])
                cidade = ustr(row[53]).upper()[0:50]

            nome_pai = ust(row[57])
            nome_mae = ust(row[58])
            naturalidade = ust(row[59])



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
                    try:
                        new_plano_internet.save()
                    except:
                        new_plano_internet.download = 307200
                        new_plano_internet.upload = 307200
                        new_plano_internet.save()
                    print('criado plano %s' %plano)
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                else:
                    raise Exception('Não localizei plano %s' %plano)

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

            #print pop
            #print row

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print nome_pai, nome_mae, naturalidade
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
                print "Import %s" %nome
                # Save Models

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
                    new_endereco.pontoreferencia=row[60]

                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_inst = copy.copy(new_endereco)
                    try:
                        new_endereco.save()
                        new_endereco_cob.save()
                        new_endereco_inst.save()
                    except Exception as a:
                        print(new_endereco)
                        print(a) 




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
                        new_pessoa.naturalidade = naturalidade
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

                if len(contrato_check) == 0:
                    new_contrato.id = idcontrato
                else:
                    new_contrato.id = incrementar
                    incrementar += 1

                new_contrato.cliente = new_cliente
                new_contrato.pop = pop_default
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

                # Servico
                new_servico = admmodels.ServicoInternet()
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
                try:
                    if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                        new_servico.ip = ip
                except:
                    new_servico.ip = None
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.data_cadastro=data_cadastro
                new_servico.observacao=servico_obs
                try:
                    new_servico.save()
                except Exception as e:
                    new_servico.login= str(login)+str(idcontrato)+'duplicado'
                    new_servico.save()


                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)

                if login != login_pai:
                    servico_pai = admmodels.ServicoInternet.objects.filter(login=login_pai)
                    if servico_pai:
                        new_cobranca.cobranca_unificada=servico_pai[0].clientecontrato.cobranca
                        new_cobranca.save()

    from apps.admcore import models as admmodels
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)


if args.chamados:
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
            time = n.strip().split()[1]
            d_,m_,y_ = date.split('/')
            return '%s-%s-%s %s'%(y_,m_,d_, time)
        except:
            return n
        

    with open(args.chamados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            protocolo = row[0]
            if len(protocolo) > 14:
                protocolo = protocolo[0:13]
            login = row[1].strip().lower()
            assunto = row[2]
            status = row[3]
            data_cadastro = format_data(row[4])
            data_agendamento = format_data(row[5])
            data_finalizacao = format_data(row[6])
            conteudo = row[7]
            if conteudo == "" or conteudo is None:
                conteudo = "Campo conteúdo vazio no MK-AUTH."
            servicoprestado = row[8]

            servico = admmodels.ServicoInternet.objects.filter(login__trim__lower=login)

            if servico:
                clientecontrato = servico[0].clientecontrato
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
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if status == 'fechado' else amodels.OCORRENCIA_ABERTA
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
                    ordem['status'] = amodels.OS_ENCERRADA if status == 'fechado' else amodels.OS_ABERTA
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
#from apps.admcore import models as admmodels




if args.coordenadas:
    with open(args.coordenadas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            print(admmodels.Endereco.objects.filter(servicointernet__login__iexact=row[0]).update(map_ll=row[1]))
            print(admmodels.Endereco.objects.filter(cobranca__clientecontrato__servicointernet__login__iexact=row[0]).update(map_ll=row[1]))




if args.msg_chamados:
    with codecs.open(args.msg_chamados, 'rb', encoding='utf-8') as csvfile:
            conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
            for row in conteudo:
                try:
                    protocolo = row[0]
                    if len(protocolo) > 14:
                        protocolo = protocolo[0:13]
                except:
                    continue
                try:
                    data= row[2]
                except:
                    data='sem data'

                try:    
                    anotacao= row[3]
                except:
                    continue

                atendente= row[1]
                try:
                    ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
                except:
                    continue

                usuario= usuario

                print(ocorrencia, atendente,usuario,data,anotacao)
                if ocorrencia:
                    new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                    new_ocorrencia_anotacao.ocorrencia= ocorrencia
                    new_ocorrencia_anotacao.anotacao=str(atendente) + ' :: ' + str(data) + ' :: '+ str(anotacao)
                    new_ocorrencia_anotacao.usuario= usuario
                    new_ocorrencia_anotacao.save()

'''
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-ativados.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-ativados.csv.utf8 --sync=1
	
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-ativados2.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-ativados2.csv.utf8 --sync=1

python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-ativados3.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-ativados3.csv.utf8 --sync=1

python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-adicional.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-adicional.csv.utf8 --sync=1

python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-adicional2.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-adicional2.csv.utf8 --sync=1


python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-desativados.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=mkauth-clientes-desativados.csv.utf8 --sync=1


python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --coordenadas=mkauth-clientes-coordenadas.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --chamados=mkauth-chamados.csv.utf8
python import_mkauth.py --settings=sgp.cwmnet.settings --nas=1 --pop=1 --portador=3 --vencimentoadd=1 --planoadd=1 --msg_chamados=mkauth-msg-ocorrencia.csv.utf8
'''

