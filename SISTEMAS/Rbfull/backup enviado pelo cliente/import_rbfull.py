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
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do NAS', required=False )
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do PORTADOR',required=False)
parser.add_argument('--paybox', dest='paybox', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--plans', dest='plans', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--subscribers', dest='subscribers', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--contracts', dest='contracts', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--charges', dest='charges', type=str, help='Arquivo importacao',required=False)
args = parser.parse_args()

'''
python import_rbfull.py --settings=sgp.wendor.settings --paybox=rbfull-paybox.csv
python import_rbfull.py --settings=sgp.wendor.settings --plans=rbfull-plains.csv
python import_rbfull.py --settings=sgp.wendor.settings --nas=2 --pop=3 --portador=1 --subscribers=  --contracts= --sync=1
python import_rbfull.py --settings=sgp.wendor.settings --charges=rbfull-charges.csv --sync=1
'''


         
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
addIdPlanos = 0
addIdCliente = 0
addIdContrato = 0
# addNumeroOcorrencia = 0
addStringLogin = ''

if args.portador_id:
  portador = fmodels.Portador.objects.get(pk=args.portador_id)

if args.nas_id:
  nas = nmodels.NAS.objects.get(pk=args.nas_id)


usuario = authmodels.User.objects.get(username='sgp')
formapagamento = fmodels.FormaPagamento.objects.all()[0]
planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')

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

contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]



if args.paybox:
  with open(args.paybox, 'rb') as csvfile:
      conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
      for row in conteudo:
        print(row)
        if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
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
          new_portador.convenio = '0'
          new_portador.carteira = '0'
          new_portador.cedente = 'PROVEDOR X'
          new_portador.cpfcnpj = '0'
          try:
            new_portador.save()
          except Exception as e:
             print('Erro ao salvar PORTADOR, ', e)
             break

          new_pontorecebimento = fmodels.PontoRecebimento()
          new_pontorecebimento.descricao = row[3]
          if row[3].strip() == '':
              new_pontorecebimento.descricao = 'BANCO_%s'%row[0]
          new_pontorecebimento.portador = new_portador
          new_pontorecebimento.empresa = admmodels.Empresa.objects.all()[0]
          new_pontorecebimento.save()


if args.plans:
  with open(args.plans, 'rb') as csvfile:
      conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
      for row in conteudo:
          try:
             if admmodels.PlanoInternet.objects.filter(id=int(row[0])+addIdPlanos).count() == 0:
              print("entrei na excessao dos planos")
              print(row[0],row[5], row[6], row[8],row[9])
              new_plano = admmodels.Plano()
              new_plano.id = int(row[0])+addIdPlanos
              new_plano.descricao = row[5]
              new_plano.preco = row[10]
              new_plano.contrato = contrato_obj
              new_plano.grupo = grupo_obj
              try:
                new_plano.save()
              except Exception as e:
                print('Erro ao cadastrar novo PLANO!', e)

              new_plano_internet = admmodels.PlanoInternet()
              new_plano_internet.id = int(row[0])+addIdPlanos
              new_plano_internet.plano = new_plano
              new_plano_internet.download = int(row[8])
              new_plano_internet.upload = int(row[9])
              new_plano_internet.diasparareduzir=row[39]
              new_plano_internet.diasparabloqueio=row[21]
              try:
                new_plano_internet.save()
              except Exception as e:
                print('Erro ao cadastrar novo PLANO INTERNET!', e)
             else:
                print('Já existe um plano com esse nome!', row[0])
          except Exception as e:
             print('Erro ao cadastrar o plano, erro: %s'%e)
              

