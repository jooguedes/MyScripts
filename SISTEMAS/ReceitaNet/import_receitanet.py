#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
from decimal import Decimal
import copy
from tkinter import NO
from unicodedata import normalize
import csv
import re

parser = argparse.ArgumentParser(description='Importação csv 1')

parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--loginsplanos', dest='loginsplanos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--notasfiscais',dest='notasfiscais',type=str,help='Arquivo importacao',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--pop', dest='pop', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--suportes', dest='suportes', type=str, help='Arquivo importacao',required=False)

'''
python import_receitanet.py --settings=sgp.proconnect.settings --portador=3 --nas=2 --pop=2 --clientes=receitanet-clientes.csv --loginsplanos=receitanet-mensalidades.csv --sync=1
python import_receitanet.py --settings=sgp.proconnect.settings --portador=3 --titulos=arquivo.csv 
python import_receitanet.py --settings=sgp.proconnect.settings --portador=3 --suportes=receitanet-suportes.csv
'''

addIdCliente = 500
addIdContrato = 500
addStringLogin = 'import_receitanet_4679'
addNumeroOcorrencia = 0

args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q
from django.db import transaction

from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.fiscal import constants as fisconstants
from apps.fiscal import models as fismodels
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
fnum2 = lambda n: re.sub('[^0-9.,]', '', unicode(n))
usuario = admmodels.User.objects.get(username='sgp')
m = manage.Manage()

logins_nao_encontrado=[]
"""INCREMENTAR PARA BASES JÁ EM USO"""
id_inclemneto=0
login_string=''

def convertdata(d):
    if "-" in d:
        return d
    else:
        try:
            d_,m_,y_ = d.strip().split('/')
            date(int(y_),int(m_),int(d_))
            return '%s-%s-%s' %(y_,m_,d_)
        except:
            return None


