#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
import csv
from datetime import date, datetime
import copy
from unicodedata import normalize

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
args = parser.parse_args()
#python import_vigo.py --settings=sgp.intermix.settings --portador=1 --arquivo=vigo-clientes.csv.utf8 --planoadd=1 --vencimentoadd=1 --nas=1 --sync=1
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
usuario_default = admmodels.User.objects.get(username='sgp')
usuario = usuario_default
usuarios = admmodels.User.objects.all()
formacobranca = fmodels.FormaCobranca.objects.all()[0]
nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
portador = fmodels.Portador.objects.get(pk=args.portador_id)

incrementar = 93000
m = manage.Manage()
i = 0
with open(args.arquivo, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        i+=1
        print i
        idcontrato = int(row[0])
        #id_cliente=int(row[0])
        login = ustrl(row[1]).strip()
        login = login.strip().replace(' ', '')
        login = normalize('NFKD', unicode(login)).encode('ASCII', 'ignore').decode('ascii')
        if login == '1':
            login = 'c%s' %idcontrato
        if row[43]:
            senha=row[43]
        else:
            senha='123'
        senhacentral = 'c%s' %idcontrato
    
        #if not senha:
        #    senha = login
    
    
        #
        # Dados pessoais 
        #
        nome = ustr(row[3])
        cpfcnpj = ustr(row[5])
        rgie = ustr(row[8])[:20]
        profissao = ustr(row[9])
        tipo = ustr(row[2])
    
        if row[10] == 'Masculino':
            sexo = 'M'
        elif row[10] == 'Feminino':
            sexo = 'F'
        else:
            sexo = None
        data_nasc = None    
        try:
            data_nasc=row[11]
        except:
            pass
    
        #
        # Endereço 
        #
        logradouro = ustr(row[14])
        numero = None
        try:
            numero = int(row[15])
        except:
            numero = None
        complemento = ustr(row[16])
        bairro = ustr(row[17])
        cep = ustr(row[18])
        uf = ustr(row[19])
        cidade = ustr(row[20]).split('/')[0]
    
        #
        # Contato
        #
        telefone = ustr(row[21]).replace('.0','').replace('(00)00000-0000','').replace('(84)00000-0000','')
        telefonecom = ustr(row[22]).replace('.0','').replace('(00)00000-0000','').replace('(84)00000-0000','')
        celular = ustr(row[23]).replace('.0','').replace('(00)00000-0000','').replace('(84)00000-0000','')
        email = ustrl(row[24])   
        conn_obs = ustr(row[25])
    
    
        #
        # DATAS 
        # 
    
        data_cadastro = datetime.now()
        try:
            data_cadastro=row[26]
        except:
            pass
    
    
        # 
        # Contrato
        # 
    
        # Servico
        nas_get = row[28].strip()
        plano = row[29].strip()
        plano_valor = str(row[30]).strip()
    
        conexao_tipo = ustrl(row[31])
        conexao_tipo = 'ppp'
        if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
        if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'
    
    
        ip = ustr(row[32])
        if len(ip) < 7: ip = None
    
        mac = ustr(row[34])
        if len(mac) < 10: mac = None
        
        try:
            vencimento = int(row[35])
        except:
            vencimento = 10
            print 'erro row (%s) - %s' %(row[35],ri)
    
        comodato = ustrl(row[40]).lower()
        if comodato == 'sim':
            comodato = True
        elif comodato in ['nao','não','N_o']:
            comodato = False
    
        isento = ustr(row[41])
        if isento == 'Sim':
            isento = 100
        else:
            isento = 0
    
        status_cc = 1
        status_s = 1
        status_c = 1
    
        status = ustr(row[42])
        status_ativo = ustr(row[42])
    
        if status == 'L':
            status_cc = 1
            status_s = 1
            status_c = 1
    
        if status == 'B':
            status_cc = 4
            status_s = 4
            status_c = 4
    
        if status == 'X':
            status_cc = 3
            status_s = 3
            status_c = 3
    
        nomepai = ustr(row[44])
        nomemae = ustr(row[45])
        anotacoes = '\n'.join(row[46].split('|'))
        latitude = row[47]
        longitude = row[48]
        map_ll = '%s,%s' %(latitude,longitude)
        dt_situacao = row[49]
        grupo_set = row[50]
        senha_txt = row[51]
        usuario_cad = row[52]
        velocidade = row[53]
        if velocidade == 'N':
            velocidade = None
        planovelocidade = None 

        try:
            usuario = admmodels.User.objects.get(username__iexact=row[52].strip().lower())
        except:
            usuario = usuario_default
    
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
                new_plano_internet.download = 2048
                new_plano_internet.upload = 1024
                new_plano_internet.save() 
                print('criado plano %s' %plano)
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            else:
                raise Exception('Não localizei plano %s' %plano)

        if velocidade and velocidade != plano:
            try:
                planovelocidade = admmodels.PlanoVelocidade.objects.filter(plano__descricao__iexact=velocidade.lower())[0]
            except:
                if args.planoadd:
                    new_plano = admmodels.Plano()
                    new_plano.descricao=velocidade
                    new_plano.preco = 0
                    new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
                    new_plano.grupo = admmodels.Grupo.objects.get(nome='cabo')
                    new_plano.save()

                    new_plano_velocidade = admmodels.PlanoVelocidade()
                    new_plano_velocidade.plano = new_plano 
                    new_plano_velocidade.download = 2048
                    new_plano_velocidade.upload = 1024
                    new_plano_velocidade.save() 
                    print('criado velocidade %s' %velocidade)
                else:
                    raise Exception('Não localizei velocidade %s' %velocidade)
    
        cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore')
        try:
            pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
            pop = pop_q
        except:
            new_pop = admmodels.Pop()
            new_pop.cidade=cidade_q.upper()
            new_pop.uf=uf
            new_pop.save()
            pop = new_pop
    
        try:
            nas = nmodels.NAS.objects.get(shortname__iexact=nas_get.strip())
        except:
            nas = nas_default
            print 'Não localizei NAS com nome %s. Definindo NAS: %s' %(nas_get,nas_default)
    
        try:
            fmodels.Vencimento.objects.get(dia=vencimento)
        except:
            print "erro vencimento %s" %vencimento 
            if args.vencimentoadd:
                print('corrigindo vencimento %s' %vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 
    
        print 'Dados Pessoa: ',nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro, data_nasc
        print 'Cadastrado Por: ',usuario
        print 'Filiacao: ',nomepai,nomemae
        print 'Endereco: ',logradouro,numero,complemento,bairro,cidade,uf,cep
        print 'Vencimento/Plano: ', vencimento, 'Plano: ', plano
        print 'Plano Velocidade:', planovelocidade
        print 'Contato: ',telefone,telefonecom,celular,conn_obs
        print 'Autenticacao: ',login,senha,senha_txt,ip,mac
        print '####################################################'
        if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__unaccent__iexact=login).count() == 0:
            print "Import %s" %nome
            # Save Models 
            
            cliente_check = admmodels.Cliente.objects.filter(id=idcontrato)
    
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
                new_endereco.map_ll = map_ll
            
                new_endereco_cob = copy.copy(new_endereco)
                new_endereco_inst = copy.copy(new_endereco)
                new_endereco.save() 
                new_endereco_cob.save()
                new_endereco_inst.save()
                
                

    
                tp = 'f'
                if len(cpfcnpj) > 14 or tipo.lower() in [u'pessoa jur_dica',u'pessoa jurídica']:
                    tp = 'j'
                
                if tp == 'f':
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
                new_cliente.id = idcontrato
                new_cliente.endereco = new_endereco
                new_cliente.pessoa = new_pessoa
                new_cliente.data_cadastro = data_cadastro
                new_cliente.data_alteracao = data_cadastro
                new_cliente.ativo = True 
                new_cliente.observacao=anotacoes
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
                
                
                # Cliente
                #new_cliente = imodels.Cliente()
                #new_cliente.endereco = new_endereco
                #new_cliente.pessoa = new_pessoa
                #new_cliente.data_cadastro = data_cadastro
                #new_cliente.data_alteracao = data_cadastro
                #new_cliente.ativo = True 
                #new_cliente.save()
                #new_cliente.data_cadastro = data_cadastro
                #new_cliente.save()
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
            
            contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
            # Contrato 
            new_contrato = admmodels.ClienteContrato()
    
            if len(contrato_check) == 0:
                new_contrato.id = idcontrato
            else:
                new_contrato.id = incrementar
                incrementar += 1
    
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
            if admmodels.ServicoInternet.objects.filter(login__iexact=login).count() > 0:
                print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                  login,
                                                                                  str(new_contrato.id))
                login += str(new_contrato.id)
            new_servico.login= login
            new_servico.endereco = new_endereco_inst
            new_servico.login_password=senha 
            new_servico.login_password_plain=senha_txt
            new_servico.central_password=senhacentral
            if admmodels.ServicoInternet.objects.filter(Q(mac_dhcp=mac)).count() == 0:
                new_servico.mac_dhcp = mac
    
            if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                new_servico.ip = ip 
            new_servico.tipoconexao = conexao_tipo
            new_servico.nas = nas
            new_servico.planointernet = planointernet
            new_servico.planovelocidade = planovelocidade
            new_servico.modoaquisicao = 1 if comodato == True else 0
            new_servico.data_cadastro=data_cadastro
            new_servico.observacao = conn_obs
            new_servico.save()
        
    
            new_servico.data_cadastro=data_cadastro
            new_servico.login_password_plain=senha_txt
            new_servico.login_password=senha
            new_servico.save()
    
            m.addRadiusServico(new_servico)
