#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import datetime
import copy
from unicodedata import normalize
import csv
import re
parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS', required=True )
parser.add_argument('--portador', dest='portador_id', type=int, help='Portador id',required=False)
parser.add_argument('--contratos', dest='contratos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--assinantes', dest='assinantes', type=str, help='Arquivo importacao',required=False)
args = parser.parse_args()

##################### Orientações ####################################
#                     Assinantes.csv                                 #
#                     Contratos.csv                                  #
######################################################################


#########################IMPORT GERAL################################
#   python import_rbfull.py --settings=sgp.speednetce.settings --nas=1 --portador=1 --planoadd=1 --assinantes=  --contratos= --sync=1

##################### ARQUIVOS NECESSARIOS ###########################
#                     Assinantes.csv                                 #
#                     Contratos.csv                                  #
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
        d,m,y = d.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None

m = manage.Manage()
usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]
nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
if args.assinantes:
    clientes= {}
    contratos={}
  

    #load assinantes
    with open(args.assinantes, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            cliente={
                'id': row[0],
                'nome': row[1],
                'nome_fantasia': row[2],
                'cpfcnpj':row[3],
                'rg': row[4],
                'data_nascimento': row[5],
                'nome_pai': row[6],
                'nome_mae': row[7],
                'vencimento': row[8],
                'data_cadastro': row[13],
                'logradouro': row[14],
                'numero': row[15],
                'complemento':str(row[16]+', '+row[17]),
                'bairro': row[18],
                'cidade': row[19],
                'estado': row[20],
                'cep': row[21],
                'email': str(row[23]+' / '+row[24]),
                'telefone_fixo': row[25],
                'telefone_celular': row[26],
                }
            clientes[indice]=cliente
            indice=indice+1


    #load contratos
    with open(args.contratos, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            contrato={
                'id': row[0],
                'nome': row[1],
                'cpfcnpj':row[2],
                'plano': row[4],
                'valor': row[5],
                'isento': row[6],
                'login': row[7],
                'senha': row[8],
                'status': row[10],
                'data_cancelamento': row[17],
                'logradouro_inst': row[18],
                'numero_inst': row[19],
                'complemento_inst': str(row[20]+' / '+row[21]),
                'bairro_inst': row[22],
                'cidade_inst': row[23],
                'estado_inst': row[24],
                'cep_inst': row[25],
                'coordenadas': row[26],
                'ip': row[36],
                'mac': row[37]
                }
            contratos[indice]=contrato
            indice=indice+1


    for cliente in clientes:
        dados={
                'id_cliente': clientes[cliente]['id'],
                'nome': clientes[cliente]['nome'],
                'nome_fantasia': clientes[cliente]['nome_fantasia'],
                'cpfcnpj': clientes[cliente]['cpfcnpj'],
                'rg': clientes[cliente]['rg'],
                'data_nascimento': clientes[cliente]['data_nascimento'],
                'nome_pai': clientes[cliente]['nome_pai'],
                'nome_mae': clientes[cliente]['nome_mae'],
                'vencimento': clientes[cliente]['vencimento'],
                'data_cadastro': clientes[cliente]['data_cadastro'],
                'logradouro': clientes[cliente]['logradouro'],
                'numero': clientes[cliente]['numero'],
                'complemento':clientes[cliente]['complemento'],
                'bairro': clientes[cliente]['bairro'],
                'cidade': clientes[cliente]['cidade'],
                'estado': clientes[cliente]['estado'],
                'cep': clientes[cliente]['cep'],
                'email': clientes[cliente]['email'],
                'telefone_fixo': clientes[cliente]['telefone_fixo'],
                'telefone_celular': clientes[cliente]['telefone_celular'],
                }

        for contrato in contratos: 
            
            if clientes[cliente]['cpfcnpj'] == contratos[contrato]['cpfcnpj']:
                dados['id_contrato'] = contratos[contrato]['id']
                dados['plano'] = contratos[contrato]['plano']
                dados['valor'] = contratos[contrato]['valor']
                dados['isento'] = contratos[contrato]['isento']
                dados['login'] = contratos[contrato]['login']
                dados['senha'] = contratos[contrato]['senha']
                dados['status'] = contratos[contrato]['status']
                dados['data_cancelamento'] = contratos[contrato]['data_cancelamento']
                dados['logradouro_inst'] = contratos[contrato]['logradouro_inst']
                dados['numero_inst'] = contratos[contrato]['numero_inst']
                dados['complemento_inst'] = contratos[contrato]['complemento_inst']
                dados['bairro_inst'] = contratos[contrato]['bairro_inst']
                dados['cidade_inst'] = contratos[contrato]['cidade_inst']
                dados['estado_inst'] = contratos[contrato]['estado_inst']
                dados['cep_inst'] = contratos[contrato]['cep_inst']
                dados['coordenadas'] = contratos[contrato]['coordenadas']
                dados['ip'] = contratos[contrato]['ip']
                dados['mac'] = contratos[contrato]['mac']

                #### VARIAVEIS ####
                plano = dados['plano']
                plano_valor = dados['valor'].replace(',', '.').strip()
                contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
                grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]
                plano_download = 204800
                plano_upload = 102400

                cidade = dados['cidade']
                uf = dados['estado']
                cidade_q = normalize('NFKD', unicode(cidade)).encode('ASCII','ignore')

                cep = dados['cep']
                numero = dados['numero']
                
                try:
                  numero=int(numero)
                except:
                  numero=0
               
                bairro = dados['bairro']
                logradouro = dados['logradouro']
                complemento = dados['complemento']

                cep_isnt = dados['cep_inst']
                numero_isnt = dados['numero_inst']

                try:
                  numero_isnt=int(numero_isnt)
                except:
                  numero_isnt=0
                if numero_isnt=='':
                  numero_isnt=0
                bairro_isnt = dados['bairro_inst']
                logradouro_isnt = dados['logradouro_inst']
                uf_isnt = dados['estado_inst']
                cidade_isnt = dados['cidade_inst']
                complemento_isnt = dados['complemento_inst']

                cpfcnpj = dados['cpfcnpj']
                nome = dados['nome']
                nomefantasia = dados['nome_fantasia']
                rg = dados['rg']
                data_nascimento = strdate(dados['data_nascimento'])

                #id_cliente = dados['id_cliente']
                data_cadastro = dados['data_cadastro'][:10].strip()
                data_cadastro=strdate(data_cadastro)
                if data_cadastro =='' or data_cadastro==None:
                    data_cadastro=datetime.now()
                

                email = dados['email'].split('/')
                telefonecom = dados['telefone_fixo']
                telefonecom = dados['telefone_fixo']

                vencimento = 10
                if dados['vencimento'] != '' and dados['vencimento'] != None:
                  vencimento = dados['vencimento']

                isento = 0
                if dados['isento'] == 'Isento':
                  isento = 100

                id_contrato = dados['id_contrato']
              
                login = dados['login']
                senha = dados['senha']
                ip = dados['ip']
                mac = dados['mac']
                conexao_tipo = 'ppp'
                servico_obs = ''
                status = dados['status']


                ###SETANDO STATUS###
                status_cc = 1
                status_s = 1
                status_c = 1

                if status == 'Bloqueado':
                    status_cc = 4
                    status_s = 4
                    status_c = 4

                if status == 'Desativado':
                    status_cc = 3
                    status_s = 3
                    status_c = 3


                ################# CRIANDO PLANOS #########################
                try:
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                except:
                    print("entrei na excessao dos planos")
                    if args.planoadd:
                        print(plano,plano_download,plano_upload,plano_valor)
                        new_plano = admmodels.Plano()
                        new_plano.descricao=plano
                        new_plano.preco = plano_valor
                        new_plano.contrato = contrato_obj
                        new_plano.grupo = grupo_obj
                        try:
                          new_plano.save()
                        except:
                          print('Erro ao cadastrar novo PLANO!')

                        new_plano_internet = admmodels.PlanoInternet()
                        new_plano_internet.plano = new_plano
                        new_plano_internet.download = plano_download
                        new_plano_internet.upload = plano_upload
                        try:
                          new_plano_internet.save()
                          planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                        except:
                          print('Erro ao cadastrar novo PLANO INTERNET!')

                        print('criado plano %s' %plano)
                    else:
                        raise Exception('Não localizei plano %s' %plano)
                    

                ################# CRIANDO POP BASEADO NAS CIDADES DOS CLIENTES############### 
                '''try:
                    pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                    pop = pop_q

                except Exception as e:
                    new_pop = admmodels.Pop()
                    new_pop.cidade=cidade_q.upper()
                    new_pop.uf=uf
                    try:
                      new_pop.save()
                    except:
                      print('Erro ao cadastrar novo POP!')'''
                pop = admmodels.Pop.objects.get(id=1)
                nas=nas_default

                if args.sync_db == True:

                  ################# CRIANDO ENDERECO CLIENTE ########
                  new_endereco = admmodels.Endereco()
                  new_endereco.uf=uf
                  new_endereco.cep=cep
                  new_endereco.cidade=cidade
                  if numero=='':
                      numero=None

                  new_endereco.numero=numero
                  new_endereco.bairro=bairro
                  new_endereco.logradouro=logradouro
                  new_endereco.complemento=complemento
                  try:
                    new_endereco.save()
                  except Exception as e:
                    print('Erro ao cadastrar dados de ENDERECO!',  e)

                  ################# CRIANDO ENDERECO COBRANÇA ########
                  new_endereco_cobranca=new_endereco
                  new_endereco_cobranca.id=None
                  try:
                    new_endereco_cobranca.save()
                  except:
                    print('Erro ao cadastrar dados de ENDERECO DE COBRANÇA!')

                  ################# CRIANDO ENDERECO INSTALAÇÃO ########               
                  new_endereco_instalacao = admmodels.Endereco()
                  new_endereco_instalacao.id = None
                  new_endereco_instalacao.uf=uf_isnt
                  new_endereco_instalacao.cep=cep_isnt
                  new_endereco_instalacao.cidade=cidade_isnt
                  new_endereco_instalacao.numero=numero_isnt
                  new_endereco_instalacao.bairro=bairro_isnt
                  new_endereco_instalacao.logradouro=logradouro_isnt
                  try:
                    new_endereco_instalacao.save()
                  except Exception as e:
                    print('Erro ao cadastrar dados de ENDERECO INSTALAÇÃO!', e)

                  print('#########################################################################################')
                  print(dados)

                  if admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=dados['cpfcnpj']).count() == 0:
                  
                    ################# CRIANDO PESSOA ##########
                    if len(fnum(cpfcnpj)) > 12:
                      try:
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='J'
                        new_pessoa.nome = nome
                        new_pessoa.nomefantasia = None
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg= rg
                        new_pessoa.insc_estadual = None
                        new_pessoa.tipo = 8
                        new_pessoa.save()
                      except Exception as e:
                        print('Erro ao cadastrar dados de PESSOA!: ', e)
                    else:
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'
                        new_pessoa.nome = nome
                        new_pessoa.sexo = None
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg= rg
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor=''
                        new_pessoa.datanasc=data_nascimento
                        try:
                            new_pessoa.save()
                        except Exception as e:
                            print('Erro ao cadastrar dados de PESSOA! - ', e)
                    
                    ################# CRAINDO CLIENTE ########
                    try:
                      new_cliente = admmodels.Cliente()
                      #new_cliente.id = id_cliente
                      new_cliente.endereco = new_endereco
                      new_cliente.pessoa = new_pessoa
                      new_cliente.data_cadastro = data_cadastro
                      new_cliente.data_alteracao = data_cadastro
                      new_cliente.ativo = True
                      new_cliente.observacao = ''
                      new_cliente.save()
                    except:
                      print('Erro ao cadastrar o CLIENTE!')
                    
                    ################# CRIANDO CONTATOS #######
                    for e in email:
                        # EMAIL
                        if len(e) > 4:
                            new_contato = admmodels.Contato() 
                            new_contato.tipo = 'EMAIL'
                            new_contato.contato = e 
                            new_contato.save() 
                            new_ccontato = admmodels.ClienteContato()
                            new_ccontato.cliente = new_cliente
                            new_ccontato.contato = new_contato
                            new_ccontato.save()
                      
                    # TELEFONE CELULAR telefone_celular
                    celular = dados['telefone_celular']
                    if len(celular) > 4:
                        new_contato = admmodels.Contato()  
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular 
                        new_contato.observacao = ''
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

                    ############## COBRANCA ################
                    try:
                        fmodels.Vencimento.objects.get(dia=vencimento)
                    except:
                        print ('erro vencimento %s'%vencimento)
                        print('corrigindo vencimento %s' %vencimento)
                        new_vencimento = fmodels.Vencimento()
                        new_vencimento.dia = vencimento
                        new_vencimento.save()

                    new_cobranca = fmodels.Cobranca()
                    new_cobranca.cliente = new_cliente
                    new_cobranca.endereco = new_endereco_cobranca
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

                    ##########SAVE DO CONTRATO#######
                    new_contrato = admmodels.ClienteContrato()
                    new_contrato.id = id_contrato
                    new_contrato.cliente = new_cliente
                    new_contrato.pop = pop
                    new_contrato.cobranca = new_cobranca
                    new_contrato.data_inicio = data_cadastro
                    new_contrato.data_cadastro = data_cadastro
                    new_contrato.data_alteracao = data_cadastro
                    try:
                      new_contrato.save()
                    except:
                      print('Erro ao cadastrar CONTRATO')
                        
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = status_cc
                    new_status.modo=2
                    new_status.usuario = usuario
                    new_status.data_cadastro = data_cadastro
                    try:
                      new_status.save()
                    except:
                      print('Erro ao cadastrar CLIENTE CONTRATO STATUS')
                        
                    #####SAVE DO SERVICO#########
                    new_servico = admmodels.ServicoInternet()
                    new_servico.clientecontrato = new_contrato
                    new_servico.status = status_s
            
                    new_servico.login= login
                    new_servico.endereco = new_endereco
                    new_servico.login_password=senha
                    new_servico.login_password_plain=senha
                    new_servico.central_password=senha
                    new_servico.endereco=new_endereco_instalacao

                    
                    new_servico.mac_dhcp = None
                    new_servico.mac = None

                    
                    new_servico.ip = None

                    new_servico.tipoconexao = conexao_tipo
                    new_servico.nas = nas
                    new_servico.planointernet = planointernet
                    new_servico.modoaquisicao =  0
                    new_servico.data_cadastro=data_cadastro
                    new_servico.observacao=servico_obs
                    try:
                      new_servico.save()
                    except Exception as e:
                      print('Erro ao cadastrar SERVICO INTERNET!', e)

                    m.addRadiusServico(new_servico)

                  elif admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=dados['cpfcnpj']).count() > 0:

                    try:
                      cliente_check = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=dados['cpfcnpj'])[0]
                    except Exception as e:
                      print('Erro: ', e)
                                        
                                      
                    ##########SAVE DO COBRANCA#######
                    ############## COBRANCA ################
                    try:
                        fmodels.Vencimento.objects.get(dia=vencimento)
                    except:
                        print ('erro vencimento %s'%vencimento)
                        print('corrigindo vencimento %s' %vencimento)
                        new_vencimento = fmodels.Vencimento()
                        new_vencimento.dia = vencimento
                        new_vencimento.save()

                    new_cobranca = fmodels.Cobranca()
                    new_cobranca.cliente = cliente_check
                    new_cobranca.endereco = new_endereco_cobranca
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

                    ##########SAVE DO CONTRATO#######
                    id_contrato = dados['id_contrato']
                    new_contrato = admmodels.ClienteContrato()
                    new_contrato.id = id_contrato
                    new_contrato.cliente = cliente_check
                    new_contrato.pop = pop
                    new_contrato.cobranca = new_cobranca
                    new_contrato.data_inicio = data_cadastro
                    new_contrato.data_cadastro = data_cadastro
                    new_contrato.data_alteracao = data_cadastro
                    try:
                      new_contrato.save()
                    except:
                      print('Erro ao cadastrar CONTRATO')
                        
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = status_cc
                    new_status.modo=2
                    new_status.usuario = usuario
                    new_status.data_cadastro = data_cadastro
                    try:
                      new_status.save()
                    except:
                      print('Erro ao cadastrar CLIENTE CONTRATO STATUS')
                        
                    #####SAVE DO SERVICO#########
                    if admmodels.ServicoInternet.objects.filter(login__trim__lower=login.strip().lower()).count() > 0:
                      login = '%s_import'%login

                    new_servico = admmodels.ServicoInternet()
                    new_servico.clientecontrato = new_contrato
                    new_servico.status = status_s
                    new_servico.login= login
                    new_servico.endereco = cliente_check.endereco
                    new_servico.login_password=senha
                    new_servico.login_password_plain=senha
                    new_servico.central_password=senha
                    new_servico.endereco=new_endereco_instalacao

          
                    new_servico.mac_dhcp = None
                    new_servico.mac = None

                   
                    new_servico.ip = None
                    new_servico.tipoconexao = conexao_tipo
                    new_servico.nas = nas
                    new_servico.planointernet = planointernet
                    new_servico.modoaquisicao =  0
                    new_servico.data_cadastro=data_cadastro
                    new_servico.observacao=servico_obs
                    try:
                      new_servico.save()
                    except Exception as e:
                      print('Erro ao cadastrar SERVICO INTERNET!', e)

                    m.addRadiusServico(new_servico)
                  else:
                    print('ERRO DESCONHECIDO!')
                    continue
   
    for p in admmodels.Pop.objects.all():
      for plano in admmodels.Plano.objects.all():
          plano.pops.add(p)
          for n in nmodels.NAS.objects.all():
              n.pops.add(p)