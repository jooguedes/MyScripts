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
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--arquivo', dest='arquivo', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--telefones', dest='telefones', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--emails', dest='emails', type=str, help='Arquivo importacao',required=False)
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


if args.telefones:
    with open(args.telefones, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in conteudo:
            print(row)
            try:
                cliente = admmodels.Cliente.objects.get(pk=row[0])
            except:
                continue
            if cliente.clientecontato_set.filter(contato__contato=row[1]).count() == 0:
                print cliente
                telefone = row[1]
                new_contato = admmodels.Contato() 
                new_contato.tipo = 'CELULAR_COMERCIAL'
                new_contato.contato = telefone
                new_contato.observacao = row[2] 
                new_contato.save() 
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()


if args.emails:
    with open(args.emails, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in conteudo:
            print(row)
            try:
                cliente = admmodels.Cliente.objects.get(pk=row[0])
            except:
                continue
            if cliente.clientecontato_set.filter(contato__contato=row[1]).count() == 0:
                print cliente
                email = row[1]
                new_contato = admmodels.Contato() 
                new_contato.tipo = 'EMAIL'
                new_contato.contato = email
                new_contato.observacao = row[2] 
                new_contato.save() 
                new_ccontato = admmodels.ClienteContato()
                new_ccontato.cliente = cliente
                new_ccontato.contato = new_contato
                new_ccontato.save()



if args.arquivo:
    pop_default = admmodels.Pop.objects.get(pk=args.pop_id)
    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)

    incrementar = admmodels.ClienteContrato.objects.all().aggregate(Max('id')).get('id__max') or 5000
    if incrementar < 5000:
        incrementar = 5000
    else:
        incrementar += 1

    m = manage.Manage()
    with open(args.arquivo, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in conteudo:
            idcliente = int(row[0])
            idcontrato = int(row[45])
            
            print row
            login=ustrl(row[1])
            if row[44]:
                senha=row[44]
            else:
                senha='controllr2sgp'
            if not login:
                login = 'c%s' %idcontrato
            #if not senha:
            #    senha = login


            #
            # Dados pessoais 
            #
            nome = ustr(row[3])
            cpfcnpj = ustr(row[5])
            rgie = ustr(row[8])
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
                y_,m_,d_ = row[11].split(' ')[0].split('-')
                data_nasc=date(int(y_),int(m_),int(d_))
            except:
                pass

            #
            # Endereço 
            #
            logradouro = ustr(row[14])[0:255]
            numero = None
            try:
                numero = int(row[15])
            except:
                numero = None
                logradouro += ",%s" %row[15]
            complemento = ustr(row[16])[0:255]
            bairro = ustr(row[17])[0:50]
            cep = ustr(row[18])
            uf = ustr(row[19])
            cidade = ustr(row[20]).upper()[0:50]

            #
            # Contato
            #
            celular = ustr(row[21]).replace('.0','')
            telefonecom = ustr(row[22]).replace('.0','')
            email = ustrl(row[23])   
            telefone = ''
            con_obs=''
            #con_obs = ustr(row[25])
            #if con_obs == 'NENHUMA':
            #    con_obs=''

            #
            # DATAS 
            # 

            data_cadastro = datetime.now()
            try:
                y_,m_,d_ = row[25].split(' ')[0].split('-')
                data_cadastro=datetime(int(y_),int(m_),int(d_),0,0,1)
            except:
                pass


            # 
            # Contrato
            # 

            # Servico
            nas_get = row[28].strip()
            plano = row[29].strip()
            plano_valor = str(row[30]).strip()
            plano_download = ustrl(row[31]) or 0
            plano_upload = ustrl(row[32]) or 0
            conexao_tipo = 'ppp'

            ip = ustr(row[33])
            if len(ip) < 7: ip = None

            mac = ustr(row[34])
            if len(mac) < 10: mac = None
            
            try:
                vencimento = int(row[35])
            except:
                vencimento = 10
                print 'erro row (%s)' %(row[35])

            comodato = ustrl(row[40]).lower()
            if comodato == 'sim':
                comodato = True
            elif comodato in ['nao','não','N_o']:
                comodato = False

            isento = ustr(row[41])
            if isento == 'sim':
                isento = 100
            else:
                isento = 0

            status_cc = 1
            status_s = 1
            status_c = 1

            cliente_status = ustrl(row[42])
            contrato_status = ustrl(row[43])
            conexao_status = ustrl(row[46])

            if cliente_status == '1':
                status_cc = 3
                status_s = 3
                status_c = 3
            else:
                if contrato_status == '1':
                    status_cc = 3
                    status_s = 3
                    status_c = 3
                elif conexao_status == '4':
                    status_cc = 4
                    status_s = 4
                    status_c = 4

            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                if args.planoadd:
                    new_plano = admmodels.Plano()
                    new_plano.descricao=plano
                    new_plano.preco = plano_valor
                    new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='cabo')
                    new_plano.grupo = admmodels.Grupo.objects.get(nome='cabo')
                    try:
                        new_plano.save()
                    except:
                        new_plano.preco=0.00
                        new_plano.save()

                    new_plano_internet = admmodels.PlanoInternet()
                    new_plano_internet.plano = new_plano 
                    new_plano_internet.download = plano_download
                    new_plano_internet.upload = plano_upload
                    new_plano_internet.save() 
                    print('criado plano %s' %plano)
                else:
                    raise Exception('Não localizei plano %s' %plano)

            cidade_q = normalize('NFKD', cidade).encode('ASCII','ignore')
            try:
                pop_q = admmodels.Pop.objects.filter(cidade__unaccent__ilike='%%%s%%' %cidade_q)[0]
                pop = pop_q
            except:
                pop = pop_default
                #print 'Não localizei cidade: %s - Definindo POP: %s' %(cidade_q,pop_default)

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

            #
            # Endereço 
            #
            c_end_logradouro = ustr(row[47])[0:255]
            c_end_numero = None
            try:
                c_end_numero = int(row[48])
            except:
                c_end_numero = None
                c_end_logradouro += ",%s" %row[48]
            c_end_complemento = ustr(row[49])[0:255]
            c_end_bairro = ustr(row[50])[0:50]
            c_end_cep = ustr(row[51])
            c_end_uf = ustr(row[52])
            c_end_cidade = ustr(row[53]).upper()[0:50]


            #
            # Endereço 
            #
            s_end_logradouro = ustr(row[54])[0:255]
            s_end_numero = None
            try:
                s_end_numero = int(row[55])
            except:
                s_end_numero = None
                s_end_logradouro += ",%s" %row[55]
            s_end_complemento = ustr(row[56])[0:255]
            s_end_bairro = ustr(row[57])[0:50]
            s_end_cep = ustr(row[58])
            s_end_uf = ustr(row[59])
            s_end_cidade = ustr(row[60]).upper()[0:50]


            #print pop
            #print row
            print nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print c_end_logradouro,c_end_numero or '',c_end_complemento,c_end_bairro,c_end_cidade,c_end_uf,c_end_cep
            print s_end_logradouro,s_end_numero or '',s_end_complemento,s_end_bairro,s_end_cidade,s_end_uf,s_end_cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print login,senha,ip,mac
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login=login).count() == 0:
                print "Import %s" %nome
                # Save Models 

                cliente_check = admmodels.Cliente.objects.filter(id=idcliente)
        
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
                    new_endereco.save() 

                    new_endereco_cob = admmodels.Endereco()
                    new_endereco_cob.logradouro = c_end_logradouro
                    new_endereco_cob.numero = c_end_numero
                    new_endereco_cob.bairro = c_end_bairro
                    new_endereco_cob.cep = c_end_cep
                    new_endereco_cob.cidade = c_end_cidade
                    new_endereco_cob.uf = c_end_uf 
                    new_endereco_cob.pais = 'BR'
                    new_endereco_cob.complemento = c_end_complemento
                    new_endereco_cob.pontoreferencia=''
                    new_endereco_cob.save() 

                    new_endereco_inst = admmodels.Endereco()
                    new_endereco_inst.logradouro = s_end_logradouro
                    new_endereco_inst.numero = s_end_numero
                    new_endereco_inst.bairro = s_end_bairro
                    new_endereco_inst.cep = s_end_cep
                    new_endereco_inst.cidade = s_end_cidade
                    new_endereco_inst.uf = s_end_uf 
                    new_endereco_inst.pais = 'BR'
                    new_endereco_inst.complemento = s_end_complemento
                    new_endereco_inst.pontoreferencia=''
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
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg = rgie.strip()[:20]
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
                    new_cliente.id = idcliente
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
                    
                    new_endereco_cob = copy.copy(new_endereco)
                    new_endereco_cob.id = None 
                    new_endereco_inst = copy.copy(new_endereco)
                    new_endereco_inst.id = None 
                    new_endereco_cob.save()
                    new_endereco_inst.save()
                    new_cliente = cliente_check[0]
                
                contrato_check = admmodels.ClienteContrato.objects.filter(id=idcontrato)
                if len(contrato_check) > 0:
                    idcontrato = incrementar
                    incrementar += 1

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

