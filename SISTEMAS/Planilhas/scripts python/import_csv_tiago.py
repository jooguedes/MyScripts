#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from turtle import down
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
args = parser.parse_args()

#python import_csv.py --settings=sgp.zevo.settings --clientes=Conv-cliente-orlando.csv --planoadd=1 --vencimentoadd=1 --portador=3 --nas=1 --sync=1
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

def formatarData(d):
    if d:
        if '/' in d:
            d,m,y = d.split('/')
            return '%s-%s-%s' %(y,m,d)
        return d
    return None
def formatarNumero(n):
    try:
        x = int(re.sub('[^0-9]','', str(n)))
    except:
        x = None
    return x

usuario = admmodels.User.objects.get(username='sgp')

if args.clientes:
    formacobranca = fmodels.FormaCobranca.objects.all()[0]
    contrato_obj = admmodels.Contrato.objects.filter(grupo__nome='fibra').order_by('-id')[0]
    grupo_obj = admmodels.Grupo.objects.filter(nome='fibra').order_by('-id')[0]

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)
    ri = -1

    incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 10000
    if incrementar < 10000:
        incrementar = 10000
    else:
        incrementar += 20

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
         
            ri += 1
            idcontrato = int(row[3]) + 2500
            idCliente= int(row[3]) + 2500
            #'%s@import'%
            login= row[1]
            
            nome = ustr(row[0])
            cpfcnpj = ustr(row[28])[:20]
            rgie = ustr(row[30])[:20]
            sexo = None
            
            data_cadastro= datetime.now()
            try:
                d_,m_,y_ = row[33].strip().split('/')
                if len(y_) == 2:
                    y_ = '19%s' %y_
                date(int(y_),int(m_),int(d_))
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass
            


            data_nasc = row[33]
            try:
                d_,m_,y_ = row[6].strip().split('/')
                if len(y_) == 2:
                    y_ = '19%s' %y_
                date(int(y_),int(m_),int(d_))
                data_nasc='%s-%s-%s' %(y_,m_,d_)
            except:
                data_nasc=None
            

            logradouro = ustr(row[20])
            numero = formatarNumero(row[21])
            complemento = row[22]
            bairro = ustr(row[23]).strip()[0:50]
            cep = ustr(row[17]).strip()[0:20]
            uf = ustr(row[25])
            cidade = ustr(row[24]).upper()[0:50]
            pop=admmodels.Pop.objects.get(id=3)
            #
            # Contato
            #
            celular = ustr(row[6])
            telefone = ustr(row[7])
            email = row[26]
            email02=row[27]
            #data_cadastro = formatarData(row[25])

            plano = ''
            
            if plano=='importador@'+str(row[13]):
                plano ='defautl'
       
            conexao_tipo = 'ppp'
            if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'

            
            ip = None
    
            mac=None    
         

            try:
                vencimento = int(row[11])
            except:
                vencimento = 10

            

            comodato = False
            '''if comodato in ['Sim','sim']:
                comodato = True
            elif comodato in ['nao','não','N_o']:
                comodato = False'''
            status=row[16]

            status_cc = 1
            status_s = 1
            status_c = 1

            if 'Suspenso por Débito' in status:
                status_cc = 4
                status_s = 4
                status_c = 4
         
            
            senha='sem senha'
            
            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__lower__iexact=plano.lower().strip())[0]
            except:
                if args.planoadd:
                    print(plano)
                    new_plano = admmodels.Plano()
                    new_plano.descricao=plano
                    new_plano.preco = 0
                    new_plano.contrato = contrato_obj
                    new_plano.grupo = grupo_obj
                    new_plano.save()

                    new_plano_internet = admmodels.PlanoInternet()
                    new_plano_internet.plano = new_plano
                    new_plano_internet.download = 0
                    new_plano_internet.upload = 0
                    new_plano_internet.save()
                    print('criado plano %s' %plano)

                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__lower__iexact=plano.lower().strip())[0]
                else:
                    raise Exception('Não localizei plano %s' %plano)
          
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

            print nome,cpfcnpj,len(cpfcnpj),sexo,data_nasc
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
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
                    if len(fnum(cpfcnpj)) > 12:
                        tp = 'j'

                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'

                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.nacionalidade = 'BR'
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
                    new_cliente.id = idCliente
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.ativo = True
                    new_cliente.save()
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
                    
                    if len(email02) > 4:
                        new_contato = admmodels.Contato()
                        new_contato.tipo = 'EMAIL'
                        new_contato.contato = email02
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
                new_cobranca.notafiscal = False
                new_cobranca.usuariocad = usuario
                new_cobranca.formacobranca = formacobranca
                new_cobranca.status = status_c
    
                new_cobranca.save()

                new_cobranca.save()

                contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
                # Contrato
                new_contrato = admmodels.ClienteContrato()

                
                new_contrato.id = idcontrato
                
                new_contrato.cliente = new_cliente
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca
                new_contrato.data_inicio=datetime.now()
                new_contrato.data_cadastro=datetime.now()
             
                new_contrato.save()

           
                new_contrato.save()
                
                for ic in [6,2,status_cc]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=2
                    new_status.usuario = usuario
                 
                    new_status.save()

                    
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
                new_servico.modoaquisicao = 1 if comodato == True else 0
             
                new_servico.observacao=''
                new_servico.save()

              
                new_servico.save()

                m.addRadiusServico(new_servico)


    from apps.admcore import models as admmodels
    from apps.netcore import models as netmodels
    for p in admmodels.Pop.objects.all():
        for plano in admmodels.Plano.objects.all():
            plano.pops.add(p)
        for n in netmodels.NAS.objects.all():
            n.pops.add(p)




	#   python import_csv.py --settings=sgp.zevo.settings --nas=1 --portador=3 --vencimentoadd=1 --planoadd=1 --clientes=
