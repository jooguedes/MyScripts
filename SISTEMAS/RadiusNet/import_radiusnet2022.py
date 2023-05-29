#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from lib2to3.pytree import type_repr
import os, sys
from datetime import date, datetime
import copy
from tabnanny import process_tokens
from tkinter.dnd import dnd_start
from tkinter.tix import ROW
from typing import ClassVar
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
parser.add_argument('--endereco', dest='endereco', type=str, help='Arquivo de importacao do endereco', required=False)
parser.add_argument('--clienteplano', dest='clienteplano', type=str, help='arquivo de importacao dos plano dos clientes', required=False)
parser.add_argument('--ordemservico', dest='ordemservico', type=str, help='arquivo de importacao da ordens de servico')
parser.add_argument('--ocorrencia', dest='ocorrencia', type=str, help='arquivo de importacao da ordens de ocorrencias')
parser.add_argument('--cobranca', dest='cobranca', type=str, help='arquivo de cobrancas', required=False)
parser.add_argument('--observacoes', dest='observacoes', type=str, help='arquivo dos clieentes que o radiusnet enviou', required=False)
parser.add_argument('--clientenotafiscal', dest='clientenotafiscal', type=str, help='mesmo arquivo dos clientes que foi retirado do radius net pela interface web', required=False)

parser.add_argument('--pop', dest='pop', type=str, help='Arquivo importacao',required=False)
'''import dos clientes'''
#python import_radiusnet.py --settings=sgp.holznetwork.settings --nas=1 --portador=1 --clientes=Conv-relatorio-clientes-radiusnet.csv --endereco=Conv-Endereco.csv --clienteplano=Conv-Cliente_plano.csv --ordemservico=Conv-OrdemServico.csv
'''import das observacoes'''
#python import_radiusnet.py --settings=sgp.holznetwork.settings --nas=1 --portador=1 --observacoes=Conv-obs.csv --sync=1
'''Import dos titulos'''
#python import_radiusnet.py --settings=sgp.holznetwork.settings --nas=1 --portador=1 --titulos=Conv-Cobranças_01.csv --sync=1

'''IMPORT NOTAS FISCAIS'''
#python import_radiusnet.py --settings=sgp.holznetwork.settings --nas=1 --portador=1 --notasfiscais=Conv-NotaFiscal.csv --cobranca=Conv-cobrancas-bkup-radius-net.csv --clientenotafiscal=Conv-relatorio-clientes-radiusnet.csv --sync=1


'''IMPORT DOS TITULOS DAS NOTAS FISCAIS'''
#python import_radiusnet.py --settings=sgp.holznetwork.settings --nas=1 --portador=1  --cobranca=Conv-Cobranças_01.csv --notatitulo=Conv-NotaFiscal.csv --sync=1

'''IMPORT OCORRENCIAS'''
#python import_radiusnet.py --settings=sgp.softbahia.settings --clientes=Conv-Cobranças_01.csv --clienteplano=Conv-NotaFiscal.csv --ordemservico=

################################################ARQUIVOS NECESSÁRIOS ################################################
#                                                                                                                   #                                         
#                                         Realtorio_dados_clientes.csv (retirado do sistema                         #
#                                         endereco.csv (enviado pelo radius net)                                    #
#                                         clientePlano.csv (enviado radius net)                                     #
#                                         cadastroCliente  (enviado radius net)                                     #
#                                         ordemservico.csv (enviado radiusnet                                       #
#                                         cobrancas(retirado do sistema)                                            #
#                                                                                                                   #
#####################################################################################################################


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


ordens_servico={}
clientes_plano={}
enderecos={}
clientes={}
emails={}
cobrancas={}
notasfiscais={}
protocolo=[]

ocorrencias={}



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


##########FUNCOES AUXILIARES###############




def busca_endereco(id):
    for endereco in enderecos:
       if enderecos[endereco]['id_cliente'] == id:
            dados={
                'id_cliente': enderecos[endereco]['id_cliente'],
                'uf':enderecos[endereco]['uf'],
                'cidade':enderecos[endereco]['cidade'],
                'logradouro': enderecos[endereco]['logradouro'],
                'numero':enderecos[endereco]['numero'],
                'coplemento': enderecos[endereco]['complemento'],
                'cep': enderecos[endereco]['cep'],
                'bairro': enderecos[endereco]['bairro'],

            }
            return dados
    
    return 0


