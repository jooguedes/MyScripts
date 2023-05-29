#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 
import re

parser = argparse.ArgumentParser(description='Importação CSV 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
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


if sys.version_info >= (3,0):
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
with open(args.arquivo, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        idclient=int(row[38])
        nome = ustr(row[0])
        login = ustrl(row[1])
        senha = row[2]
        if not senha:
            senha = login
        email = row[3]
        tipo = row[4]

        cpfcnpj = row[5]
        rgie = row[6]

        insc_estadual = row[7]
        telefone = row[8]
        celular = row[9]
        telefonecom = row[10]
        celular3 = row[11]
        celular4 = row[12]

        data_nasc = None
        try:
            d_,m_,y_ = row[13].split('/')
            data_nasc='%s-%s-%s' %(y_,m_,d_)
        except:
            pass




        profissao = ''
        
        sexo = None 

        comodato = False
        isento = 0

        #
        # Endereço 
        #
        cep = ustr(row[14])
        logradouro = ustr(row[15])
        numero = None
        try:
            numero = int(re.sub('[^0-9]','', str(row[16])))
        except:
            numero = None
            logradouro += ",%s" %row[16]
        complemento = ustr(row[17])
        bairro = ustr(row[18])
        cidade = ustr(row[19]).upper()
        grupo_clientes=ustr(row[22]).upper()
        uf = ustr(row[20])

        #
        # Contato
        #

        con_obs=''
        #con_obs = ustr(row[25])
        #if con_obs == 'NENHUMA':
        #    con_obs=''

        #
        # DATAS 
        # 

        data_cadastro = datetime.now()
        try:
            d_,m_,y_ = row[21].split('/')
            data_cadastro='%s-%s-%s' %(y_,m_,d_)
        except:
            pass


        # 
        # Contrato
        # 

        # Servico
        plano = row[24].strip()
        plano_valor = str(row[25]).strip()
        print(plano,plano_valor)
        conexao_tipo = ustrl(row[26])
        conexao_tipo = 'ppp'
        if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
        if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'


        ip = ustr(row[28])
        if len(ip) < 7: ip = None

        mac = ustr(row[29])
        if len(mac) < 10: mac = None
        
        try:
            vencimento = int(row[30])
            print(vencimento)
        except:
            vencimento = 10
            print 'erro row (%s) - %s' %(row[30],row)

        servico_observacao = row[34]
        '''if servico_observacao and row[32]:
            servico_observacao +='|%s' %row[32]'''

        
        status_cc = 1
        status_s = 1
        status_c = 1

        status = row[33]


        if status == 'Ativo':
            status_cc = 1
            status_s = 1
            status_c = 1

        elif status == 'Desativado':
            status_cc = 3
            status_s = 3
            status_c = 3

        '''if servico_observacao and row[34]:
            servico_observacao += '[%s]' %row[34]
        elif row[34]:
            servico_observacao = '[%s]' %row[34]'''

        map_ll = '%s,%s' %(row[35],row[36])

        try:
            planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
        except:
            if args.planoadd:
                new_plano = admmodels.Plano()
                new_plano.descricao=plano
                new_plano.preco = plano_valor
                new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='radio')
                new_plano.grupo = admmodels.Grupo.objects.get(nome='radio')
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano 
                new_plano_internet.download = 2048
                new_plano_internet.upload = 1024
                new_plano_internet.save() 
                print('criado plano %s' %plano)
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            else:
                raise Exception('Não localizei plano %s' %plano)

        cidade_q = normalize('NFKD', grupo_clientes).encode('ASCII','ignore')
        pop=admmodels.Pop.objects.get(id=1)
        '''try:
            pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
            
            pop = pop_q
        except:
            new_pop = admmodels.Pop()
            new_pop.cidade=cidade_q.upper()
            new_pop.uf=uf
            new_pop.save()
            pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
            #print 'Não localizei cidade: %s - Definindo POP: %s' %(cidade_q,pop_default)'''
        
        pop=pop_default
        nas = nas_default

        try:
            fmodels.Vencimento.objects.get(dia=vencimento)
        except:
            print "erro vencimento %s" %vencimento 
            if args.vencimentoadd:
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
            new_endereco.logradouro = logradouro[0:49]
            new_endereco.numero = numero
            new_endereco.bairro = bairro[0:49]
            new_endereco.cep = cep
            new_endereco.cidade = cidade[0:49]
            new_endereco.uf = uf 
            new_endereco.pais = 'BR'
            new_endereco.complemento = complemento[0:49]
            new_endereco.pontoreferencia=''
            new_endereco.map_ll = map_ll
            
            new_endereco_cob = copy.copy(new_endereco)
            new_endereco_inst = copy.copy(new_endereco)
            new_endereco.save() 
            new_endereco_cob.save()
            new_endereco_inst.save()
            
            

            
            tp = 'f'
            if len(cpfcnpj) > 14 or tipo.lower() in [u'jurídica',u'juridica']:
                tp = 'j'
            
            if tp == 'f':
                new_pessoa = admmodels.Pessoa()
                new_pessoa.tipopessoa='F'
                
                new_pessoa.nome = nome
                new_pessoa.sexo = sexo
                new_pessoa.datanasc = data_nasc
                new_pessoa.profissao = profissao
                new_pessoa.nacionalidade = 'BR'
                new_pessoa.rg = rgie
                new_pessoa.cpfcnpj = cpfcnpj
                new_pessoa.rg_emissor=''
                try:
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
                new_pessoa.insc_estadual = ''
                new_pessoa.tipo = 8
                new_pessoa.save()

            # Cliente
            new_cliente = admmodels.Cliente()
            new_cliente.id=idclient
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
            new_contrato.id= idclient
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
            new_servico.observacao=servico_observacao
            new_servico.save()

            new_servico.data_cadastro=data_cadastro
            new_servico.save()

            m.addRadiusServico(new_servico)

#python import_mikweb.py --settings=sgp.cavalcantenet.settings --nas=1 --pop=1 --portador=1 --planoadd=1 --vencimentoadd=1 --arquivo=Conv-CLIENTE-amaronet.csv --sync=1