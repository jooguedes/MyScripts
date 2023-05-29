#!/usr/bin/python
# -*- coding: utf-8 -*-
# CLIENTES 
# ID  
# Nome / Razão social 
# Usuário 
# Cliente desde   
# Telefone(s) 
# Tipo    
# E-mail  
# Data do cadastro    
# CPF 
# RG  
# CNPJ    
# Inscrição Estadual  
# Inscrição Municipal 
# Gênero  
# Data de nascimento  
# Aniversário 
# Nome fantasia   
# Observação  
# Endereço    
# Número  
# Complemento 
# Bairro  
# CEP 
# Coordenadas 
# Estado  
# Cidade  
# Vencimento

# CONTRATOS 
# ID X 
# Número  
# Titular 
# Status  
# Vencimento 
# Banco   
# Endereço    
# Numero da casa  
# Bairro  a
# Cidade  
# Estado  
# Complemento 
# Emite NF    
# Data de Contratação 
# Data de Registro 

# CONTAS
# ID  
# Avulsa  
# Online  
# Usuário 
# Senha   
# Contrato    
# Titular 
# CPF  X
# Observação X
# Endereço  X
# Número  X
# Complemento X  
# Bairro  X
# CEP X
# Estado X   
# Cidade X  
# Telefone X    
# Coordenadas X
# Plano   
# Método  
# IP  
# IPv6 - PPPoE (PD)   
# IPv6 - DHCP (PD)    
# MAC 
# Auto login  
# Comodato    
# Adquirido pela empresa  
# Ativo



from __future__ import unicode_literals
import argparse
from hashlib import new
import os, sys
from datetime import date, datetime
import copy
from turtle import down
from unicodedata import normalize
import csv
import re


parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planos', dest='planos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--contas', dest='contas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--contratos', dest='contratos', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--portador', dest='portador', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--nas', dest='nas', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--pop', dest='pop', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--plano', dest='plano', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--status', dest='status', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--dominio', dest='dominio', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--faturas', dest='faturas', type=str, help='argumento para import das faturas', required=False)
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
from apps.netcore import models as nmodels
from apps.netcore.utils.radius import manage

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]', '', unicode(n))
usuario = admmodels.User.objects.get(username='sgp')
if args.portador:
    portador = fmodels.Portador.objects.get(id=args.portador)
formacobranca = fmodels.FormaCobranca.objects.all()[0]
if args.nas:
    nas = nmodels.NAS.objects.get(id=args.nas)
popdefault = None
m = manage.Manage()
if args.pop:
    popdefault = admmodels.Pop.objects.get(id=args.pop)
planodefault = None
if args.plano:
    planodefault = admmodels.PlanoInternet.objects.get(plano__id=args.plano)

logins_alterar = []

def strdate(d):
    try:
        d,m,y = d.split()[0].split('/')
        return '%s-%s-%s' %(y,m,d)
    except:
        return None
def formatar_data(dt):
    if dt:
        try:
            d,m,y = dt.split(' ')[0].split('/')
            if len(y) == 2:
                if int(y) >= 0 and int(y) <= 16:
                    y = '20%s' %y
                else:
                    y = '19%s' %y
            return '%s-%s-%s' %(y,m,d)
        except:
            print 'error formatar %s' %dt
    return ''


def verifica_vencimento(v):
    try:
        fmodels.Vencimento.objects.get(dia=v)
    except:
        print "erro vencimento %s" %v
        print('corrigindo vencimento %s' %v)
        new_vencimento = fmodels.Vencimento()
        new_vencimento.dia = v
        new_vencimento.save()