if args.clientes:

    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]
    nas = nmodels.NAS.objects.get(pk=args.nas)
    portador = fmodels.Portador.objects.get(pk=args.portador)
   
    #load email
    '''with open(args.email, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotchar='')
        indice=0
        for row in conteudo:
            email={
                'id':row[0],
                'email':row[1],
                'id_cliente':row[2]
            }
            emails[indice]=email
            indice=indice+1'''


    #load endereco
    with open(args.endereco, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
        indice=0
        for row in conteudo:
            endereco={
                'id':row[0],
                'id_cliente': row[1],
                'uf':row[2],
                'cidade':row[3],
                'logradouro': row[4],
                'numero':row[5],
                'complemento': row[6],
                'cep': row[7],
                'bairro': row[8],
            }

            enderecos[indice]=endereco
            indice=indice+1


    #load cliente plano
    with open(args.clienteplano, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
       
        indice=0
        for row in conteudo:
            cliente_plano={
                'id':row[0],
                'id_cliente': row[1],
                'nome_plano':  row[2],
            }

            clientes_plano[indice]=cliente_plano
            indice=indice+1
    
    
    #load ordem de servico
    if args.ordemservico:
        with open(args.ordemservico, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
            indice=0
            for row in conteudo:
                ordem_servico={
                    'id_ordem_servico':row[0],
                    'protocolo': row[1],
                    'cliente_plano_id':  row[2],
                    'data_abertura': row[3],
                    'data_finalizacao': row[4],
                    'descricao': row[5]
                }
                ordens_servico[indice]=ordem_servico
                indice= indice+1
            
    if args.ocorrencia:
        with open(args.ocorrencia, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
            indice=0
            for row in conteudo:
                ocorrencia={
                    'id_ordem_servico':row[1],
                    'data_ocorrencia': row[2],
                    'descricao': row[3],
                }
                ocorrencias[indice]=ocorrencia
                indice= indice+1

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
    #nome_pano
    #vencimento
    #ip
    #usuario
    #senha
    #email
    #telefone
    #plano_valor
    #mac



    #load cliente
    with open(args.clientes, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
        indice=0
        for row in conteudo:
            cliente={
                'id': row[0],
                'tipo_pesssoa': row[1],
                'status': row[9],
                'nome': row[2],
                'cpfcnpj': row[3],
                'rg': row[5],
                'data_nascimento': row[8],
                'nome_fantasia': row[4],
                'incricao_estadual': row[6],
                'inscricao_municipal': row[7],
                'data_cadastro': row[10],
                'nome_plano': row[11],
                'vencimento': row[17],
                'ip': row[15],
                'usuario': row[13],
                'senha': row[14],
                'email': row[18],
                'telefone': row[19],
                'plano_valor': row[12],
                'mac': row[16]
            }

            clientes[indice]=cliente
            indice=indice+1
  
  
    #load cobrancas    
    if args.cobranca:   
        with open(args.cobranca, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
            indice=0
            for row in conteudo:
                cobranca={
                    'id': row[0],
                    'id_cliente':row[2],
                    'data_vencimento': row[7],
                    'valor_total': row[8],
                    'nosso_numero': row[4], 
                    'pago': row[9]
                                }

                cobrancas[indice]=cobranca
                indice = indice + 1


    #load NotaFiscal
    if args.notasfiscais:     
        with open(args.notasfiscais, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
            indice = 0
            for row in conteudo:
                nota={
                    'id': row[0],
                    'id_cobranca': row[1],
                    'numero': row[2],
                    'data_emissao': row[3],
                    'data_servico': row[4],
                    'CFOP': row[5],
                    'aliquota': row[7]
                }
                indice= indice+1


    
    for  cliente in clientes:
        dados={
            'id': clientes[cliente]['id'],
            'status': clientes[cliente]['status'],
            'tipo_pessoa': clientes[cliente]['tipo_pesssoa'],
            'nome': clientes[cliente]['nome'],
            'cpfcnpj': clientes[cliente]['cpfcnpj'],
            'rg': clientes[cliente]['rg'],
            'data_cadastro': clientes[cliente]['data_cadastro'],
            'data_nascimento': clientes[cliente]['data_nascimento'],
            'nome_fantasia': clientes[cliente]['nome_fantasia'],
            'incricao_estadual': clientes[cliente]['incricao_estadual'],
            'inscricao_municipal':clientes[cliente]['inscricao_municipal'],
            'vencimento': clientes[cliente]['vencimento'],
            'ip': clientes[cliente]['ip'],
            'nome_plano':clientes[cliente]['nome_plano'],
            'usuario': clientes[cliente]['usuario'],
            'senha': clientes[cliente]['senha'],
            'email': clientes[cliente]['email'],
            'telefone': clientes[cliente]['telefone'],
            'plano_valor': clientes[cliente]['plano_valor'],
            'mac': clientes[cliente]['mac']
        }



        for endereco in enderecos:
            
            if enderecos[endereco]['id_cliente']==clientes[cliente]['id']:
                dados['cidade']= enderecos[endereco]['cidade']
                dados['uf']= enderecos[endereco]['uf']
                dados['logradouro']= enderecos[endereco]['logradouro'],
                dados['numero'] = enderecos[endereco]['numero']
                dados['complemento'] = enderecos[endereco]['complemento']
                dados['cep']= enderecos[endereco]['cep']
                dados['bairro']= enderecos[endereco]['bairro']
        



      ######################## MONTANDO CLIENTE ##################

        idcliente = dados['id']
        nome = dados['nome']
        cpfcnpj = dados['cpfcnpj']
        nomefantasia = dados['nome_fantasia']
        rg = dados['rg']
        insc_estadual = dados['incricao_estadual']
        insc_municipal = dados['inscricao_municipal']
        data_nasc = convertdata(dados['data_nascimento'])
        status = dados['status']
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
        data_cadastro = convertdata(dados['data_cadastro'])

       
       ############ MONTANDO PLANO CLIENTE ##############
        plano = dados['nome_plano']
        plano_valor = float (fnum2(str(dados['plano_valor']).replace('R$ ','').replace('.','').replace(',','.')))
        plano_download = 2048 
        plano_upload = 2048 

        login = dados['usuario']
        if not login:
            login = 'semlogin%s' %idcliente 
        senha = dados['senha']
        if not senha:
            senha = login

        ip = dados['ip']
        mac= dados['mac']
        if not ip:
            ip = None
        if not mac:
            mac = None

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

        vencimento = row[17] or 10

        try:
            new_vencimento = fmodels.Vencimento.objects.get(dia=row[17] or 10)
        except:
            new_vencimento = fmodels.Vencimento()
            new_vencimento.dia = row[17] or 10
            new_vencimento.save()

        emails = str(dados['email']).split(';')
        telefones = str(dados['telefone']).split('||')

        cidade=''
        uf=''
        logradouro=''
        numero=''
        complemento=''
        cep=''
        bairro=''

            ###################### ENDERECO #####################
       
       
        uf=dados['uf']
        logradouro=''.join(dados['logradouro'])
        #print('esse é meu logradouro', dados['logradouro'])
        cidade=str(dados['cidade'])
        numero=dados['numero']
        complemento=dados['complemento']
        cep=dados['cep']
        bairro=dados['bairro']

        

        cidade_q = normalize('NFKD', unicode(cidade)).encode('ASCII','ignore')
        try:
            pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
            pop = pop_q
        except:
            new_pop = admmodels.Pop()
            new_pop.cidade=cidade_q.upper()
            new_pop.uf=uf
            new_pop.save()
            pop = new_pop

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
        print ('vencimento: ', vencimento, 'Plano: ', plano, 'Numero:',numero, 'Login:', login)
        print (telefones,emails)
        print (login,senha,ip,mac)
        print '####################################################'
        if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=login).count() == 0:
            print "Import %s" %nome
            # Save Models

            cliente_check = admmodels.Cliente.objects.filter(id=idcliente)

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







#################### CADASTRA COM BASE NO PORTADOR ########################
if args.titulos:
    portador = fmodels.Portador.objects.get(pk=args.portador)
    with open(args.titulos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print("passei 01")
            id_cliente = fnum(normalize('NFKD', unicode(row[1])).encode('ASCII','ignore').strip().lower())
            if not id_cliente:
                continue
            cliente = admmodels.Cliente.objects.filter(Q(id=id_cliente))
            if cliente:
                print("passei 02")
                cliente = cliente[0]
                cobranca_set = cliente.cobranca_set.all()
                if not cobranca_set:
                    cobranca = None
                else:
                    cobranca = cobranca_set[0]
                if fmodels.Titulo.objects.filter(portador=portador,
                                                 numero_documento=row[0]).count() == 0:
                    print("passei 03")
                    print row
                    tdata = {}
                    tdata['cliente'] = cliente
                    tdata['cobranca'] = cobranca
                    tdata['nosso_numero'] = row[3] # nrboleto
                    tdata['numero_documento'] = row[0] # documento
                    if not tdata['nosso_numero']:
                        tdata['nosso_numero'] = tdata['numero_documento']

                    tdata['parcela'] = 1
                    tdata['portador'] = portador        
                    tdata['valor'] = row[7].replace('R$ ','').replace('.','').replace(',','.')
                    tdata['observacao'] = ''
                    tdata['demonstrativo'] = 'Período: %s' %row[6]
                    tdata['valorpago'] =row[9].replace('R$ ','').replace('.','').replace(',','.')  
                    tdata['data_baixa'] = convertdata(row[10])
                    tdata['data_pagamento'] = convertdata(row[10])
                    tdata['data_documento'] = convertdata(row[4]) # emissao
                    tdata['data_vencimento'] = convertdata(row[5]) # vencimento
                    #tdata['data_cancela'] = ro w[13]

                    if row[10] == '':
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











#DADOS PEGOS DO ARQUIVO CADASTRO_CLIENTE.CSV QUE O RADIUS NET ENVIOU
if args.observacoes:
    observacoes={}
    with open(args.observacoes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        indice=0
        for row in conteudo:
            cliente_obs=row[12]
            id_cliente=row[0]

            print("observação:", cliente_obs)
            if args.sync_db==True:

                cliente= admmodels.Cliente.objects.filter(id=id_cliente).update(observacao=cliente_obs)
                



#DADOS RETIRADOS DOS ARQUIVOS DE COBRANCA E NOTA FISCAL QUE O RADIUSNET ENVIOU
empresa='09.177.560/0001-90' 
if args.notasfiscais:
    nota={}
    with open(args.clientenotafiscal, 'rb') as csvfile:
        conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
        indice=0
        for row in conteudo:
            cliente={
                'id': row[0],
                'nome': row[2],
                'cpfcnpj': row[3],
                'rg': row[5],
            }

            clientes[indice]=cliente
            indice=indice+1
    

    #load cobrancas    
    if args.cobranca:   
        with open(args.cobranca, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
            indice=0
            for row in conteudo:
                cobranca={
                    'id': row[0],
                    'id_cliente':row[2],
                    'data_vencimento': row[7],
                    'valor_total': row[8],
                    'nosso_numero': row[4], 
                    'pago': row[9]
                                }

                cobrancas[indice]=cobranca
                indice = indice + 1

  
    empresa = admmodels.Empresa.objects.get(cpfcnpj__numfilter=empresa)
    with open(args.notasfiscais, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            for cobranca in cobrancas:
                if row[1]==cobrancas[cobranca]['id']:
                    for cliente in clientes:    
                        if cobrancas[cobranca]['id_cliente']==clientes[cliente]['id']:
                            nota={
                                'id': clientes[cliente]['id'],
                                'data_emissao': row[3],
                                'valor_total': cobrancas[cobranca]['valor_total'],
                                'cfop':row[5],
                                'cpfcnpj': clientes[cliente]['cpfcnpj'],
                                'numero': row[2]
                            
                            }

            #print("essa é a nota: ", nota)
            if fismodels.NotaFiscal.objects.filter(empresa=empresa,numero=row[1]).count() == 0:
                cliente = admmodels.Cliente.objects.filter(id=nota['id'])
                contratos= admmodels.ServicoInternet.objects.filter(clientecontrato__cliente=cliente[0].id)
                #contrato= admmodels.ServicoInternet.objects.filter(clientecontrato__cliente__pessoa__cpfcnpj__numfilter=nota['cpfcnpj'])
                descricoes={}
                increment=0
                if cliente:
                    cliente = cliente[0]
                    nfdest = {}
                    #print('Esse é meu contrato', contrato[0].planointernet.plano.descricao)
                    #print("O tamanho é",contrato.count())
                    indice=0
                    for contrato in contratos:
                        descricao={
                            'descricao':contrato.planointernet.plano.descricao,
                            'valor': contrato.planointernet.plano.preco
                        }
                        descricoes[indice]=descricao
                        indice=indice+1


                    
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

                    #print(nfdest)
                    if args.sync_db:
                        nfdest_obj = fismodels.NFDestinatario(**nfdest)
                        nfdest_obj.save()

                    nf = {}
                    if args.sync_db:
                        nf['destinatario'] = nfdest_obj
                    nf['empresa'] = empresa
                    nf['data_emissao'] = convertdata(row[3])
                    nf['data_saida'] = convertdata(row[4])
                    nf['modelo'] = '21'
                    nf['tipoutilizacao'] = '4'
                    nf['serie'] = 'U'
                    nf['numero']= nota['numero']
                    nf['valortotal'] = nota['valor_total']
                    nf['icms'] = 0
                    nf['outrosvalores'] = nota['valor_total']
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
                        nf['cfop'] = fismodels.CFOP.objects.get(cfop=nota['cfop'])
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
                    for descricao in descricoes:
                        nfitem = {}
                        if args.sync_db:
                            nfitem['notafiscal'] = new_nf
                        nfitem['descricao'] = descricoes[descricao]['descricao']
                        nfitem['codigoservico'] = '010101'
                        nfitem['classificacao'] = '0104'
                        nfitem['unidade'] = ''
                        nfitem['qt_contratada'] = 1
                        nfitem['qt_fornecida'] = 1
                        nfitem['valortotal'] = Decimal(descricoes[descricao]['valor'])
                        nfitem['desconto'] = Decimal('0.00')
                        nfitem['acrescimo_despesa'] = Decimal('0.00')
                        nfitem['bcicms'] = Decimal('0.00')
                        nfitem['icms'] = Decimal('0.00')
                        nfitem['outrosvalores'] = Decimal(nota['valor_total'])
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



if args.notatitulo :
    empresa = admmodels.Empresa.objects.get(cpfcnpj__numfilter=empresa)
    with open(args.cobranca, 'rb') as csvfile:
            conteudo= csv.reader(csvfile, delimiter='|', quotechar='"')
            indice=0
            for row in conteudo:
                cobranca={
                    'numero_documento': row[0], 
                                }

                cobrancas[indice]=cobranca
                indice = indice + 1

    with open(args.notatitulo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        titulosnota={}
        for row in conteudo:
            for cobranca in cobrancas:
                
                if int(row[1]) == int(cobrancas[cobranca]['numero_documento']):

                    titulosnota={
                        'numero':row[2],
                        'numero_documento': cobrancas[cobranca]['numero_documento']
                    }


            print(titulosnota)

            nf = fismodels.NotaFiscal.objects.filter(empresa=empresa,numero=titulosnota['numero'])
            titulo = fmodels.Titulo.objects.filter(nosso_numero=titulosnota['numero_documento'],notafiscaltitulo__isnull=True)

            print(nf, titulo)
            if nf and titulo and args.sync_db:
                nft = fismodels.NotaFiscalTitulo()
                nft.titulo = titulo[0]
                nft.notafiscal = nf[0]
                nft.save()
                print("Essa é a NF e o Titulo ", nf[0],titulo[0])