portador = fmodels.Portador.objects.get(pk=args.portador)
if args.clientes:

    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='cabo').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='cabo').order_by('-id')[0]
    nas = nmodels.NAS.objects.get(pk=args.nas)
    portador = fmodels.Portador.objects.get(pk=args.portador)

    print('Importando clientes')
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:   
            sexo = ''
            naturalidade = ''
            estadocivil = ''

            nome_pai = ''
            nome_mae = ''
            comodato = False
            profissao = ''

            notafiscal = False

            con_obs=''
            conexao_tipo = 'ppp'

            isento = 0
            nao_suspende = False 

            #idcliente = row[0]
            login = '%s%s'%(row[0].strip(),addStringLogin)
            senha = row[1]
            cnpj = row[2]
            cpf = row[3]
            cpfcnpj = cnpj #or cpf
            rg = row[3]
            rg_emissor = ''
            insc_estadual = ''


            senha_central = cpfcnpj
            
            if cnpj:
                insc_estadual = row[3]
            nome = row[4]
            nomefantasia = row[4]
            
            endereco = {}
            endereco['logradouro'] = row[5]
            endereco['pontoreferencia'] = row[6]
            endereco['map_ll']=str(row[27])+',' + str(row[28])

            if endereco['map_ll']=='':
                endereco['map_ll']=None

            endereco['cidade'] = row[7]
            endereco['uf'] = row[8]
            endereco['bairro'] = row[9]
            endereco['cep'] = row[10]
            endereco['complemento'] = row[11]

            vencimento = row[12]
            telefones = [row[13],row[14],row[15]]
            
            data_nasc=  row[17]
            if data_nasc=='':
                data_nasc=None
            data_cadastro = row[18]
            if data_cadastro=='':
                data_cadastro=datetime.now()
            
            data_inicio = row[19]
            if data_inicio=='':
                data_inicio=None
           
            data_ativacao = row[20]
            if data_ativacao=='':
                data_ativacao=None
            data_bloqueio = row[21]
            if data_bloqueio=='':
                data_bloqueio=None

            data_cancela = row[22]
            if data_cancela=='':
                data_cancela=None 
           
            #cli_obs = row[24]
            emails = []
            if row[23]:
                emails = row[23].split(';')

            mac = row[24]
            map_ll = '%s,%s' %(row[27],row[28])
            ip = row[30]


            if  ip == '' or not ip:
                ip = None
            if mac=='' or not mac:
                mac = None



            status_cc = 1
            status_s = 1
            status_c = 1

            if data_bloqueio:
                status_cc = 4
                status_s = 4
                status_c = 4
            if data_cancela:
                status_cc = 3
                status_s = 3
                status_c = 3

            respempresa = ''
            respcpf = ''

            plano ="plano_default"   #'%s - %s' %(row[33],row[37])
            plano_valor = '0.00'
            plano_download = 10240
            plano_upload = 10240 

            #login = row[22]
            if not login:
                continue

            #senha = row[23]
            if not senha:
                senha = login


            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                print(plano,plano_valor,plano_download,plano_upload)
                new_plano = admmodels.Plano()
                new_plano.descricao=plano
                new_plano.preco = plano_valor
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj
                new_plano.save()
                planointernet = admmodels.PlanoInternet()
                planointernet.plano = new_plano
                planointernet.download = plano_download
                planointernet.upload = plano_upload
                planointernet.save()

            try:
                new_vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                try:
                    print('criando vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento or 10
                    new_vencimento.save()
                except:
                    new_vencimento = fmodels.Vencimento.objects.get(dia=10)



            '''cidade_q = normalize('NFKD', unicode(endereco.get('cidade'))).encode('ASCII','ignore')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=endereco.get('uf')
                new_pop.save()
                pop = new_pop
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                
            '''
            pop=admmodels.Pop.objects.get(id=args.pop)

            print (nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc)
            print (nome_pai, nome_mae, naturalidade)
            print (endereco)
            print ('vencimento: ', vencimento, 'Plano: ', plano)
            print (telefones,emails)
            print (login,senha,ip,mac)
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=login).count() == 0:
                print "Import %s" %nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj)

                if len(cliente_check) == 0:

                    # Endereco
                    new_endereco = admmodels.Endereco(**endereco)
                    new_endereco_cob = admmodels.Endereco(**endereco)
                    new_endereco_inst = admmodels.Endereco(**endereco)
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
                        new_pessoa.naturalidade = naturalidade
                        new_pessoa.rg = rg
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
                        new_pessoa.insc_estadual = insc_estadual
                        #new_pessoa.insc_municipal = insc_municipal
                        new_pessoa.tipo = 8
                        new_pessoa.save()

                    # Cliente
                    new_cliente = admmodels.Cliente()
                    new_cliente.id = addIdCliente
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    try:
                        new_cliente.save()
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.save()
                        addIdCliente += 1
                    except Exception as e:
                        print('Erro ao cadastrar CLIENTE, erro: ', e)

                    # contato 1
                    for email in emails:
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
                    for celular in telefones:
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

                else:
                    new_endereco_cob = admmodels.Endereco(**endereco)
                    new_endereco_inst = admmodels.Endereco(**endereco)
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    new_cliente = cliente_check[0]


                # Cobranca
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob
                new_cobranca.portador = portador
                try:
                    new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
                except:
                   new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=10) 
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
                new_contrato.id=addIdContrato
                new_contrato.cliente = new_cliente
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca

                new_contrato.data_inicio = data_cadastro
                new_contrato.data_cadastro = data_cadastro
                new_contrato.data_alteracao = data_cadastro
                try:
                    new_contrato.save()
                    new_contrato.data_inicio = data_cadastro
                    new_contrato.data_cadastro = data_cadastro
                    new_contrato.data_alteracao = data_cadastro
                    new_contrato.save()
                    addIdContrato += 1
                except Exception as e:
                    print('Erro ao cadastrar CONTRATO, erro: ', e)


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
                if admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=login).count() > 0:
                    print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                      login,
                                                                                      str(new_contrato.id))
                    login += str(new_contrato.id)
                new_servico.login= login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password=senha
                new_servico.login_password_plain=senha
                new_servico.central_password=senha
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.ip=ip
                new_servico.mac=mac
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao = 1 if comodato == True else 0
                new_servico.data_cadastro=data_cadastro
                #new_servico.observacao=cli_obs
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)



