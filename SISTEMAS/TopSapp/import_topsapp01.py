#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os, sys
import csv
from datetime import date, datetime
import copy
from unicodedata import normalize
import re

parser = argparse.ArgumentParser(description='Importação XLS 1')
parser.add_argument('--settings', dest='settings', type=str, help='settings django',required=True)
parser.add_argument('--pop', dest='pop_id', type=int, help='ID do POP',required=False)
parser.add_argument('--nas', dest='nas_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--portador', dest='portador_id', type=int, help='ID do NAS',required=False)
parser.add_argument('--sync',dest='sync_db', type=bool, help='Sync Database',default=False)
parser.add_argument('--portadores', dest='portadores', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--ftth', dest='ftth', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--anotacoes', dest='anotacoes', type=str, help='Arquivo importacao',required=False)
parser.add_argument('--clientes', dest='clientes', type=str, help='Arquivo importacao',required=False)
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
from unicodedata import normalize

if sys.version_info < (3,0):
    reload(sys)
    sys.setdefaultencoding('utf-8')

ustr = lambda x: unicode(str(x).upper()).strip()
ustrl = lambda x: unicode(str(x).lower()).strip()
fstr = lambda x: unicode(str(x).lower()).strip()
fnum = lambda n: re.sub('[^0-9]','',n) 
fstrx = lambda n: re.sub('[^A-Za-z]','',n) 

usuario = admmodels.User.objects.get(username='sgp')
formacobranca = fmodels.FormaCobranca.objects.all()[0]