cliente_incremento=0
if args.planos:
    with open(args.planos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__trim__lower=row[0].strip().lower())[0]
            except:
                new_plano = admmodels.Plano()
                new_plano.descricao="@webmikrotik-16410%s" %row[0].strip()
                new_plano.preco = float(row[1].replace(',','.'))
                new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='fibra')
                new_plano.grupo = admmodels.Grupo.objects.get(nome='fibra')
                new_plano.save()

                download = row[2]
                upload = row[3]
                
                if download.strip().lower() == 'ilimitado':
                    download = 1024000
                    upload = 1024000

                else:
                    download= int(download.replace('Kbps',"").strip())
                    upload=int(upload.replace('Kbps',"").strip())
                
                if(not download or  download==None):
                    download=1024

                if(not upload or upload==None):
                    upload=1024
                
                print('meu download e upload é :', download, upload)
                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano
                new_plano_internet.download = download
                new_plano_internet.upload = upload
                print('meu plano de internet em download ', new_plano_internet.download )
                new_plano_internet.save()
                print('criado plano %s' %row[0].strip())


if args.clientes and args.contratos and args.contas:
    contratos = {}
    contas = {}
    clientes = {}

    # load contas
    with open(args.contas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            if contas.get(row[6]):
                contas[row[6]].append(row)
            else:
                contas[row[6]] = [row]

    # load contratos
    with open(args.contratos, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            if contratos.get(row[3]):
                contratos[row[3]].append(row)

    # load clientes
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            if clientes.get(row[1]):
                clientes[row[1]].append(row)
            else:
                clientes[row[1]] = [row]

    for cliente in clientes:
        for row in clientes[cliente]:
            print(row)
            #
            # CLIENTE 
            # 
            idcliente = int(row[0]) + 4000
            nome = unicode(row[1])
            login_central = "@webmikrotik-16410%s" %row[2]
            senha_central = row[8] or row[10]
            data_cadastro = formatar_data(row[3])
            telefone = ''
            celular = ''
            telefonecom = ''
            celularcom = ''
            array_celulares=[]
            celulares = row[4].split('/')
            for f in celulares:
                array_celulares.append(fnum(f))

            email = row[6]
            data_cadastro = formatar_data(row[7])
            cpfcnpj = row[8]
            rgie = row[9]
            if row[10]:
                cpfcnpj = row[10]
            insc_estadual = row[11]
            insc_municipal = row[12]
            sexo = row[13]
            if sexo == 'feminino':
                sexo = 'F'
            if sexo == 'masculino':
                sexo = 'M'
            data_nasc = formatar_data(row[14])
            nomefantasia = row[16]
            cli_obs = row[17]

            endereco_cliente = {}
            endereco_cliente['logradouro'] = row[18][0:255]
            try:
                endereco_cliente['numero'] = int(row[19])
            except:
                endereco_cliente['numero'] = None
            endereco_cliente['complemento'] = row[20][0:255]
            endereco_cliente['bairro'] = row[21][0:50]
            endereco_cliente['cep'] = row[22][0:50]
            endereco_cliente['uf'] = row[24][0:50]
            endereco_cliente['cidade'] = row[25][0:50]
            cliente_vencimento =  '10' #row[26] or
            verifica_vencimento(cliente_vencimento)
            nomepai = ''
            nomemae = ''
            profissao = ''
            respempresa = ''
            respcpf = ''

            # 
            # SERVICO
            # 
            
            if contas.get(cliente):
                for contarow in contas[cliente]:
                    print(contarow)
                    login = "@webmikrotik-16410%s" %contarow[3]
                    
                    senha = contarow[4]

                    if not senha or senha=='':
                        senha=idcliente

                    if not login:
                        continue
                    
                    coordenadas=contarow[17]
                    endereco_servico = {}
                    endereco_servico['logradouro'] = contarow[9][0:255]
                    try:
                        endereco_servico['numero'] = int(contarow[10])
                    except:
                        endereco_servico['numero'] = None
                    endereco_servico['complemento'] = contarow[11][0:255]
                    endereco_servico['bairro'] = contarow[12][0:50]
                    endereco_servico['cep'] = contarow[13] or endereco_cliente['cep']
                    endereco_servico['uf'] = contarow[14][0:50]
                    endereco_servico['cidade'] = contarow[15][0:50]
                    endereco_servico['map_ll']=coordenadas

                    cidade_q = normalize('NFKD', unicode(endereco_servico['cidade'])).encode('ASCII','ignore')
                    pop = popdefault
        
                    plano = "@webmikrotik-16410%s" %contarow[18] or "20MB"
                    plano_obj = admmodels.PlanoInternet.objects.filter(plano__descricao__lower=plano.lower())
                    if not plano_obj:
                        if planodefault:
                            plano_obj = planodefault
                        else:
                            raise Exception("nao achei o plano %s" %plano)
                    else:
                        plano_obj = plano_obj[0]

                    ip = contarow[20]
                    mac_dhcp = contarow[23]

                    status = 'a'
                    if args.status:
                        status = args.status

                    senha_central = cpfcnpj
     

                    addresslist = ''
                    respempresa = ''
                    comodato = False
                    notafiscal = False

                    con_obs=''
                    mac = None
                    conexao_tipo = 'ppp'

                    isento = 0
                    nao_suspende = False

                    status_cc = 1
                    status_s = 1
                    status_c = 1

                    if status == 's':
                        status_cc = 4
                        status_s = 4
                        status_c = 4

                    if status == 'c':
                        status_cc = 3
                        status_s = 3
                        status_c = 3

                    status_criar = [6,2,status_cc]


                    #print pop
                    #print row
                    print status, login, nome, cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
                    print endereco_cliente,endereco_servico
                    print 'vencimento: ', cliente_vencimento, 'Plano: ', plano
                    print telefone,telefonecom,celular,email,con_obs
                    print login,senha,ip,mac
                    print '####################################################'
                    if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                        print "Import %s" %nome
                        # Save Models

                        cliente_check = admmodels.Cliente.objects.filter(clientecontrato__servicointernet__login=login)
                        if cliente_check.count() > 0:
                            continue

                        # Endereco
                        new_endereco = admmodels.Endereco(**endereco_cliente)
                        new_endereco_cob = admmodels.Endereco(**endereco_cliente)
                        new_endereco_inst = admmodels.Endereco(**endereco_servico)
                        new_endereco.save()
                        new_endereco_cob.save()
                        new_endereco_inst.save()


                        if len(fnum(cpfcnpj)) > 12:
                            new_pessoa = admmodels.Pessoa()
                            new_pessoa.tipopessoa='J'
                            new_pessoa.nome = nome

                            new_pessoa.nomefantasia = nomefantasia
                            new_pessoa.respempresa = respempresa
                            new_pessoa.respcpf = respcpf
                            new_pessoa.cpfcnpj = cpfcnpj
                            new_pessoa.insc_estadual = insc_estadual
                            new_pessoa.tipo = 8
                            new_pessoa.save()
                        else:
                            new_pessoa = admmodels.Pessoa()
                            new_pessoa.tipopessoa='F'

                            new_pessoa.nome = nome
                            new_pessoa.sexo = sexo
                            new_pessoa.datanasc = data_nasc
                            new_pessoa.profissao = profissao
                            new_pessoa.nomepai = nomepai
                            new_pessoa.nomemae = nomemae
                            new_pessoa.nacionalidade = 'BR'
                            new_pessoa.rg = rgie
                            new_pessoa.cpfcnpj = cpfcnpj
                            new_pessoa.rg_emissor=''
                            try:
                                new_pessoa.save()
                            except:
                                try:
                                    new_pessoa.save()
                                except:
                                    new_pessoa.datanasc=None
                                    new_pessoa.save()

                        # Cliente
                        new_cliente = admmodels.Cliente()
                        new_cliente.id = idcliente
                        new_cliente.endereco = new_endereco
                        new_cliente.pessoa = new_pessoa
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.data_alteracao = data_cadastro
                        new_cliente.ativo = True
                        new_cliente.observacao = cli_obs
                        new_cliente.save()
                        new_cliente.data_cadastro = data_cadastro
                        
                      
                        new_cliente.save()
                      

                        # contato 1
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
                        for f in array_celulares:
                            if f:
                                new_contato = admmodels.Contato()
                                new_contato.tipo = 'CELULAR_PESSOAL'
                                new_contato.contato = f
                                new_contato.observacao = ''
                                new_contato.save()
                                new_ccontato = admmodels.ClienteContato()
                                new_ccontato.cliente = new_cliente
                                new_ccontato.contato = new_contato
                                new_ccontato.save()




                        # contato 3
                        if len(telefone) > 4:
                            new_contato = admmodels.Contato()
                            new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                            new_contato.contato = telefone
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

                        # Cobranca
                        new_cobranca = fmodels.Cobranca()
                        new_cobranca.cliente = new_cliente
                        new_cobranca.endereco = new_endereco_cob
                        new_cobranca.portador =portador
                        new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=cliente_vencimento)
                        new_cobranca.isento = isento
                        new_cobranca.notafiscal = False
                        new_cobranca.data_cadastro = data_cadastro
                        new_cobranca.datacobranca1 = data_cadastro
                        new_cobranca.usuariocad = usuario
                        new_cobranca.formacobranca = formacobranca
                        new_cobranca.nao_suspende=nao_suspende
                        new_cobranca.status = status_c
                        new_cobranca.save()

                        new_cobranca.data_cadastro = data_cadastro
                        new_cobranca.save()

                        # Contrato
                       
                        new_contrato = admmodels.ClienteContrato()
                        new_contrato.id=idcliente
                        new_contrato.cliente = new_cliente
                        new_contrato.pop = pop
                        new_contrato.cobranca = new_cobranca

                        new_contrato.data_inicio = data_cadastro
                        new_contrato.data_cadastro = data_cadastro
                        new_contrato.data_alteracao = data_cadastro
                        new_contrato.save()

                        for ic in status_criar:
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
                        if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
                            print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                              login,
                                                                                              str(new_contrato.id))
                            login += str(new_contrato.id)
                        new_servico.login= login
                        new_servico.endereco = new_endereco_inst
                        new_servico.login_password=senha
                        new_servico.login_password_plain=senha
                        new_servico.central_password=senha_central
                        try:
                            if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                                new_servico.mac_dhcp = mac_dhcp
                                new_servico.mac = mac
                        except:
                            new_servico.mac_dhcp=None
                            new_servico.mac=None
                        try:
                            if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                                new_servico.ip = ip
                        except:
                            new_servico.ip=None
                        new_servico.tipoconexao = conexao_tipo
                        new_servico.nas = nas
                        new_servico.planointernet = plano_obj
                        new_servico.modoaquisicao = 1 if comodato == True else 0
                        new_servico.data_cadastro=data_cadastro
                        new_servico.addresslist=addresslist
                        new_servico.save()

                        new_servico.data_cadastro=data_cadastro
                        new_servico.save()

                        m.addRadiusServico(new_servico)
                    else:
                        print("Cliente Já importado", nome)

