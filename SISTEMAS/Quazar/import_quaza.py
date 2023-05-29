#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
from itertools import count
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
#parser.add_argument('--chamados', dest='chamados', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
#parser.add_argument('--adcobranca', dest='adcobranca', type=str, help='adicionar remover acrescimos',required=False)
#parser.add_argument('--coordenadas', dest='coordenadas', type=str, help='adicionar remover acrescimos',required=False)
args = parser.parse_args()


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
    count=0
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        
        for row in conteudo:
            count=count+1
            print("rodei ", count," Vezes")
            ri += 1
            #idcontrato = int(row[35])+ 10100 
            idcontrato = row[35]
            #login='%s@quaza2' %str(row[26].lower().strip())
            login=row[26].lower().strip()
            '''descomentar isso ingnora acentos em logins'''

            #login=normalize('NFKD', login).encode('ASCII','ignore')

            #if ':' in login:
            #    continue

            #if not senha:
            #    senha = login

            #                                                                                                                         #
            ######################################################## Dados pessoais ###################################################
            #                                                                                                                         #
            nome = row[2].upper().strip()
            cpfcnpj = row[4].lower().strip()
            rgie = row[7]
            data_nasc=None
            #profissao = ustr(row[9])
            tipo = row[1].upper().strip()
            sexo= row[9]
            if (row[9] != 'M' or row[9] !='F'):
                if(row[9] == 'Feminino'):
                    sexo = 'F'
                elif row[9] == 'Masculino':
                    sexo = 'M'
            else:
                sexo = row[9]
                data_nasc = None
            try:
                y_,m_,d_ = row[10].strip().split('-')
                if len(y_) == 2:
                    y_ = '19%s' %y_

                date(int(y_),int(m_),int(d_))
                data_nasc='%s-%s-%s' %(y_,m_,d_)
            except:
                pass
            
            #dados pessoais finalizados

            #
            # Endereço
            #
            logradouro = row[13]
            numero = None
            try:
                numero = int(row[14])
            except:
                numero = None
                logradouro += ",%s" %row[14]
            complemento = row[15] or None
            bairro = row[16].strip()[0:50]
            cep = row[17].strip()[0:20]
            uf = row[18]
            cidade =unicode(str(row[19].upper()[0:50]))
            #                                                                                               #
            ######################################### Contato ###############################################
            #                                                                                               #
            celular =row[20]
            telefonecom = row[21]
            try:
             email = row[22]
            except:
                email= "sem@email.com"
            #servico_obs=row[23]
            #con_obs = ''
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #                                                                                                       #
            # ####################################################DATAS##############################################
            #                                                                                                       #     
            data_cadastro = datetime.now()

            try:
                y_,m_,d_= row[33].strip().split('/')
                if len(y_) == 2:
                    y_ = '20%s' %y_
                date(int(y_),int(m_),int(d_))
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass
            #                                                                                                      #
            ########################################################Contrato########################################
            #                                                                                                      #

            # Servico
            plano = row[30].strip()
            #plano_valor = str(row[29]).strip()

            conexao_tipo = row[29]
            conexao_tipo = 'indefinida'
            if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
            if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'
            ip = row[28]
            if len(ip) < 7: ip = None

            mac = row[29]
            if len(mac) < 10: mac = None

            try:
                vencimento = int(row[32])
            except:
                vencimento = 10
                print 'erro row (%s) - %s' %(row[32],ri)
            #=======parte do contrato finalizada========#

            #comodato = ustrl(row[39]).lower()
            #if comodato in ['Sim','sim']:
            #    comodato = True
            #elif comodato in ['nao','não','N_o']:
            #    comodato = False

            #isento = ustr(row[40])
            #if isento in ['Sim','sim']:
            #    isento = 100
            #else:
            #    isento = 0
            # status 3 == cancelado
            # status 4 == suspenso
            # status 1 == ativo

            status_cc = 1
            status_s = 1
            status_c = 1

            status =int(row[36].strip())
            #status_bloqueado = row[42]

            if(status):
                if(status==1):
                    status_cc = 1
                    status_s = 1
                    status_c = 1

                if (status ==2 or status==3):
                    status_cc = 4
                    status_s = 4
                    status_c = 4

                if (status==4):
                    status_cc = 3
                    status_s = 3
                    status_c = 3
            else:
                print('não existe status')
                continue
            
            if row[27]:
                senha=row[27]
            else:
                senha='quazar2sgp'

            plano_download = 0
            plano_upload = 0
            plano_valor = row[31]

            #login_pai = ustrl(row[49])

            #retirei devido a não precisar, creio eu
            '''if len(ustr(row[14])) == 0 and len(cidade.strip()) == 0:

                logradouro = ustr(row[50])
                numero = None
                try:
                    numero = int(row[51])
                except:
                    numero = None
                    logradouro += ",%s" %row[51]
                bairro = ustr(row[52]).strip()[0:50]
                cidade = ustr(row[53]).upper()[0:50]
                cep = ustr(row[54]).strip()[0:20]
                uf = ustr(row[55])
                complemento = ustr(row[56])'''

            '''nome_pai = row[57]
            nome_mae = row[58]
            naturalidade = row[59]'''



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
            #print nome_pai, nome_mae, naturalidade
            print numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefonecom,celular,email
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__trim__lower=login).count() == 0:
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

                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco.save()
                    new_endereco_cob.save()
                    new_endereco_inst.save()

                    tp = 'f'
                    if len(cpfcnpj.strip()) > 12:
                        tp = 'j'

                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'

                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        #new_pessoa.profissao = profissao
                        new_pessoa.nacionalidade = 'BR'
                        #new_pessoa.nomepai = nome_pai
                        #new_pessoa.nomemae = nome_mae
                        #new_pessoa.naturalidade = naturalidade
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
                    new_cliente.id = idcontrato
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
                        #new_contato.observacao = con_obs
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()


                    # contato 3
                    '''if len(telefone) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                        #new_contato.contato = telefone
                        new_contato.save()
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()'''

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
                    print("entrei no else do cliente check")
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
                #new_cobranca.isento = isento
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
                #new_contrato.data_cadastro = data_cadastro
                #new_contrato.data_alteracao = data_cadastro
                #new_contrato.save() 
                
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
                if admmodels.ServicoInternet.objects.filter(Q(mac=mac)|Q(mac_dhcp=mac)).count() == 0:
                    new_servico.mac_dhcp = mac
                    new_servico.mac = mac

                if ip and admmodels.ServicoInternet.objects.filter(Q(ip=ip)).count() == 0:
                    new_servico.ip = ip
                new_servico.tipoconexao = conexao_tipo
                new_servico.nas = nas
                new_servico.planointernet = planointernet
                new_servico.modoaquisicao =0
                new_servico.data_cadastro=data_cadastro
                #new_servico.observacao=servico_obs
                new_servico.save()

                new_servico.data_cadastro=data_cadastro
                new_servico.save()

                m.addRadiusServico(new_servico)

                #if login != login_pai:
                    #servico_pai = admmodels.ServicoInternet.objects.filter(login=login_pai)
                    #if servico_pai:
                        #new_cobranca.cobranca_unificada=servico_pai[0].clientecontrato.cobranca
                        #new_cobranca.save()





#if args.clientes:
   # cadastraClientes()


#python import_quazar.py --settings=sgp.vianetpe.settings --nas=1  --vencimentoadd=1 --planoadd=1 --portador=1 --clientes=quazar-clientes-ativados.csv.utf8  --sync=1