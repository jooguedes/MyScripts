#!/usr/bin/python
# -*- coding: utf-8 -*-

from django.conf import settings
from django.core.wsgi import get_wsgi_application
import argparse
from nis import cat
import os
import sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv
import re
from decimal import Decimal
import codecs
from warnings import catch_warnings
import hashlib
from unicodedata import normalize
parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str,help='settings django', required=True)
parser.add_argument('--sync', dest='sync_db', type=bool,help='Sync Database', default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--pop', dest='pop', type=str, help='id do pop', required=False)
parser.add_argument('--nas', dest='nas', type=str, help='id do NAS', required=False)
parser.add_argument('--senhas', dest='senhas', type=str, help='senhas dos clientes', required=False)
parser.add_argument('--nf2122', dest='nf2122',type=str, help='notas fiscais', required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='titulos', required=False)
parser.add_argument('--email', dest='email', type=str, help='email', required=False)
parser.add_argument('--celular', dest='celular', type=str, help='celular', required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='chamados', required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='portadores', required=False)
parser.add_argument('--radacct', dest='radacct', type=str, help='radacct', required=False)
parser.add_argument('--usuarios', dest='usuarios', type=str, help='usuarios do sistema', required=False )

#python import_bemtevi --settings=sgp.local.settings --portadores=bemtevi-portadores.csv.utf8
#python import_bemtevi --settings=sgp.local.settings --pop=1 --nas=1 --clientes= --sync=1
#python import_bemtevi --settings=sgp.local.settings  --senhas=bemtevi-usuarios-radius.csv 
#python import_bemtevi.py --settings=sgp.local.settings  --titulos=bemtevi-titulos.csv
#python import_bemtevi.py --settings=sgp.local.settings  --nf2122=
# python import_bemtevi.py --settings=sgp.local.settings  --email=bemtevi-emails.csv
# python import_bemtevi.py --settings=sgp.local.settings  --celular=bemtevi-celulares.csv
# python import_bemtevi.py --settings=sgp.local.settings  --chamados=bemtevi-chamados.csv
# python import_bemtevi.py --settings=sgp.local.settings  --usuarios=bemtevi-chamados.csv
# python import_bemtevi.py --settings=sgp.local.settings  --radacct=bemtevi-radacct.csv
    




# nas, planos, portadores, caixas clientes,fornecedor, contas a pagar,

args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
application = get_wsgi_application()
from django.db.models import Q
from apps.atendimento import models as amodels
from apps.netcore.utils.radius import manage
from apps.netcore import models as nmodels
from apps.fiscal import models as fismodels, constants as fisconstants
from apps.financeiro import models as fmodels
from apps.admcore import models as admmodels
from apps.netcore import models_radius as rmodels

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

def fnum(n): return re.sub('[^0-9]', '', unicode(n))

def valida_data(dt):
    if len(dt.split(' '))>1:
        return dt.split(' ')[0]
    elif dt:
        pass

def verifica_vencimento(v):
    if v!='':
        if fmodels.Vencimento.objects.filter(dia=v).count() > 0:
            return int(v.strip())
        else:
            new_vencimento= fmodels.Vencimento()
            new_vencimento.dia=int(v.strip())
            new_vencimento.save()

            return int(v.strip())
    else:
        if fmodels.Vencimento.objects.filter(dia=10) > 0:
            return 10
        else:
            new_vencimento= fmodels.Vencimento()
            new_vencimento.dia=10
            new_vencimento.save()
            return 10




usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome__icontains='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome__icontains='fibra').order_by('-id')[0]



if args.clientes:
    nas = nmodels.NAS.objects.all()[0]
    formacobranca = fmodels.FormaCobranca.objects.all()[0]

    m = manage.Manage()

    with codecs.open(args.clientes, 'ru') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            idcliente = int(row[0])
            idcontrato = int(row[0])
            try:
                if admmodels.ServicoInternet.objects.filter(login=row[27]).count() != 0:
                    continue
                print row
            except:
                login=str(idcliente)+"sem_login"
            try:
                idcliente = int(row[0])
                idcontrato = int(row[0])
            except:
                continue
            nome = row[1]
            nomefantasia = row[4]
            insc_estadual = ''
            rgie = row[6][0:20]
            sexo = ''
            data_nasc = row[7]
            profissao = row[16]
            cpfcnpj = row[2][0:20]
            observacao=row[10]

            endereco_inst = {}
            endereco_inst['logradouro'] = row[33]  # tipo_insta,endereco_insta
            try:
                endereco_inst['numero'] = int(row[37])  # numero_insta
            except:
                endereco_inst['numero'] = None
            endereco_inst['complemento'] = row[35]
            endereco_inst['bairro'] = row[32][0:40]
            endereco_inst['cidade'] = row[30][0:40]
            endereco_inst['uf'] = 'MS' if 'Mato Grosso do Sul' in row[31] else row[31]
            endereco_inst['cep'] = fnum(row[34])
            endereco_inst['pontoreferencia'] = row[36]
            nomepai = row[8]
            nomemae = row[9]
            
            cli_obs = row[10]
            login = row[27]
            senha = 'sem_senha'
            status=row[18]
            ip=None
            mac=None
            mac_dhcp=None
            plano=row[23]
            try:
                plano = admmodels.PlanoInternet.objects.filter(plano__descricao=row[23])[0]
            except Exception:
                new_plano = admmodels.Plano()
                new_plano.descricao=row[23]
                new_plano.preco = row[24]
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano
                new_plano_internet.download = 0
                new_plano_internet.upload = 0
                try:
                    new_plano_internet.save()
                except:
                    new_plano_internet.download = 307200
                    new_plano_internet.upload = 307200
                    new_plano_internet.save()

                
                plano = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                print('criado plano %s' %plano)
           
            portador = row[40]
            vencimento = verifica_vencimento(row[40])
            data_cadastro = valida_data(row[5])
            data_ativacao = data_cadastro

            comodato = False
            respempresa = ''
            respcpf = ''

            pop = admmodels.Pop.objects.filter(id=args.pop)[0]
            nas = nmodels.NAS.objects.filter(id=args.nas)[0]

            conexao_tipo = 'ppp'
            isento = 0
            status_cc = 1
            status_s = 1
            status_c = 1

            """
               0 = Ativo
               1 = Arquivado (SERIA CANCELADO)
               2 = Bloqueado
               """

            if status=='0':
                status_cc = 1
                status_s = 1
                status_c = 1

            if status =='1':
                status_cc = 3
                status_s = 3
                status_c = 3

            if status =='2':
                status_cc = 4
                status_s = 4
                status_c = 4


            status_criar = [6, 2, status_cc]

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" % vencimento
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' % vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save()
                    
            print status, login, nome, cpfcnpj, len(cpfcnpj), sexo, data_cadastro, data_nasc
            print  endereco_inst
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print login, senha, ip, mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" % nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)

                if len(cliente_check) == 0:

                    # Endereco
                    new_endereco = admmodels.Endereco(**endereco_inst)
                    new_endereco_cob = admmodels.Endereco(**endereco_inst)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    
                    new_endereco.save()
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    try:
                        fmodels.Portador.objects.get(pk=portador)
                    except:
                        portador = 255


                    if len(cpfcnpj) <= 11:
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa = 'F'
                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.profissao = profissao
                        new_pessoa.nomepai = nomepai
                        new_pessoa.nomemae = nomemae
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg = rgie
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor = ''
                       
                        try:
                            new_pessoa.save()
                        except:
                            try:
                                new_pessoa.save()
                            except:
                                new_pessoa.datanasc = None
                                new_pessoa.save()

                    if len(cpfcnpj) > 11:
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa = 'J'
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
                    if data_cadastro in ('0000-00-00'):
                        data_cadastro = datetime.now()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    new_cliente.observacao = cli_obs
                    new_cliente.save()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()

                else:
                    new_endereco = cliente_check[0].endereco

                    new_endereco_cob = admmodels.Endereco(**endereco_inst)
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
                    # new_cliente.save()
                    #new_cliente.data_cadastro = data_cadastro
                    # new_cliente.save()
                    new_cliente = cliente_check[0]

                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob

                try:
                    new_cobranca.portador = fmodels.Portador.objects.get(
                        pk=portador)
                except:
                    new_cobranca.portador = fmodels.Portador.objects.all()[0]

                new_cobranca.vencimento = fmodels.Vencimento.objects.get(
                    dia=vencimento)
                new_cobranca.isento = isento
                new_cobranca.notafiscal = False
                if str(data_cadastro) in ('0000-00-00'):
                    data_cadastro = datetime.now()
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
                    new_status.modo = 2
                    new_status.usuario = usuario
                    new_status.data_cadastro = data_cadastro
                    new_status.save()

                    new_status.data_cadastro = data_cadastro
                    new_status.save()

                # Servico
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login=normalize('NFKD', unicode(login.strip())).encode('ASCII', 'ignore').decode('ascii')).count() > 0:
                    print u'Já existe serviço com o login %s. Ajustando login: %s%s' % (login,
                                                                                        login,
                                                                                        str(new_contrato.id))
                    login += str(new_contrato.id)
                new_servico.login = login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password = senha
                new_servico.login_password_plain = senha
                new_servico.central_password = senha
                if admmodels.ServicoInternet.objects.filter(Q(mac=mac) | Q(mac_dhcp=mac)).count() == 0:
                    new_servico.mac_dhcp = mac_dhcp
                    new_servico.mac = mac

                if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                    new_servico.ip = ip
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = plano
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.data_cadastro = data_cadastro
                new_servico.save()

                new_servico.data_cadastro = data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)



