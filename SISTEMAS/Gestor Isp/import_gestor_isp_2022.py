#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from tkinter.tix import ROW
from unicodedata import normalize
import csv

from numpy import indices 

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=True)
# python import_ --settings=sgp.conectadoemcristo.settings --pop=1 --nas=1 --portador=1 --clientes=


args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q 

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
usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]

pop_default = admmodels.Pop.objects.get(pk=args.pop_id)
nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
portador = fmodels.Portador.objects.get(pk=args.portador_id)
m = manage.Manage()

clientes = {} 


with open(args.clientes, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    indice=0
    for row in conteudo:
        idcliente = int(row[0])
        fantasia = ''
        nome = row[4]
        status= row[34]
        cpfcnpj = row[3]
        
        email = row[32]
        celular = row[29]
        telefone = row[30]
        telefonecom = ''

        plano_valor = '0.00'
        plano_download = 10240
        plano_upload = 10240
        plano = 'PLANO DEFAULT'
        vencimento = row[27]
        login = row[35]
        senha = row[36]

        pai = ''
        mae = ''

        tipo = 'f'
        if len(cpfcnpj) > 12:
            tipo = 'j'

        sexo = None

        rgie = None
        rg_emissor = None
        profissao = ''
        data_cadastro = row[15]
        
        logradouro = row[18]
        try:
            numero = int(row[19])
        except:
            numero = None

        complemento = row[20]
        bairro = row[21]
        cidade = row[22]
        uf = row[23]
        cep = row[17]
        pontoreferencia = ''
        
        con_obs= None

        data_nasc = None
       
       

        # Servico

        conexao_tipo = 'ppp'



        ip = None
        
        mac = None

        comodato = 'nao'
        if comodato == 'sim':
            comodato = True
        elif comodato in ['nao','não','N_o']:
            comodato = False

        isento = 'nao'
        if isento == 'Sim':
            isento = 100
        else:
            isento = 0

        status_cc = 1
        status_s = 1
        status_c = 1

        if status == 'Bloqueado':
            status_cc = 4
            status_s = 4
            status_c = 4

        if status == 'Cancelamento':
            status_cc = 3
            status_s = 3
            status_c = 3


        try:
            planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
        except:
            new_plano = admmodels.Plano()
            new_plano.descricao=plano
            new_plano.preco = plano_valor
            new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
            new_plano.grupo = admmodels.Grupo.objects.get(nome='cabo')
            new_plano.save()

            new_plano_internet = admmodels.PlanoInternet()
            new_plano_internet.plano = new_plano 
            new_plano_internet.download = plano_download
            new_plano_internet.upload = plano_upload
            new_plano_internet.save() 
            print('criado plano %s' %plano)
            planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]

        
        pop = pop_default
            

        nas = nas_default

        try:
            fmodels.Vencimento.objects.get(dia=vencimento)
        except:
            print "erro vencimento %s" %vencimento 
            print('corrigindo vencimento %s' %vencimento)
            new_vencimento = fmodels.Vencimento()
            new_vencimento.dia = vencimento
            new_vencimento.save() 

        #print pop
        #print row
        print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
        print logradouro,numero or '',complemento,bairro,cidade,uf,cep
        print 'vencimento: ', vencimento, 'Plano: ', plano
        print telefone,telefonecom,celular,email,con_obs
        print login,senha,ip,mac
        print '####################################################'
        if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
            print "Import %s" %nome
            # Save Models 
            
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
            new_endereco.pontoreferencia=pontoreferencia
            
            new_endereco_cob = copy.copy(new_endereco)
            new_endereco_inst = copy.copy(new_endereco)
            new_endereco.save() 
            new_endereco_cob.save()
            new_endereco_inst.save()
            
            #if admmodels.Cliente.objects.filter(id=idcliente).count() == 0:

                
            tp = 'f'
            if len(cpfcnpj) > 14 or tipo.lower() in [u'pessoa jur_dica',u'pessoa jurídica']:
                tp = 'j'
            
            if tp in['f','F']:
                new_pessoa = admmodels.Pessoa()
                new_pessoa.tipopessoa='F'
                
                new_pessoa.nome = nome
                new_pessoa.sexo = sexo
                new_pessoa.datanasc = data_nasc
                new_pessoa.profissao = profissao
                new_pessoa.nacionalidade = 'BR'
                new_pessoa.rg = rgie
                new_pessoa.cpfcnpj = cpfcnpj
                new_pessoa.rg_emissor=rg_emissor
                new_pessoa.nomepai = pai 
                new_pessoa.nomemae = mae
                new_pessoa.save()

            
            if tp in ['j','J']:
                new_pessoa = admmodels.Pessoa()
                new_pessoa.tipopessoa='J'
                new_pessoa.nome = nome
                
                new_pessoa.nomefantasia = nome
                new_pessoa.resempresa = ''
                new_pessoa.cpfcnpj = cpfcnpj
                new_pessoa.insc_estadual = rgie
                new_pessoa.tipo = 8
                new_pessoa.save()

            # Cliente
            new_cliente = admmodels.Cliente()
            #new_cliente.id = idcliente
            new_cliente.endereco = new_endereco
            new_cliente.pessoa = new_pessoa
            new_cliente.data_cadastro = data_cadastro
            new_cliente.data_alteracao = data_cadastro
            new_cliente.ativo = True 
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
                new_contato.contato = telefone 
                new_contato.save() 
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = new_cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()
            #else:
            #    new_cliente = admmodels.Cliente.objects.filter(id=idcliente)[0]
            
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
            #new_contrato.id = id
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
            if admmodels.ServicoInternet.objects.filter(login=login).count() > 0:
                print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                login,
                                                                                str(new_contrato.id))
                login += str(new_contrato.id)
            new_servico.login= login
            new_servico.endereco = new_endereco_inst
            new_servico.login_password=senha 
            new_servico.login_password_plain=senha
            new_servico.central_password=senha
            if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                new_servico.mac_dhcp = mac
                new_servico.mac = mac

            if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                new_servico.ip = ip 
            new_servico.tipoconexao = conexao_tipo
            new_servico.nas = nas
            new_servico.planointernet = planointernet
            new_servico.modoaquisicao = 1 if comodato == True else 0
            new_servico.data_cadastro=data_cadastro
            new_servico.save()

            new_servico.data_cadastro=data_cadastro
            new_servico.save()

            m.addRadiusServico(new_servico)