if args.loginsplanos:
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='cabo').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='cabo').order_by('-id')[0]
    with open(args.loginsplanos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row[0],row[1])
            #login_busca=str(row[0])+str(login_string)
            try:
                login = '%s%s'%(row[0].strip(), addStringLogin)
                servico = admmodels.ServicoInternet.objects.filter(login__lower__lower=login.lower())
            except Exception as e:
                print(e)
            plano_nome = row[1]
            if servico:
                print("entrei no servico")
                try:
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano_nome)[0]
                except:
                    new_plano = admmodels.Plano()
                    new_plano.descricao=plano_nome
                    new_plano.preco = '0.00'
                    new_plano.contrato = contrato_obj
                    new_plano.grupo = grupo_obj
                    new_plano.save()
                    planointernet = admmodels.PlanoInternet()
                    planointernet.plano = new_plano
                    planointernet.download = 20480
                    planointernet.upload = 20480
                    planointernet.save()

                servico[0].planointernet = planointernet 
                servico[0].save()
            else:
                print('servico não encontrado', servico)


if args.titulos:
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print row[3]
            login = row[3]
            if login != '':
                try:
                    login = '%s%s'%(row[0].strip(),addStringLogin)
                    servico = admmodels.ServicoInternet.objects.get(login__trim__lower=login.lower())
                except Exception as e:
                    logins_nao_encontrado.append(login)
                    print(e)
                    continue
                contrato = servico.clientecontrato
                cobranca = contrato.cobranca
                cliente = contrato.cliente
                if cobranca:
                    if fmodels.Titulo.objects.filter(portador=portador,
                                                    numero_documento=row[0]).count() == 0:
                        print row
                        tdata = {}
                        tdata['cliente'] = cliente
                        tdata['cobranca'] = cobranca
                        tdata['nosso_numero'] = row[0] # nrboleto
                        tdata['numero_documento'] = row[0] # documento
                        if not tdata['nosso_numero']:
                            tdata['nosso_numero'] = tdata['numero_documento']

                        tdata['parcela'] = 1
                        tdata['portador'] = portador
                        tdata['valor'] = fnum2(row[9]).replace(',','.')
                        tdata['observacao'] = row[2]
                        tdata['demonstrativo'] = 'Período: %s' %row[3]
                        tdata['valorpago'] = fnum2(row[10]).replace(',','.')
                        tdata['data_baixa'] = convertdata(row[5])
                        tdata['data_pagamento'] = convertdata(row[5])
                        tdata['data_documento'] = convertdata(row[4]) # emissao
                        tdata['data_vencimento'] = convertdata(row[6]) # vencimento
                        #tdata['data_cancela'] = row[13]

                        if row[5] == '':
                            tdata['valorpago'] = None
                            tdata['data_baixa'] = None
                            tdata['data_pagamento'] = None

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
                            tdata['usuario_c'] = None
                        #if tdata['data_cancela'] is None:
                        #    tdata['usuario_c'] = None

                        if tdata['data_baixa']:
                            tdata['status'] = fmodels.MOVIMENTACAO_PAGA
                        #elif tdata['data_cancela']:
                        #    tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA
                        else:
                            tdata['status'] = fmodels.MOVIMENTACAO_GERADA
                        if tdata['demonstrativo'] is None:
                            tdata['demonstrativo'] = ''

                        print tdata
                        try:
                            new_titulo = fmodels.Titulo(**tdata)
                            new_titulo.save()
                            new_titulo.data_documento = tdata['data_documento']
                            new_titulo.save()
                        except Exception as e:
                            print(e)
                            pass