m = manage.Manage()
usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]
if args.subscribers and args.contracts:

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)

    clientes={}
    contratos={}
  

    #load assinantes
    with open(args.subscribers, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            cliente={
                'id': int(row[0])+addIdCliente,
                'vencimento': row[6],
                'nome': row[8],
                'cpfcnpj': row[10],
                'rgie': row[11],
                'pai': row[14],
                'mae': row[15],
                'data_nascimento': row[16],
                'emails': '%s/%s'%(row[18], row[19]),
                'telefones': '%s/%s/%s'%(row[20], row[21], row[22]),
                'logradouro': row[34],
                'numero': fnum(row[35]),
                'complemento': row[36],
                'referencia': row[37],
                'bairro': row[38],
                'cidade': row[39],
                'uf': row[40],
                'cep': row[41],
                'coordenadas': row[42],
                'data_cadastro': row[43].split()[0],
                'data_atualizacao': row[44].split()[0]
              }
            clientes[indice]=cliente
            indice=indice+1

            print(row[43].split()[0], row[44].split()[0])
    #load contratos
    with open(args.contracts, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            try:
              plano_id = int(row[5])+addIdPlanos
            except:
               plano_id = 8641
            contrato={
                'id': int(row[0])+addIdContrato,
                'plano_id': plano_id,
                'cliente_id': int(row[6])+addIdCliente,
                'login': '%s%s'%(row[10],addStringLogin),
                'senha': row[11],
                'isento': row[13],
                'obs_servico': row[15],
                'ip': row[25],
                'mac': row[26],
                'status': row[38],
                'bloqueio': row[39],
                'bloqueio': row[39],
                'logradouro': row[46],
                'numero': row[47],
                'complemento': row[48],
                'referencia': row[49],
                'bairro': row[50],
                'cidade': row[51],
                'uf': row[52],
                'cep': row[53],
                'coordenadas': row[54],
                'obs_contrato': row[66],
                'dici_meio': row[67],
              }
            contratos[indice]=contrato
            indice=indice+1

    for cliente in clientes:
        dados={
                'id_cliente': clientes[cliente]['id'],
                'vencimento': clientes[cliente]['vencimento'],
                'nome': clientes[cliente]['nome'],
                'cpfcnpj': clientes[cliente]['cpfcnpj'],
                'rgie': clientes[cliente]['rgie'],
                'pai': clientes[cliente]['pai'],
                'mae': clientes[cliente]['mae'],
                'data_nascimento': clientes[cliente]['data_nascimento'],
                'emails': clientes[cliente]['emails'],
                'telefones': clientes[cliente]['telefones'],
                'logradouro': clientes[cliente]['logradouro'],
                'numero': clientes[cliente]['numero'],
                'complemento': clientes[cliente]['complemento'],
                'referencia': clientes[cliente]['referencia'],
                'bairro': clientes[cliente]['bairro'],
                'cidade': clientes[cliente]['cidade'],
                'uf': clientes[cliente]['uf'],
                'cep': clientes[cliente]['cep'],
                'coordenadas': clientes[cliente]['coordenadas'],
                'data_cadastro': clientes[cliente]['data_cadastro'],
                'data_atualizacao': clientes[cliente]['data_atualizacao'],
              }

        for contrato in contratos: 
            if clientes[cliente]['id'] == contratos[contrato]['cliente_id']:
                dados['id_contrato'] = contratos[contrato]['id']
                dados['plano_id'] = contratos[contrato]['plano_id']
                dados['login'] = contratos[contrato]['login']
                dados['senha'] = contratos[contrato]['senha']
                dados['isento'] = contratos[contrato]['isento']
                dados['obs_servico'] = contratos[contrato]['obs_servico']
                dados['ip'] = contratos[contrato]['ip']
                dados['mac'] = contratos[contrato]['mac']
                dados['status'] = contratos[contrato]['status']
                dados['bloqueio'] = contratos[contrato]['bloqueio']
                dados['bloqueio'] = contratos[contrato]['bloqueio']
                dados['cob_logradouro'] = contratos[contrato]['logradouro']
                dados['cob_numero'] = contratos[contrato]['numero']
                dados['cob_complemento'] = contratos[contrato]['complemento']
                dados['cob_referencia'] = contratos[contrato]['referencia']
                dados['cob_bairro'] = contratos[contrato]['bairro']
                dados['cob_cidade'] = contratos[contrato]['cidade']
                dados['cob_uf'] = contratos[contrato]['uf']
                dados['cob_cep'] = contratos[contrato]['cep']
                dados['obs_contrato'] = contratos[contrato]['obs_contrato']
                dados['dici_meio'] = contratos[contrato]['dici_meio']

                print('Passei aqui')
                try:
                  planointernet = admmodels.PlanoInternet.objects.get(id=dados['plano_id'])
                except:
                   print('Plano não encontrato')

                try:
                  contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='dici_meio').order_by('-id')[0]
                  grupo_obj = admmodels.Grupo.objects.filter(nome='dici_meio').order_by('-id')[0]
                  planointernet.contrato = contrato_obj
                  planointernet.grupo = grupo_obj
                  planointernet.save()
                except Exception as e:
                   print('Erro ao atualizar o planos, %s'%e)
                   pass

              

                ###SETANDO STATUS###

                if '30' in dados['status']:
                    status_cc = 1
                    status_s = 1
                    status_c = 1

                    if '1' in dados['bloqueio']:
                        status_cc = 4
                        status_s = 4
                        status_c = 4

                if '40' in dados['status']:
                    status_cc = 3
                    status_s = 3
                    status_c = 3



                print('#########################################################################################')
                print(dados)
                if args.sync_db == True and admmodels.ClienteContrato.objects.filter(id=dados['id_contrato']).count() == 0:
                  try:
                    pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %dados['cidade'])[0]
                    pop = pop_q

                  except Exception as e:
                      new_pop = admmodels.Pop()
                      new_pop.cidade=dados['cidade'].upper()
                      new_pop.uf=dados['uf']
                      try:
                        new_pop.save()
                      except:
                        print('Erro ao cadastrar novo POP!')
                      pop = new_pop
                  
                  if str(dados['data_cadastro']).strip() == '':
                     dados['data_cadastro'] = datetime.now()
                  if str(dados['data_nascimento']).strip() == '':
                     dados['data_nascimento'] = None
                     
                  new_endereco = admmodels.Endereco()
                  new_endereco.uf=dados['uf']
                  new_endereco.cep=dados['cep']
                  new_endereco.cidade=dados['cidade']
                  new_endereco.numero=dados['numero']
                  new_endereco.bairro=dados['bairro']
                  new_endereco.logradouro=dados['logradouro']
                  new_endereco.complemento=dados['complemento']
                  new_endereco.pontoreferencia=dados['referencia']
                  try:
                    new_endereco.save()
                  except Exception as a:
                    print('Erro ao cadastrar dados de ENDERECO!, erro: ',a)
                  
                  new_endereco_cob = admmodels.Endereco()
                  new_endereco_cob.uf=dados['cob_uf']
                  new_endereco_cob.cep=dados['cob_cep']
                  new_endereco_cob.cidade=dados['cob_cidade']
                  new_endereco_cob.numero=dados['cob_numero']
                  new_endereco_cob.bairro=dados['cob_bairro']
                  new_endereco_cob.logradouro=dados['cob_logradouro']
                  new_endereco_cob.complemento=dados['cob_complemento']
                  new_endereco_cob.pontoreferencia=dados['cob_referencia']
                  try:
                    new_endereco_cob.save()
                  except Exception as a:
                    print('Erro ao cadastrar dados de ENDERECO!, erro: ',a)

                  ################# CRIANDO ENDERECO COBRANÇA ########
                  new_endereco_inst=new_endereco_cob
                  new_endereco_inst.id=None
                  try:
                    new_endereco_inst.save()
                  except:
                    print('Erro ao cadastrar dados de ENDERECO DE COBRANÇA!')
                
                  ################# CRIANDO PESSOA ##########
                  if len(fnum(dados['cpfcnpj'])) > 12:
                    try:
                      new_pessoa = admmodels.Pessoa()
                      new_pessoa.tipopessoa='J'
                      new_pessoa.nome = dados['nome']
                      new_pessoa.nomefantasia = dados['nome']
                      new_pessoa.cpfcnpj = dados['cpfcnpj']
                      new_pessoa.rg= dados['rgie']
                      new_pessoa.insc_estadual = None
                      new_pessoa.tipo = 8
                      new_pessoa.save()
                    except Exception as e:
                      print('Erro ao cadastrar dados de PESSOA!: ', e)
                  else:
                      new_pessoa = admmodels.Pessoa()
                      new_pessoa.tipopessoa='F'
                      new_pessoa.nome = dados['nome']
                      new_pessoa.sexo = None
                      new_pessoa.nacionalidade = 'BR'
                      new_pessoa.rg= dados['rgie']
                      new_pessoa.cpfcnpj = dados['cpfcnpj']
                      new_pessoa.rg_emissor=''
                      new_pessoa.datanasc=dados['data_nascimento']
                      try:
                          new_pessoa.save()
                      except Exception as e:
                          print('Erro ao cadastrar dados de PESSOA! - ', e)
                  
                  ################# CRAINDO CLIENTE ########
                  new_cliente = admmodels.Cliente()
                  new_cliente.id = dados['id_cliente']
                  new_cliente.endereco = new_endereco
                  new_cliente.pessoa = new_pessoa
                  new_cliente.data_cadastro = dados['data_cadastro']
                  new_cliente.data_alteracao = dados['data_cadastro']
                  new_cliente.ativo = True
                  new_cliente.observacao = ''
                  try:
                    new_cliente.save()

                    new_cliente.data_cadastro = dados['data_cadastro']
                    new_cliente.save()
                  except Exception as a:
                    print('Erro ao cadastrar o CLIENTE!, erro: ', a)
                  
                  ################# CRIANDO CONTATOS #######
                  for e in dados['emails'].split('/'):
                      # EMAIL
                      if len(e) > 4:
                          new_contato = admmodels.Contato() 
                          new_contato.tipo = 'EMAIL'
                          new_contato.contato = e 
                          new_contato.save() 
                          new_ccontato = admmodels.ClienteContato()
                          new_ccontato.cliente = new_cliente
                          new_ccontato.contato = new_contato
                          try:
                             new_ccontato.save()
                          except Exception as e:
                             print(e)
                    
                  # TELEFONE CELULAR telefone_celular
                  for c in dados['telefones'].split('/'):
                    if len(c) > 4:
                        new_contato = admmodels.Contato()  
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = c 
                        new_contato.observacao = ''
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        try:
                            new_ccontato.save()
                        except Exception as e:
                            print(e)
                    
                  ############## COBRANCA ################
                  try:
                      fmodels.Vencimento.objects.get(dia=dados['vencimento'])
                  except:
                      print ('erro vencimento %s'%dados['vencimento'])
                      print('corrigindo vencimento %s' %dados['vencimento'])
                      new_vencimento = fmodels.Vencimento()
                      new_vencimento.dia = dados['vencimento']
                      new_vencimento.save()

                  new_cobranca = fmodels.Cobranca()
                  new_cobranca.cliente = new_cliente
                  new_cobranca.endereco = new_endereco_cob
                  new_cobranca.portador = portador
                  new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=dados['vencimento'])
                  new_cobranca.isento = int(dados['isento'])
                  new_cobranca.notafiscal = False
                  new_cobranca.data_cadastro = dados['data_cadastro']
                  new_cobranca.datacobranca1 = dados['data_cadastro']
                  new_cobranca.usuariocad = usuario
                  new_cobranca.formacobranca = formacobranca
                  new_cobranca.status = status_c
                  try:
                    new_cobranca.save()

                    new_cobranca.data_cadastro = dados['data_cadastro']
                    new_cobranca.save()
                  except Exception as e:
                     print(e)
                  ##########SAVE DO CONTRATO#######
                  new_contrato = admmodels.ClienteContrato()
                  new_contrato.id = dados['id_contrato']
                  new_contrato.cliente = new_cliente
                  new_contrato.pop = pop
                  new_contrato.cobranca = new_cobranca
                  new_contrato.data_inicio = dados['data_cadastro']
                  new_contrato.data_cadastro = dados['data_cadastro']
                  new_contrato.data_alteracao = dados['data_cadastro']
                  try:
                    new_contrato.save()

                    new_contrato.data_inicio = dados['data_cadastro']
                    new_contrato.data_cadastro = dados['data_cadastro']
                    new_contrato.data_alteracao = dados['data_cadastro']
                    new_contrato.save()
                  except Exception as e:
                    print('Erro ao cadastrar CONTRATO', e)
                      
                  new_status = admmodels.ClienteContratoStatus()
                  new_status.cliente_contrato = new_contrato
                  new_status.status = status_cc
                  new_status.modo=2
                  new_status.usuario = usuario
                  new_status.data_cadastro = dados['data_cadastro']
                  try:
                    new_status.save()
                  except Exception as e:
                    print('Erro ao cadastrar CLIENTE CONTRATO STATUS', e)
                      
                  #####SAVE DO SERVICO#########
                  new_servico = admmodels.ServicoInternet()
                  new_servico.clientecontrato = new_contrato
                  new_servico.status = status_s
                  if admmodels.ServicoInternet.objects.filter(login__lower__trim=dados['login'].lower().strip()).count() > 0:
                     dados['login'] += addStringLogin
                  new_servico.login= dados['login']
                  new_servico.endereco = new_endereco_cob
                  new_servico.login_password=dados['senha']
                  new_servico.login_password_plain=dados['senha']
                  new_servico.central_password=dados['senha']
                  new_servico.endereco=new_endereco_inst

                  if admmodels.ServicoInternet.objects.filter(Q(mac=dados['mac'])|Q(mac_dhcp=dados['mac'])).count() == 0:
                      new_servico.mac_dhcp = dados['mac']
                      new_servico.mac = dados['mac']

                  try:
                    if dados and admmodels.ServicoInternet.objects.filter(Q(ip=dados['ip'])).count() == 0:
                      new_servico.ip = dados['ip']
                  except:
                    new_servico.ip = None
                         

                  new_servico.tipoconexao = 'ppp'
                  new_servico.nas = nas
                  new_servico.planointernet = planointernet
                  new_servico.modoaquisicao =  0
                  new_servico.data_cadastro=dados['data_cadastro']
                  new_servico.observacao=dados['obs_servico']
                  try:
                    new_servico.save()

                    new_servico.data_cadastro=dados['data_cadastro']
                    new_servico.observacao=dados['obs_servico']
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





