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
import shutil

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django', required=True)
parser.add_argument('--sync', dest='sync_db', type=bool, help='Sync Database', default=False)
parser.add_argument('--empresas', dest='empresas', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--pops', dest='pops', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--boletos', dest='boletos', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--contaapagar', dest='contaapagar', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--suportes', dest='suportes', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--notasfiscais', dest='notasfiscais', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--usuarios', dest='usuarios', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--historicocliente', dest='historicocliente', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP', required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID PORTADOR', required=False)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID NAS', required=False)


'''
EMPRESAS, POPS, PORTADORES, PLANOS, CLIENTES, BOLETOS, CONTAS A PAGAR, SUPORTES, NOTAS FISCAIS 1 e 2, USUARIOS, HISTORICO DO CLIENTE
python import_ixc.py --settings=sgp.local.settings --empresas=scut-empresas.csv.utf8
python import_ixc.py --settings=sgp.local.settings --pops=scut-pops.csv.utf8
python import_ixc.py --settings=sgp.local.settings --portadores=scut-portadores.csv.utf8
python import_ixc.py --settings=sgp.local.settings --planos=scut-planos.csv.utf8
python import_ixc.py --settings=sgp.local.settings --clientes=scut-clientes.csv.utf8 --nas= --portador= --pop=
python import_ixc.py --settings=sgp.local.settings --boletos=scut-boletos.csv.utf8
python import_ixc.py --settings=sgp.local.settings --contaapagar=scut-contaapagar.csv.utf8
python import_ixc.py --settings=sgp.local.settings --suportes=scut-suportes.csv.utf8
python import_ixc.py --settings=sgp.local.settings --notasfiscais=scut-notasfiscais.csv.utf8
python import_ixc.py --settings=sgp.local.settings --usuarios=scut-usuarios.csv.utf8
python import_ixc.py --settings=sgp.local.settings --historicocliente=scut-historicocliente.csv.utf8
'''

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

if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def ustr(x): return unicode(str(x).upper()).strip()
def ustrl(x): return unicode(str(x).lower()).strip()
def fstr(x): return unicode(str(x).lower()).strip()
def fnum(n): return re.sub('[^0-9]', '', unicode(n))
def fnum2(n): return re.sub('[^0-9\-]', '', unicode(n))


usuario = admmodels.User.objects.get(username='sgp')


formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome__icontains='Cabo').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome__icontains='Cabo').order_by('-id')[0]
if args.portador:
    portador = fmodels.Portador.objects.get(id=args.portador)


def convertdata(d):
    try:
        d_, m_, y_ = d.strip().split('-')
        date(int(y_), int(m_), int(d_))
        return '%s-%s-%s' % (y_, m_, d_)
    except:
        return None


