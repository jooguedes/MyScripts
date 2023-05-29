#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from hashlib import new
import os, sys
from datetime import date, datetime
import copy
from tarfile import ENCODING
from unicodedata import normalize
from decimal import Decimal
import csv
import re

parser = argparse.ArgumentParser(description='Importação csv 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--notasfiscais',dest='notasfiscais',type=str,help='Arquivo importacao',required=False)
parser.add_argument('--notatitulo',dest='notatitulo',type=str,help='Arquivo importacao',required=False)
parser.add_argument('--empresa',dest='empresa',type=str,help='Arquivo importacao',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--pop', dest='pop', type=str, help='Arquivo importacao',required=False)

args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

#python import_radiusnet.py settings=sgp.local.settings clientes=Conv-clientes.csv ---portador=83 --nas=2  --sync=1
#python import_radiusnet.py --settings=sgp.medievalnet.settings --titulos=santander_total.csv --portador=83 --sync=1
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
from apps.fiscal import models as fismodels, constants as fisconstants
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage

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


#id
    #tipo_pessoa
    #status
    #nome
    #cpfcnpj
    #rg
    #data_nascimento
    #nome_fantasia
    #inscricao_estadual
    #inscricaco_municipal
    #data_cadastro
    #nome_plano
    #vencimento
    #ip
    #usuario
    #senha
    #email
    #telefone
    #plano_valor
    #mac
    #status


if args.clientes:

    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='cabo').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='cabo').order_by('-id')[0]
    nas = nmodels.NAS.objects.get(pk=args.nas)
    portador = fmodels.Portador.objects.get(pk=args.portador)

    print('Importando clientes')
    with open(args.clientes, 'rb',  ) as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"', )
        for row in conteudo:   
            row = [entry.decode("utf8") for entry in row] 
            idcliente = int(row[0]) + 50000
            nome = row[2]
            cpfcnpj = row[3]
            nomefantasia = row[4]
            rg = row[5]
            insc_estadual = row[6]
            insc_municipal = row[7]
            data_nasc = convertdata(row[8])
            status = row[9]
            status_cc = 1
            status_s = 1
            status_c = 1

            if status.strip() == 'Bloqueado':
                status_cc = 4
                status_s = 4
                status_c = 4
            if status.strip() == 'Arquivado':
                status_cc = 3
                status_s = 3
                status_c = 3

            respempresa = ''
            respcpf = ''
            cli_obs = ''
            data_cadastro = convertdata(row[10])

            plano = row[11]
            plano_valor = fnum2(row[12]).replace('.','').replace(',','.').replace('R$','')
            plano_download = 2048 
            plano_upload = 2048 

            login ='importacao_radiusnet-08-05-2023%s' %row[13]
            if not login or login=='':
                login = 'semlogin%s' %idcliente 
            senha = row[14]
            if not senha or senha=='':
                senha = login

            ip = row[15]
            mac= row[16]
            if not ip:
                ip = None
            if not mac:
                mac = None

            planointernet=admmodels.PlanoInternet.objects.filter(plano__id=47)[0]
            
            '''try:
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
                planointernet.save()'''

            vencimento = row[17]

            try:
                new_vencimento = fmodels.Vencimento.objects.get(dia=row[17]) or 10
            except:
                try:
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = row[17] 
                    new_vencimento.save()
                except:
                    vencimento=10

            emails = row[18].split(';')
            telefones = row[19].split(';')

            end_inst = row[20].split('-') 
            if len(end_inst) == 1:
                end_inst = 'FALTA PREENCHER, 0  - BAIRRO - São Paulo/SP CEP: 02309130'.split('-')

            end_cob = row[21].split('-')
            if len(end_cob) == 1:
                end_cob = end_inst

    
            
            print(end_inst)
            endereco_inst = {}
            try:
                endereco_inst['cep'] = end_inst[-1].split('CEP:')[1].strip()
            except:
                endereco_inst['cep']='00000000'
            endereco_inst['logradouro'] = end_inst[0].strip()[:50]
            endereco_inst['numero'] = fnum(end_inst[1].strip())[:5]
            if not endereco_inst.get('numero'):
                endereco_inst['numero'] = None
            if len(str(endereco_inst['numero']))>4:
                endereco_inst['numero'] =str(endereco_inst['numero'])[-4:-1]
            endereco_inst['cidade'] = end_inst[-1].split('CEP:')[0].strip().split('/')[0][:50]
            try:
                endereco_inst['uf'] = end_inst[-1].split('CEP:')[0].strip().split('/')[1]
            except:
                endereco_inst['uf']='AC'
            endereco_inst['bairro'] = end_inst[-2].strip()[:50]
            if len(end_inst) > 3:
                endereco_inst['complemento'] = end_inst[-3].strip()[:50]
                endereco_inst['complemento']= endereco_inst['complemento'][:49]
 
            endereco_inst['logradouro']=endereco_inst['logradouro'][:49]
            endereco_inst['cidade']= endereco_inst['cidade'][:49]
            endereco_inst['bairro']= endereco_inst['bairro'][:49]
            endereco_inst['uf'] ==endereco_inst['uf'][:49]
            endereco_inst['cep'] = endereco_inst['cep'][:49]

            print(end_cob)
            endereco_cob = {}
            try:
                endereco_cob['cep'] = end_cob[-1].split('CEP:')[1].strip()
            except:
                endereco_cob['cep']= '0000000'
            endereco_cob['logradouro'] = end_cob[0].strip()[:50]
            endereco_cob['numero'] = fnum(end_cob[1].strip())[:5]
            if not endereco_cob.get('numero'):
                endereco_cob['numero'] = None
            if len(str(endereco_inst['numero']))>4:
                endereco_cob['numero'] =str(end_cob['numero'])[-4:-1]
            endereco_cob['cidade'] = end_cob[-1].split('CEP:')[0].strip().split('/')[0][:50]
            try:
                endereco_cob['uf'] = end_cob[-1].split('CEP:')[0].strip().split('/')[1]
            except:
                endereco_cob['uf'] ='AC'
            endereco_cob['bairro'] = end_cob[-2].strip()[:50]
            if len(end_cob) > 3:
                endereco_cob['complemento'] = end_cob[-3].strip()[:50]
                
                endereco_cob['complemento'] = endereco_cob['complemento'][:49]

            endereco_cob['logradouro'] = endereco_cob['logradouro'][:49]
            endereco_cob['cidade']=  endereco_cob['cidade'][:49]
            endereco_cob['bairro'] =  endereco_cob['bairro'][:49]
            endereco_cob['uf']=endereco_cob['uf'][:49]
            endereco_cob['cep'] =endereco_cob['cep'][:49]
            cidade_q = normalize('NFKD', unicode(endereco_inst.get('cidade'))).encode('ASCII','ignore')

            '''try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=endereco_inst.get('uf')
                new_pop.save()
                pop = new_pop'''
            
            pop= admmodels.Pop.objects.get(id=181)

            rg_emissor = ''
            sexo = ''
            naturalidade = ''
            estadocivil = ''

            nome_pai = ''
            nome_mae = ''


            senha_central = cpfcnpj


            comodato = False
            profissao = ''

            notafiscal = False

            con_obs=''
            conexao_tipo = 'ppp'

            isento = 0
            nao_suspende = False

            print (nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc)
            print (nome_pai, nome_mae, naturalidade)
            print (endereco_inst)
            print ('vencimento: ', vencimento, 'Plano: ', plano)
            print (telefones,emails)
            print (login,senha,ip,mac)
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=login).count() == 0:
                print "Import %s" %nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)

                if len(cliente_check) == 0:
                    
                    # Endereco
                    new_endereco = admmodels.Endereco(**endereco_inst)
                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    print(new_endereco)
                    
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
                        new_pessoa.insc_municipal = insc_municipal
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
                    new_cliente.observacao='Importado do Radius Net'
                    new_cliente.save()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()

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
                    new_endereco_cob = admmodels.Endereco(**endereco_cob)
                    new_endereco_inst = admmodels.Endereco(**endereco_inst)
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    new_cliente = cliente_check[0]
                    #idcliente=int(idcliente)+50000


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
                
               
                new_contrato.id=idcliente

                
                #new_contrato.id=idcliente
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
    portador = fmodels.Portador.objects.get(pk=args.portador)
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            id_cliente = fnum(normalize('NFKD', unicode(row[1])).encode('ASCII','ignore').strip().lower())
            #cpfcnpj=row[2]
            cliente = admmodels.Cliente.objects.filter(id=int(id_cliente)+50000, clientecontrato__pop=181)
            if cliente:
                cliente = cliente[0]
                cobranca_set = cliente.cobranca_set.all()
                if not cobranca_set:
                    cobranca = None 
                else:
                    cobranca = cobranca_set[0]
                if fmodels.Titulo.objects.filter(portador=portador,
                                                 numero_documento=row[0]).count() == 0:
                    print row
                    tdata = {}
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[2] # nrboleto
                    tdata['numero_documento'] = row[0] # documento
                    if not tdata['nosso_numero'] or tdata['nosso_numero']=='':
                        tdata['nosso_numero'] = tdata['numero_documento']

                    tdata['parcela'] = 1
                    tdata['portador'] = portador
                    tdata['valor'] = fnum2(row[6]).replace('R$ ','').replace('.','').replace(',','.')
                    tdata['observacao'] = ''
                    tdata['demonstrativo'] = 'Período: %s' %row[5]
                    tdata['valorpago'] = fnum2(row[8]).replace('R$ ','').replace('.','').replace(',','.')
                    tdata['data_baixa'] = convertdata(row[9])
                    tdata['data_pagamento'] = convertdata(row[9])
                    tdata['data_documento'] = convertdata(row[3]) # emissao
                    tdata['data_vencimento'] = convertdata(row[4]) # vencimento
                    #tdata['data_cancela'] = row[13]

                    if row[9] == '' or not row[9]:
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

                    if row[2] == 'Arquivado' and tdata['data_baixa'] is None:
                        tdata['valorpago'] = None
                        tdata['data_baixa'] = None
                        tdata['data_pagamento'] = None
                        tdata['data_cancela'] = tdata['data_vencimento']
                        tdata['usuario_c'] = usuario
                        tdata['status'] = fmodels.MOVIMENTACAO_CANCELADA

                    print tdata
                    try:
                        new_titulo = fmodels.Titulo(**tdata)
                        new_titulo.save()
                        new_titulo.data_documento = tdata['data_documento']
                        new_titulo.save()
                    except Exception as e:
                        print(e)
                        pass


