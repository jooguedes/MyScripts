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
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS', required=False )
parser.add_argument('--portador', dest='portador', type=int, help='Portador id',required=False)
parser.add_argument('--contratos', dest='contratos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--assinantes', dest='assinantes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--titulos', dest='titulos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--chamados', dest='chamados', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--pop', dest='pop', type=int, help='POP', required=False )
args = parser.parse_args()


#####################################################IMPORT GERAL###################################################################
#                                                                                                                                  #
#   python import_rbfull.py --settings=sgp.cristalnet.settings --nas=6 --pop=48 --portador=14 --assinantes=  --contratos= --sync=1           #
#   python import_rbfull.py --settings=sgp.cristalnet.settings --portador=14 --assinantes= --titulos=                               #
#   python import_rbfull.py --settings=sgp.cristalnet.settings --chamados=                                                         #
#                                                                                                                                  #
####################################################################################################################################


##################### ARQUIVOS NECESSARIOS ###########################
#                     Assinantes.csv                                 #
#                     Contratos.csv                                  #
#                     titulos.csv                                    #
#                     chamados.csv                                   #
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
from apps.atendimento import models as amodels
from apps.netcore.utils.radius import manage
from apps.cauth import models as authmodels
from apps.fiscal import models as fismodels, constants as fisconstants

# Se já existir clientes na base adicionar os valores de increments
addIdCliente = 25
addIdContrato = 25
addNumeroOcorrencia = 25
addStringLogin = ''

if args.portador:
  portador = fmodels.Portador.objects.get(pk=args.portador)
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
if args.assinantes and args.contratos:

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)

    clientes={}
    contratos={}
  

    #load assinantes
    with open(args.assinantes, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            cliente={
                'id': int(row[0])+addIdCliente,
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
                'id': int(row[0])+addIdContrato,
                'nome': row[1],
                'cpfcnpj':row[2],
                'rgie': row[3],
                'plano': row[4],
                'valor': row[5],
                'isento': row[6],
                'login': '%s%s'%(row[7],addStringLogin),
                'senha': row[8],
                'vencimento': row[9].strip(),
                'status': row[10],
                'data_cancelamento': row[17],
                'logradouro_inst': row[20],
                'numero_inst': row[21],
                'complemento_inst': str(row[22]),
                'referencia_inst': str(row[23]),
                'bairro_inst': row[24],
                'cidade_inst': row[25],
                'estado_inst': row[26],
                'cep_inst': row[27],
                'coordenadas': row[28],
                'email2': row[30],
                'ip': row[38],
                'mac': row[39]
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
                dados['referencia_inst'] = contratos[contrato]['referencia_inst']
                dados['bairro_inst'] = contratos[contrato]['bairro_inst']
                dados['cidade_inst'] = contratos[contrato]['cidade_inst']
                dados['estado_inst'] = contratos[contrato]['estado_inst']
                dados['cep_inst'] = contratos[contrato]['cep_inst']
                dados['coordenadas'] = contratos[contrato]['coordenadas']
                dados['ip'] = contratos[contrato]['ip']
                dados['mac'] = contratos[contrato]['mac']
                dados['vencimento'] = contratos[contrato]['vencimento']
                dados['email2'] = contratos[contrato]['email2']

                #### VARIAVEIS ####
                #ALTERAR NOME DO PLANO PARA BASE EM USO
                plano = '%s@rbfull'%dados['plano']
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
                if numero == '':
                  numero = None
                bairro = dados['bairro']
                logradouro = dados['logradouro']
                complemento = dados['complemento']
                

                cep_isnt = dados['cep_inst']
                numero_isnt = dados['numero_inst']
                if numero_isnt ==  '':
                  numero_isnt = None
                bairro_isnt = dados['bairro_inst']
                logradouro_isnt = dados['logradouro_inst']
                uf_isnt = dados['estado_inst']
                cidade_isnt = dados['cidade_inst']
                complemento_isnt = dados['complemento_inst']
                referencia_inst = dados['referencia_inst']

                cpfcnpj = dados['cpfcnpj']
                nome = dados['nome']
                nomefantasia = dados['nome_fantasia']
                rg = dados['rg']
                data_nascimento = strdate(dados['data_nascimento'])

                #ALTERAR AQUI PARA BASE EM USO 
                id_cliente = int(dados['id_cliente']) + 25000
                data_cadastro = dados['data_cadastro'][:10].strip()

                email = dados['email'].split('/')
                email2 = dados['email2'].split('/')
                telefonecom = dados['telefone_fixo']
                telefonecom = dados['telefone_fixo']

                vencimento = 10
                if dados['vencimento'] != '' and dados['vencimento'] != None:
                  vencimento = dados['vencimento']

                isento = 0
                if dados['isento'] == 'Isento':
                  isento = 100

                #ALTERAR AQUI PARA BASE EM USO 
                id_contrato = int(dados['id_contrato']) + 25000
              

                #ALTERAR AQUI PARA BASE EM USO 
                login = '%s@rbfull'%dados['login']
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
                      planointernet = admmodels.PlanoInternet.objects.filter(plano__id=106)[0]
                    print('criado plano %s' %plano)

                    

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
                      print('Erro ao cadastrar novo POP!')
                    pop = new_pop'''
                
                pop=admmodels.Pop.objects.get(id=args.pop)
                nas=nas_default

                if args.sync_db == True:

                  ################# CRIANDO ENDERECO CLIENTE ########
                  new_endereco = admmodels.Endereco()
                  new_endereco.uf=uf
                  new_endereco.cep=cep
                  new_endereco.cidade=cidade
                  new_endereco.numero=numero
                  new_endereco.bairro=bairro
                  new_endereco.logradouro=logradouro
                  new_endereco.complemento=complemento
                  try:
                    new_endereco.save()
                  except Exception as a:
                    print('Erro ao cadastrar dados de ENDERECO!, erro: ',a)

                  ################# CRIANDO ENDERECO COBRANÇA ########
                  new_endereco_cobranca=copy.copy(new_endereco)
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
                  new_endereco_instalacao.logradouro=complemento_isnt
                  new_endereco_instalacao.referencia=referencia_inst
                  try:
                    new_endereco_instalacao.save()
                  except Exception as a:
                    print('Erro ao cadastrar dados de ENDERECO INSTALAÇÃO!, erro: ',a)

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
                      new_cliente.id = id_cliente
                      new_cliente.endereco = new_endereco
                      new_cliente.pessoa = new_pessoa
                      new_cliente.data_cadastro = data_cadastro
                      new_cliente.data_alteracao = data_cadastro
                      new_cliente.ativo = True
                      new_cliente.observacao = ''
                      new_cliente.save()
                    except Exception as a:
                      print('Erro ao cadastrar o CLIENTE!, erro: ', a)
                    
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
                    
                    for e in email2:
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
                    new_servico.observacao=servico_obs
                    try:
                      new_servico.save()
                    except:
                      print('Erro ao cadastrar SERVICO INTERNET!')

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
                    new_servico.observacao=servico_obs
                    try:
                      new_servico.save()
                    except:
                      print('Erro ao cadastrar SERVICO INTERNET!')

                    m.addRadiusServico(new_servico)
                  else:
                    print('ERRO DESCONHECIDO!')
                    continue
   
    for p in admmodels.Pop.objects.all():
      for plano in admmodels.Plano.objects.all():
          plano.pops.add(p)
          for n in nmodels.NAS.objects.all():
              n.pops.add(p)
  

if args.titulos and args.assinantes:
  clientes ={}
  with open(args.assinantes, 'rb') as csvfile:
      conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
      indice = 0
      for row in conteudo:
          cliente={
                'id': int(row[0])+int(addIdCliente) + 25000,
                'nome': row[1],
                'cpfcnpj':row[3]
                }
          clientes[indice]=cliente
          indice +=1


  with open(args.titulos, 'rb') as csvfile:
      conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
      for row in conteudo:
          try:
              for c in clientes:
                  if clientes[c]['cpfcnpj'] == row[2]:
                      cpfcnpj = clientes[c]['cpfcnpj']
                      cpfcnpj = fnum(cpfcnpj)
                      servico = None
                      try:
                          if cpfcnpj and cpfcnpj != '':
                              servico = admmodels.ServicoInternet.objects \
                                  .filter(Q(clientecontrato__cliente__pessoa__cpfcnpj__numfilter=cpfcnpj))[:1]
                          else:
                              ilike = '%'.join(row[1].strip().lower().split())
                              servico = admmodels.ServicoInternet.objects \
                                  .filter(Q(clientecontrato__cliente__pessoa__nome__unaccent__ilike='%%%s%%' %ilike))

                          if not servico:
                              print('nao achei Cliente %s' %row[1].strip().lower())
                              continue
                          if servico:
                              servico = servico[0]
                              contrato = servico.clientecontrato
                              cobranca = contrato.cobranca
                              cliente = contrato.cliente
                              usuario = authmodels.User.objects.get(username='sgp')
                              descricao = 'Telefone: %s'%unicode(row[5].decode('latin-1'))
                              nosso_numero_f = None
                              data_vencimento = strdate(row[9])
                              data_documento = data_vencimento
                              data_pagamento = None
                              data_cancela = None
                              usuario_b = None
                              data_baixa = None
                              valorpago = None
                              status = fmodels.MOVIMENTACAO_GERADA
                              valor = row[5].replace('R$', '').replace(',', '.').strip()
                              observacao = None
                              if 'Pago' in row[7]:
                                  data_pagamento = strdate(row[10])
                                  valorpago = row[6].replace('R$', '').replace(',', '.').strip()
                                  status =  fmodels.MOVIMENTACAO_PAGA
                                  usuario_b = usuario 
                                  data_baixa = data_pagamento 
                              numero_documento = row[0].strip()
                              nosso_numero = numero_documento     
                              desconto = 0.00
                              linha_digitavel = None 
                              codigo_barras = None
                              
                              if nosso_numero:
                                  if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador).count() == 0:
                                      dados = {'cliente': cliente,
                                              'cobranca': cobranca,
                                              'portador': portador,
                                              'formapagamento': fmodels.FormaPagamento.objects.all()[0],
                                              'centrodecusto': fmodels.CentrodeCusto.objects.get(codigo='01.01.01'),
                                              'modogeracao': 'l',
                                              'usuario_g': usuario,
                                              'usuario_b': usuario,
                                              'demonstrativo': descricao,
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
                                              'observacao': observacao
                                              }
                                      #print dados
                                      print("Importando boleto",cliente,nosso_numero,data_vencimento,portador)
                                      try:
                                          titulo = fmodels.Titulo(**dados)
                                          titulo.save()
                                          nosso_numero_f = titulo.getNossoNumero()
                                          if nosso_numero_f:
                                              titulo.nosso_numero_f = re.sub('[^0-9A-Z]', '', nosso_numero_f) 
                                          titulo.data_documento=data_documento
                                          titulo.data_alteracao=data_documento
                                          titulo.save()
                                      except Exception as e:
                                          print("Erro cadastrar",e,dados)
                      except Exception(a):
                          print(a)
          except Exception as e:
              print(e)


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
            protocolo = row[2]
            if len(protocolo) > 14:
                try:
                  protocolo = protocolo[14:]
                except:
                  protocolo = protocolo[:14]
            login = '%s%s'%(row[1].strip().lower(),addStringLogin)
            assunto = row[3]
            status = row[4].strip()
            data_cadastro = format_data(row[10])
            try:
              data_agendamento = format_data(row[11])
            except:
              data_agendamento = None
            try:
              data_finalizacao = format_data(row[11])
            except:
              data_finalizacao = None
            conteudo = 'Prioridade: %s \n%s - %s | %s \n%s'%(row[5], row[6], row[7],assunto, row[8])
            if conteudo == "" or conteudo is None:
                conteudo = "Campo conteúdo vazio no RBFULL."
            servicoprestado = 'Chamado executado por %s'%row[9]

            servico = admmodels.ServicoInternet.objects.filter(login__trim__lower=login)

            if servico:
                clientecontrato = servico[0].clientecontrato
                tipo_obj = amodels.Tipo.objects.filter(descricao=row[6])
                motivo_obj = amodels.MotivoOS.objects.filter(descricao=row[6])

                if tipo_obj:
                    tipo_obj = tipo_obj[0]
                else:
                    tipo_obj = amodels.Tipo()
                    tipo_obj.codigo=cdtipo
                    tipo_obj.descricao=row[6]
                    tipo_obj.save()
                    cdtipo += 1

                if motivo_obj:
                    motivo_obj = motivo_obj[0]
                else:
                    motivo_obj = amodels.MotivoOS()
                    motivo_obj.codigo=cdmotivo
                    motivo_obj.descricao=row[6]
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
                    ocorrencia['status'] = amodels.OCORRENCIA_ABERTA if status in ['Aberto', 'Aguardando'] else amodels.OCORRENCIA_ENCERRADA
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

                    try:
                      new_ocorrencia = amodels.Ocorrencia(**ocorrencia)
                      new_ocorrencia.save()
                    except:
                      ocorrencia['data_agendamento'] = None
                      ocorrencia['data_finalizacao'] = data_cadastro
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
                    ordem['status'] = amodels.OS_ABERTA if status != '' else amodels.OS_ENCERRADA
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