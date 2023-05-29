#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from hashlib import new
from logging import exception
import os, sys
from pydoc import cli
from datetime import date, datetime
import copy
from traceback import print_tb
from unicodedata import normalize
import csv
import re
parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='Portador id',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS', required=True )
parser.add_argument('--titulos', dest='titulos', type=str, help='Cobrancas', required=False)
parser.add_argument('--planos', dest='planos', type=str, help='cadastra planos', required=False)
parser.add_argument('--plano', dest='plano', type=int, help='plano',required=False)
parser.add_argument('--acessos', dest='acessos', type=str, help='arquivo com dados de acessox', required=False)
args = parser.parse_args()


#########################IMPORT GERAL################################
#python import_perfacio.py --settings=sgp.stoynet.settings --nas=1 --portador=1 --vencimentoadd=1 --planoadd=1 --clientes=Conv-clientes-perfacio.csv  --planos=Conv-planos-perfacio.csv --titulos=Conv-recebiveis-perfacio.csv --acessos=Conv-contas-acesso-perfacio.csv --sync=1

##################### ARQUIVOS NECESSARIOS ###########################
#                     clientes.csv                                   #
#                     contas_acesso.csv                              #
#                     planos.csv                                     #
#                     recebiveis.csv                                 #
######################################################################


PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.db.models import Q
from django.conf import settings
from django.db.models import Q, Max
from apps.admcore import models as admmodels
from apps.financeiro import models as fmodels
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage
from apps.cauth import models as authmodels
from apps.fiscal import models as fismodels, constants as fisconstants

portador = fmodels.Portador.objects.get(pk=args.portador_id)
usuario = authmodels.User.objects.get(username='sgp')
if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

fnum = lambda n: re.sub('[^0-9]', '', unicode(n))

def strdate(d):
    try:
        d,m,y = d.split()[0].split('.')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None
incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 10000
if incrementar < 10000:
    incrementar = 10000
else:
    incrementar += 1


m = manage.Manage()
if args.plano:
    planodefault = admmodels.PlanoInternet.objects.get(plano__id=args.plano)