if args.notasfiscais and args.empresa:
    empresa = admmodels.Empresa.objects.get(cpfcnpj__numfilter=args.empresa)
    with open(args.notasfiscais, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            if fismodels.NotaFiscal.objects.filter(empresa=empresa,numero=row[1]).count() == 0:
                cliente = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=row[5])
                if cliente:
                    cliente = cliente[0]
                    nfdest = {}
                    nfdest['cliente'] = cliente
                    nfdest['cpfcnpj'] = cliente.getCPFCNPJNumero()
                    nfdest['inscricaoestadual'] = cliente.pessoa.insc_estadual
                    nfdest['razaosocial'] = cliente.getNome()
                    nfdest['logradouro'] = cliente.endereco.logradouro
                    nfdest['numero'] = cliente.endereco.numero
                    nfdest['complemento'] = cliente.endereco.complemento
                    nfdest['cep'] = cliente.endereco.cep
                    nfdest['bairro'] = cliente.endereco.bairro[:50]
                    nfdest['cidade'] = cliente.endereco.cidade[:50]
                    nfdest['uf'] = cliente.endereco.uf
                    nfdest['telefone'] = ''.join(cliente.getTelefones()[:1]).split('||')[0]
                    nfdest['codigocliente'] = str(cliente.id)
                    nfdest['tipoassinante'] = 1 if cliente.pessoa.tipopessoa == 'J' else 3

                    print(nfdest)
                    if args.sync_db:
                        nfdest_obj = fismodels.NFDestinatario(**nfdest)
                        nfdest_obj.save()

                    nf = {}
                    if args.sync_db:
                        nf['destinatario'] = nfdest_obj
                    nf['data_emissao'] = convertdata(row[7])
                    nf['data_saida'] = convertdata(row[7])
                    nf['modelo'] = '21'
                    nf['tipoutilizacao'] = '4'
                    nf['serie'] = 'U'
                    nf['numero']= row[1]
                    row[9] = row[9].replace('R$ ','').replace('.','').replace(',','.')
                    row[10] = row[10].replace('R$ ','').replace('.','').replace(',','.')
                    nf['valortotal'] = Decimal(row[9])
                    nf['icms'] = Decimal(row[10])
                    nf['outrosvalores'] = Decimal(row[9])
                    #if row[23] == 'N':
                    nf['status'] = fisconstants.NOTAFISCAL_GERADA
                    #else:
                    #    nf['status'] = fisconstants.NOTAFISCAL_CANCELADA
                    #    nf['data_cancela'] = '%s-%s-%s' %(row[15][0:4],row[15][4:6],row[15][6:8])
                    #nf['bcicms'] = Decimal('%s.%s' %(row[24][:-2],row[24][-2:]))
                    nf['bcicms'] = Decimal('0.00')
                    nf['tipo_es'] = fisconstants.NOTAFISCAL_TIPO_SAIDA
                    nf['tipo_nf'] = fisconstants.NOTAFISCAL_SERVICO
                    try:
                        nf['cfop'] = fismodels.CFOP.objects.get(cfop=row[11])
                    except Exception as e:
                        print e
                        nf['cfop'] = fismodels.CFOP.objects.get(cfop='5307')

                    nf['usuario_g'] = usuario
                    nf['usuario_c'] = usuario

                    print(nf)
                    if args.sync_db:
                        new_nf = fismodels.NotaFiscal(**nf)
                        new_nf.save()
                        new_nf.data_emissao=nf['data_emissao']
                        new_nf.data_saida=nf['data_saida']
                        new_nf.save()

                    # Cria nota fiscal com titulo
                    #nft = fismodels.NotaFiscalTitulo()
                    #nft.titulo = titulo
                    #nft.notafiscal = new_nf
                    #nft.save()

                    nfitem = {}
                    if args.sync_db:
                        nfitem['notafiscal'] = new_nf
                    nfitem['descricao'] = row[3]
                    nfitem['codigoservico'] = '010101'
                    nfitem['classificacao'] = '0104'
                    nfitem['unidade'] = ''
                    nfitem['qt_contratada'] = 1
                    nfitem['qt_fornecida'] = 1
                    nfitem['valortotal'] = Decimal(row[9])
                    nfitem['desconto'] = Decimal('0.00')
                    nfitem['acrescimo_despesa'] = Decimal('0.00')
                    nfitem['bcicms'] = Decimal('0.00')
                    nfitem['icms'] = Decimal('0.00')
                    nfitem['outrosvalores'] = Decimal(row[9])
                    nfitem['aliquotaicms'] = Decimal('0.00')
                    nfitem['item'] = 1
                    if args.sync_db:
                        nfitem['data_cadastro'] = new_nf.data_emissao
                        nfitem['data_alteracao'] = new_nf.data_emissao

                    print(nfitem)
                    if args.sync_db:
                        new_nfitem = fismodels.NotaFiscalItem(**nfitem)
                        new_nfitem.save()
                        new_nfitem.data_cadastro=new_nf.data_emissao
                        new_nfitem.data_alteracao=new_nf.data_emissao
                        new_nfitem.save()

if args.notatitulo and args.empresa:
    empresa = admmodels.Empresa.objects.get(cpfcnpj__numfilter=args.empresa)
    with open(args.notatitulo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            nf = fismodels.NotaFiscal.objects.filter(empresa=empresa,numero=row[1])
            titulo = fmodels.Titulo.objects.filter(numero_documento=row[6],notafiscaltitulo__isnull=True)
            if nf and titulo:
                nft = fismodels.NotaFiscalTitulo()
                nft.titulo = titulo[0]
                nft.notafiscal = nf[0]
                nft.save()
                print(nf[0],titulo[0])



