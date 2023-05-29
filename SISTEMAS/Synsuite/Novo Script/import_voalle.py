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
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do portador', required=False)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do nas', required=False)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do pop', required=False)
parser.add_argument('--empresas', dest='empresas', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--fornecedores', dest='fornecedores', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--contasapagar', dest='contasapagar', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--ocorrencias', dest='ocorrencias', type=str, help='Arquivo importacao', required=False)
parser.add_argument('--notasfiscais', dest='notasfiscais', type=str, help='Arquivo importacao', required=False)

'''
python import_synsuit.py --settings=sgp.local.settings --empresas=synsuit-empresas.csv
python import_synsuit.py --settings=sgp.local.settings --portadores=synsuit-portadores.csv
python import_synsuit.py --settings=sgp.local.settings --clientes=synsuit-clientes.csv --pop= --nas= --portador= --sync=
python import_synsuit.py --settings=sgp.local.settings --titulos=synsuit-titulos-areceber.csv
python import_synsuit.py --settings=sgp.local.settings --fornecedores=synsuit-fornecedores.csv
python import_synsuit.py --settings=sgp.local.settings --contasapagar=synsuit-contas-a-pagar.csv
python import_synsuit.py --settings=sgp.local.settings --ocorrencias=synsuit-ocorrencias.csv
python import_synsuit.py --settings=sgp.local.settings --notasfiscais=synsuit-notasfiscais.csv
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
from apps.financeiro.utils import titulofunc
from apps.cauth import models as authmodels



if sys.version_info < (3, 0):
    reload(sys)
    sys.setdefaultencoding('utf-8')


def ustr(x): return str(x).upper().strip()
def ustrl(x): return str(x).lower().strip()
def fnum(n): return re.sub('[^0-9]', '', n)
def convertdata(d):
    try:
        d_, m_, y_ = d.strip().split('-')
        date(int(y_), int(m_), int(d_))
        return '%s-%s-%s' % (y_, m_, d_)
    except:
        return None

def strdate(d):
    try:
        d,m,y = d.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome__icontains='Cabo').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome__icontains='Cabo').order_by('-id')[0]


if args.portador_id:
    portador = fmodels.Portador.objects.get(id=args.portador_id)

if args.nas_id:
    nas = nmodels.NAS.objects.get(id=args.nas_id)

if args.pop_id:
    pop = admmodels.Pop.objects.get(id=args.pop_id)


if args.empresas:
    with open(args.empresas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            new_empresa = admmodels.Empresa()
            new_empresa.id = int(row[0])
            new_empresa.razaosocial = ustr(row[4])
            new_empresa.nomefantasia = ustr(row[3])
            new_empresa.cpfcnpj = row[5]
            new_empresa.telefone1 = row[14]
            new_empresa.data_cadastro = row[16].split()[0]
            new_empresa.logradouro = row[7]
            new_empresa.cep = row[6]
            new_empresa.numero = fnum(row[8])
            if fnum(row[8]) == '':
                new_empresa.numero = None
            new_empresa.complemento = row[9]
            new_empresa.bairro = row[10]
            new_empresa.cidade = row[11]
            new_empresa.uf = row[12]
            try:
                new_empresa.save()
                new_empresa.data_cadastro = row[16].split()[0]
                new_empresa.save()
                print(new_empresa)
            except Exception as e:
                print('Erro ao salvar EMPRESA, erro: ', e)
                break

if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print(row)
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[5]
                new_portador.codigo_banco = row[3] or row[4]
                new_portador.agencia = row[6] or '0'
                new_portador.agencia_dv = row[7]
                new_portador.conta = row[8] or '0'
                new_portador.conta_dv = row[9]
                new_portador.convenio = ''
                new_portador.carteira = ''
                new_portador.cedente = 'PROVEDOR X'
                new_portador.cpfcnpj = '0'
                new_portador.save()

                new_pontorecebimento = fmodels.PontoRecebimento()
                new_pontorecebimento.descricao = row[5]
                new_pontorecebimento.portador = new_portador
                new_pontorecebimento.empresa = admmodels.Empresa.objects.all()[0]
                new_pontorecebimento.save()


if args.clientes:
    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            id_cliente = int(row[0])
            cpfcnpj = row[3]
            nome = row[4]
            nomefantasia = row[5]

            endereco = {}
            endereco['cep'] = fnum(row[6])
            endereco['logradouro'] = '%s %s'%(row[8], row[7])
            try:
                endereco['numero'] = int(row[9])
            except:
                endereco['numero'] = None
            endereco['complemento'] = row[10]
            endereco['bairro'] = row[11][0:40]
            endereco['cidade'] = row[12][0:40]
            endereco['uf'] = row[14]
            endereco['map_ll'] = '%s, %s'%(row[15], row[16])
            endereco['pontoreferencia'] = row[17]

            if row[20] == 't':
                status_c = 1
            else:
                status_c = 3
            
            endereco_cob = {}
            endereco_cob['cep'] = fnum(row[20])
            endereco_cob['logradouro'] = row[21]
            try:
                endereco_cob['numero'] = int(row[22])
            except:
                endereco_cob['numero'] = None
            endereco_cob['complemento'] = row[23]
            endereco_cob['bairro'] = row[24][0:40]
            endereco_cob['cidade'] = row[25][0:40]
            endereco_cob['uf'] = row[27]
            endereco_cob['pontoreferencia'] = row[28]

            emails = '%s;%s'%(row[30], row[31])
            cliente_obs = row[33]
            rgie = row[34]
            data_nasc = row[35]
            nomemae = row[36]
            cliente_obs += '\n%s'%(row[37])
            data_cadastro = row[38].split()[0]
            if data_cadastro.strip() == '':
                data_cadastro = datetime.now()
            telefones = '%s;%s;%s;%s;%s'%(row[40], row[41], row[42], row[43], row[44])

            cliente_obs += '\n%s \n%s'%(row[45], row[46])

            id_contrato = int(row[47])
            contrato_obs = '%s \n%s'%(row[49], row[51])
            try:
                vencimento = int(row[52])
            except:
                vencimento = 10
            
            status = row[53]

            isento = 0

            # status 1 - Ativo
            # status 2 - ???
            # status 3 - Isento
            # status 4 - Cancelado
            # status 5 - ???
            # status 6 - Bloqueio Financeiro
            # status 7 - Bloqueio Administrativo
            # status 8 - ???
            # status 9 - Encerrado

            status_cc = 1
            status_s = 1
            status_c = 1
            if status == '3':
                isento = 100

            if status in ['6', '7']:
                status_cc = 4
                status_s = 4
                status_c = 4

            if status in ['4', '9']:
                status_cc = 3
                status_s = 3
                status_c = 3

            status_criar = [6, 2, status_cc]

            data_cancelamento = row[54]
            motivo_cancelamento = row[55]

            plano_valor = row[58]
            plano_descricao = row[59]
            plano_observacao = row[60]
            try:
                plano_upload = int(row[61])
                plano_download = int(row[62])
            except:
                plano_upload = 51200
                plano_download = 102400

            login = row[64]
            senha = row[65]
            if login.strip() == '' and status in ['4', '9']:
                login = 'CLIENTE_CANCELADO_%s'%(id_contrato)
                senha = '123'

            if login.strip() == '':
                login = 'SEM_LOGIN_%s'%(id_contrato)
                senha = '123'
            if senha.strip() == '':
                senha = '123'

            endereco_inst = {}
            endereco_inst['cep'] = fnum(row[68])
            try:
                endereco_inst['numero'] = int(row[69])
            except:
                endereco_inst['numero'] = None
            endereco_inst['bairro'] = row[70][0:40]
            endereco_inst['logradouro'] = row[71]
            endereco_inst['cidade'] = row[72][0:40]
            endereco_inst['uf'] = row[73]
            endereco_inst['complemento'] = row[74]          
            endereco_inst['pontoreferencia'] = row[75]
            endereco_inst['map_ll'] = '%s, %s'%(row[76], row[77])

            servico_obs = row[78]
            mac = row[80]
            mac_dhcp = mac
            ip = None

            comodato = False
            if row[69].strip() != '':
                comodato = True
            servico_obs += '\nSN: %s'%(row[69])

            conexao_tipo = 'ppp'

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__lower__iexact=plano_descricao.lower())[0]
            except:
                try:
                    print(plano_descricao,plano_download,plano_upload,plano_valor)
                    new_plano = admmodels.Plano()
                    new_plano.descricao=plano_descricao
                    new_plano.preco = plano_valor
                    new_plano.contrato = contrato_obj
                    new_plano.grupo = grupo_obj
                    new_plano.observacao = plano_observacao
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
                    print('criado plano %s' %plano_descricao)
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano_descricao.lower())[0]
                except:
                    raise Exception('Não localizei plano %s' %plano_descricao)
            
            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print ("erro vencimento %s" % vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save()

            print (status, login, nome, cpfcnpj, len(cpfcnpj), data_cadastro, data_nasc)
            print (endereco_cob, endereco_inst)
            print ('vencimento: ', vencimento, 'Plano: ', plano_descricao)
            print (telefones, emails)
            print (login, senha, ip, mac)
            print ('####################################################')
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print ("Import %s" % nome)
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=id_cliente)

                if len(cliente_check) == 0:

                    # Endereco
                    new_endereco = admmodels.Endereco(**endereco)
                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    try:
                        new_endereco.save()
                        new_endereco_cob.save()
                        new_endereco_inst.save()
                    except Exception as e:
                        print('Erro ao salvar ENDERECO, erro: ', e)
                        break

                    tp = 'f'
                    if len(fnum(cpfcnpj)) > 12:
                        tp = 'j'

                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'

                        new_pessoa.nome = nome
                        new_pessoa.sexo = ''
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.profissao = ''
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.nomepai = ''
                        new_pessoa.nomemae = nomemae
                        new_pessoa.naturalidade = ''
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
                                try:
                                    new_pessoa.save()
                                except Exception as e:
                                    print('Erro ao cadastrar PESSOA, erro', e)
                                    break

                    if tp == 'j':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = nome

                        new_pessoa.nomefantasia = nome
                        new_pessoa.resempresa = ''
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = ''
                        new_pessoa.tipo = 8
                        try:
                            new_pessoa.save()
                        except Exception as e:
                            print('Erro ao cadastrar PESSOA')
                            break

                    # Cliente
                    new_cliente = admmodels.Cliente()
                    new_cliente.id = id_cliente
                    new_cliente.pessoa = new_pessoa
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    if data_cadastro in ('0000-00-00'):
                        data_cadastro = datetime.now()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    new_cliente.observacao = cliente_obs
                    try:
                        new_cliente.save()
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.save()
                    except Exception as e:
                        print('Erro ao cadastrar CLIENTE, erro: ', e)
                        break

                    # contatos
                    for email in emails.split(';'):
                        if len(email) > 4:
                            new_contato = admmodels.Contato()
                            new_contato.tipo = 'EMAIL'
                            new_contato.contato = email
                            new_contato.save()
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            try:
                                new_ccontato.save()
                            except Exception as e:
                                print('Erro ao salvar EMAIL, erro: ', e)
                                break

                    # contatos
                    for celular in telefones.split(';'):
                        if len(celular) > 4:
                            new_contato = admmodels.Contato()
                            new_contato.tipo = 'CELULAR_PESSOAL'
                            new_contato.contato = celular
                            new_contato.save()
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            try:
                                new_ccontato.save()
                            except Exception as e:
                                print('Erro ao cadastrar TELEFONE, erro: ', e)
                                break

                else:
                    new_endereco = cliente_check[0].endereco

                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    try:
                        new_endereco_cob.save()
                        new_endereco_inst.save()
                    except Exception as e:
                        print('Erro ao cadastrar ENDERECOS, erro: ', e)
                        break

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
                if str(data_cadastro) in ('0000-00-00'):
                    data_cadastro = datetime.now()
                new_cobranca.data_cadastro = data_cadastro
                new_cobranca.datacobranca1 = data_cadastro
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = status_c
                try:
                    new_cobranca.save()
                    new_cobranca.data_cadastro = data_cadastro
                    new_cobranca.save()
                except Exception as e:
                    print('Erro ao cadastrar COBRANÇA')
                    break

                # Contrato
                new_contrato = admmodels.ClienteContrato()
                new_contrato.id = id_contrato
                new_contrato.cliente = new_cliente
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca
                new_contrato.data_inicio = data_cadastro
                new_contrato.data_cadastro = data_cadastro
                new_contrato.data_alteracao = data_cadastro
                new_contrato.observacao = contrato_obs
                try:
                    new_contrato.save()
                    new_contrato.data_cadastro = data_cadastro
                    new_contrato.data_alteracao = data_cadastro
                    new_contrato.save()
                except Exception as e:
                    print('Erro ao cadastrar CONTRATO, erro: ', e)
                    break

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
                if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
                    print ('Já existe serviço com o login %s. Ajustando login: %s%s' % (login, login, str(new_contrato.id)))
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
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.observacao = servico_obs
                new_servico.data_cadastro = data_cadastro
                try:
                    new_servico.save()
                    new_servico.data_cadastro = data_cadastro
                    new_servico.save()
                except Exception as e:
                    print('Erro ao cadastrar SERVICOINTERNET, erro: ', e)
                    break

                m.addRadiusServico(new_servico)


if args.titulos:
    usuario = authmodels.User.objects.get(username='sgp')
    formapagamento = fmodels.FormaPagamento.objects.all()[0]
    planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            id_cliente = int(row[2])
            try:
                id_contrato = int(row[23])
                contrato = admmodels.ClienteContrato.objects.filter(id=id_contrato)
                cliente = admmodels.Cliente.objects.filter(id=id_cliente)
            except: 
                cliente = admmodels.Cliente.objects.filter(id=id_cliente)
                contrato = admmodels.ClienteContrato.objects.all()
            if cliente:
                print("Esse é meu cliente: ", cliente)
                cliente = cliente[0]
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    numero_documento = fnum(row[4])
                    if numero_documento.strip() == '':
                        numero_documento = fnum(row[0])
                    nosso_numero = fnum(row[6])
                    if nosso_numero.strip() == '':
                        nosso_numero = numero_documento
                    nosso_numero_f = None
                    demonstrativo = '%s\n%s'%(row[22], row[23])
                    data_documento = row[27].split()[0]
                    data_vencimento = row[13]
                    parcela = row[5]
                    data_pagamento = None
                    data_baixa = None
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None

                    juros = 0.00
                    codigo_barras=row[26]
                    linha_digitavel=row[25]
                    valor = row[8]
                    desconto = 0.00
                    titulo_obs = '%s\n%s'%(row[15], row[17])
                    try:
                        portador = fmodels.Portador.objects.get(id=row[20])
                    except:
                        try:
                            portador = fmodels.Portador.objects.get(id=row[18])
                        except:
                            new_portador = fmodels.Portador()
                            new_portador.id = row[20] or row[18]
                            new_portador.descricao = row[19]
                            new_portador.codigo_banco = '999'
                            new_portador.cedente = 'PROVEDOR X'
                            new_portador.cpfcnpj = '0'
                            new_portador.save()

                            new_pontorecebimento = fmodels.PontoRecebimento()
                            new_pontorecebimento.descricao = row[19]
                            new_pontorecebimento.portador = new_portador
                            new_pontorecebimento.empresa = admmodels.Empresa.objects.all()[0]
                            new_pontorecebimento.save()
                            portador = new_portador

                    if row[29].strip() != '' or row[30].strip() != '':
                        valorpago = row[31]
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None
                        data_pagamento = row[30] if row[30].strip() != '' else data_vencimento
                        data_baixa = row[29] if row[29].strip() != '' else data_pagamento

                    # elif 'Cancelado' == row[2].strip():
                    #     data_cancela = data_vencimento
                    #     status = fmodels.MOVIMENTACAO_CANCELADA
                    #     data_baixa = None
                    #     data_pagamento = None
                    #     usuario_b = None
                    #     usuario_c = usuario


                    if nosso_numero:
                        print('entrei no nosso numero')
                        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                            dados = {'cliente': cliente,
                                    'cobranca': cobranca,
                                    'portador': portador,
                                    'codigo_barras':codigo_barras, 
                                    'linha_digitavel':linha_digitavel,
                                    'formapagamento': formapagamento,
                                    'centrodecusto': planocontas,
                                    'modogeracao': 'l',
                                    'usuario_g': usuario,
                                    'usuario_b': usuario_b,
                                    'usuario_c': usuario_c,
                                    'demonstrativo': demonstrativo,
                                    'data_documento': data_documento,
                                    'data_alteracao': data_documento,
                                    'data_vencimento': data_vencimento,
                                    'data_cancela': data_cancela,
                                    'data_pagamento': data_pagamento,
                                    'data_baixa': data_baixa,
                                    'numero_documento': numero_documento,
                                    'nosso_numero': nosso_numero,
                                    'nosso_numero_f': nosso_numero_f,
                                    'linha_digitavel': linha_digitavel,
                                    'codigo_barras': codigo_barras,
                                    'valor': valor,
                                    'valorpago': valorpago,
                                    'desconto': desconto,
                                    'status': status,
                                    'observacao': 'Boleto de importação',
                                    'parcela': parcela,
                                    'djson': {'juros': juros }
                                    }
                            if not args.sync_db:
                                print(dados)
                            else:
                                print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                                try:
                                    titulo = fmodels.Titulo(**dados)
                                    titulo.save()
                                    titulo.data_documento=data_documento
                                    titulo.data_alteracao=data_documento
                                    titulo.save()

                                except Exception as e:
                                    print ("Erro cadastrar",e,dados)
                        else:
                            print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)




if args.fornecedores:
    with open(args.fornecedores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            dados = {}
            dados['id'] = int(row[0])
            dados['cpfcnpj'] = row[2]
            dados['nome'] = row[3]
            dados['nomefantasia'] = row[4]
            dados['cep'] = row[5]
            dados['logradouro'] = row[6]
            dados['pontoreferencia'] = '%s\n%s'%(row[7], row[16])
            try:
                dados['numero'] = int(fnum(row[8]))
            except:
                dados['numero'] = None
            dados['complemento'] = row[9]
            dados['bairro'] = row[10]
            dados['cidade'] = row[11]
            dados['uf'] = row[13]
            dados['map_ll'] = '%s, %s'%(row[14], row[15])
            dados['email'] = '%s;%s'%(row[17], row[18])
            dados['observacao'] = row[20]
            dados['data_cadastro'] = row[20].split()[0]
            dados['telefones'] = '%s; %s; %s; %s'%(row[22], row[23], row[25], row[26])
            dados['fax'] = row[24]
            dados['responsavelempresa'] = row[4]            
            dados['ativo'] = True
            try:
                novo_fornecedor = fmodels.Fornecedor(**dados)
                novo_fornecedor.save()
                novo_fornecedor.data_cadastro = dados['data_cadastro']
                novo_fornecedor.save()
                print(novo_fornecedor)
            except Exception as e:
                print(e, dados)


if args.contasapagar:
    with open(args.contasapagar, 'rb') as csvfile:
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

if args.ocorrencias:
    metodo = amodels.Metodo.objects.all()[0]
    with open(args.ocorrencias, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=row[5])
                if clientecontrato and amodels.Ocorrencia.objects.filter(numero=fnum(row[7])).count()==0:
                    print(row)
                    ocorrencia = {}
                    ocorrencia['id'] = int(row[0])
                    ocorrencia['numero'] = fnum(row[7])
                    if len(fnum(row[7])) > 14:
                        ocorrencia['numero'] = row[7][7:]
                    ocorrencia['clientecontrato'] = clientecontrato[0]
                    ocorrencia['setor'] = None
                    ocorrencia['tipo'] = amodels.Tipo.objects.get(id=5)
                    ocorrencia['usuario'] = usuario
                    ocorrencia['metodo'] = metodo
                    ocorrencia['status'] = amodels.OCORRENCIA_ENCERRADA if row[3].strip() in ['Encerramento', 'Cancelado'] else amodels.OCORRENCIA_ABERTA
                    ocorrencia['responsavel'] = ocorrencia['usuario']
                    ocorrencia['metodo'] = amodels.Metodo.objects.all()[0]
                    ocorrencia['data_cadastro'] = row[18].split()[0]
                    ocorrencia['data_agendamento'] = row[8].split()[0]
                    ocorrencia['data_finalizacao'] = row[15].split()[0]
                    ocorrencia['conteudo'] = '%s - %s \n %s'%(row[9], row[10], row[11])
                    for ok in ocorrencia:
                        if ocorrencia[ok] == '0000-00-00 00:00:00':
                            ocorrencia[ok] = None
                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    new_ocorrencia.save()

                    new_ocorrencia.data_cadastro = row[18].split()[0]
                    if new_ocorrencia.data_cadastro=='':
                        new_ocorrencia.data_cadastro= datetime.now()
                    new_ocorrencia.data_agendamento = row[8].split()[0]
                    new_ocorrencia.data_finalizacao = row[15].split()[0]
                    if new_ocorrencia.data_agendamento == '0000-00-00 00:00:00'  or new_ocorrencia.data_agendamento =='':
                        new_ocorrencia.data_agendamento = None
                    if new_ocorrencia.data_finalizacao == '0000-00-00 00:00:00' or new_ocorrencia.data_finalizacao=='':
                        new_ocorrencia.data_finalizacao = None
                    new_ocorrencia.save()

                    ordem = {}
                    ordem['id'] = int(row[0])
                    ordem['ocorrencia'] = amodels.Ocorrencia.objects.get(id=int(row[0]))
                    ordem['status'] = amodels.OS_ENCERRADA if row[3].strip() in ['Encerramento', 'Cancelado'] else amodels.OS_ABERTA
                    ordem['usuario'] = usuario
                    ordem['setor'] = ocorrencia['setor']
                    ordem['motivoos'] = amodels.MotivoOS.objects.get(id=4)
                    ordem['data_cadastro'] = ocorrencia['data_cadastro']
                    ordem['data_agendamento'] = ocorrencia['data_agendamento']
                    ordem['data_finalizacao'] = ocorrencia['data_finalizacao']
                    ordem['conteudo'] = ocorrencia['conteudo']
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

                    servicoprestado = row[4].strip()

                    if servicoprestado != '':
                        new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                        new_ocorrencia_anotacao.ocorrencia=amodels.Ocorrencia.objects.get(numero=fnum(row[7]))
                        new_ocorrencia_anotacao.anotacao=servicoprestado
                        new_ocorrencia_anotacao.usuario= usuario
                        new_ocorrencia_anotacao.save()
                else:
                    print('Ocorrencia já importada')
            except Exception as e:
                print(e)
                break

if args.notasfiscais:
    with open(args.notasfiscais, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            empresa = admmodels.Empresa.objects.filter(id=row[1])
            if empresa:
                empresa = empresa[0]
                try:
                    v_nota = fismodels.NotaFiscal.objects.filter(empresa=empresa, numero=int(row[7]))
                except:
                    continue
                cfop = fismodels.CFOP.objects.get(cfop=5301)
                if len(v_nota) == 0:
                    try:
                        cliente = admmodels.Cliente.objects.filter(id=fnum(row[17]))
                    except:
                        continue
                    if cliente:
                        cliente = cliente[0]
                    else:
                        cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=row[20])
                        if cliente:
                            cliente = cliente[0]

                    if cliente:
                        endereco = cliente.endereco
                        try:
                            clientecontrato = cliente.clientecontrato_set.filter(id=row[8])
                        except Exception as e:
                            clientecontrato = cliente.clientecontrato_set.all()
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
                        nf['data_emissao'] = row[14]
                        nf['data_saida'] = row[14]
                        nf['modelo'] = row[12]
                        nf['tipoutilizacao'] = '4'
                        nf['serie'] = row[11]
                        try:
                            nf['numero'] = int(row[7])
                        except:
                            pass
                        nf['valortotal'] = row[23]
                        nf['icms'] = '0.00'
                        nf['outrosvalores'] = row[9]
                        nf['djson'] = {}
                        nf['status'] = fisconstants.NOTAFISCAL_GERADA
                        nf['bcicms'] = '0.00'
                        nf['tipo_es'] = fisconstants.NOTAFISCAL_TIPO_SAIDA
                        nf['tipo_nf'] = fisconstants.NOTAFISCAL_SERVICO
                        nf['cfop'] = cfop
                        nf['usuario_g'] = usuario
                        nf['usuario_c'] = usuario
                        nf['djson']['documento'] = row[7]
                        nf['djson']['contrato'] = row[8]
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
                        nfitem['descricao'] = '%s - %s - %s'%(row[10], row[12], row[24])
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
                            try:
                                titulo = fmodels.Titulo.objects.filter(cliente=cliente, portador=int(row[16]), valor=row[23], data_vencimento=row[14])
                                if len(titulo) > 0:
                                    # Cria nota fiscal com titulo
                                    nft = fismodels.NotaFiscalTitulo()
                                    nft.titulo = titulo[0]
                                    nft.notafiscal = new_nf
                                    nft.save()
                            except:
                                continue
            else:
                print('empresa não identificada')