if args.empresas:
    with open(args.empresas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            new_empresa = admmodels.Empresa()
            new_empresa.id = int(row[0])
            new_empresa.razaosocial = ustr(row[2])
            new_empresa.nomefantasia = ustr(row[3])
            new_empresa.cpfcnpj = row[13]
            new_empresa.telefone1 = row[15]
            new_empresa.data_cadastro = datetime.now()
            new_empresa.logradouro = row[4]
            new_empresa.cep = row[12]
            new_empresa.numero = fnum(row[8])
            if fnum(row[5]) == '':
                new_empresa.numero = None
            new_empresa.complemento = row[6]
            new_empresa.bairro = row[9]
            new_empresa.cidade = row[7]
            new_empresa.uf = row[8]
            try:
                new_empresa.save()
                print(new_empresa)
            except Exception as e:
                print('Erro ao salvar EMPRESA, erro: ', e)
                break
            

if args.pops:
    with open(args.pops, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Pop.objects.filter(id=row[0]).count() == 0:
                new_pop = admmodels.Pop()
                new_pop.id = row[0]
                new_pop.cidade = row[2]
                new_pop.uf = row[3].upper()
                try:
                    new_pop.save()
                    print(new_pop)
                except Exception as e:
                    print('Erro ao criar POP, erro: ', e)
                    break

if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print(row)
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[3]
                if row[3].strip() == '':
                    new_portador.descricao = 'BANCO_%s'%row[0]
                new_portador.codigo_banco = '999'
                new_portador.agencia = row[5] or '0'
                new_portador.agencia_dv = ''
                new_portador.conta = row[6] or '0'
                new_portador.conta_dv = ''
                new_portador.convenio = row[7]
                new_portador.carteira = row[10]
                new_portador.cedente = 'PROVEDOR X'
                new_portador.cpfcnpj = '0'
                new_portador.instrucoes1 = row[11]
                new_portador.instrucoes2 = row[12]
                new_portador.instrucoes3 = row[13]
                new_portador.instrucoes4 = row[14]
                new_portador.instrucoes5 = row[15]
                new_portador.save()

                new_pontorecebimento = fmodels.PontoRecebimento()
                new_pontorecebimento.descricao = row[3]
                if row[3].strip() == '':
                    new_pontorecebimento.descricao = 'BANCO_%s'%row[0]
                new_pontorecebimento.portador = new_portador
                new_pontorecebimento.empresa = admmodels.Empresa.objects.all()[0]
                new_pontorecebimento.save()

if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(descricao=row[0]).count() == 0:
                print(row)
                new_plano = admmodels.Plano()
                new_plano.id = row[0]
                new_plano.descricao = row[4]
                new_plano.preco = row[5]
                new_plano.grupo = grupo_obj
                new_plano.contrato = contrato_obj
                new_plano.desconto_venc = row[8]
                new_plano.anotacoes = row[6]
                new_plano.data_cadastro = datetime.now()
                new_plano.save()
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id = row[0]
                new_plano_internet.plano = new_plano
                try:
                    new_plano_internet.download = int(row[1].split('/')[0])
                except:
                    new_plano_internet.download = 204800
                try:
                    new_plano_internet.upload = int(row[1].split('/')[1])
                except:
                    new_plano_internet.upload = 204800
                new_plano_internet.data_cadastro = datetime.now()
                if 'EXCLUIDO' in row[9]:
                    new_plano_internet.active = False
                new_plano_internet.save()

if args.clientes:
    formacobranca = fmodels.FormaCobranca.objects.all()[0]
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
            login = row[0]
            senha = row[2]
            cpfcnpj = row[3]
            if cpfcnpj.strip() == '' or len(cpfcnpj) < 10:
                cpfcnpj = row[4]
            nome = row[6]
            logradouro = row[7]
            pontoreferencia = row[8]
            cidade = row[9]
            uf = row[10]
            bairro = row[11]
            cep = row[12]
            complemento = row[13]
            map_ll = '%s, %s'%(row[14], row[15])
            numero = fnum(logradouro.split()[-1])
            if numero == '':
                numero = None
            vencimento = row[16]
            if vencimento.strip() == '':
                vencimento = 10
            telefone = row[17]
            telefonecom = row[18]
            celular = row[19]
            data_nasc = row[22]
            if data_nasc.strip() == '':
                data_nasc = None
            data_cadastro = row[23]
            if data_cadastro.strip() == '':
                data_cadastro = datetime.now()
            data_ativacao = row[25]
            if data_ativacao.strip() == '':
                data_ativacao = data_cadastro
            cliente_obs = row[28]
            mac = row[29]
            ip = row[30]
            if len(ip) < 7: ip = None
            if len(mac) < 10: mac = None
            plano_id = row[33]
            if row[34].strip() != '':
                try:
                    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome=row[34]).order_by('-id')[0]
                except:
                    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
                try:
                    grupo_obj = admmodels.Grupo.objects.filter(nome=row[34]).order_by('-id')[0]
                except:
                    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]
            if row[37].strip() != '':
                comodato = True
                comodato_obs = row[36]
            else:
                comodato = False
                comodato_obs = ''

            rgie = ''

            sexo = None

            conexao_tipo = 'ppp'

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            if row[27].strip() != '':
                status_cc = 4
                status_s = 4
                status_c = 4

            if row[26].strip() != '':
                status_cc = 3
                status_s = 3
                status_c = 3

            nas = nas_default
            try:
                pop = admmodels.Pop.objects.get(pk=row[38])
            except:
                pop = pop_default

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print("erro vencimento %s" %vencimento)
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save()
            
            planointernet = admmodels.PlanoInternet.objects.get(id=row[33])

            print (nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc)
            print (logradouro,numero or '',complemento,bairro,cidade,uf,cep)
            print ('vencimento: ', vencimento, 'Plano: ', planointernet)
            print (telefone,telefonecom,celular)
            print (login,senha,ip,mac)
            print ('####################################################')
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
                print ("Import %s" %nome)
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)

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
                    new_endereco.map_ll=map_ll

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
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.observacao = cliente_obs
                    new_cliente.ativo = True
                    new_cliente.save()
                    
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()

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

                # Contrato
                new_contrato = admmodels.ClienteContrato()
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

                # Servico
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() > 0:
                    print ('Já existe serviço com o login %s. Ajustando login: %s%s' %(login, login, str(new_contrato.id)))
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
                new_servico.observacao=comodato_obs
                try:
                    new_servico.save()
                    new_servico.data_cadastro=data_cadastro
                    new_servico.save()
                except Exception as e:
                    print('Erro ao cadastrar SERVICO INTERNET, ', e)

                m.addRadiusServico(new_servico)

    from apps.admcore import models as admmodels
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)

            