if args.senhas:
   with open(args.senhas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo: 
            print('Atualizando senha do login: ', admmodels.ServicoInternet.objects.filter(login__lower=row[0].lower()))
            admmodels.ServicoInternet.objects.filter(login__lower=row[0].lower()).update(login_password=row[1], login_password_plain=row[1])




if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            codigo_banco = '999'
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print row
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[1]
                new_portador.codigo_banco = codigo_banco
                new_portador.agencia =  '0'
                new_portador.agencia_dv = '0'
                new_portador.conta =  '0'
                new_portador.conta_dv = '0'
                new_portador.convenio = '0'
                new_portador.carteira = '0'
                new_portador.cedente = 'PROVEDOR X'
                new_portador.cpfcnpj = '0'
                new_portador.save()

if args.chamados:
    with open(args.chamados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(
                    cliente__id=row[1])
                if clientecontrato and amodels.Ocorrencia.objects.filter(numero=row[6]).count()==0:
                    print(row)
                    ocorrencia = {}
                    ocorrencia['id'] = int(row[0])
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                
                    ocorrencia['tipo'] = amodels.Tipo.objects.get(id=5)
                    ocorrencia['usuario'] = usuario
                    ocorrencia['numero'] = row[6]
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if row[7] == 'fechado' else amodels.OCORRENCIA_ABERTA

                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['data_cadastro'] = row[3]
                    ocorrencia['data_agendamento'] = None
                    ocorrencia['data_finalizacao'] = None if '0000-00-00' in row[4] else row[4]
                    ocorrencia['conteudo'] = row[2] + "\n" + row[5]
                   
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()
                    new_ocorrencia.data_cadastro = row[3]
                    if new_ocorrencia.data_cadastro=='':
                        new_ocorrencia.data_cadastro= datetime.now()
                    
                    new_ocorrencia.save()
                else:
                    print('Ocorrencia já importada')
            except Exception as e:
                print(e)


if args.email:
    with open(args.email, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                new_cliente=admmodels.Cliente.objects.get(id=row[1])
                new_contato = admmodels.Contato()
                new_contato.tipo = 'EMAIL'
                new_contato.contato = row[0]
                new_contato.save()
               
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = new_cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()
                print("Importando email: ", row[0])
            except Exception as e:
                print(e)
                continue


if args.celular:
    with open(args.celular, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                new_cliente=admmodels.Cliente.objects.get(id=row[1])
                new_contato = admmodels.Contato()
                new_contato.tipo = 'CELULAR'
                new_contato.contato = row[0]
                new_contato.save()
                print("Importando celular: ", row[0])
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = new_cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()
            except Exception as e:
                print(e)



if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            cliente = admmodels.Cliente.objects.filter(id=row[0])
            if not cliente:
                    continue

            cobranca = None
            contrato = None

            if cliente:
                cliente = cliente[0]
                contrato = admmodels.ClienteContrato.objects.filter(cliente_id=cliente.id)
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca

                
                portador = fmodels.Portador.objects.filter(id=row[10])
                if not portador:
                    continue
                else:
                    portador = portador[0]
                try:
                    nosso_numero=int(row[4])
                except:
                    continue
                if fmodels.Titulo.objects.filter(portador=portador, nosso_numero=row[4]).count() == 0:
                    print row
                    print('Passei do IF')
                    tdata = {}
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[4]  # nrboleto
                    tdata['numero_documento']= row[4]
                    tdata['parcela'] = 1  # parcela
                    tdata['portador'] = portador
                    tdata['valor'] = row[3]
                    tdata['observacao'] = row[7]
                    tdata['demonstrativo'] = row[7]
                    tdata['valorpago'] = row[8]
                    tdata['data_baixa'] = row[6]
                    tdata['data_pagamento'] = row[6]
                    tdata['data_documento'] = row[1]  # emissao
                    
                    tdata['data_vencimento'] = row[2]  # vencimento
                    if tdata['valorpago'] == '0' or tdata['valorpago'] == '' or tdata['valorpago'] == '0.00':
                        tdata['valorpago'] = None
                    tdata['usuario_b'] = usuario  # usuariobaixa 28
                    tdata['usuario_g'] = usuario  # usuariogerou 29
                    tdata['usuario_c'] = usuario  # usuariocancela 30
                    tdata['modogeracao'] = 'l'
                    tdata['motivocancela'] = None
                    tdata['motivodesconto'] = None

                    tdata['centrodecusto'] = fmodels.CentrodeCusto.objects.get(
                        codigo='01.01.01')
                    for k in tdata:
                        if tdata[k] in ['NULL', '0000-00-00', '']:
                            tdata[k] = None
                    if tdata['data_pagamento'] is None:
                        tdata['usuario_b'] = None
                        tdata['usuario_c'] = None


                    if tdata['data_pagamento'] :
                        tdata['status'] = fmodels.MOVIMENTACAO_PAGA
                        
                    else:
                        tdata['status'] = fmodels.MOVIMENTACAO_GERADA
                    if tdata['demonstrativo'] is None:
                        tdata['demonstrativo'] = ''

                    print tdata
                    new_titulo = fmodels.Titulo(**tdata)
                    new_titulo.save()
                    new_titulo.data_documento = tdata['data_documento']

                    new_titulo.save()




if args.nf2122:
    with open(args.nf2122, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            empresa = admmodels.Empresa.objects.all()[0]
            if empresa:
                empresa = empresa
                # nota
                v_nota = fismodels.NotaFiscal.objects.filter(
                    empresa=empresa, numero=row[2] or 0)
                

                if not row[14] or row[14]=='' or str(row[14])=='0':
                    cfop=5303
                else:
                    cfop=row[14]
                cfop = fismodels.CFOP.objects.get(cfop=cfop)
                if len(v_nota) == 0:

                    # cliente
                    cliente = admmodels.Cliente.objects.filter(
                        id=row[6], pessoa__cpfcnpj__numfilter=row[7])
                    if cliente:
                        cliente = cliente[0]
                    else:
                        cliente = admmodels.Cliente.objects.filter(
                            pessoa__cpfcnpj__numfilter=row[3])
                        if cliente:
                            cliente = cliente[0]

                    if cliente:
                        endereco = cliente.endereco
                        try:
                            clientecontrato = cliente.clientecontrato_set.filter(
                            cliente__id=cliente.id)
                        except Exception as e:
                            print(e)
                            continue
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
                        nfdest['telefone'] = row[15] if row[15]!='' else '8499999999'
                        nfdest['codigocliente'] = cliente.id
                        nfdest['tipoassinante'] = '1'
                        print(nfdest)
                        nfdest_obj = fismodels.NFDestinatario(**nfdest)
                        nfdest_obj.save()
                        nf = {}
                        nf['empresa'] = empresa
                        nf['destinatario'] = nfdest_obj
                        nf['data_emissao'] = row[3]
                        nf['data_saida'] = row[3]
                        nf['modelo'] = row[13]
                        nf['tipoutilizacao'] = '4'
                        nf['serie'] = 'U'
                        try:
                            nf['numero'] = int(row[2])
                        except:
                            pass
                        nf['valortotal'] = row[8]
                        nf['icms'] = row[9]
                        nf['outrosvalores'] = row[9]
                        nf['djson'] = {}
                        
                        nf['status'] = fisconstants.NOTAFISCAL_GERADA
                        nf['bcicms'] = '0.00'
                        nf['tipo_es'] = fisconstants.NOTAFISCAL_TIPO_SAIDA
                        nf['tipo_nf'] = fisconstants.NOTAFISCAL_SERVICO
                        nf['cfop'] = cfop
                        nf['usuario_g'] = usuario
                        nf['usuario_c'] = usuario
                        print(
                            "################################################NF###########################", nf)
                        new_nf = fismodels.NotaFiscal(**nf)
                        try:
                            new_nf.save()
                        except:
                            print("essa foi a data que deu erro",
                                  nf['data_emissao'], nf['data_saida'])

                        new_nf.data_emissao = nf['data_emissao']
                        new_nf.data_saida = nf['data_saida']
                        new_nf.save()
                        nfitem = {}
                        nfitem['notafiscal'] = new_nf
                        nfitem['descricao'] = row[10]
                        nfitem['codigoservico'] = '010101'
                        nfitem['classificacao'] = '0104'
                        nfitem['unidade'] = '1'
                        nfitem['qt_contratada'] = '1'
                        nfitem['qt_fornecida'] = '1'
                        nfitem['valortotal'] = row[17]
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
                        new_nfitem.data_cadastro = nf['data_emissao']
                        new_nfitem.data_alteracao = nf['data_emissao']
                        new_nfitem.save()

                        if row[16]:
                            titulo = fmodels.Titulo.objects.filter(Q(cliente=cliente),
                                                                   Q(nosso_numero=row[16], valor=row[8]))
                            if len(titulo) == 1:
                                # Cria nota fiscal com titulo
                                nft = fismodels.NotaFiscalTitulo()
                                nft.titulo = titulo[0]
                                nft.notafiscal = new_nf
                                nft.save()
                        
                else:
                    if row[10]!='':
                        nfitem = {}
                        nfitem['notafiscal'] = new_nf
                        nfitem['descricao'] = row[10]
                        nfitem['codigoservico'] = '010101'
                        nfitem['classificacao'] = '0104'
                        nfitem['unidade'] = '1'
                        nfitem['qt_contratada'] = '1'
                        nfitem['qt_fornecida'] = '1'
                        nfitem['valortotal'] = row[17]
                        nfitem['desconto'] = '0.00'
                        nfitem['acrescimo_despesa'] = '0.00'
                        nfitem['bcicms'] = '0.00'
                        nfitem['icms'] = '0.00'
                        nfitem['outrosvalores'] = fismodels.NotaFiscal.objects.filter(numero=row[2])[0].valortotal
                        nfitem['aliquotaicms'] = '0.00'
                        nfitem['item'] = '1'
                        nfitem['data_cadastro'] =  fismodels.NotaFiscal.objects.filter(numero=row[2])[0].data_emissao
                        nfitem['data_alteracao'] = fismodels.NotaFiscal.objects.filter(numero=row[2])[0].data_emissao
                        print(nfitem)
                        new_nfitem = fismodels.NotaFiscalItem(**nfitem)
                        new_nfitem.save()
                        new_nfitem.data_cadastro = fismodels.NotaFiscal.objects.filter(numero=row[2])[0].data_emissao
                        new_nfitem.data_alteracao = fismodels.NotaFiscal.objects.filter(numero=row[2])[0].data_emissao
                        new_nfitem.save()

if args.radacct:
    RadAcctId=2000
    md5=hashlib.md5()
    with open(args.radacct, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            usuario = usuario
            login = row[3]
            cliente = admmodels.ServicoInternet.objects.filter(login__trim__lower=login)
            radacct = rmodels.Radacct()
            radacct.username = login
            radacct.nasipaddress = row[6]
            radacct.radacctid=RadAcctId
            hash=str(RadAcctId)
            radacct.acctstarttime = row[9]
            print(radacct.acctstarttime)
            radacct.nasipaddress= row[6]
            radacct.acctstoptime= row[11] if row[11] !='' else row[10]
            print(radacct.acctstoptime)
            print(row)
            radacct.acctinputoctets = row[17]
            radacct.acctoutputoctets = row[18]
            radacct.calledstationid = row[19]
            radacct.callingstationid = row[20]
            radacct.acctsessionid = row[1]
            radacct.framedipaddress= row[24]
            radacct.framedipv6prefix=''
            radacct.delegatedipv6prefix=''
            md5.update(hash)
            radacct.acctuniqueid = md5.hexdigest()
            radacct.save()
            print(row)
            RadAcctId=RadAcctId+1


if args.usuarios:

    with open(args.usuarios, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.User.objects.filter(username=row[1]).count() == 0:
                nome = row[3]
                usuario = row[1]
                senha = row[2]
                new_usuario = admmodels.User()
                new_usuario.name = row[3]
                new_usuario.username = row[1]
                new_usuario.password = 'sha256_unsalted$%s' % row[2]
                new_usuario.is_staff = True
                new_usuario.is_active = True
                new_usuario.save()