for p in admmodels.Pop.objects.all():
    for plano in admmodels.Plano.objects.all():
        plano.pops.add(p)


    
if args.faturas:
    with open(args.faturas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=str('|'), quotechar=str('"'))
        for row in conteudo:
            try:
                #portador = fmodels.Portador.objects.filter(descricao__lower__trim__icontains=ustrl(row[11]))
                portador=fmodels.Portador.objects.filter(id=args.portador)
                '''if fmodels.Portador.objects.filter(descricao__lower__trim__icontains=ustrl(row[11])).count() == 0 or ustrl(row[11]) == '':
                    portador = fmodels.Portador.objects.filter(descricao__lower__trim__icontains='Boleto Interno')'''
            except Exception as a:
                print('Erro ao encontrar PORTADOR, erro: %s'%a)
                break
            usuario = usuario
            formapagamento = fmodels.FormaPagamento.objects.all()[0]
            planocontas = fmodels.CentrodeCusto.objects.get(codigo='01.01.01')
            cpfcnpj = row[16].strip()
            if cpfcnpj == '':
                try:
                    cpfcnpj = row[16].strip()
                except:
                    ilike = '%'.join(row[14].strip().lower().split())
                    clientes = admmodels.Cliente.objects.filter(pessoa__nome__unaccent__ilike='%%%s%%' %ilike, clientecontrato__pop=2)
            if cpfcnpj == '':
                ilike = '%'.join(row[14].strip().lower().split())
                clientes = admmodels.Cliente.objects.filter(pessoa__nome__unaccent__ilike='%%%s%%' %ilike, clientecontrato__pop=2)
            else:
                clientes = admmodels.Cliente.objects.filter(pessoa__cpfcnpj__numfilter=cpfcnpj, clientecontrato__pop=2)

            if clientes:
                try:
                    cliente = clientes[0]
                    contrato = cliente.clientecontrato_set.all()
                except Exception as a:
                    print('Erro ao encontrar o cliente e o contrato, erro: %s'%a)
                    
                if contrato:
                    contrato = contrato[0]
                    cobranca = contrato.cobranca
                    idtransacao = row[0]
                    numero_documento = row[2]
                    nosso_numero = row[0]
                    nosso_numero_f = row[0]
                    demonstrativo = ''
                    data_documento = strdate(row[5])
                    if data_documento == None:
                        data_documento = strdate(row[3])
                    data_vencimento = strdate(row[3])
                    data_pagamento = None
                    data_baixa = None
                    data_cancela = None
                    status = fmodels.MOVIMENTACAO_GERADA
                    valorpago = None
                    usuario_b = None
                    usuario_c = None
                    juros = row[7].replace('.','').replace(',','.')
                    if juros.strip() == '':
                        juros = 0.00
                    valor = row[6].replace('.','').replace(',','.')

                    if 'Liquidada' in row[12]:
                        valorpago = row[9].replace('.','').replace(',','.')
                        if valorpago.strip() == '':
                            valorpago = valor
                        data_pagamento = strdate(row[4])
                        if data_pagamento == '' or data_pagamento == '0000-00-00':
                            data_pagamento = data_vencimento
                        data_baixa = data_pagamento
                        status = fmodels.MOVIMENTACAO_PAGA
                        usuario_b = usuario
                        usuario_c = None

                    elif 'Cancelada' in row[12] or 'Isenta' in row[12]:
                        data_cancela = data_vencimento
                        status = fmodels.MOVIMENTACAO_CANCELADA
                        data_baixa = None
                        data_pagamento = None
                        usuario_b = None
                        usuario_c = usuario

                    desconto = row[8].replace('.','').replace(',','.')
                    if desconto == '':
                        desconto = 0.00
                    linha_digitavel = ''
                    codigo_barras = ''
                    codigo_carne = ''
                    chave = ''
                    if nosso_numero:
                        if fmodels.Titulo.objects.filter(nosso_numero=nosso_numero,portador=portador[0]).count() == 0:
                            dados = {'cliente': cliente,
                                    'cobranca': cobranca,
                                    'portador': portador[0],
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
                            try:
                                print("Importantando Boleto: %s - %s | %s | %s | %s"%(cliente.pessoa.nome, 
                                                                                    cliente.pessoa.cpfcnpj,
                                                                                    nosso_numero,
                                                                                    data_vencimento,
                                                                                    portador[0].descricao))
                                titulo = fmodels.Titulo(**dados)
                                titulo.save()
                                titulo.data_documento=data_documento
                                titulo.data_alteracao=data_documento
                                titulo.save()

                            except Exception as e:
                                print("Erro cadastrar",e,dados)
                        else:
                            print("Boleto ja foi importado: %s - %s | %s | %s | %s"%(cliente.pessoa.nome, 
                                                                                    cliente.pessoa.cpfcnpj,
                                                                                    nosso_numero,
                                                                                    data_vencimento,
                                                                                    portador[0].descricao))
      
#python import_webmikrotik.py --settings=sgp.keunet.settings --nas=1 --portador=4 --clientes=Conv-Clientes.csv --plano=27 --planos=Conv-planos.csv --contas=Conv-Contas.csv --pop=3 --contratos=Conv-Contratos.csv --sync=1
#python import_webmikrotik.py --settings=sgp.keunet.settings --nas=1 --portador=3 --faturas=