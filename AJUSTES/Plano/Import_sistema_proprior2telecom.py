#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from distutils.command.upload import upload
from hashlib import new
from http import client
import os, sys
from pickle import NONE
from datetime import date, datetime
import copy
from unicodedata import normalize
from decimal import Decimal
import csv
import re

from pandas import value_counts


parser = argparse.ArgumentParser(description='Importação csv 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--produtos', dest='produtos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='boletos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--contratos',dest='contratos',type=str,help='Arquivo importacao',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--pop', dest='pop', type=str, help='Arquivo importacao',required=False)

#python --settings=sgp.local.settings --clientes= --produtos= --contratos= --portador=1
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

from apps.atendimento import models as amodels
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.fiscal import models as fismodels, constants as fisconstants
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
from apps.cauth import models as authmodels

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))
fnum2 = lambda n: re.sub('[^0-9.,]', '', unicode(n))

usuario = authmodels.User.objects.get(username='sgp')
m = manage.Manage()



contratos={}
clientes={}
cobrancas={}
notasfiscais={}
produtos={}
boletos={}




formacobranca = fmodels.FormaCobranca.objects.all()[0]
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]
grupo_obj_tv = admmodels.Grupo.objects.filter(nome='tv').order_by('-id')[0]
grupo_obj_multimidia = admmodels.Grupo.objects.filter(nome='multimidia').order_by('-id')[0]
grupo_obj_telefonia=admmodels.Grupo.objects.filter(nome='telefonia').order_by('-id')[0]
nas = nmodels.NAS.objects.get(pk=args.nas)
portador = fmodels.Portador.objects.get(pk=args.portador)

def convertdata(d):
  
    try:
        d_,m_,y_ = d.strip().split('/')
        date(int(y_),int(m_),int(d_))
        return '%s-%s-%s' %(y_,m_,d_)
    except:
        return None


##########FUNCOES AUXILIARES###############