if args.charges:
  with open(args.charges, 'rb') as csvfile:
      conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
      for row in conteudo:          
        cliente_id = int(row[3])+addIdCliente
        cliente = admmodels.Cliente.objects.filter(id=cliente_id)
        if cliente:
            print("Esse é meu cliente: ", cliente)
            cliente = cliente[0]
            contrato = cliente.clientecontrato_set.all()
            if contrato:
                contrato = contrato[0]
                cobranca = contrato.cobranca
                
                numero_documento = row[0]
                nosso_numero = row[0]
                nosso_numero_f = row[0]
                demonstrativo = row[22]
                data_documento = row[43].split()[0]
                data_vencimento = row[24]
                if row[29].strip() != '':
                  data_pagamento = row[29].split()[0]
                else:
                   data_pagamento = None
                data_baixa = data_pagamento
                data_cancela = None
                status = fmodels.MOVIMENTACAO_GERADA
                valorpago = None
                usuario_b = None
                usuario_c = None
                juros = ''
                codigo_barras=row[15]
                linha_digitavel=row[15]
                valor = row[27].replace('.','').replace(',','.')
                portador = fmodels.Portador.objects.get(pk=row[5])

                if data_pagamento != None:
                    valorpago = row[11].replace('.','').replace(',','.')
                    status = fmodels.MOVIMENTACAO_PAGA
                    usuario_b = usuario
                    usuario_c = None
                    valorpago = row[31]
                    if valorpago.strip() == '':
                       valorpago = valor

                elif row[46].strip() != '':
                    data_cancela = data_vencimento
                    status = fmodels.MOVIMENTACAO_CANCELADA
                    data_baixa = None
                    data_pagamento = None
                    usuario_b = None
                    usuario_c = usuario

                desconto = 0.00
                linha_digitavel = ''
                codigo_carne = ''

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
                                  'observacao': codigo_carne,
                                  'djson': {'juros': juros }
                                  }
                        if not args.sync_db:
                            print(dados)
                        else:
                            try:
                                titulo = fmodels.Titulo(**dados)
                                titulo.save()
                                titulo.data_documento=data_documento
                                titulo.data_alteracao=data_documento
                                titulo.save()

                            except Exception as e:
                                print "Erro cadastrar",e,dados
                    else:
                        print("Boleto já foi importado ",cliente,nosso_numero,data_vencimento,portador)