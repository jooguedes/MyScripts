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
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
args = parser.parse_args()

PATH_APP = '/usr/local/sgp'

#python import_duobox.py --settings=sgp.isp.settings --nas=1 --pop=1 --vencimentoadd=1 --planoadd=1 --portador=1 --arquivo=duobox-clientes.csv.utf8
if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

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

import socket, struct

def ip2long(num):
    """
    Convert an IP string to long
    """
    return socket.inet_ntoa(struct.pack('!L', long(num)))


m = manage.Manage()
with open(args.arquivo, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        print row
        print '-------------------------------------------------------------------------------'
        # 
        #  Dados Do Cliente
        # 
        id = int(row[0])
        nome = ustr(row[1])
        fantasia = ustr(row[2])
        data_nasc = None 
        try:
            data_nasc = row[3]
        except:
            data_nasc = None
        sexo = row[4]
        if sexo == 'NI':
            sexo = None
        estadocivil = 'S'
        if row[5] == '2':
            estadocivil = 'C'
        else:
            estadocivil = 'S'
        tipo_pessoa = row[6]
        cpf = row[9]
        cnpj = row[10]
        ruc = row[11]

        telefone = row[12]
        celular = row[13]
        email = ustrl(row[14])   
        email2 = row[15]
        telefonecom = ''
        con_obs=''

        rg = ustr(row[16])
        nomepai = ustr(row[17])
        nomemae = ustr(row[18])
        profissao = ustr(row[19])
        inscricao_estadual = row[21]

        #
        # Endereço Principal
        #
        cep = ustr(row[22])
        logradouro = ustr(row[23])
        numero = None
        try:
            numero = re.sub('[^0-9]', '', row[24])
        except:
            numero = None

        complemento = ustr(row[25])
        bairro = ustr(row[26])
        preferencia = ustr(row[27])
        cidade = ustr(row[29])
        uf = ustr(row[31])
        coordenadas_gps = row[33]

        cobranca_end_igual = row[34]
        # Endereço Cobrança

        cobranca_cep = ustr(row[35])
        cobranca_logradouro = ustr(row[36])
        cobranca_numero = None
        try:
            cobranca_numero = re.sub('[^0-9]', '', row[37])
        except:
            cobranca_numero = None
        cobranca_complemento = ustr(row[38])
        cobranca_bairro = ustr(row[39])
        cobranca_preferencia = ustr(row[40])
        cobranca_cidade = ustr(row[42])
        cobranca_uf = ustr(row[44])
        cobranca_coordenadas_gps = row[46]

        email_cobranca = row[47]
        email_aniversario = row[48]
        email_outros = ''


        #
        # DATAS 
        # 
        print(row[50])
        data_cadastro = datetime.now()
        try:
            data_cadastro=row[50]
        except:
            pass

        if data_cadastro == '1':
            data_cadastro = datetime.now()


        endereco_instalacao_igual_principal = row[52]

        endinstall_cep = ustr(row[53])
        endinstall_logradouro = ustr(row[54])
        endinstall_numero = None
        try:
            endinstall_numero = re.sub('[^0-9]', '', row[55])
        except:
            endinstall_numero = None
        endinstall_complemento = ustr(row[56])
        endinstall_bairro = ustr(row[57])
        endinstall_preferencia = ustr(row[58])
        endinstall_cidade = ustr(row[60])
        endinstall_uf = ustr(row[62])
        endinstall_coordenadas_gps = row[63]

        endereco_cobranca_igual_principal = row[64]

        endcob_cep = ustr(row[65])
        endcob_logradouro = ustr(row[66])
        endcob_numero = None
        try:
            endinstall_numero = re.sub('[^0-9]', '', row[67])
        except:
            endinstall_numero = None
        endcob_complemento = ustr(row[68])
        endcob_bairro = ustr(row[69])
        endcob_preferencia = ustr(row[70])
        endcob_cidade = ustr(row[72])
        endcob_uf = ustr(row[74])
        endcob_coordenadas_gps = row[75]


        try:
            vencimento = int(row[76])
        except:
            vencimento = 10




        login = row[80]
        if not login:
            login = 'c%s' %id
        if login == '0':
            continue 
        senha = row[81]
        if not senha:
            senha = '123456'
        ip = ustr(row[82])
        if ip and '.' not in ip:
            ip = ip2long(ip)
            if ip == '0.0.0.0':
                ip = None
            else:
                print 'IP:::::::::::::::::::::::::::::%s' %ip

        comodato = False
        #comodato = ustrl(row[40]).lower()
        #if comodato == 'sim':
        #    comodato = True
        #elif comodato in ['nao','não','N_o']:
        #    comodato = False

        status_cc = 1
        status_s = 1
        status_c = 1
        
        ativo = row[83]



        isento = ustr(row[84])
        if isento == '1':
            isento = 100
        else:
            isento = 0

        status = ustrl(row[85])

        if ativo == '1':
            if status == '1':
                status_cc = 1
                status_s = 1
                status_c = 1
            else:
                status_cc = 4
                status_s = 4
                status_c = 4
        else:
            status_cc = 3
            status_s = 3
            status_c = 3
        

        # 
        # Contrato
        # 

        # Servico
        nas_get = ''
        plano = row[86].strip()
        plano_valor = float(row[87].strip().replace(',','.'))

        download = int(row[92]) or 0
        upload = int(row[94]) or 0

        conexao_tipo = 'ppp'
        mac = None
        
        idcontrato = row[105]

        try:
            planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
        except:
            if args.planoadd:
                new_plano = admmodels.Plano()
                new_plano.descricao=plano
                new_plano.preco = plano_valor
                new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
                new_plano.grupo = admmodels.Grupo.objects.get(nome='cabo')
                new_plano.save()

                new_plano_internet = admmodels.PlanoInternet()
                new_plano_internet.plano = new_plano 
                new_plano_internet.download = download
                new_plano_internet.upload = upload
                new_plano_internet.save() 

                planointernet=admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                print('criado plano %s' %plano)
            else:
                raise Exception('Não localizei plano %s' %plano)

        try:
            fmodels.Vencimento.objects.get(dia=vencimento)
        except:
            print "erro vencimento %s" %vencimento 
            if args.vencimentoadd:
                print('corrigindo vencimento %s' %vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 

      
        pop = pop_default
            #print 'Não localizei cidade: %s - Definindo POP: %s' %(cidade_q,pop_default)

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
        print nome,tipo_pessoa,cpf,cnpj,sexo, data_cadastro,data_nasc
        print logradouro,numero or '',complemento,bairro,cidade,uf,cep
        print 'vencimento: ', vencimento, 'Plano: ', plano
        print telefone,telefonecom,celular,email,con_obs
        print login,senha,ip,mac
        print '####################################################'
        if cobranca_end_igual == '0':
            print(cobranca_cep,cobranca_logradouro,cobranca_numero,cobranca_complemento,cobranca_bairro,cobranca_preferencia,cobranca_cidade,cobranca_uf,cobranca_coordenadas_gps)

        if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
            print "Import %s" %nome
            # Save Models 

            cliente_check = admmodels.Cliente.objects.filter(id=id)
    
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
                new_endereco.pontoreferencia=preferencia
                new_endereco.map_ll=coordenadas_gps
                
                if cobranca_end_igual == '1':
                    new_endereco_cob = copy.copy(new_endereco)            
                else:
                    new_endereco_cob = admmodels.Endereco()
                    new_endereco_cob.logradouro = cobranca_logradouro
                    new_endereco_cob.numero = cobranca_numero
                    new_endereco_cob.bairro = cobranca_bairro
                    new_endereco_cob.cep = cobranca_cep
                    new_endereco_cob.cidade = cobranca_cidade
                    new_endereco_cob.uf = cobranca_uf 
                    new_endereco_cob.pais = 'BR'
                    new_endereco_cob.complemento = cobranca_complemento
                    new_endereco_cob.pontoreferencia=cobranca_preferencia
                    new_endereco_cob.map_ll=cobranca_coordenadas_gps

                if endereco_instalacao_igual_principal == '1':
                    new_endereco_inst = copy.copy(new_endereco)
                else:
                    new_endereco_inst = admmodels.Endereco()
                    new_endereco_inst.logradouro = endinstall_logradouro
                    new_endereco_inst.numero = endinstall_numero
                    new_endereco_inst.bairro = endinstall_bairro
                    new_endereco_inst.cep = endinstall_cep
                    new_endereco_inst.cidade = endinstall_cidade
                    new_endereco_inst.uf = endinstall_uf 
                    new_endereco_inst.pais = 'BR'
                    new_endereco_inst.complemento = endinstall_complemento
                    new_endereco_inst.pontoreferencia=endinstall_preferencia
                    new_endereco_inst.map_ll=endinstall_coordenadas_gps

                if not new_endereco_cob.numero:
                    new_endereco_cob.numero = None

                if not new_endereco.numero:
                    new_endereco.numero = None

                if not new_endereco_inst.numero:
                    new_endereco_inst.numero = None

                new_endereco_cob.save()
                new_endereco.save() 
                
                new_endereco_inst.save()
                


                            
                if tipo_pessoa == 'F':
                    new_pessoa = admmodels.Pessoa()
                    new_pessoa.tipopessoa='F'
                    
                    new_pessoa.nome = nome
                    new_pessoa.sexo = sexo
                    new_pessoa.datanasc = data_nasc
                    new_pessoa.profissao = profissao
                    new_pessoa.nacionalidade = 'BR'
                    new_pessoa.rg = rg
                    new_pessoa.cpfcnpj = cpf
                    new_pessoa.rg_emissor=''
                    new_pessoa.estadocivil=estadocivil
                    new_pessoa.nomepai = nomepai
                    new_pessoa.nomemae = nomemae
                    try:
                        new_pessoa.save()
                    except:
                        new_pessoa.datanasc=None
                        new_pessoa.save()
                
                if tipo_pessoa == 'J':
                    new_pessoa = admmodels.Pessoa()
                    new_pessoa.tipopessoa='J'
                    new_pessoa.nome = nome
                    
                    new_pessoa.nomefantasia = nome
                    new_pessoa.resempresa = ''
                    new_pessoa.cpfcnpj = cnpj
                    new_pessoa.insc_estadual = inscricao_estadual
                    new_pessoa.tipo = 8
                    new_pessoa.save()


                # Cliente
                new_cliente = admmodels.Cliente()
                new_cliente.id = id
                new_cliente.endereco = new_endereco
                new_cliente.pessoa = new_pessoa
                new_cliente.data_cadastro = data_cadastro
                new_cliente.data_alteracao = data_cadastro
                new_cliente.ativo = True 
                new_cliente.save()
                new_cliente.data_cadastro = data_cadastro
                try:
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()
                except:
                    new_cliente.data_cadastro = datetime.now()
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
                
                if email_cobranca == '1':
                    new_contato = admmodels.Contato() 
                    new_contato.tipo = 'EMAIL_COBRANCA'
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
            new_contrato.id = idcontrato
            new_contrato.cliente = new_cliente 
            new_contrato.pop = pop
            new_contrato.cobranca = new_cobranca
             
            data_inicio = date.today()
            try:
                diy,dim,did = data_cadastro.split(' ')[0].split('-')
                data_inicio = date(int(diy),int(dim),int(did))
            except:
                pass 
            new_contrato.data_inicio = data_inicio 
            new_contrato.data_cadastro = data_cadastro 
            new_contrato.data_alteracao = data_cadastro
            new_contrato.save()

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