if args.clientes:
    with open(args.clientes, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
        indice=0
        for row in conteudo:
            #print(row)
            cliente={
                'id': row[0],
                'nome': row[1],
                'cnpj': row[3],
                'cpf': row[4],
                'email': row[5],
                'logradouro':row[6],
                'data_nascimento': row[8],
                'complemento': row[7],
                'cidade': row[8],
                'estado': row[9],
                'cep': row[10],
                'celular': str(row[11])+str(row[12]),
                'telefone_residencial': str(row[11])+ str(row[13]),
                'celular02': row[14],
                'data_nascimento': row[15],
                'sexo': row[16],
                'profissao': row[17],
                'cobranca_unificada':row[18]
            }

            clientes[indice]=cliente
            indice=indice+1
if args.contratos:
    with open(args.contratos, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
        indice=0
        for row in conteudo:
            contrato={
                'id_cliente':row[0],
                'codigo_contrato':row[3],
                'senha':row[5],
                'login':row[4],
                'data_contrato':row[6],
                'data_ativacao':row[7],
                'valor':row[8],
                'codigo_produto':row[10],
                'status':row[9],
                'produto':row[11]
            }
        
            contratos[indice]=contrato
            indice=indice+1
if args.produtos:
    with open(args.produtos, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|')
        indice=0
        for row in conteudo:
            produto={
                'cod_produto':row[0], 
                'nome_produto':row[1],
                'descricao':row[2],
                'valor':row[3],
                'tipo':row[5],
                'velocidade': row[6]
            } 

            produtos[indice]=produto
            indice=indice+1



                



############################
##   CADASTRO DOS PLANOS  ##
############################
if args.produtos:
    for p in produtos:
        print('Esse é meu tipo de produto: ', produtos[p]['tipo'])
        if ((str(produtos[p]['tipo'])=='telefonia') or (str(produtos[p]['tipo'])=='sms')):
            if admmodels.PlanoTelefonia.objects.filter(plano__descricao=produtos[p]['nome_produto']).count()==0:
                new_plano = admmodels.Plano()
                new_plano.descricao=produtos[p]['nome_produto']
                new_plano.preco = produtos[p]['valor']
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj_telefonia
                new_plano.save()
                planotelefonia = admmodels.PlanoTelefonia()
                planotelefonia.plano = new_plano
                planotelefonia.save()
        elif str(produtos[p]['tipo'])=='TV':
           if admmodels.PlanoTV.objects.filter(plano__descricao=produtos[p]['nome_produto']).count()==0:
                new_plano = admmodels.Plano()
                new_plano.descricao=produtos[p]['nome_produto']
                new_plano.preco = produtos[p]['valor']
                
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj_tv
                try:
                    new_plano.save()
                except:
                    new_plano.preco=0
                    new_plano.save()
                
                planotv = admmodels.PlanoTV()
                planotv.plano = new_plano
                planotv.save()

        elif str(produtos[p]['tipo'])=='sva':
           if admmodels.PlanoMultimidia.objects.filter(plano__descricao=produtos[p]['nome_produto']).count()==0:
                if (('Desconto'.lower().strip()) in (str(produtos[p]['nome_produto']).lower().strip()) or  '-' in str(produtos[p]['valor'])) :
                    continue
                new_plano = admmodels.Plano()
                new_plano.descricao=produtos[p]['nome_produto']
                new_plano.preco = produtos[p]['valor']
                
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj_multimidia
                try:
                    new_plano.save()
                except:
                    new_plano.preco=0
                    new_plano.save()
                
                planotv = admmodels.PlanoMultimidia()
                planotv.plano = new_plano
                planotv.save()
        else:
            if admmodels.PlanoInternet.objects.filter(plano__descricao=produtos[p]['nome_produto']).count()==0:
                if (('Desconto'.lower().strip()) in (str(produtos[p]['nome_produto']).lower().strip()) or  '-' in str(produtos[p]['valor'])) :
                    continue
                new_plano = admmodels.Plano()
                new_plano.descricao=produtos[p]['nome_produto']
                new_plano.preco = produtos[p]['valor']
                
                new_plano.contrato = contrato_obj
                new_plano.grupo = grupo_obj
                try:
                    new_plano.save()
                except:
                    new_plano.preco=0
                    new_plano.save()
                
                planointernet = admmodels.PlanoInternet()
                planointernet.plano = new_plano
                try:
                    velocidade=''.join(produtos[p]['velocidade'])
                    velocidade=velocidade.split('/')
                    velocidade_down=int(fnum(velocidade[0]))*1024
                    velocidade_up= int (fnum(velocidade[1]))*1024
                except:
                    velocidade_down=2500
                    velocidade_up=2500

                planointernet.download = velocidade_down
                planointernet.upload = velocidade_up
                planointernet.save()



####################################
##        CADASTRO CLIENTES       ##
####################################

if args.clientes and args.contratos and args.produtos:
    for contrato in contratos:
        dados={
                'codigo_contrato':contratos[contrato]['codigo_contrato'],
                'senha': contratos[contrato]['senha'],
                'login':contratos[contrato]['login'],
                'data_ativacao':contratos[contrato]['data_ativacao'],
                'data_contrato':contratos[contrato]['data_contrato'],
                'valor': contratos[contrato]['valor'],
                'codigo_produto':contratos[contrato]['codigo_produto'],
                'status':contratos[contrato]['status'],
                'produto': contratos[contrato]['produto']
                
                
                
            }

        for cliente in clientes:
            if contratos[contrato]['id_cliente']==clientes[cliente]['id']:
               dados['id']= clientes[cliente]['id'],
               dados['cpf']= clientes[cliente]['cpf'],
               dados['email']= clientes[cliente]['email'],
               dados['nome']= clientes[cliente]['nome'],
               dados['cnpj']= clientes[cliente]['cnpj'],
               dados['complemento']= clientes[cliente]['complemento']
               #dados['rg']= clientes[cliente]['rg'],
               dados['logradouro']=clientes[cliente]['logradouro'],
               dados['cidade']= clientes[cliente]['cidade'],
               dados['estado']= clientes[cliente]['estado'],
               dados['cep']= clientes[cliente]['cep'],
               dados['celular']=clientes[cliente]['celular'],
               dados['telefone_residencial']= clientes[cliente]['telefone_residencial'],
               dados['celular02']= clientes[cliente]['celular02'],
               dados['data_nascimento']= clientes[cliente]['data_nascimento'],
               dados['sexo']= clientes[cliente]['sexo'],
               dados['profissao']= clientes[cliente]['profissao']
               dados['cobranca_unificada']=clientes[cliente]['cobranca_unificada']
               
       
        ######################## MONTANDO CLIENTE ##################

        idcliente = dados['id'][0]
        idcontrato=dados['codigo_contrato']
        print(idcliente)
        nome = ''.join(dados['nome'])
        cnpj=''.join(dados['cnpj'])
        cpf =  ''.join(dados['cpf'])
        if len(cpf)>3:
            cpfcnpj= cpf
        else:
            cpfcnpj=cnpj
        #rg=dados['rg']
        data_nasc = convertdata(dados['data_nascimento'])
        celular=''.join(dados['celular'])
        telefone_residencial=''.join(dados['telefone_residencial'])
        celular02=''.join(dados['celular02'])
        sexo=''.join(dados['sexo'])
        if len(sexo):
            sexo=None
        status = ''.join(dados['status'])
        complemento=dados['complemento']
        data_cadastro=convertdata(''.join(dados['data_contrato']))
        data_inicio=convertdata(''.join(dados['data_ativacao']))
        if not data_cadastro or data_cadastro=='':
            data_cadastro=datetime.now()
        

        profissao= dados['profissao']
        email=''.join(dados['email'])

        #############ENDERECO############
        logradouro=''.join(dados['logradouro'])
        cidade=''.join(dados['cidade'])
       
        estado=str(''.join(dados['estado'])).strip()
        print('esse é meu estado:',estado, type(estado))
        cep=''.join(dados['cep'])

        print(cep,type(cep),logradouro, type(logradouro),cidade,type(cidade),estado,type(estado), complemento, type(complemento))


        ################## PLANO #################
        planotelefonia=''
        planoTV=''
        planointernet=''
        planomultimidia=''
        try:
            produto=''.join(dados['produto'])
            if str('Desconto'.lower().strip()) in str(produto) or '-' in str(dados['valor']):
                continue
            planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=produto)[0]
            print('esse é o meu plano de internet: ', planointernet.plano.descricao)

        except:
            planointernet=''
            try:
                produto=''.join(dados['produto'])
                print('Esse é meu servico de Telefonia: ', produto)
                planotelefonia = admmodels.PlanoTelefonia.objects.filter(plano__descricao__iexact=produto)[0]
                print(planotelefonia)
          
            except:
                planotelefonia=''
                try:
                
                    produto=''.join(dados['produto'])
                    print('Esse é meu servico de TV: ', produto)
                    planoTV=admmodels.PlanoTV.objects.filter(plano__descricao__iexact=produto)[0]
                    print(planoTV)
                except:
                    planoTV=''
            
                   
                    try:
                        produto=''.join(dados['produto'])
                        print('Esse é meu plano de Multimidia')
                        if  '-' in str(produtos[p]['valor']):
                            continue    
                        planomultimidia=admmodels.PlanoMultimidia.objects.filter(plano__descricao__iexact=produto)[0]
                        print(planomultimidia)
                    except:
                        continue
        
            
        login=''.join(dados['login'])
        if login=='':
            login=str(idcliente) + 'sem_login'
        senha=dados['senha']


                   
        ###############SETANDO POP E VENCIMENTO ##############

        
        pop = admmodels.Pop.objects.get(id=args.pop)
        try:
            vencimento = fmodels.Vencimento.objects.get(dia=10)
        except:
            new_vencimento = fmodels.Vencimento()
            new_vencimento.dia =  10
            new_vencimento.save()

            vencimento=fmodels.Vencimento.objects.get(dia=10)

        ############# SETANDO STATUS ###########
        status_cc = 1
        status_s = 1
        status_c = 1
        if status =='1':
            status_cc = 1
            status_s = 1
            status_c = 1
        if status=='2' or status=='3':
            status_cc=4
            status_s = 4
            status_c = 4
        if status=='99':
            status_cc=3
            status_s = 3
            status_c = 3
        if status=='00' or status=='0':
            status_cc=2
            status_s =2
            status_c = 2


        print ('nome: ',nome,'cpfcnpj: ',cpfcnpj,'Sexo: ',sexo, 'Data Cadastro: ', data_cadastro,'Data Nascimento:', data_nasc)
        print ('vencimento: ', vencimento, 'Login:', login)
        print (login,senha)
        print '####################################################'
        if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=login).count() == 0:
            print "Import %s" %nome
            # Save Models

            cliente_check = admmodels.Cliente.objects.filter(id=idcliente)

            if len(cliente_check) == 0:

                # Endereco
                new_endereco = admmodels.Endereco()
                new_endereco.logradouro = logradouro
                new_endereco.numero = None
                new_endereco.bairro = 'SEM_BAIRRO'
                new_endereco.cep = cep
                new_endereco.cidade = cidade
                new_endereco.uf = estado
                new_endereco.pais = 'BR'
                new_endereco.complemento = complemento
                new_endereco.pontoreferencia=''
                #print('esse é o logradouro: ', logradouro)

                new_endereco_cob = copy.copy(new_endereco)
                new_endereco_inst = copy.copy(new_endereco)
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
                    new_pessoa.profissao = profissao[:15]
                    new_pessoa.nacionalidade = 'BR'
                    new_pessoa.nomepai = None
                    new_pessoa.nomemae = None
                    new_pessoa.naturalidade = None
                    new_pessoa.rg = None
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
                    print(nome)
                    new_pessoa.nomefantasia = nome
                    new_pessoa.resempresa = ''
                    new_pessoa.cpfcnpj = cpfcnpj
                    print(cpfcnpj)
                    new_pessoa.insc_estadual = None
                    new_pessoa.insc_municipal = None
                    new_pessoa.tipo = 8
                    new_pessoa.save()

                ############# CLIENTE ##########
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

                
                ############ CONTATO 1 ###############
                
                if len(str(email)) > 4:
                    new_contato = admmodels.Contato()
                    new_contato.tipo = 'EMAIL'
                    new_contato.contato = email
                    new_contato.save()
                    new_ccontato = admmodels.ClienteContato()
                    new_ccontato.cliente = new_cliente
                    new_ccontato.contato = new_contato
                    new_ccontato.save()

                ############# CONTATO 2 ###########
                
                if len(str(celular)) > 4:
                    new_contato = admmodels.Contato()
                    new_contato.tipo = 'CELULAR_PESSOAL'
                    new_contato.contato = celular
                    new_contato.observacao = None
                    new_contato.save()
                    new_ccontato = admmodels.ClienteContato()
                    new_ccontato.cliente = new_cliente
                    new_ccontato.contato = new_contato
                    new_ccontato.save()

                if len(str(celular02)) > 4:
                    new_contato = admmodels.Contato()
                    new_contato.tipo = 'CELULAR_PESSOAL'
                    new_contato.contato = celular02
                    new_contato.observacao = None
                    new_contato.save()
                    new_ccontato = admmodels.ClienteContato()
                    new_ccontato.cliente = new_cliente
                    new_ccontato.contato = new_contato
                    new_ccontato.save()
                if len(str(telefone_residencial)) > 4:
                    new_contato = admmodels.Contato()
                    new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                    new_contato.contato = telefone_residencial
                    new_contato.observacao = None
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
            new_cobranca.vencimento = vencimento
            new_cobranca.isento = 0
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
            new_contrato.id=idcontrato
            new_contrato.cliente = new_cliente
            new_contrato.pop = pop
            new_contrato.cobranca = new_cobranca

            new_contrato.data_inicio = data_inicio
            new_contrato.data_cadastro = data_cadastro
            new_contrato.data_alteracao = data_cadastro
            try:
                new_contrato.save()
            except:
                data_inicio=None
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

            ############SALVANDO OBJETO DE SERVICO###########
            if planointernet !='':
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
                new_servico.tipoconexao = 'ppp'
                new_servico.nas = nas
                new_servico.ip=None
                new_servico.mac=None
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao =  0
                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)


            if planotelefonia!='':
                new_servico = admmodels.ServicoTelefonia()
                new_servico.clientecontrato = new_contrato
                new_servico.login=login
                new_servico.login_password=senha
                new_servico.login_password_plain=senha
                new_servico.central_password=senha
                new_servico.status = status_s
                new_servico.endereco = new_endereco_inst

                new_servico.nas = nas
                new_servico.plano = planotelefonia
                try:
                    new_servico.save()
                except:
                    new_servico.login=str(login)+str(idcliente)
                    new_servico.save()
                new_servico.data_cadastro=data_cadastro
                new_servico.save()

            if planoTV!='':
                new_servico = admmodels.ServicoTV()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                new_servico.endereco = new_endereco_inst
                new_servico.login=login
                new_servico.login_password=senha
                new_servico.login_password_plain=senha
                new_servico.central_password=senha
                new_servico.nas = nas
                new_servico.plano = planoTV
                new_servico.save()
                new_servico.data_cadastro=data_cadastro
                new_servico.save()
            
            if planomultimidia!='':
                new_servico = admmodels.ServicoMultimidia()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                new_servico.endereco = new_endereco_inst
                new_servico.email_password=senha
                new_servico.central_password=senha
                new_servico.email=email
                new_servico.nas = nas
                new_servico.plano = planomultimidia
                new_servico.data_cadastro=data_cadastro
                try:
                    new_servico.save()
                except:
                    new_servico.email=str(email)+str(''.join(dados['codigo_contrato']))
                    new_servico.save()
            '''cobranca_unificada= ''.join(dados['cobranca_unificada'])
            print('Essa é Minha cobranca unificada: >>>>>>', cobranca_unificada)
            if ''.join(dados['cobranca_unificada'])=='1':
                try:
                    internet=admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__id=idcliente)
                    if((internet>0) and (int(internet[0].clientecontrato.id)!=int(idcontrato))):
                        new_cobranca.cobranca_unificada=internet[0].clientecontrato.cobranca
                        new_cobranca.save()
                except Exception as e:
                    print(e)     '''               
                    
                

    from apps.admcore import models as admmodels
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)