if args.ftth:

    #0 tc.id,
    #1 tc.nome,
    #2 tsc.id,
    #3 tsca.usuario,
    #4 te.id as oltid,
    #5 te.nome as oltnome,
    #6 te.ip as oltip,
    #7 tbpp.porta_slot,
    #8 tbpp.porta_id,
    #9 tbpp.descricao,
    #10 tscaf.serial_equipamento,
    #11 tscaf.id_onu,
    #12 tscaf.id_service_port,
    #13 tscaf.provisionado,
    #14 tsccafp.valor as vlan


    with open(args.ftth, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            servico = admmodels.ServicoInternet.objects.filter(login__lower__trim=row[3].lower().strip(),onu__isnull=True)
            if servico:
                servico = servico[0]
                onu = nmodels.ONU.objects.filter(phy_addr=row[10])
                if onu:
                    onu = onu[0]
                    onu.service=servico
                    onu.notes='pslot: %s pid: %s' %(row[7],row[8])
                    onu.save()
                    print(servico,row[10])



if args.anotacoes:
    #0 tc.id,
    #1 tc.nome,
    #2 tsc.id,
    #3 tsca.usuario,
    #4 tscat.latitude,
    #5 tscat.longitude,
    #6 tscat.observacoes

   with open(args.anotacoes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            servico = admmodels.ServicoInternet.objects.filter(login__lower__trim=row[3].lower().strip())
            if servico and row[6].strip():
                anotacao = '<pre>id servico: %s\nlogin servico: %s\n-----------------------------------\n%s</pre>' %(row[2],row[3],row[6].strip())
                servico = servico[0]
                if row[4] and row[5]:
                    servico.endereco.map_ll='%s,%s' %(row[4],row[5])
                    servico.endereco.save()
                cliente = servico.clientecontrato.cliente
                if admmodels.ClienteAnotacao.objects.filter(cliente=cliente,anotacao=anotacao).count() == 0:
                    new_anotacao = admmodels.ClienteAnotacao()
                    new_anotacao.cliente = cliente
                    new_anotacao.anotacao=anotacao
                    new_anotacao.data_cadastro=cliente.data_cadastro
                    new_anotacao.usuario=usuario
                    new_anotacao.save()
                    print(servico,row[6])


if args.portadores:
    with open(args.portadores, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:
            codigo_banco = row[2]
            if not row[2]:
                codigo_banco = '999'
            if fmodels.Portador.objects.filter(id=row[0]).count() == 0:
                print row
                new_portador = fmodels.Portador()
                new_portador.id = row[0]
                new_portador.descricao = row[1]
                new_portador.codigo_banco = codigo_banco
                new_portador.agencia = row[3] or '0'
                new_portador.agencia_dv = row[4]
                new_portador.conta = row[5] or '0'
                new_portador.conta_dv = row[6]
                new_portador.convenio = row[7]
                new_portador.carteira = row[8]
                new_portador.cedente = row[9]
                new_portador.cpfcnpj = '0'
                new_portador.save()

if args.clientes:

    nas_default = nmodels.NAS.objects.get(pk=args.nas_id)
    portador = fmodels.Portador.objects.get(pk=args.portador_id)

    m = manage.Manage()
    with open(args.clientes, 'rb') as csvfile:
        conteudo = csv.reader(csvfile, delimiter='|', quotechar='"')
        for row in conteudo:

            idcliente = row[0]
            idservico = row[58]

            login=ustrl(row[1])
            login = normalize('NFKD', unicode(login)).encode('ASCII','ignore')
            if row[43]:
                senha=row[43]
            else:
                senha='123456'

            #
            # Dados pessoais 
            #
            nome = ustr(row[3])
            cpfcnpj = ustr(row[5])
            rgie = fnum(row[8])
            rg_emissor = fstrx(row[8])
            profissao = ustr(row[9])
            tipo = ustr(row[2])

            pai = row[49]
            mae = row[50]
            naturalidade = '-'.join(row[51:53])
            ie = row[53]
            im = row[54]
            cliobs = row[55]
            senhacentral = row[56]
            obstec = row[57]

            cliobs += '\n%s' %obstec

            sexo = row[10]
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
                logradouro += ",%s" %row[15]
            complemento = ustr(row[16])
            bairro = ustr(row[17])
            cep = ustr(row[18])
            uf = ustr(row[19])
            cidade = ustr(row[20]).upper()

            #
            # Contato
            #
            celular = row[21]
            telefonecom = row[22]
            email = ustrl(row[23])   
            telefone = ''
            con_obs=row[24]
          
            #
            # DATAS 
            # 

            data_cadastro = row[26]
            data_status = row[46]


            # 
            # Contrato
            # 

            # Servico
            nas_get = row[28].strip()
            plano = row[29].strip()
            plano_valor = str(row[30]).strip()
            plano_download = row[44].replace('K','')
            plano_upload = row[45].replace('K','')

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
                print 'erro row (%s) - %s' %(row[35],vencimento)

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

            status = ustrl(row[42])

            if status == 'liberado':
                status_cc = 1
                status_s = 1
                status_c = 1
            elif status == 'bloqueado':
                data_status = row[47]
                status_cc = 4
                status_s = 4
                status_c = 4
            elif status == 'desativado':
                data_status = row[48]
                status_cc = 3
                status_s = 3
                status_c = 3
            try:
                planointernet = admmodels.PlanoInternet.objects.filter(plano__descricao__iexact=plano.lower())[0]
            except:
                if args.planoadd:
                    new_plano = admmodels.Plano()
                    new_plano.descricao=plano
                    new_plano.preco = plano_valor
                    new_plano.contrato = admmodels.Contrato.objects.get(grupo__nome='radio')
                    new_plano.grupo = admmodels.Grupo.objects.get(nome='radio')
                    try:
                        new_plano.save()
                    except:
                        new_plano.preco='0.00'
                        new_plano.save()

                    new_plano_internet = admmodels.PlanoInternet()
                    new_plano_internet.plano = new_plano 
                    new_plano_internet.download = plano_download
                    new_plano_internet.upload = plano_upload
                    try:
                        new_plano_internet.save() 
                    except:
                        new_plano_internet.download = 2048
                        new_plano_internet.upload = 1024
                        new_plano_internet.save()
                    print('criado plano %s' %plano)
                    planointernet = new_plano_internet
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

            #print pop
            #print row
            print idcliente,nome,cpfcnpj,len(cpfcnpj),sexo, data_cadastro,data_nasc
            print logradouro,numero or '',complemento,bairro,cidade,uf,cep
            print 'vencimento: ', vencimento, 'Plano: ', plano
            print telefone,telefonecom,celular,email,con_obs
            print idservico,login,senha,ip,mac,status
            print '####################################################'
            if args.sync_db == True and admmodels.ServicoInternet.objects.filter(login__unaccent__trim__lower=login).count() == 0:
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
                        new_pessoa.nacionalidade = 'BR'
                        new_pessoa.rg = rgie
                        new_pessoa.cpfcnpj = cpfcnpj
                        new_pessoa.rg_emissor=rg_emissor
                        new_pessoa.nomepai = pai
                        new_pessoa.nomemae = mae
                        new_pessoa.naturalidade = naturalidade
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
                        new_pessoa.insc_estadual = ie
                        new_pessoa.insc_municipal = im
                        new_pessoa.tipo = 8
                        new_pessoa.save()

                    new_cliente = admmodels.Cliente()
                    new_cliente.id = idcliente
                    new_cliente.endereco = new_endereco
                    new_cliente.pessoa = new_pessoa
                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.data_alteracao = data_cadastro
                    new_cliente.observacao = cliobs
                    new_cliente.ativo = True 
                    try:
                        new_cliente.save()
                    except:
                        data_cadastro=date.today().strftime('%Y-%m-%d')
                        new_cliente.data_cadastro = data_cadastro
                        new_cliente.save()

                    new_cliente.data_cadastro = data_cadastro
                    new_cliente.save()
                
                    # contato 1
                    if len(email) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'EMAIL'
                        new_contato.contato = email.strip()[0:200] 
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                    
                    # contato 2
                    if len(celular) > 4:
                        new_contato = admmodels.Contato()  
                        new_contato.tipo = 'CELULAR_PESSOAL'
                        new_contato.contato = celular.strip()[0:200]
                        if con_obs:
                            new_contato.observacao = con_obs[0:200]
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()
                    
                    
                    # contato 3
                    if len(telefone) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'TELEFONE_FIXO_RESIDENCIAL'
                        new_contato.contato = telefone.strip()[0:200]  
                        new_contato.save() 
                        new_ccontato = admmodels.ClienteContato()
                        new_ccontato.cliente = new_cliente
                        new_ccontato.contato = new_contato
                        new_ccontato.save()

                    # contato 4
                    if len(telefonecom) > 4:
                        new_contato = admmodels.Contato() 
                        new_contato.tipo = 'TELEFONE_FIXO_COMERCIAL'
                        new_contato.contato = telefonecom.strip()[0:200] 
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

                
                if not data_cadastro:
                    data_cadastro=date.today().strftime('%Y-%m-%d')

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
                new_contrato.id = idservico
                new_contrato.cliente = new_cliente 
                new_contrato.pop = pop
                new_contrato.cobranca = new_cobranca
                 
                new_contrato.data_inicio = data_cadastro 
                new_contrato.data_cadastro = data_cadastro 
                new_contrato.data_alteracao = data_cadastro
                new_contrato.save()
                
                for ic in [6,2]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=1
                    new_status.usuario = usuario 
                    new_status.data_cadastro = data_cadastro 
                    new_status.save() 
                
                    new_status.data_cadastro = data_cadastro 
                    new_status.save() 

                for ic in [status_cc]:
                    new_status = admmodels.ClienteContratoStatus()
                    new_status.cliente_contrato = new_contrato
                    new_status.status = ic
                    new_status.modo=1
                    new_status.usuario = usuario 
                    new_status.data_cadastro = data_status
                    try: 
                        new_status.save() 
                    except:
                        new_status.data_cadastro=data_cadastro
                        new_status.save()

                    new_status.data_cadastro = data_status 
                    try: 
                        new_status.save() 
                    except:
                        new_status.data_cadastro=data_cadastro
                        new_status.save()

                # Servico 
                new_servico = admmodels.ServicoInternet()
                new_servico.id = idservico
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
                new_servico.central_password=senhacentral or senha
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

