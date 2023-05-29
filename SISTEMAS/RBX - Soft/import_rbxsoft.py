#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from pickle import NONE
from datetime import date, datetime
import copy
from tkinter.messagebox import NO
from unicodedata import normalize
import csv
import re
parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
parser.add_argument('--coordenadas', dest='coordenadas', type=str, help='adicionar remover acrescimos',required=False)
args = parser.parse_args()

#python import_rbx.py --setting=sgp.local.settings --portador=1 --clientes= --planoadd=1 --vencimentoadd=1 --nas=1 --sync=1

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
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)

    m = manage.Manage()
    with open(args.clientes, 'rU') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            try:
                idcontrato = int(row[0])
            except:
                print("ocorreu uma excessao no contrato de id", idcontrato)
            idcliente= row[0]
            login=ustrl(row[29])
            nome = ustr(row[3])
            cpfcnpj = ustr(row[2])
            rgie = ustr(row[14])
            sexo=None
            
            
            ####### ENDERECO ######
            logradouro = ustr(row[4])
            numero = row[5]
            try:
                numero = int(re.sub('[^0-9]','', str(row[15])))
            except:
                numero = None
            complemento = ustr(row[6])
            bairro = ustr(row[7]).strip()[0:50]
            cep = ustr(row[10]).strip()[0:20]
            uf = ustr(row[9])
            cidade = ustr(row[8]).upper()[0:50]

            
            ####### CONTATO ########
            
            celular = ustr(row[13])
            telefonecom = ustr(row[11])
            email = ''
 
            telefone = row[12]
            servico_obs=''
            con_obs = ''
    

            
            ############# DATAS ##########
            

            data_cadastro = datetime.now()
            try:
                y_,m_,d_ = row[31].strip().split('-')
                if len(y_) == 2:
                    y_ = '20%s' %y_
                date(int(y_),int(m_),int(d_))
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass


            data_nasc = None
            try:
                y_,m_,d_ = row[15].strip().split('-')
                if len(y_) == 2:
                    y_ = '19%s' %y_
                date(int(y_),int(m_),int(d_))
                data_nasc='%s-%s-%s' %(y_,m_,d_)
            except:
                pass

            data_cancelamento=''
            try:
                y_,m_,d_ = row[27].strip().split('-')
                if len(y_) == 2:
                    y_ = '19%s' %y_
                date(int(y_),int(m_),int(d_))
                data_cancelamento='%s-%s-%s' %(y_,m_,d_)
            except:
                pass





            
            ######### Status ########
            status_cc = 1
            status_s = 1
            status_c = 1

            if data_cancelamento!='' :
                status_cc = 3
                status_s = 3
                status_c = 3

          
           
            ######## PLANO DE INTERNET #####
            plano = row[20].strip()
            plano_valor = str(row[21]).strip()

            conexao_tipo = 'ppp'
            ip = None

            try:
                vencimento = int(row[28])
            except:
                vencimento = 10
            plano_download = int(row[22])
            plano_upload = int(row[23])
            senha=row[30]
            nome_pai = ''
            nome_mae = ''
            naturalidade = ''
            
            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                if args.planoadd:
                    print(plano,plano_download,plano_upload,plano_valor)
                    new_plano = admmodels.Plano()
                    new_plano.descricao=plano
                    new_plano.preco = plano_valor
                    new_plano.contrato = contrato_obj
                    new_plano.grupo = grupo_obj
                    new_plano.save()

                    new_plano_internet = admmodels.PlanoInternet()
                    new_plano_internet.plano = new_plano
                    new_plano_internet.download = plano_download
                    new_plano_internet.upload = plano_upload
                    new_plano_internet.save()
                    print('criado plano %s' %plano)
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                else:
                    raise Exception('Não localizei plano %s' %plano)

            pop=admmodels.Pop.objects.get(id=1)
            nas = nas_default

            ########CADASTRA VENCIMENTOS#########
            try:
                fmodels.Vencimento.objects.get(dia=vencimento)
            except:
                print "erro vencimento %s" %vencimento
                if args.vencimentoadd:
                    print('corrigindo vencimento %s' %vencimento)
                    new_vencimento = fmodels.Vencimento()
                    new_vencimento.dia = vencimento
                    new_vencimento.save()



            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print nome_pai, nome_mae, naturalidade
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
                print "Import %s" %nome
                # Save Models

                cliente_check = admmodels.Cliente.objects.filter(id=idcontrato)
                #cliente_check02=admmodels.Cliente.objects.filter(pessoa__cpfcnpj__nufilter=cpfcnpj, pessoa__nome__iexact=nome)[0]

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
                        new_pessoa.profissao = None
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
                    new_cliente.id = idcliente
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    new_cliente.save()
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()

                    ### contato 1
                    if len(email) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'EMAIL'
                        new_contato.contato = email
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    ####### SAVE CONTATO 2 ######
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


                    ######### SAVE CONTATO 3 #####
                    if len(telefone) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                        new_contato.contato = telefone
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    ###### SAVE CONTATO 4 ######
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


                ###### SAVE COBRANCA #######
                new_cobranca = fmodels.Cobranca()
                new_cobranca.cliente = new_cliente
                new_cobranca.endereco = new_endereco_cob
                new_cobranca.portador = portador
                new_cobranca.vencimento = fmodels.Vencimento.objects.get(dia=vencimento)
                new_cobranca.isento = 0
                new_cobranca.notafiscal = False
                new_cobranca.data_cadastro = data_cadastro
                new_cobranca.datacobranca1 = data_cadastro
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = status_c
                new_cobranca.save()

                new_cobranca.data_cadastro = data_cadastro
                new_cobranca.save()

               
               
                ##### CONTRATO ####
                new_contrato = admmodels.ClienteContrato()
                new_contrato.id = idcontrato
                new_contrato.cliente = new_cliente
                try:
                    new_contrato.pop = pop
                except:
                    new_contrato.pop = admmodels.Pop.objects.filter(id=1)[0]
                new_contrato.cobranca = new_cobranca

                new_contrato.data_inicio = data_cadastro
                new_contrato.data_cadastro = data_cadastro
                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()
                try:
                    new_contrato.data_cadastro = data_cadastro
                    new_contrato.data_alteracao = data_cadastro
                    new_contrato.save()
                except:
                    new_contrato.pop = admmodels.Pop.objects.filter(id=1)[0]
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


                ######### SAVE  SERVICO ###########
                new_servico = admmodels.ServicoInternet()
                new_servico.clientecontrato = new_contrato
                new_servico.status = status_s
                if admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() > 0:
                    print u'Já existe serviço com o login %s. Ajustando login: %s%s' %(login,
                                                                                      login,
                                                                                      str(new_contrato.id))
                    login += str(new_contrato.id)
                new_servico.login= login
                new_servico.endereco = new_endereco_inst
                new_servico.login_password=senha
                new_servico.login_password_plain=senha
                new_servico.central_password=senha
                
                new_servico.mac_dhcp = None
                new_servico.mac = None
                
                new_servico.ip = ip
               
                    
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao = 1 
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


if args.coordenadas:
    with open(args.coordenadas, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            print(row)
            print(admmodels.Endereco.objects.filter(servicointernet__login__iexact=row[0]).update(map_ll=row[1]))
            print(admmodels.Endereco.objects.filter(cobranca__clientecontrato__servicointernet__login__iexact=row[0]).update(map_ll=row[1]))