if args.notasfiscais:
    with open(args.notafiscal, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj=row[5])
            if cliente:
                cliente = cliente[0]

                nfdest = {}
                nfdest['cliente'] = cliente
                nfdest['cpfcnpj'] = row[5]
                nfdest['inscricaoestadual'] = row[3]
                nfdest['razaosocial'] = row[4]
                nfdest['logradouro'] = row[5]
                nfdest['numero'] = row[6]
                nfdest['complemento'] = row[7]
                nfdest['cep'] = row[8]
                nfdest['bairro'] = row[9]
                nfdest['cidade'] = row[10]
                nfdest['uf'] = row[11]
                nfdest['telefone'] = row[12]
                nfdest['codigocliente'] = row[13]
                nfdest['tipoassinante'] = row[14]

                print nfdest
                nfdest_obj = fismodels.NFDestinatario(**nfdest)
                nfdest_obj.save()

                nf = {}
                nf['destinatario'] = nfdest_obj
                nf['data_emissao'] = '%s-%s-%s 00:00:00' %(row[15][0:4],row[15][4:6],row[15][6:8])
                nf['data_saida'] = '%s-%s-%s 00:00:00' %(row[15][0:4],row[15][4:6],row[15][6:8])
                nf['modelo'] = row[16]
                nf['tipoutilizacao'] = '4'
                nf['serie'] = row[17]
                nf['numero']= row[18]
                nf['valortotal'] = Decimal('%s.%s' %(row[19][:-2],row[19][-2:]))
                nf['icms'] = Decimal('%s.%s' %(row[20][:-2],row[20][-2:]))
                nf['outrosvalores'] = Decimal('%s.%s' %(row[21][:-2],row[21][-2:]))
                if row[23] == 'N':
                    nf['status'] = fisconstants.NOTAFISCAL_GERADA
                else:
                    nf['status'] = fisconstants.NOTAFISCAL_CANCELADA
                    nf['data_cancela'] = '%s-%s-%s' %(row[15][0:4],row[15][4:6],row[15][6:8])
                nf['bcicms'] = Decimal('%s.%s' %(row[24][:-2],row[24][-2:]))

                nf['tipo_es'] = fisconstants.NOTAFISCAL_TIPO_SAIDA
                nf['tipo_nf'] = fisconstants.NOTAFISCAL_SERVICO
                try:
                    nf['cfop'] = fismodels.CFOP.objects.get(cfop=row[27])
                except Exception as e:
                    print e
                    nf['cfop'] = fismodels.CFOP.objects.get(cfop='5307')

                nf['usuario_g'] = usuario
                nf['usuario_c'] = usuario

                print nf

                new_nf = fismodels.NotaFiscal(**nf)
                new_nf.save()
                new_nf.data_emissao=nf['data_emissao']
                new_nf.data_saida=nf['data_saida']
                new_nf.save()

                # Cria nota fiscal com titulo
                nft = fismodels.NotaFiscalTitulo()
                #nft.titulo = titulo
                nft.notafiscal = new_nf
                nft.save()

                if new_nf.notafiscalitem_set.filter(item=int(row[42])).count() == 0:
                    nfitem = {}
                    nfitem['notafiscal'] = new_nf
                    nfitem['descricao'] = row[28]
                    nfitem['codigoservico'] = row[29]
                    nfitem['classificacao'] = row[30]
                    nfitem['unidade'] = row[31]
                    nfitem['qt_contratada'] = row[32]
                    nfitem['qt_fornecida'] = row[33]
                    nfitem['valortotal'] = Decimal('%s.%s' %(row[34][:-2],row[34][-2:]))
                    nfitem['desconto'] = Decimal('%s.%s' %(row[35][:-2],row[35][-2:]))
                    nfitem['acrescimo_despesa'] = Decimal('%s.%s' %(row[36][:-2],row[36][-2:]))
                    nfitem['bcicms'] = Decimal('%s.%s' %(row[37][:-2],row[37][-2:]))
                    nfitem['icms'] = Decimal('%s.%s' %(row[38][:-2],row[38][-2:]))
                    nfitem['outrosvalores'] = Decimal('%s.%s' %(row[39][:-2],row[39][-2:]))
                    nfitem['aliquotaicms'] = Decimal('%s.%s' %(row[41][:-2],row[41][-2:]))
                    nfitem['item'] = int(row[42])
                    nfitem['data_cadastro'] = new_nf.data_emissao
                    nfitem['data_alteracao'] = new_nf.data_emissao

                    print nfitem

                    new_nfitem = fismodels.NotaFiscalItem(**nfitem)
                    new_nfitem.save()
                    new_nfitem.data_cadastro=new_nf.data_emissao
                    new_nfitem.data_alteracao=new_nf.data_emissao
                    new_nfitem.save()

