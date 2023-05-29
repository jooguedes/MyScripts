#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--plano', dest='plano', type=int, help='Arquivo importacao',required=False)
parser.add_argument('--pop', dest='pop', type=int, help='Arquivo importacao',required=False)

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
fnum = lambda n: re.sub('[^0-9]','',n) 

usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]

nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
portador = fmodels.Portador.objects.get(pk=args.portador_id)

if args.clientes and args.plano and args.pop:

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            #idcliente = int(row[1])
            nome = row[1]
            cpfcnpj = row[2]
            data_nasc = row[3]

            #idcontrato = 
            login = row[16]
            senha = row[16]
            
            
            rgie = ''
            profissao = ''
            tipo = ''
            sexo = None
            
            nome_pai = ''
            nome_mae = ''


            #
            # Endereço 
            #
            cep = row[4]
            logradouro = '%s %s' %(row[5],row[6])
            numero = None
            complemento = None
            try:
                numero = int(row[7])
            except:
                numero = None
                complemento = row[7]
            bairro = row[8][0:50]
            cidade = row[9][0:50]
            uf = row[10]

            #
            # Contato
            #
            telefone = row[11]   
            telefonecom = row[12]
            celular = row[13]
            if not telefonecom and row[14]:
                telefonecom = row[14]
            email = row[15]
            
            servico_obs=''
            con_obs = ''
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS 
            # 

            data_cadastro = date.today().strftime('%Y-%m-%d')


            # 
            # Contrato
            # 

            conexao_tipo = 'ppp'
            ip = None
            mac = None
            
            vencimento = 10

            comodato = False

            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1
            planointernet = admmodels.PlanoInternet.objects.get(id=args.plano)
            pop = admmodels.Pop.objects.get(id=args.pop)
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
            naturalidade = ''

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print nome_pai, nome_mae, naturalidade
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', planointernet
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" %nome
                # Save Models 

                #cliente_check = admmodels.Cliente.objects.filter(id=idcliente)
        
                #if len(cliente_check) == 0:

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
                    new_pessoa.tipopessoa='J'
                    
                    new_pessoa.nome = nome
                    new_pessoa.sexo = sexo
                    new_pessoa.datanasc = data_nasc
                    new_pessoa.profissao = profissao
                    new_pessoa.nacionalidade = 'BR'
                    new_pessoa.nomepai = nome_pai
                    new_pessoa.nomemae = nome_mae
                    new_pessoa.naturalidade = naturalidade
                    new_pessoa.rg = rgie
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
                    new_pessoa.insc_estadual = ''
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
                    new_contato.contato = telefonecom
                    new_contato.save() 
                    new_ccontato = admmodels.ClienteContato()
                    new_ccontato.cliente = new_cliente
                    new_ccontato.contato = new_contato
                    new_ccontato.save()

                #else:
                #    new_endereco = cliente_check[0].endereco
                #    
                #    new_endereco_cob = copy.copy(new_endereco)
                #    new_endereco_cob.id = None 
                #    new_endereco_inst = copy.copy(new_endereco)
                #    new_endereco_inst.id = None 
                #    new_endereco_cob.save()
                #    new_endereco_inst.save()
                #    
                #    
                #    # Cliente
                #    #new_cliente = imodels.Cliente()
                #    #new_cliente.endereco = new_endereco
                #    #new_cliente.pessoa = new_pessoa
                #    #new_cliente.data_cadastro = data_cadastro
                #    #new_cliente.data_alteracao = data_cadastro
                #    #new_cliente.ativo = True 
                #    #new_cliente.save()
                #    #new_cliente.data_cadastro = data_cadastro
                #    #new_cliente.save()
                #    new_cliente = cliente_check[0]

                
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
                
                #contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
                # Contrato 
                new_contrato = admmodels.ClienteContrato()
                #new_contrato.id = idcontrato
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
                #new_servico.id = idcontrato
                new_servico.clientecontrato = new_contrato 
                new_servico.status = status_s
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
                new_servico.observacao=servico_obs
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)