usuario = admmodels.User.objects.get(username='sgp')
contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]
formacobranca = fmodels.FormaCobranca.objects.all()[0]
nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
if args.clientes:
    clientes= {}
    planos={}
    titulos={}
    acessos={}
    dados={}
    

    #load clientes
    with open(args.clientes, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            cliente={
                'id': row[0],
                'nome': row[1],
                'cpfcnpj':row[3],
                'rg': row[5],
                'sexo':row[7],
                'incricao_estadual': row[9],
                'inscricao_municipal': row[10],
                'nome_pai': row[11],
                'nome_mae': row[12],
                'nome_fantasia': row[13],
                'email': row[14],
                'telefone_fixo': row[15],
                'telefone_celular': row[16],
                'logradouro': row[18],
                'numero': row[19],
                'complemento':row[20],
                'bairro': row[22],
                'cep': row[23],
                'cidade': row[24],
                'estado': row[26],
                'observacao': row[29]
                }
            clientes[indice]=cliente
            indice=indice+1




    #load planos
    with open(args.planos, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            plano={
                'id': row[0],
                'nome': row[2],
                'download':row[3],
                'upload': row[4],
                'valor': row[7],
                }
            planos[indice]=plano
            indice=indice+1



    #load titulos
    if args.titulos:
        with open(args.titulos, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
            indice=0
            for row in conteudo:
                titulo={
                    'id': row[0],
                    'id_cliente': row[1],
                    'id_carteira':row[3],
                    'data_vencimento': row[4],
                    'valor': row[5],
                    'valor_pago': row[6],
                    'pago': row[8],
                    'cancelado': row[9],
                    'nosso_numero': row[10],
                    'data_cadastro': row[14]
                    }
                titulos[indice]=titulo
                indice=indice+1



    #load acessos
    with open(args.acessos, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            acesso={
                'id': row[0],
                'id_plano': row[1],
                'id_cliente':row[2],
                'login': row[5],
                'senha': row[6],
                'mac': row[7],
                'vencimento': row[13],
                'ip':row[4]
                }
            acessos[indice]=acesso
            indice=indice+1




    for cliente in clientes:
        dados={
                'id': clientes[cliente]['id'],
                'nome': clientes[cliente]['nome'],
                'cpfcnpj':clientes[cliente]['cpfcnpj'],
                'rg': clientes[cliente]['rg'],
                'sexo':clientes[cliente]['sexo'],
                'incricao_estadual':clientes[cliente]['incricao_estadual'],
                'inscricao_municipal': clientes[cliente]['inscricao_municipal'],
                'nome_pai': clientes[cliente]['nome_pai'],
                'nome_mae': clientes[cliente]['nome_mae'],
                'nome_fantasia': clientes[cliente]['nome_fantasia'],
                'email': clientes[cliente]['email'],
                'telefone_fixo': clientes[cliente]['telefone_fixo'],
                'telefone_celular': clientes[cliente]['telefone_celular'],
                'logradouro': clientes[cliente]['logradouro'],
                'numero': clientes[cliente]['numero'],
                'complemento':clientes[cliente]['complemento'],
                'bairro': clientes[cliente]['bairro'],
                'cep': clientes[cliente]['cep'],
                'cidade': clientes[cliente]['cidade'],
                'estado': clientes[cliente]['estado'],
                'observacao': clientes[cliente]['observacao']
                }

        for acesso in acessos: 
            
            if clientes[cliente]['id']== acessos[acesso]['id_cliente']:
                dados['login']= acessos[acesso]['login']
                dados['senha'] = acessos[acesso]['senha']
                dados['mac']= acessos[acesso]['mac']
                dados['ip']=acessos[acesso]['ip']
                dados['vencimento']=acessos[acesso]['vencimento']

                for plano in planos:
                    if  planos[plano]['id']==acessos[acesso]['id_plano']:
                        dados['nome_plano'] = planos[plano]['nome']
                        dados['download'] = planos[plano]['download']
                        dados['upload'] = planos[plano]['upload']
                        dados['valor_plano'] = planos[plano]['valor']



        id_contrato= dados['id']

        print("esse é o id do meu contrato: " , id_contrato)
   
           
        ################# CRIANDO CLIENTE #########################
        id_cliente=id_contrato
        nome = dados['nome']

        data_cadastro = datetime.now()


        celular=dados['telefone_celular']
       
        email=dados['email']
    
        cpfcnpj = dados['cpfcnpj']
        data_nascimento=None
        rg = dados['rg']
        sexo = dados['sexo']
        if len(sexo)==0 or len(sexo)>1:
            sexo= None
        
        
        
        
        nomefantasia = None
        inscricao_estadual=dados['incricao_estadual']
        inscricao_miunicipal= dados['inscricao_municipal']


        ################# MONTANDO ENDERECO #####################
        try:
            numero= int(dados['numero'])
        except:
            numero=0
        
        uf= str(dados['estado']).strip()
        if(len(uf)>2):
            uf='BA'
        bairro= dados['bairro']
        cidade= dados['cidade']
        logradouro = str(dados['logradouro'])
        cep= dados['cep']
     
    


        #####################Servico ################################
        login=None
        try:
            login = str(dados['login']).strip()
            if len(login) == 0:
                login=str(id_cliente).strip()

        except Exception as e:
            print('Essa é minha excessao:', e)
            login=id_cliente

        senha=None
        try:
            senha = str(dados['senha'])
            if not senha:
                senha=id_cliente
        except:
            senha=id_cliente

        print('###########Esse é meu Login##############', login)
        print('############Esse é minha senha###############', senha)

        servico_cidade= cidade
        servico_logradouro= logradouro
        servico_uf=uf
        servico_numero= numero
        servico_uf= uf

        try:

            vencimento = dados['vencimento']
        except:
            vencimento = 10
    
       ####################CRIANDO POP BASEADO NAS CIDADES DOS CLIENTES############### 
        cidade_q = normalize('NFKD', unicode(cidade)).encode('ASCII','ignore')
        pop = admmodels.Pop.objects.filter(id=1)[0]
        '''try:
            pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
            pop = pop_q

        except Exception as e:
            new_pop = admmodels.Pop()
            new_pop.cidade=cidade_q.upper()
            new_pop.uf=uf
            new_pop.save()
            pop = new_pop'''
        nas=nas_default

        #################### CRIANDO PLANOS ########################
        
        try:
            plano = str(dados['nome_plano']).replace('.',',') 
        except:
            plano= "SEM PLANO DEFINIDO"
        
        try:
            plano_valor=dados['valor_plano']
        except:
            plano_valor='000'

        try:
            plano_download=int(dados['download']) or 0
        except:
            plano_download=0
       
        try:
            plano_upload= int(dados['upload']) or 0
        except:
            plano_upload=0

        conexao_tipo = 'ppp'
        try:
            ip=dados['ip']
            if not ip or ip=='':
                ip=None
        except:
            ip=None
        try:
            mac = dados['mac']
        except:
            mac=None

        
        '''try:  
            
            mac_list.append(mac)

            for at_mac in mac_list:
                if at_mac == mac:
                    mac= None
        except:
            mac=None'''




        ###########SAVE  DE PLANOS#############
        try:
            planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
        except:
            print("entrei na excessao dos planos")
            #planointernet = admmodels.PlanoInternet.objects.filter(id=19)[0]
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
                print('criado plano %s' %plano)
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            else:
                raise Exception('Não localizei plano %s' %plano)

       
        ###SETANDO STATUS###
        status_cc = 1
        status_s = 1
        status_c = 1


           
            
        if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login.lower()).count() == 0:
    
            print(dados)
            print('entrei no if do sync ')
            ###checa se já existe cliente com esse login###
            id_atual=int(id_contrato)+140
            cliente_check = admmodels.ServicoInternet.objects.filter(login__trim__lower=login.lower())
            

            if cliente_check.count() > 0:
                continue

                
            print('passei do cliente check')

                ########## SAVE ENDERECO OBJECT ########
            new_endereco = admmodels.Endereco()
            new_endereco.uf=uf
            new_endereco.cep=cep
            new_endereco.cidade=cidade
            new_endereco.numero=numero
            new_endereco.bairro=bairro
            new_endereco.logradouro=logradouro
            new_endereco.save()

            new_endereco_cobranca=new_endereco
            new_endereco_cobranca.id=None
            new_endereco_cobranca.save()

            new_endereco_servico=new_endereco
            new_endereco_servico.id=None
            new_endereco_servico.save()


            ########## SAVE PESSOA OBJECT ##########
            if len(fnum(cpfcnpj)) > 12:
                new_pessoa = admmodels.Pessoa()
                new_pessoa.tipopessoa='J'
                new_pessoa.nome = nome
                new_pessoa.nomefantasia = None
                    #new_pessoa.respempresa = respempresa
                    #new_pessoa.respcpf = respcpf
                new_pessoa.cpfcnpj = cpfcnpj
                new_pessoa.rg= rg
                new_pessoa.insc_estadual = inscricao_estadual
                new_pessoa.tipo = 8
                new_pessoa.save()
            else:
                new_pessoa = admmodels.Pessoa()
                new_pessoa.tipopessoa='F'

                new_pessoa.nome = nome
                new_pessoa.sexo = sexo
                
                new_pessoa.nacionalidade = 'BR'
                new_pessoa.rg= rg
                new_pessoa.cpfcnpj = cpfcnpj
                new_pessoa.rg_emissor=''
                new_pessoa.datanasc=data_nascimento
                try:
                    new_pessoa.save()
                except:
                    try:
                        new_pessoa.save()
                    except:
                        new_pessoa.datanasc=None
                        new_pessoa.save()  

                
                ####### SAVE CLIENTE ########
            new_cliente = admmodels.Cliente()
            new_cliente.id = int(id_contrato) + 140
            new_cliente.endereco = new_endereco
            new_cliente.pessoa = new_pessoa
            new_cliente.data_cadastro = data_cadastro
            new_cliente.data_alteracao = data_cadastro
            new_cliente.ativo = True
            new_cliente.observacao = dados['observacao']
            new_cliente.save()
            new_cliente.data_cadastro = data_cadastro

                #SAVE NO EMAIL
            if len(email) > 4:
                new_contato = admmodels.Contato()
                new_contato.tipo = 'EMAIL'
                new_contato.contato = email
                new_contato.save()
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = new_cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()


                #SAVE NO CELULAR
            if len(celular) > 4:
                new_contato = admmodels.Contato()
                new_contato.tipo = 'CELULAR_PESSOAL'
                new_contato.contato = celular
                    # new_contato.observacao = con_obs
                new_contato.save()
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = new_cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()


                ############## COBRANCA ################
            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save()


            new_cobranca = fmodels.Cobranca()
            new_cobranca.cliente = new_cliente
            new_cobranca.endereco = new_endereco_cobranca
            
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

            new_cobranca.data_cadastro = data_cadastro
            new_cobranca.save()

                 ##########SAVE DO CONTRATO#######

            contrato_check = admmodels.ClienteContrato.objects.filter(id=id_contrato)
            new_contrato = admmodels.ClienteContrato()

               
            new_contrato.id = int(id_contrato) + 140
                #incrementar += 1

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

               
            new_status = admmodels.ClienteContratoStatus()
            new_status.cliente_contrato = new_contrato
            new_status.status = status_cc
            new_status.modo=2
            new_status.usuario = usuario
            new_status.data_cadastro = data_cadastro
            new_status.save()
               
                #####SAVE DO SERVICO#########
            new_servico = admmodels.ServicoInternet()
            new_servico.clientecontrato = new_contrato
            new_servico.status = status_s

            if admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() > 0:
                print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                      login,
                                                                                      str(new_contrato.id))
                login += str(new_contrato.id)
                
    
            new_servico.login= login
            new_servico.endereco = new_endereco
            new_servico.login_password=senha
            new_servico.login_password_plain=senha
            new_servico.central_password=senha
            new_servico.endereco=new_endereco_servico

            if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                new_servico.mac_dhcp = mac
                new_servico.mac = mac

            if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                new_servico.ip = ip

            new_servico.tipoconexao = conexao_tipo
            new_servico.nas = nas
            new_servico.planointernet = planointernet
            new_servico.modoaquisicao =  0
            new_servico.data_cadastro=data_cadastro
                #new_servico.observacao=servico_obs
            
            new_servico.save()


            m.addRadiusServico(new_servico)
                
                            

    
from apps.admcore import models as admmodels
from apps.netcore import models as netmodels
for p in admmodels.Pop.objects.all():
    for plano in admmodels.Plano.objects.all():
        plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)

        
