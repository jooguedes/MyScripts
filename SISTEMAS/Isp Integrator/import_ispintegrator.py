#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
from datetime import date, datetime
import copy
from unicodedata import normalize
import csv 

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=False)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=True)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--planos', dest='planos', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--logins', dest='logins', type=str, help='Arquivo importacao',required=True)
parser.add_argument('--planoadd', dest='planoadd', type=bool, help='Criar plano para corrigir',required=False)
parser.add_argument('--vencimentoadd', dest='vencimentoadd', type=bool, help='Criar vencimento para corrigir',required=False)
args = parser.parse_args()
#python import_ispintegrator.py --settings=sgp.dunet.settings --portador=1 --clientes=Conv-EXPORTAR_CLIENTES.CSV.csv --logins=Conv-EXPORTAR_LOGINS.CSV.csv --planos=Conv-EXPORTAR_PLANOS.csv --sync=1 --planoadd=1 --vencimentoadd=1 --nas=1 --pop=1
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
ri = -1
incrementar = 90000
m = manage.Manage()

logins = []
clientes = []
clientes_dict = {} 
planos = [] 

with open(args.clientes, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        clientes.append(row)

with open(args.logins, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        logins.append(row)

with open(args.planos, 'rb') as csvfile:
    conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
    for row in conteudo:
        planos.append(row)


print ("Mapeando clientes")
for cli in clientes:
    clientes_dict[cli[0]] = {'dados': cli } 
    clientes_dict[cli[0]]['logins'] = []
    clientes_dict[cli[0]]['planos'] = []

    for l in logins:
        if int(l[0]) == int(cli[0]):
            clientes_dict[cli[0]]['logins'].append(l)
    
    for p in planos:
        if int(p[2]) == int(cli[0]):
            clientes_dict[cli[0]]['planos'].append(p)

    print cli[0],len(clientes_dict[cli[0]]['logins']),len(clientes_dict[cli[0]]['planos'])


print "Mapeamento finalizado"
print len(clientes)

for c in clientes_dict:
    crow = clientes_dict[c]['dados']
    clogins= clientes_dict[c]['logins']
    cplanos = clientes_dict[c]['planos']
    
    if len(clogins) > 0 and len(cplanos) > 0: 

        for lrow in clogins:
            lindex = 0
            try:
                prow = cplanos[lindex]
            except:
                prow = cplanos[0]

            ri += 1
            idcontrato = int(crow[0])
            tipo = ustr(crow[2])

            #
            # Dados pessoais 
            #
            nome = ustr(crow[5])
            fantasia = ustr(crow[6])
            sexo = None
            cpfcnpj = crow[19]
            ie = None
            im = None
            rg = ustr(crow[22])[:20]

            profissao = ''
            


            data_nasc = None
            #try:
            #    d_,m_,y_ = crow[3].split('/')
            #    data_nasc='%s-%s-%s' %(y_,m_,d_)
            #except:
            #    pass

            #
            # Endereço 
            #
            logradouro = ustr(crow[7])
            numero = None
            complemento = ''
            bairro = ustr(crow[8])
            cidade = ustr(crow[9]).upper()
            uf = ustr(crow[10])
            preferencia = ustr(crow[11])
            cep = ustr(crow[12])

            

            #
            # Endereço Cobrança
            #
            cob_logradouro = ustr(crow[22])
            cob_numero = None
            cob_complemento = ''
            cob_bairro = ustr(crow[23])
            cob_cep = ustr(crow[24])
            cob_cidade = ustr(crow[25]).upper()
            cob_uf = ustr(crow[10])
            cob_preferencia = ustr(crow[11])
            

            #
            # Contato
            #
            ddd = crow[13]
            telefone = crow[14].replace('.0','')
            telefonecom = crow[15].replace('.0','')
            celular = crow[16].replace('.0','')
            if telefone:
                telefone = ddd + telefone
            if telefonecom:
                telefonecom = ddd + telefonecom

            email = ''   
            con_obs=''
            #con_obs = ustr(row[25])
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS 
            # 

            data_cadastro = datetime.now()
            try:
                d_,m_,y_ = crow[3].split('/')
                data_cadastro='%s-%s-%s' %(y_,m_,d_)
            except:
                pass


            # 
            # Contrato
            # 

            # Servico
            plano = lrow[2].strip()
            login=ustrl(lrow[3])
            senha=lrow[4]
            #plano_valor = str(row[29]).strip()

            #conexao_tipo = ustrl(lrow[10])
            conexao_tipo = 'ppp'
            if conexao_tipo == 'hotspot': conexao_tipo = 'mkhotspot'
            if conexao_tipo == 'pppoe': conexao_tipo = 'ppp'


            ip = ustr(lrow[5])
            if len(ip) < 7: ip = None

            mac = ustr(lrow[6])
            if len(mac) < 10: mac = None

            if mac:
                mac = mac.replace('-',':')
            
            try:
                vencimento = int(prow[-1:][0])
            except:
                vencimento = 10
                print 'erro row (%s) - %s' %(prow[-1:][0],ri)

            comodato = False
            #if comodato == 'sim':
            #    comodato = True
            #elif comodato in ['nao','não','N_o']:
            #    comodato = False
#

            isento = 0
            
            #if isento == 'Sim':
            #    isento = 100
            #else:
            #    isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            if 'inativo' in row[2]:
                status_cc = 3
                status_s = 3
                status_c = 3

                
            #status = prow[14]
            #if 'suspenso' in status.lower():
            #    status_cc = 4
            #    status_s = 4
            #    status_c = 4
#
            #if 'cancelado' in status.lower():
            #    status_cc = 3
            #    status_s = 3
            #    status_c = 3
            

            plano_download = 2048
            plano_upload = 1024
            plano_valor = 0
            planointernet=''
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
                    new_plano_internet.download = plano_download
                    new_plano_internet.upload = plano_upload
                    new_plano_internet.save() 
                    print('criado plano %s' %plano)
                    planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
                else:
                    raise Exception('Não localizei plano %s' %plano)

            '''cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                new_pop = admmodels.Pop()
                new_pop.cidade=cidade_q.upper()
                new_pop.uf=uf
                new_pop.save()
                pop = new_pop'''
            
            pop=admmodels.Pop.objects.get(id=1)

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
                    new_endereco.pontoreferencia=preferencia

                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco.save() 
                    new_endereco_inst.save()
                    
                    new_endereco_cob = admmodels.Endereco()
                    new_endereco_cob.logradouro = cob_logradouro
                    new_endereco_cob.numero = cob_numero
                    new_endereco_cob.bairro = cob_bairro
                    new_endereco_cob.cep = cob_cep
                    new_endereco_cob.cidade = cob_cidade
                    new_endereco_cob.uf = cob_uf 
                    new_endereco_cob.pais = 'BR'
                    new_endereco_cob.complemento = cob_complemento
                    new_endereco_cob.pontoreferencia=cob_preferencia
                    new_endereco_cob.save()



                    
                    tp = 'f'
                    if len(cpfcnpj) > 14 or tipo.lower().strip() in [u'juridica',u'Jurídica']:
                        tp = 'j'
                    
                    if tp == 'f':
                        new_pessoa = admmodels.Pessoa()
                        new_pessoa.tipopessoa='F'
                        
                        new_pessoa.nome = nome
                        new_pessoa.sexo = sexo
                        new_pessoa.datanasc = data_nasc
                        new_pessoa.profissao = profissao
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg = rg
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
                        
                        new_pessoa.nomefantasia = fantasia[:20]
                        new_pessoa.resempresa = ''
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.insc_estadual = None
                        new_pessoa.insc_municipal =None
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

                    new_endereco_cob = admmodels.Endereco()
                    new_endereco_cob.logradouro = cob_logradouro
                    new_endereco_cob.numero = cob_numero
                    new_endereco_cob.bairro = cob_bairro
                    new_endereco_cob.cep = cob_cep
                    new_endereco_cob.cidade = cob_cidade
                    new_endereco_cob.uf = cob_uf 
                    new_endereco_cob.pais = 'BR'
                    new_endereco_cob.complemento = cob_complemento
                    new_endereco_cob.pontoreferencia=cob_preferencia
                    new_endereco_cob.save()


                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco_inst.id = None 
                    new_endereco_inst.save()
                    
                    
                    # Cliente
                    #new_cliente = imodels.Cliente()
                    #new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
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

            lindex += 1