if args.boletos:
    with open(args.boletos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            

            

if args.suportes:
    with open(args.suportes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            

if args.contaapagar:
    with open(args.contaapagar, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                dados = {}
                try:
                    dados['fornecedor'] = fmodels.Fornecedor.objects.get(pk=int(row[2]))
                except:
                    dados['fornecedor'] = None

                dados['descricao'] = row[11][:100]
                dados['valor'] = row[5]
                if fnum(row[5]) == '':
                    dados['valor'] = 0.00
                dados['forma_pagamento'] = fmodels.FormaPagamento.objects.get(id=1)
                try:
                    dados['centrodecusto'] = fmodels.CentrodeCusto.objects.get(id=50)
                except:
                    continue
                dados['data_emissao'] = row[7]
                dados['data_cadastro'] = row[6]
                dados['data_alteracao'] = row[6]
                dados['usuario'] = usuario

                print(dados)

                pagar = fmodels.Pagar(**dados)
                pagar.save()
                pagar.data_cadastro = pagar.data_emissao
                pagar.save()

                dadosparcela = {}
                dadosparcela['pagar'] = pagar
                dadosparcela['valor'] = dados['valor']
                dadosparcela['parcela'] = 1
                dadosparcela['status'] = fmodels.PAGAR_STATUS_PENDENTE
                if Decimal(row[22]) > Decimal('0.00'):
                    dadosparcela['status'] = fmodels.PAGAR_STATUS_QUITADO
                    dadosparcela['data_pagamento'] = row[21]
                    dadosparcela['valor_pago'] = row[22]
                    if fnum(row[22]) == '':
                        dadosparcela['valor_pago'] = 0.00
                dadosparcela['data_vencimento'] = row[8]
                dadosparcela['data_cadastro'] = dados['data_cadastro']
                dadosparcela['juros'] = 0
                dadosparcela['multa'] = 0
                dadosparcela['desconto'] = 0
                dadosparcela['usuario'] = dados['usuario']

                print(dadosparcela)

                pagaritem = fmodels.PagarItem(**dadosparcela)
                pagaritem.save()

            except Exception as e:
                print ('------------------- ERROR ------------------------\n%s - %s\n--------------------------------------------------'%(row, e))
            

if args.notasfiscais:
    with open(args.notasfiscais, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            empresa = admmodels.Empresa.objects.filter(
                cpfcnpj__numfilter=row[1])
            if empresa:
                empresa = empresa[0]
                # nota
                v_nota = fismodels.NotaFiscal.objects.filter(
                    empresa=empresa, numero=row[13] or 0)
                cfop = fismodels.CFOP.objects.get(cfop=row[10])
                if len(v_nota) == 0:

                    # cliente
                    cliente = admmodels.Cliente.objects.filter(
                        id=row[2], pessoa__cpfcnpj__numfilter=row[3])
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
                            id=row[4])
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
                        try:
                            nf['numero'] = int(row[13])
                        except:
                            pass
                        nf['valortotal'] = row[9]
                        nf['icms'] = '0.00'
                        nf['outrosvalores'] = row[9]
                        nf['djson'] = {}
                        if row[7]:
                            nf['status'] = fisconstants.NOTAFISCAL_CANCELADA
                            nf['djson']['motivocancela'] = row[8]
                            if row[7] == '0000-00-00':
                                nf['data_cancela'] = None
                            else:
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
                        new_nfitem.data_cadastro = nf['data_emissao']
                        new_nfitem.data_alteracao = nf['data_emissao']
                        new_nfitem.save()
                        if row[17]:
                            titulo = fmodels.Titulo.objects.filter(Q(cliente=cliente),
                                                                   Q(nosso_numero__endswith=row[17], valor=row[9]))
                            if len(titulo) == 1:
                                # Cria nota fiscal com titulo
                                nft = fismodels.NotaFiscalTitulo()
                                nft.titulo = titulo[0]
                                nft.notafiscal = new_nf
                                nft.save()
            else:
                print('empresa não identificada')


if args.usuarios:
    with open(args.usuarios, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.User.objects.filter(username=row[2]).count() == 0:
                new_usuario = admmodels.User()
                new_usuario.name = row[3]
                new_usuario.username = row[2]
                new_usuario.password = '123@mudar'
                new_usuario.is_staff = True
                new_usuario.is_active = True
                if 'x' in row[8].lower():
                    new_usuario.is_active = False
                new_usuario.save()

            
if args.historico:
    with open(args.historico, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            clientecontrato = admmodels.ClienteContrato.objects.filter(
                id=row[0])
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
                h.date_created = row[2]
                h.save()