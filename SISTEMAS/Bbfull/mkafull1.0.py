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
args = parser.parse_args()

#   python import_mkfull.py --settings=sgp.linktechprovedor.settings --nas=1 --portador=1 --clientes= --sync=1

PATH_APP = '/usr/local/sgp'

if PATH_APP not in sys.path:
    sys.path.append(PATH_APP)

os.environ["DJANGO_SETTINGS_MODULE"] = args.settings
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

from django.conf import settings
from django.db.models import Q, Max

from apps.admcore import models as admmodels
from apps.atendimento import models as amodels
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


if args.clientes:
    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='cabo').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='cabo').order_by('-id')[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
    ri = -1

    incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 10000
    if incrementar < 10000:
        incrementar = 10000
    else:
        incrementar += 1

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            ri += 1
            idcontrato = int(row[0])
            nome = ustr(row[1])
            fantasia = ustr(row[1])
            cpfcnpj = row[2]
            rgie = row[3]

            data_nasc = None
            diasparabloqueio = 15
            

            sexo = None

            profissao = ''
  
            #data_nasc = None
            #try:
            #    d_,m_,y_ = row[11].strip().split('/')
            #    if len(y_) == 2:
            #        y_ = '19%s' %y_
            #    date(int(y_),int(m_),int(d_))
            #    data_nasc='%s-%s-%s' %(y_,m_,d_)
            #except:
            #    pass

            #
            # Endereço 
            #
            logradouro = ustr(row[18])
            numero = None
            try:
                numero = int(row[19])
            except:
                numero = None
            complemento = ustr(row[20])
            pontoreferencia = ustr(row[21]).upper()
            bairro = ustr(row[22]).strip()[0:50]
            cidade = ustr(row[23]).upper()[0:50]
            uf = ustr(row[24])
            cep = ustr(row[25]).strip()[0:20]
            map_ll = row[26]

            #
            # Contato
            #
            celular = ustr(row[29])
            telefonecom = ustr(row[30])
            telefonecom2 = ustr(row[32])
            emails = [row[27], row[28]]
            telefone = ustr(row[31]) 
            servico_obs=row[33]
            con_obs = ''
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS 
            # 
            data_cadastro = row[15]
            if data_cadastro:
                d = row[15].split(' ')[0]
                data_cadastro = '%s-%s-%s' %(d.split('/')[2],d.split('/')[1],d.split('/')[0])
            else:
                data_cadastro = date.today()
            data_cancela = None

            # 
            # Contrato
            # 

            # Servico
            plano = row[4]
            plano_valor = row[5]
            plano_download = 20480
            plano_upload = 20480
            conexao_tipo = 'ppp'


            ip = ustr(row[36])
            if len(ip) < 7: ip = None

            mac = ustr(row[37])
            if len(mac) < 10: mac = None
            
            try:
                vencimento = int(row[9])
            except:
                vencimento = 10
                print 'erro row (%s) - %s' %(row[9],ri)

            
            desconto = 9
            acrescimo = 0
            comodato = ustrl(row[35]).lower()

            if 'sim' in comodato:
                comodato = True
            else:
                comodato = False 

            isento_txt = ustr(row[6]).lower()
            isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            status = row[10]

            if status == 'bloqueado':
                status_cc = 4
                status_s = 4
                status_c = 4

            if status== 'Desativado':
                status_cc = 3
                status_s = 3
                status_c = 3

            logins = [row[6], row[8]]
            senha = row[7]

            if senha=='' or  not senha:
                senha='sem_senha'

            nome_pai = None
            nome_mae = None
            naturalidade = None
            observacao = row[38]

            if servico_obs:
                servico_obs += "Equipamento: %s" %servico_obs
            else:
                servico_obs = "Equipamento: %s" %servico_obs

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                if row[4]=='':
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact='DESATIVDOS')[0]
                else:
                    print(plano,plano_download,plano_upload,plano_valor)
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
                    print('criado plano %s' %plano)
            
            pop=admmodels.Pop.objects.all()[0]

            nas = nas_default

            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except: 
                print('corrigindo vencimento %s' %vencimento)
                new_vencimento = fmodels.Vencimento()
                new_vencimento.dia = vencimento
                new_vencimento.save() 

            #print pop
            #print row

            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print nome_pai, nome_mae, naturalidade
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', planointernet
            print telefone,telefonecom,celular,emails,con_obs
            print logins,senha,ip,mac
            print '####################################################'
            if args.sync_db == True:
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
                    new_endereco.pontoreferencia=pontoreferencia

                    new_endereco_cob = admmodels.Endereco()
                    new_endereco_cob.logradouro = logradouro
                    new_endereco_cob.numero = numero
                    new_endereco_cob.bairro = bairro
                    new_endereco_cob.cep = cep
                    new_endereco_cob.cidade = cidade
                    new_endereco_cob.uf = uf 
                    new_endereco_cob.pais = 'BR'
                    new_endereco_cob.complemento = complemento
                    new_endereco_cob.pontoreferencia=pontoreferencia
                    new_endereco_cob.save() 

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
                        
                        new_pessoa.nomefantasia = fantasia
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
                    new_cliente.observacao = observacao
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True 
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
                        new_contato.tipo = 'CELULAR_COMERCIAL'
                        new_contato.contato = telefone 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 4
                    if len(telefonecom) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                        new_contato.contato = telefonecom
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                    
                    # contato 5
                    if len(telefonecom2) > 4:
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

                for login in logins:
                    if len(login) > 3:
                        if admmodels.ServicoInternet.objects.filter(login=login).count() == 0:

                            # Enderecos
                            new_endereco_cob = copy.copy(new_endereco)
                            new_endereco_cob.id = None 
                            new_endereco_inst = copy.copy(new_endereco)
                            new_endereco_inst.id = None 
                            new_endereco_cob.save()
                            new_endereco_inst.save()

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
                            
                            status_l = [6,2,status_cc]
                            
                            if status == 'fila':
                                status_l = [6,2]

                            for ic in status_l:
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
                            new_servico.login= login[:79]
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
        
    from apps.admcore import models as admmodels 
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)