if args.suportes:
    cdtipo = 300
    cdmotivo = 300

    max_tipo = amodels.Tipo.objects.all().order_by('-id')[0]
    if max_tipo.codigo > 200:
        cdtipo = max_tipo.codigo + 1
    max_motivo = amodels.MotivoOS.objects.all().order_by('-id')[0]
    if max_motivo.codigo > 200:
        cdmotivo = max_motivo.codigo + 1

    metodo = amodels.Metodo.objects.all()[0]

    with open(args.suportes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            protocolo = row[1] or row[0]
            if len(protocolo) > 14:
                protocolo = protocolo[0:13]
            login = '%s%s'%(row[2].strip(),addStringLogin)
            assunto = row[4][:30]
            if row[10] == '':
                status = amodels.OCORRENCIA_ABERTA
            else:
                status = amodels.OCORRENCIA_ENCERRADA
            try:
                data_cadastro = row[3].split()[0]
            except:
                data_cadastro = datetime.now()

            try:
                data_agendamento = row[5].split()[0]
            except:
                data_agendamento = None

            try:
                data_finalizacao = row[10].split()[0]
            except:
                data_finalizacao = None
            conteudo = 'TÉCNICO: %s| Tipo:  %s | Valor a Receber: %s | Descriação: %s'%(row[7], row[6], row[8], row[4])
            if conteudo == "" or conteudo is None:
                conteudo = "Campo conteúdo vazio no ReceitaNet."
            servicoprestado = row[9]

            servico = admmodels.ServicoInternet.objects.filter(login__trim__lower=login.lower())

            if servico:
                print('entrei no servico')
                clientecontrato = servico[0].clientecontrato
                try:
                    tipo_obj = amodels.Tipo.objects.get(codigo=5)
                    motivo_obj = amodels.MotivoOS.objects.get(codigo=40)
                    print('Entrei no laco do continue')
                except:
                    continue

                if tipo_obj:
                    tipo_obj = tipo_obj
                else:
                    tipo_obj = amodels.Tipo()
                    tipo_obj.codigo=cdtipo
                    tipo_obj.descricao=assunto[:99]
                    try:
                        tipo_obj.save()
                        cdtipo += 1
                    except:
                        continue

                if motivo_obj:
                    motivo_obj = motivo_obj
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
                    new_ocorrencia.save()

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
                    ordem['status'] = status
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
                    new_ordem.save()

                    if servicoprestado != '':
                        new_ocorrencia_anotacao= amodels.OcorrenciaAnotacao()
                        new_ocorrencia_anotacao.ocorrencia=amodels.Ocorrencia.objects.get(numero=protocolo)
                        new_ocorrencia_anotacao.anotacao=servicoprestado
                        new_ocorrencia_anotacao.usuario= usuario
                        new_ocorrencia_anotacao.save()
print(logins_nao_encontrado)