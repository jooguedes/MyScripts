#!/usr/bin/python
# -*- coding: utf-8 -*-
from django.core.wsgi import get_wsgi_application
from datetime import date, datetime
from unicodedata import normalize
from django.conf import settings
from decimal import Decimal
import argparse
import shutil
import codecs
import copy
import csv
import sys
import os
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str,help='settings django', required=True)
parser.add_argument('--sync', dest='sync_db', type=bool, help='Sync Database', default=False)
parser.add_argument('--pop', dest='pop_id', type=int,help='Pop ID', required=False)
parser.add_argument('--nas', dest='nas', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--planos', dest='planos', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--portadores', dest='portadores', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--clientes', dest='clientes', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--telefones', dest='telefones', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--emails', dest='emails', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--titulos', dest='titulos', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--chamados', dest='chamados', type=str,help='Arquivo importacao', required=False)
parser.add_argument('--anotacoes', dest='anotacoes', type=str,help='Arquivo importacao', required=False)


# python import_controllr.py --settings=sgp.local.settings --nas=controllr-nas.csv
# python import_controllr.py --settings=sgp.local.settings --planos=controllr-planos.csv
# python import_controllr.py --settings=sgp.local.settings --portadores=controllr-portadores.csv
# python import_controllr.py --settings=sgp.local.settings --pop=12 --clientes=controllr-clientes.csv --sync=1
# python import_controllr.py --settings=sgp.local.settings --emails=controllr-emails.csv
# python import_controllr.py --settings=sgp.local.settings --telefones=controllr-telefones.csv
# python import_controllr.py --settings=sgp.local.settings --titulos=controllr-titulos.csv --sync=1
# python import_controllr.py --settings=sgp.local.settings --chamados=controllr-chamados.csv
# python import_controllr.py --settings=sgp.local.settings --anotacoes=controllr-anotacoes.csv


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

# Definir ip para plano default
plano_id_default = 1079

formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

ustr = lambda x: unicode(str(x).upper()).strip()
fnum = lambda n: re.sub('[^0-9.]','',n)

def convertdata(d):
    try:
        d_, m_, y_ = d.strip().split('-')
        date(int(y_), int(m_), int(d_))
        return '%s-%s-%s' % (y_, m_, d_)
    except:
        return None

if args.nas:
    with open(args.nas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if nmodels.NAS.objects.filter(id=row[0]).count() == 0:
                print(row)
                new_nas = nmodels.NAS()
                new_nas.id = row[0].strip()
                new_nas.descricao = row[1].strip()
                if row[2].strip() == 'f':
                  new_nas.active == False 
                new_nas.shortname = row[3].strip()
                if row[3].strip() == '':
                    new_nas.shortname = 'shortname_%s'%row[0]
                new_nas.nasname = row[4].strip()
                new_nas.secret = row[5]
                new_nas.xuser = row[6]
                new_nas.xtype = 'mikrotik'
                new_nas.xpassword = row[7]
                new_nas.ports = row[8]
                try:
                    new_nas.save()
                except:
                    new_nas.nasname = '172.0.0.%s'%row[0].strip()
                    new_nas.save()


if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if admmodels.Plano.objects.filter(descricao=row[0]).count() == 0:
                print(row)
                new_plano = admmodels.Plano()
                new_plano.id = row[0].strip()
                new_plano.descricao = row[1]
                new_plano.preco = row[2]
                if row[2] == '':
                    new_plano.preco = 0.00
                new_plano.grupo = grupo_obj
                new_plano.contrato = contrato_obj
                new_plano.data_cadastro=datetime.now()
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.id = row[0].strip()
                new_plano_internet.plano = new_plano
                new_plano_internet.modo_velocidade = 'mb'
                if row[3].strip() != '':
                    new_plano_internet.upload = int(row[3])
                elif row[5].strip() != '':
                    new_plano_internet.upload = int(row[5])
                else:
                    new_plano_internet.upload = 1024
                if row[4].strip() != '':
                    new_plano_internet.download = int(row[4])
                elif row[6].strip() != '':
                    new_plano_internet.download = int(row[6])
                else:
                    new_plano_internet.download = 2048
                try:
                  new_plano_internet.save()
                except Exception as a:
                  print('Erro ao cadastrar o PLANO: %s'%a)

if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print(row)
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[2][:25]
                new_portador.codigo_banco = fnum(row[1])
                if fnum(row[1]) == '0' or fnum(row[1]) == '':
                  new_portador.codigo_banco = '999'
                new_portador.cedente = 'PROVEDOR X'
                if row[3].strip() != '':
                  new_portador.cedente = row[3].strip()

                new_portador.agencia = row[8] or '0'
                new_portador.agencia_dv = row[9]
                new_portador.conta = row[10] or '0'
                new_portador.conta_dv = row[11]
                new_portador.carteira = row[12]
                new_portador.convenio = row[13]
                new_portador.cpfcnpj = '0'
                new_portador.save()

            if fmodels.GatewayPagamento.objects.filter(portadores__id=row[0]).count() == 0:
                if row[1].strip() in ['gerencianet', 'boleto_facil', 'boletofacil', 'fortunus', 'juno', 'widepay', 'galaxPay']:
                    new_gateway_pagamento = fmodels.GatewayPagamento()
                    new_gateway_pagamento.descricao = row[2]
                    new_gateway_pagamento.gerencia_boleto = True
                    if row[8]:
                        new_gateway_pagamento.token = row[8]
                    if row[6]:
                        new_gateway_pagamento.usuario = row[6]
                    if row[7]:
                        new_gateway_pagamento.senha = row[7]
                    if row[1] == 'fortunus' or 'gerencianet':
                        new_gateway_pagamento.nome = 'gerencianet'
                    elif row[1] == 'boleto_facil' or 'boletofacil':
                        new_gateway_pagamento.nome = 'boletofacil'
                    elif row[1]== 'galaxpay':
                        new_gateway_pagamento.nome='galaxpay'
                    elif row[1]== 'galaxpay':
                        new_gateway_pagamento.nome='galaxpay'
                    else:
                        new_gateway_pagamento.nome = 'gerencianetapi'
                    new_gateway_pagamento.save()
                    new_portador = fmodels.Portador.objects.get(id=row[0])
                    new_gateway_pagamento.portadores.add(new_portador)

         

if args.clientes:
    nas_default = nmodels.NAS.objects.all()[0]
    pop_default = admmodels.Pop.objects.get(pk=args.pop_id)
    formacobranca = fmodels.FormaCobranca.objects.all()[0]

    m = manage.Manage()

    with codecs.open(args.clientes, 'ru') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            # CLIENTE
            idCliente = row[0]
            data_cadastro_cliente = row[1].split()[0].strip()
            if row[8].strip() == '' or row[1].strip() in ['0000-00-00 00:00:00']:
                data_cadastro_cliente = datetime.now()

            data_nascimento = row[2]
            nome = ustr(row[3])
            cliente_obs = row[4]
            cpfcnpj = row[5]
            rgie = row[6]
            if row[7].strip() == 't':
                status_c = 3
            else:
                status_c = 1
            if row[8].strip() == '' or row[8].strip() in ['0000-00-00 00:00:00']:
                data_cadastro_alteracao = data_cadastro_cliente
            else:
                data_cadastro_alteracao =  row[8].split()[0].strip()
            nomefantasia = row[9]

            # ENDEREÇO DE CADASTRO
            end_cadastro = {}
            end_cadastro['logradouro'] = row[10].strip()
            try:
                end_cadastro['numero'] = int(fnum(row[11]))
            except:
                end_cadastro['numero'] = None
            end_cadastro['bairro'] = row[12].strip()
            end_cadastro['cidade'] = row[13].strip()
            end_cadastro['uf'] = row[14].strip()
            end_cadastro['cep'] = row[15].strip()
            end_cadastro['complemento'] = row[16].strip()
            end_cadastro['map_ll'] = '%s, %s'%(row[17].strip(), row[18].strip())
            
            # CONTRATO
            idContrato = row[19]
            try:
                vencimento = int(row[21].strip())
            except:
                vencimento = 10
            isento = int(row[22].strip())
            data_cadastro_contrato = row[23].split()[0].strip()
            status_s = 1
            status_cc = 1
            if row[24].strip() == '0':
                status_s = 3
                status_s = 3

            if row[25].strip() == 't':
                status_s = 4
                status_s = 4
            
            if row[40].strip() == '0':
                status_s = 3
                status_cc = 3
            
            contrato_obs = row[26].strip()
            portador_id = int(fnum(row[29]))
            portador_descricao = row[30].strip()


            end_cadastro_cob = {}
            if (len(row[31].strip()) < 10 
                and len(fnum(row[32].strip())) < 1 
                and len(row[33].strip()) < 3 
                and row[38].strip() == '0' 
                and row[39].strip() == '0'):

                end_cadastro_cob = end_cadastro

            else:
                end_cadastro_cob['logradouro'] = row[31].strip()
                try:
                    end_cadastro_cob['numero'] = int(fnum(row[32]))
                except:
                    end_cadastro_cob['numero'] = None
                end_cadastro_cob['bairro'] = row[33].strip()
                end_cadastro_cob['cidade'] = row[34].strip()
                end_cadastro_cob['uf'] = row[35].strip()
                end_cadastro_cob['cep'] = row[36].strip()
                end_cadastro_cob['complemento'] = row[37].strip()
                end_cadastro_cob['map_ll'] = '%s, %s'%(row[38].strip(), row[39].strip())
            
            login = row[41].strip()
            senha = row[42].strip()

            ip = row[43].strip()
            if len(ip) < 6:
                ip = None
            mac = row[45].strip()
            mac_dhcp = row[45].strip()
            if len(mac) < 10:
                mac = None
                mac_dhcp = None

            try:
                plano_id = int(row[46].strip())
            except:
                plano_id = plano_id_default

            # Endereço de Instalação
            if (len(row[47].strip()) < 10 
                and len(fnum(row[48].strip())) < 1 
                and len(row[49].strip()) < 3 
                and row[54].strip() == '0' 
                and row[55].strip() == '0'):
                
                end_cadastro_int = end_cadastro_cob

            else:
                end_cadastro_int = {}
                end_cadastro_int['logradouro'] = row[47].strip()
                try:
                    end_cadastro_int['numero'] = int(fnum(row[48]))
                except:
                    end_cadastro_int['numero'] = None
                end_cadastro_int['bairro'] = row[49].strip()
                end_cadastro_int['cidade'] = row[50].strip()
                end_cadastro_int['uf'] = row[51].strip()
                end_cadastro_int['cep'] = row[52].strip()
                end_cadastro_int['complemento'] = row[53].strip()
                end_cadastro_int['map_ll'] = '%s, %s'%(row[54].strip(), row[55].strip())

            servico_obs = row[56].strip()
            nas_id = row[57].strip()
            if nas_id == '':
                nas_id = 12

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print("erro vencimento %s"%vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save()
            
            comodato = False
            conexao_tipo = 'ppp'
            status_criar = [6, 2, status_cc]


            print(idCliente, nome, nomefantasia, cpfcnpj, len(cpfcnpj), data_cadastro_cliente, data_nascimento, cliente_obs)
            print(end_cadastro)
            print(idContrato, vencimento, data_cadastro_contrato, contrato_obs, isento, portador_id, portador_descricao)
            print(end_cadastro_cob)
            print(login, senha, ip, mac, admmodels.PlanoInternet.objects.get(id=plano_id), nmodels.NAS.objects.get(id=nas_id))
            print(end_cadastro_int)
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__lower=login.strip().lower()).count() == 0:
                print("| Import %s - %s | %s"%(nome, 
                                              cpfcnpj,
                                              "\n---------------------------------------------\n"))

                cliente_check = admmodels.Cliente.objects.filter(id=idCliente)

                if len(cliente_check) == 0: 
                    # Endereço
                    new_endereco = admmodels.Endereco(**end_cadastro)
                    new_endereco_cob = admmodels.Endereco(**end_cadastro_cob)
                    new_endereco_inst = admmodels.Endereco(**end_cadastro_int)

                    new_endereco.save()
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    # Portador
                    try:
                        portador = fmodels.Portador.objects.get(pk=portador_id)
                    except:
                        try:
                            portador = fmodels.Portador.objects.get(descricao__lower__iexact=portador_descricao)
                        except:
                            portador = fmodels.Portador.objects.get(id=22)

                    # Pessoa
                    tp = 'f'
                    if len(fnum(cpfcnpj)) > 12:
                        tp = 'j'

                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'

                        new_pessoa.nome = nome
                        new_pessoa.datanasc = data_nascimento
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.naturalidade = ''
                        new_pessoa.rg = rgie.strip()[:25]
                        new_pessoa.cpfcnpj = cpfcnpj.strip()[:25]
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
                        new_pessoa.nomefantasia = nomefantasia
                        new_pessoa.cpfcnpj = cpfcnpj.strip()[:25]
                        new_pessoa.insc_estadual = rgie.strip()[:25]
                        new_pessoa.tipo = 8
                        new_pessoa.save()

                    # Cliente
                    new_cliente = admmodels.Cliente()
                    new_cliente.id = idCliente
                    new_cliente.pessoa = new_pessoa
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    if str(data_cadastro_cliente) in ('0000-00-00'):
                        data_cadastro_cliente = datetime.now()
                    new_cliente.data_cadastro = data_cadastro_cliente
                    new_cliente.data_alteracao = data_cadastro_alteracao
                    new_cliente.ativo = True
                    new_cliente.observacao = cliente_obs
                    new_cliente.save()
                    new_cliente.data_cadastro = data_cadastro_cliente
                    new_cliente.save()

                else:
                    
                    new_endereco = cliente_check[0].endereco
                    new_endereco_cob = admmodels.Endereco(**end_cadastro_cob)
                    new_endereco_inst = admmodels.Endereco(**end_cadastro_int)

                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    new_cliente = cliente_check[0]

                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob

                try:
                    new_cobranca.portador = fmodels.Portador.objects.get(
                        pk=portador_id)
                except:
                    new_cobranca.portador = fmodels.Portador.objects.all()[0]

                new_cobranca.vencimento = fmodels.Vencimento.objects.get(
                    dia=vencimento)
                new_cobranca.isento = isento
                new_cobranca.notafiscal = False
                if str(data_cadastro_contrato) in ('0000-00-00 '):
                    data_cadastro_contrato = datetime.now()
                new_cobranca.data_cadastro = data_cadastro_contrato
                new_cobranca.datacobranca1 = data_cadastro_contrato
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = status_c
                new_cobranca.save()

                new_cobranca.data_cadastro = data_cadastro_contrato
                new_cobranca.save()

                # Contrato
                new_contrato = admmodels.ClienteContrato()
                new_contrato.id = idContrato

                new_contrato.cliente = new_cliente
                new_contrato.pop = pop_default
                new_contrato.cobranca = new_cobranca

                new_contrato.data_inicio = data_cadastro_contrato
                new_contrato.data_cadastro = data_cadastro_contrato
                new_contrato.data_alteracao = data_cadastro_contrato
                new_contrato.save()
                new_contrato.data_cadastro = data_cadastro_contrato
                new_contrato.data_alteracao = data_cadastro_contrato
                new_contrato.save()

                for ic in status_criar:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo = 2
                    new_status.usuario = usuario
                    new_status.data_cadastro = data_cadastro_contrato
                    new_status.save()

                    new_status.data_cadastro = data_cadastro_contrato
                    new_status.save()

                # Servico
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                new_servico.login = login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password = senha
                new_servico.login_password_plain = senha
                new_servico.central_password = senha
                if admmodels.ServicoInternet.objects.filter(mac_dhcp=mac_dhcp).count() == 0:
                    new_servico.mac_dhcp = mac_dhcp
                if admmodels.ServicoInternet.objects.filter(mac=mac).count() == 0:
                    new_servico.mac = mac

                if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                    new_servico.ip = ip
                new_servico.tipoconexao = conexao_tipo
                try:
                    new_servico.nas = nmodels.NAS.objects.get(id=nas_id)
                except:
                    nmodels.NAS.objects.all().order_by('-id')[0]
                new_servico.planointernet = admmodels.PlanoInternet.objects.get(id=plano_id)
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.data_cadastro = data_cadastro_contrato
                try:
                    new_servico.save()
                except:
                    new_servico.mac_dhcp = None
                    new_servico.mac = None
                    new_servico.save()

                new_servico.data_cadastro = data_cadastro_contrato
                new_servico.save()

                m.addRadiusServico(new_servico)

if args.emails:
  with open(args.emails, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
          try:
            cliente = admmodels.Cliente.objects.get(id=row[3])
            email = row[2]
            con_obs = row[1]
            if len(email) > 4 and cliente:
                new_contato = admmodels.Contato()
                new_contato.tipo = 'EMAIL'
                new_contato.contato = email
                new_contato.observacao = con_obs
                new_contato.save()
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()
                print(row)
          except Exception as a:
            print('Erro ao cadastrar EMAIL, erro: %s'%a)
            continue
  
if args.telefones:
    with open(args.telefones, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            
            try:
                cliente = admmodels.Cliente.objects.get(id=row[4])
            
                
                telefone = row[2]
                con_obs = '%s - %s'%(row[1], row[3])
                if len(telefone) > 4 and cliente:
                    print('entrei no if do cadastro')
                    new_contato = admmodels.Contato()
                    new_contato.tipo = 'CELULAR_COMERCIAL'
                    new_contato.contato = telefone
                    new_contato.observacao = con_obs
                    new_contato.save()
                    new_ccontato = admmodels.ClienteContato()
                    new_ccontato.cliente = cliente
                    new_ccontato.contato = new_contato
                    try:
                        new_ccontato.save()
                        print(row)
                    except Exception as a:
                        print('Erro ao cadastrar TELEFONE, erro: %s'%a)
            except Exception as e:
                print ("Cliente não encontrato, erro: %s",e)



if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            formapagamento = fmodels.FormaPagamento.objects.all()[0]
            planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
            cliente = admmodels.Cliente.objects.filter(id=fnum(row[10]))
            if cliente:
                cliente = cliente[0]
                try:
                    contrato = admmodels.ClienteContrato.objects.filter(id=row[11].strip())
                except:
                   continue
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    
                    numero_documento = row[14].strip()
                    if numero_documento == '':
                        numero_documento = row[0]
                    nosso_numero = row[14]
                    if nosso_numero == '':
                        nosso_numero = numero_documento
                    nosso_numero_f = None
                    valor = row[2].strip()
                    if valor == '':
                        continue
                    data_vencimento = row[6]
                    data_documento = row[7].split()[0].strip()
                    if row[8].strip() == '':
                        data_pagamento = None
                    else:
                        data_pagamento = row[8].split()[0].strip()
                    data_baixa = data_pagamento
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None
                    idtransacao = row[14]

                    link = row[15]
                    juros = 0.00
                    carne_id = ''
                    carne_link = ''
                    portador = fmodels.Portador.objects.get(id=54)

                    if data_pagamento != None and row[3].strip() != '':
                        valorpago = row[3].strip()
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None

                    elif 't' in row[13]:
                        data_cancela = data_vencimento
                        status = fmodels.MOVIMENTACAO_CANCELADA
                        data_baixa = None
                        data_pagamento = None
                        usuario_b = None
                        usuario_c = usuario

                    desconto = row[9]
                    if desconto == '':
                        desconto =  0.00
                    linha_digitavel = row[16]
                    codigo_barras = ''
                    codigo_carne = ''
                    chave = ''
                    if link:
                        try:
                            chave = "-".join(link.split('/')[-1].split('-')[-3:]).strip()
                        except Exception as e:
                            print(e)

                    if fmodels.Titulo.objects.filter(portador=portador, nosso_numero=nosso_numero).count() == 0:
                        dados = {'cliente': cliente,
                                    'cobranca': cobranca,
                                    'portador': portador,
                                    'formapagamento': formapagamento,
                                    'centrodecusto': planocontas,
                                    'modogeracao': 'l',
                                    'usuario_g': usuario,
                                    'usuario_b': usuario_b,
                                    'usuario_c': usuario_c,
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
                                    'observacao': codigo_carne,
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

                                if idtransacao != '' and link != '':
                                    novo_titulogateway = fmodels.TituloGateway()
                                    novo_titulogateway.titulo = titulo
                                    novo_titulogateway.gateway = titulo.portador.gateway_boleto
                                    novo_titulogateway.idtransacao = idtransacao
                                    novo_titulogateway.link = link
                                    novo_titulogateway.djson={'carne_id': carne_id,'carne_link': carne_link,'chave': chave}
                                    novo_titulogateway.save()

                            except Exception as e:
                                print("Erro cadastrar",e,dados)
                else:
                    print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)


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

    with open(args.chamados, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            protocolo = row[1].strip()
            if protocolo == '':
                protocolo = row[0].strip()
            if len(protocolo) > 14:
                protocolo = protocolo[0:13]
            idCliente = int(row[14].strip())
            
            try:
                idContrato = int(row[15].strip())
            except:
                idContrato = None

            assunto = row[3][:30]
            if row[7].strip() == '':
                status = amodels.OCORRENCIA_ABERTA
            else:
                status = amodels.OCORRENCIA_ENCERRADA
            try:
                data_cadastro = row[5].split()[0]
            except:
                data_cadastro = datetime.now()

            try:
                data_agendamento = row[6].split()[0]
            except:
                data_agendamento = None

            try:
                data_finalizacao = row[7].split()[0]
            except:
                data_finalizacao = None
            conteudo = 'Tipo:  %s | Descrição: %s | Observação: %s'%(row[13], row[2], row[3])
            if conteudo == "" or conteudo is None:
                conteudo = "Campo conteúdo vazio no ReceitaNet."
            servicoprestado = row[9]

            try:
                clientecontrato = admmodels.ClienteContrato.objects.filter(id=idContrato)[0]
            except:
                try:
                    clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=idCliente)[0]
                except:
                    continue

            if clientecontrato:
                try:
                    tipo_obj = amodels.Tipo.objects.get(descricao=row[12][:25])
                except:
                    tipo_obj = amodels.Tipo()
                    tipo_obj.codigo=cdtipo
                    tipo_obj.descricao=row[12][:25]
                    try:
                        tipo_obj.save()
                        cdtipo += 1
                    except:
                        continue
                
                try:
                    motivo_obj = amodels.MotivoOS.objects.get(descricao=row[12][:25])
                except:
                    motivo_obj = amodels.MotivoOS()
                    motivo_obj.codigo=cdmotivo
                    motivo_obj.descricao=row[12][:25]
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
                    ocorrencia['status'] = status
                    ocorrencia['responsavel'] = ocorrencia['usuario']

                    ocorrencia['data_cadastro'] = data_cadastro
                    ocorrencia['data_agendamento'] = data_agendamento
                    ocorrencia['data_finalizacao'] = data_finalizacao
                    ocorrencia['conteudo'] = conteudo
                    for ok in ocorrencia:
                        if ocorrencia[ok] in ['0000-00-00 00:00:00','0000-00-00','']:
                            ocorrencia[ok] = None

                    new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                    try:
                        new_ocorrencia.save()
                    except Exception as a:
                        print('Erro ao cadastrar OC, erro: %s'%a)

                    new_ocorrencia.data_cadastro = data_cadastro
                    new_ocorrencia.data_agendamento = data_agendamento
                    new_ocorrencia.data_finalizacao = data_finalizacao

                    if str(new_ocorrencia.data_agendamento) in ['0000-00-00 00:00:00','0000-00-00','']:
                        new_ocorrencia.data_agendamento = None
                    if str(new_ocorrencia.data_finalizacao) in ['0000-00-00 00:00:00','0000-00-00','']:
                        new_ocorrencia.data_finalizacao = None
                    new_ocorrencia.save()

                    ordem = {}
                    ordem['ocorrencia'] = new_ocorrencia
                    ordem['status'] = amodels.OS_ENCERRADA if row[7].strip() == '' else amodels.OS_ABERTA
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
                    except Exception as a:
                        print('Erro ao cadastrar OS, erro: %s'%a)

                    if servicoprestado != '':
                        new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                        new_ocorrencia_anotacao.ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
                        new_ocorrencia_anotacao.anotacao=servicoprestado
                        new_ocorrencia_anotacao.usuario= usuario
                        new_ocorrencia_anotacao.save()

if args.anotacoes:
    with open(args.anotacoes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            idCliente = fnum(row[4])
            idContrato = fnum(row[6])
            if idContrato != '':
                try:
                    clientecontrato = admmodels.ClienteContrato.objects.filter(id=int(idContrato)+1000)[0]
                except Exception as a:
                    print('Erro ao consultar idContrato, erro: %s'%a)
            else:
                try:
                    clientecontrato = admmodels.ClienteContrato.objects.filter(cliente__id=int(idCliente)+1000)[0]
                except Exception as a:
                    print('Erro ao consultar idContrato, erro: %s'%a)

            anotacao = 'Usuário: %s \nConteúdo: %s\n'%(row[2].strip(), row[0])
            if row[5].strip() != '':
                anotacao += 'Observações: %s'%row[5]
                
            status = 'Ativa' if row[3].strip() == '0' else 'Deletada'
            data_cadastro = row[1].split()[0]
            if status == 'Ativa' and admmodels.ClienteAnotacao.objects.filter(anotacao=anotacao).count() == 0:
                new_anotacoes = admmodels.ClienteAnotacao()
                new_anotacoes.clientecontrato=clientecontrato
                new_anotacoes.cliente=clientecontrato.cliente
                new_anotacoes.anotacao=anotacao
                new_anotacoes.data_cadastro=datetime.now()
                new_anotacoes.usuario=usuario
                try:
                    new_anotacoes.save()
                    print('Importando Anotação: | %s'%new_anotacoes)
                except Exception as a:
                    print('idCliente: %s - idContrato: %s | Erro: %s'%(idCliente, idContrato, a))
